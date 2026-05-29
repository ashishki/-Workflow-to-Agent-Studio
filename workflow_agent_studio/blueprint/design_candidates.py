"""Design candidate generation for workflow-to-agent blueprints."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from workflow_agent_studio.blueprint.service import synthesize_blueprint
from workflow_agent_studio.domain.blueprint import (
    ApprovalBoundary,
    AutomationBlueprint,
    RiskOrAssumption,
)
from workflow_agent_studio.domain.design_candidate import (
    AgentDesignCandidate,
    CostPosture,
    DesignCandidateVariant,
    EvalNeed,
    EvidenceGap,
    PermissionRuntimeBoundary,
    RuntimeTier,
    RuntimeTierJustification,
    ToolRequirement,
    ToolSurfaceBoundary,
)
from workflow_agent_studio.domain.workflow import EvidenceReference
from workflow_agent_studio.extraction import ExtractedWorkflowMap, MissingQuestion
from workflow_agent_studio.patterns import profile_for_workflow_kind
from workflow_agent_studio.retrieval import EvidenceGapReport, EvidenceSnippet
from workflow_agent_studio.validators import (
    BlueprintValidationFinding,
    validate_design_candidate_for_approval,
)

DesignCandidateStatus = Literal["ready", "needs_review"]


@dataclass(frozen=True)
class DesignCandidateDraft:
    candidate: AgentDesignCandidate
    status: DesignCandidateStatus
    assumptions: list[RiskOrAssumption]
    findings: list[BlueprintValidationFinding]


@dataclass(frozen=True)
class DesignTradeoffComparison:
    variant: DesignCandidateVariant
    autonomy_level: str
    runtime_tier: RuntimeTier
    cost_posture: CostPosture
    approval_count: int
    eval_count: int
    risk_count: int
    evidence_gap_count: int


@dataclass(frozen=True)
class DesignCandidatePortfolio:
    candidates: list[DesignCandidateDraft]
    tradeoff_comparison: list[DesignTradeoffComparison]
    consolidated_blueprint: AutomationBlueprint


@dataclass(frozen=True)
class _CandidateSpec:
    variant: DesignCandidateVariant
    autonomy_level: Literal["none", "assisted", "bounded", "high"]
    runtime_tier: RuntimeTier
    cost_posture: CostPosture
    tool_boundary: str
    approval_reason: str
    risk_description: str
    eval_behavior: str


_CANDIDATE_SPECS: tuple[_CandidateSpec, ...] = (
    _CandidateSpec(
        variant="deterministic_first",
        autonomy_level="none",
        runtime_tier="T0",
        cost_posture="low",
        tool_boundary="No autonomous tool calls; deterministic validation and local export only.",
        approval_reason="Humans own all workflow decisions and external commitments.",
        risk_description="Coverage may be lower because LLM and tool autonomy are minimized.",
        eval_behavior="The design should identify deterministic checks before any LLM-owned step.",
    ),
    _CandidateSpec(
        variant="human_in_the_loop",
        autonomy_level="assisted",
        runtime_tier="T0",
        cost_posture="medium",
        tool_boundary="Draft-only tool use; humans approve every proposed action.",
        approval_reason="Operator approval is required before a draft changes downstream work.",
        risk_description="Review load may stay high for frequent workflow items.",
        eval_behavior="The design should preserve explicit human approval before action.",
    ),
    _CandidateSpec(
        variant="bounded_agent",
        autonomy_level="bounded",
        runtime_tier="T0",
        cost_posture="medium",
        tool_boundary="Read permitted sources and draft bounded handoff artifacts only.",
        approval_reason="Bounded agents still need approval before external side effects.",
        risk_description="Permission boundaries may be too broad without source-specific limits.",
        eval_behavior="The design should keep tool permissions inside the approved boundary.",
    ),
    _CandidateSpec(
        variant="high_autonomy",
        autonomy_level="high",
        runtime_tier="T1",
        cost_posture="high",
        tool_boundary="Propose autonomous execution only as a future option after approval.",
        approval_reason="High-autonomy behavior cannot proceed without human scope approval.",
        risk_description="Premature autonomy could create unsafe customer or team commitments.",
        eval_behavior="The design should surface high-autonomy risk before implementation.",
    ),
    _CandidateSpec(
        variant="compliance_heavy",
        autonomy_level="assisted",
        runtime_tier="T0",
        cost_posture="high",
        tool_boundary="Use auditable local artifacts and require approval for sensitive decisions.",
        approval_reason="Compliance-sensitive workflows require accountable human sign-off.",
        risk_description="Compliance checks can slow delivery if evidence is incomplete.",
        eval_behavior="The design should include audit and approval checks for sensitive steps.",
    ),
    _CandidateSpec(
        variant="low_cost_mvp",
        autonomy_level="assisted",
        runtime_tier="T0",
        cost_posture="low",
        tool_boundary="Use the smallest local workflow that can produce a reviewed draft.",
        approval_reason="The MVP should avoid automated action until value is proven.",
        risk_description="The MVP may defer integrations that are important for production fit.",
        eval_behavior="The design should prove the workflow blueprint before integration buildout.",
    ),
)


def generate_design_candidate_portfolio(
    *,
    workflow: ExtractedWorkflowMap,
    evidence: list[EvidenceSnippet],
    evidence_gaps: EvidenceGapReport | None = None,
) -> DesignCandidatePortfolio:
    reference = _first_reference(evidence)
    assumptions = _candidate_assumptions(
        missing_questions=workflow.missing_questions,
        evidence_gaps=evidence_gaps,
    )
    candidates = [
        _draft_candidate(
            spec=spec,
            workflow=workflow,
            reference=reference,
            assumptions=assumptions,
            evidence_gaps=evidence_gaps,
        )
        for spec in _CANDIDATE_SPECS
    ]
    return DesignCandidatePortfolio(
        candidates=candidates,
        tradeoff_comparison=[_compare_tradeoffs(draft.candidate) for draft in candidates],
        consolidated_blueprint=synthesize_blueprint(
            workflow=workflow,
            evidence=evidence,
            evidence_gaps=evidence_gaps,
        ),
    )


def _draft_candidate(
    *,
    spec: _CandidateSpec,
    workflow: ExtractedWorkflowMap,
    reference: EvidenceReference,
    assumptions: list[RiskOrAssumption],
    evidence_gaps: EvidenceGapReport | None,
) -> DesignCandidateDraft:
    profile = profile_for_workflow_kind(workflow.workflow_kind)
    approver = _approval_actor(workflow)
    risk_items = [
        RiskOrAssumption(
            description=spec.risk_description,
            kind="risk",
            evidence_references=[reference],
        ),
        *assumptions,
    ]
    candidate = AgentDesignCandidate(
        variant=spec.variant,
        name=f"{spec.variant.replace('_', ' ').title()} Design",
        summary=f"{profile.summary} Candidate lens: {spec.variant.replace('_', ' ')}.",
        autonomy_level=spec.autonomy_level,
        required_tools=[
            ToolRequirement(
                name=system,
                permission_boundary=spec.tool_boundary,
                evidence_references=[reference],
            )
            for system in workflow.systems
        ],
        permission_runtime_boundary=_permission_runtime_boundary(
            spec=spec,
            workflow=workflow,
            approval_decision=profile.approval_decision,
        ),
        human_approvals=[
            ApprovalBoundary(
                decision=profile.approval_decision,
                approver=approver,
                reason=spec.approval_reason,
            )
        ],
        runtime_tier=spec.runtime_tier,
        eval_needs=[
            EvalNeed(
                name=f"{spec.variant} eval",
                expected_behavior=spec.eval_behavior,
                verification_method=(
                    "Inspect candidate boundaries, assumptions, and evidence links."
                ),
                evidence_references=[reference],
            )
        ],
        risks=risk_items,
        cost_posture=spec.cost_posture,
        evidence_gaps=_candidate_evidence_gaps(evidence_gaps),
        evidence_references=[reference],
    )
    validation = validate_design_candidate_for_approval(candidate)
    status: DesignCandidateStatus = (
        "needs_review"
        if validation.findings or (evidence_gaps is not None and evidence_gaps.gap_count)
        else "ready"
    )
    return DesignCandidateDraft(
        candidate=candidate,
        status=status,
        assumptions=assumptions,
        findings=validation.findings,
    )


def _candidate_assumptions(
    *,
    missing_questions: list[MissingQuestion],
    evidence_gaps: EvidenceGapReport | None,
) -> list[RiskOrAssumption]:
    assumptions = [
        RiskOrAssumption(description=question.question, kind="assumption")
        for question in missing_questions
    ]
    if evidence_gaps is not None:
        assumptions.extend(
            RiskOrAssumption(description=gap.question, kind="assumption")
            for gap in evidence_gaps.gaps
        )
    return assumptions


def _candidate_evidence_gaps(evidence_gaps: EvidenceGapReport | None) -> list[EvidenceGap]:
    if evidence_gaps is None:
        return []
    return [
        EvidenceGap(section=gap.section, question=gap.question, impact=gap.reason)
        for gap in evidence_gaps.gaps
    ]


def _permission_runtime_boundary(
    *,
    spec: _CandidateSpec,
    workflow: ExtractedWorkflowMap,
    approval_decision: str,
) -> PermissionRuntimeBoundary:
    return PermissionRuntimeBoundary(
        runtime_tier=spec.runtime_tier,
        runtime_justification=RuntimeTierJustification(
            runtime_tier=spec.runtime_tier,
            mutability=_mutability_for_spec(spec),
            privilege_level=_privilege_for_spec(spec),
            blast_radius=_blast_radius_for_spec(spec),
            rationale=(
                f"{spec.runtime_tier} fits {spec.variant} because the design has "
                f"{_mutability_for_spec(spec)} mutability, "
                f"{_privilege_for_spec(spec)} privilege, and "
                f"{_blast_radius_for_spec(spec)} blast radius."
            ),
        ),
        tool_surfaces=[
            ToolSurfaceBoundary(
                tool_name=system,
                read_surfaces=[f"Read workflow evidence from {system}"],
                write_surfaces=_write_surfaces_for_spec(spec, system),
                destructive_surfaces=[],
                confirmation_required=bool(_write_surfaces_for_spec(spec, system)),
                sandbox_recommended=spec.runtime_tier != "T0",
                rationale=spec.tool_boundary,
            )
            for system in workflow.systems
        ],
        human_approval_points=[approval_decision],
    )


def _mutability_for_spec(
    spec: _CandidateSpec,
) -> Literal["read_only", "draft_only", "writes_allowed", "destructive"]:
    if spec.variant == "deterministic_first":
        return "read_only"
    if spec.variant == "high_autonomy":
        return "writes_allowed"
    return "draft_only"


def _privilege_for_spec(spec: _CandidateSpec) -> Literal["none", "low", "medium", "high"]:
    if spec.variant == "deterministic_first":
        return "none"
    if spec.variant == "high_autonomy":
        return "high"
    if spec.variant in {"bounded_agent", "compliance_heavy"}:
        return "medium"
    return "low"


def _blast_radius_for_spec(
    spec: _CandidateSpec,
) -> Literal["local", "team", "customer", "production"]:
    if spec.variant == "high_autonomy":
        return "customer"
    if spec.variant in {"bounded_agent", "compliance_heavy"}:
        return "team"
    return "local"


def _write_surfaces_for_spec(spec: _CandidateSpec, system: str) -> list[str]:
    if spec.variant in {"deterministic_first", "low_cost_mvp"}:
        return []
    return [f"Draft proposed update for {system}"]


def _compare_tradeoffs(candidate: AgentDesignCandidate) -> DesignTradeoffComparison:
    return DesignTradeoffComparison(
        variant=candidate.variant,
        autonomy_level=candidate.autonomy_level,
        runtime_tier=candidate.runtime_tier,
        cost_posture=candidate.cost_posture,
        approval_count=len(candidate.human_approvals),
        eval_count=len(candidate.eval_needs),
        risk_count=sum(item.kind == "risk" for item in candidate.risks),
        evidence_gap_count=len(candidate.evidence_gaps),
    )


def _first_reference(evidence: list[EvidenceSnippet]) -> EvidenceReference:
    if not evidence:
        raise ValueError("design candidate generation requires at least one evidence snippet")
    first = evidence[0]
    return EvidenceReference(source_id=first.source_id, chunk_id=first.chunk_id)


def _approval_actor(workflow: ExtractedWorkflowMap) -> str:
    for actor in workflow.actors:
        if "approv" in actor.casefold() or "operator" in actor.casefold():
            return actor
    return workflow.actors[0]
