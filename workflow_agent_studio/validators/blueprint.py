"""Deterministic automation blueprint validators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from workflow_agent_studio.domain.blueprint import (
    AutomationBlueprint,
    AutomationCandidate,
    Claim,
    EvalCase,
    ImplementationTaskPlan,
)
from workflow_agent_studio.domain.workflow import WorkflowStep
from workflow_agent_studio.retrieval import EvidenceGapReport
from workflow_agent_studio.validators.forbidden_claims import (
    scan_blueprint_text_for_forbidden_claims,
)


@dataclass(frozen=True)
class BlueprintValidationFinding:
    rule_id: str
    severity: str
    section: str
    message: str
    repair_hint: str


@dataclass(frozen=True)
class BlueprintValidationResult:
    findings: list[BlueprintValidationFinding]

    @property
    def blocking_count(self) -> int:
        return sum(finding.severity == "blocking" for finding in self.findings)

    @property
    def can_approve(self) -> bool:
        return self.blocking_count == 0


@dataclass(frozen=True)
class AutomationReadinessResult:
    score: int
    status: Literal["ready", "needs_review", "blocked"]
    blockers: list[str]
    risks: list[str]
    next_questions: list[str]


def validate_blueprint_for_approval(
    blueprint: AutomationBlueprint,
) -> BlueprintValidationResult:
    findings: list[BlueprintValidationFinding] = []
    findings.extend(_validate_required_sections(blueprint))
    findings.extend(_validate_evidence_coverage(blueprint))
    findings.extend(_validate_forbidden_claims(blueprint))
    findings.extend(_validate_eval_cases(blueprint.eval_cases))
    findings.extend(_validate_implementation_tasks(blueprint.next_implementation_tasks))
    findings.extend(_validate_candidate_boundaries(blueprint.automation_candidates))
    return BlueprintValidationResult(findings=findings)


def validate_evidence_gap_report(report: EvidenceGapReport) -> BlueprintValidationResult:
    return BlueprintValidationResult(
        findings=[
            BlueprintValidationFinding(
                rule_id="PLAN-EVIDENCE-GAP",
                severity="blocking",
                section=gap.section,
                message=gap.question,
                repair_hint=gap.reason,
            )
            for gap in report.gaps
        ]
    )


def compute_automation_readiness(
    blueprint: AutomationBlueprint,
    *,
    validation: BlueprintValidationResult | None = None,
) -> AutomationReadinessResult:
    validation_result = validation or validate_blueprint_for_approval(blueprint)
    blockers = [
        finding.message for finding in validation_result.findings if finding.severity == "blocking"
    ]
    risks = _readiness_risks(blueprint)
    next_questions = _readiness_next_questions(blueprint)
    if blockers:
        return AutomationReadinessResult(
            score=0,
            status="blocked",
            blockers=blockers,
            risks=risks,
            next_questions=next_questions,
        )

    score = 100
    score -= min(len(risks) * 5, 25)
    score -= min(len(next_questions) * 5, 25)
    status: Literal["ready", "needs_review"] = "ready" if score >= 90 else "needs_review"
    return AutomationReadinessResult(
        score=score,
        status=status,
        blockers=[],
        risks=risks,
        next_questions=next_questions,
    )


def _validate_required_sections(
    blueprint: AutomationBlueprint,
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    required_sections = {
        "actors": blueprint.actors,
        "systems": blueprint.systems,
        "triggers": blueprint.triggers,
        "inputs": blueprint.inputs,
        "current_workflow_steps": blueprint.current_workflow_steps,
        "decisions": blueprint.decisions,
        "exceptions": blueprint.exceptions,
        "data_fields": blueprint.data_fields,
        "integration_map": blueprint.integration_map,
        "pain_points": blueprint.pain_points,
        "automation_candidates": blueprint.automation_candidates,
        "approval_boundaries": blueprint.human_approval_boundaries,
        "risks_and_assumptions": blueprint.risks_and_assumptions,
        "eval_cases": blueprint.eval_cases,
        "observability_needs": blueprint.observability_needs,
        "next_implementation_tasks": blueprint.next_implementation_tasks,
    }
    for section, value in required_sections.items():
        if not value:
            findings.append(
                BlueprintValidationFinding(
                    rule_id="PLAN-REQUIRED-SECTION",
                    severity="blocking",
                    section=section,
                    message=f"Blueprint section `{section}` is required.",
                    repair_hint=f"Add at least one item to `{section}` before approval.",
                )
            )
    if not blueprint.rough_effort_band:
        findings.append(
            BlueprintValidationFinding(
                rule_id="PLAN-REQUIRED-SECTION",
                severity="blocking",
                section="rough_effort_band",
                message="Blueprint rough effort band is required.",
                repair_hint="Set a rough effort band before approval.",
            )
        )
    return findings


def _validate_evidence_coverage(
    blueprint: AutomationBlueprint,
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    claims = [
        ("workflow_summary", blueprint.workflow_summary),
        *[(f"triggers[{index}]", claim) for index, claim in enumerate(blueprint.triggers)],
        *[(f"decisions[{index}]", claim) for index, claim in enumerate(blueprint.decisions)],
        *[(f"exceptions[{index}]", claim) for index, claim in enumerate(blueprint.exceptions)],
        *[(f"pain_points[{index}]", claim) for index, claim in enumerate(blueprint.pain_points)],
        *[
            (f"observability_needs[{index}]", claim)
            for index, claim in enumerate(blueprint.observability_needs)
        ],
    ]
    for path, claim in claims:
        if isinstance(claim, Claim) and not claim.evidence_references and not claim.assumption:
            findings.append(_evidence_finding(path))

    for index, step in enumerate(blueprint.current_workflow_steps):
        if isinstance(step, WorkflowStep) and not step.evidence_references and not step.assumption:
            findings.append(_evidence_finding(f"current_workflow_steps[{index}]"))

    for index, candidate in enumerate(blueprint.automation_candidates):
        if isinstance(candidate, AutomationCandidate) and not candidate.evidence_references:
            findings.append(_evidence_finding(f"automation_candidates[{index}]"))

    for index, eval_case in enumerate(blueprint.eval_cases):
        if isinstance(eval_case, EvalCase) and not eval_case.evidence_reference:
            findings.append(_evidence_finding(f"eval_cases[{index}]"))
    return findings


def _validate_forbidden_claims(
    blueprint: AutomationBlueprint,
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    for forbidden in scan_blueprint_text_for_forbidden_claims(_stringify(blueprint)):
        findings.append(
            BlueprintValidationFinding(
                rule_id=forbidden.rule_id,
                severity=forbidden.severity,
                section="forbidden_claims",
                message=f"Forbidden claim detected: {forbidden.claim}.",
                repair_hint=(
                    "Remove autonomy claims that imply the system builds or acts without review."
                ),
            )
        )
    return findings


def _validate_eval_cases(eval_cases: list[EvalCase]) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    for index, eval_case in enumerate(eval_cases):
        missing_fields = [
            field
            for field in ("input_condition", "expected_behavior", "verification_method")
            if not getattr(eval_case, field, "")
        ]
        if missing_fields:
            findings.append(
                BlueprintValidationFinding(
                    rule_id="PLAN-EVAL-CASE-COMPLETE",
                    severity="blocking",
                    section="eval_cases",
                    message=f"Eval case {index} is missing measurable fields.",
                    repair_hint=(
                        "Add input condition, expected behavior, and verification method."
                    ),
                )
            )
    return findings


def _validate_implementation_tasks(
    tasks: list[ImplementationTaskPlan],
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    for index, task in enumerate(tasks):
        if not task.owner or not task.acceptance_criteria or not task.tests_or_evals:
            findings.append(
                BlueprintValidationFinding(
                    rule_id="PLAN-IMPLEMENTATION-TASK-COMPLETE",
                    severity="blocking",
                    section="next_implementation_tasks",
                    message=f"Implementation task {index} is incomplete.",
                    repair_hint=(
                        "Add owner, dependencies, acceptance criteria, and tests or evals."
                    ),
                )
            )
    return findings


def _validate_candidate_boundaries(
    candidates: list[AutomationCandidate],
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    for index, candidate in enumerate(candidates):
        if not candidate.implementation_boundary or not candidate.human_approval_boundary:
            findings.append(
                BlueprintValidationFinding(
                    rule_id="PLAN-AUTOMATION-BOUNDARY",
                    severity="blocking",
                    section="automation_candidates",
                    message=f"Automation candidate {index} is missing a boundary.",
                    repair_hint=(
                        "Add both implementation and human approval boundaries before approval."
                    ),
                )
            )
    return findings


def _readiness_risks(blueprint: AutomationBlueprint) -> list[str]:
    risks = [
        f"{candidate.risk_level.title()}-risk automation candidate: {candidate.name}"
        for candidate in blueprint.automation_candidates
        if candidate.risk_level in {"medium", "high"}
    ]
    risks.extend(
        item.description for item in blueprint.risks_and_assumptions if item.kind == "risk"
    )
    return risks


def _readiness_next_questions(blueprint: AutomationBlueprint) -> list[str]:
    questions = [
        f"Confirm assumption: {item.description}"
        for item in blueprint.risks_and_assumptions
        if item.kind == "assumption"
    ]
    questions.extend(
        f"Confirm assumption: {claim.text}"
        for claim in [
            blueprint.workflow_summary,
            *blueprint.triggers,
            *blueprint.decisions,
            *blueprint.exceptions,
            *blueprint.pain_points,
            *blueprint.observability_needs,
        ]
        if isinstance(claim, Claim) and claim.assumption
    )
    return questions


def _evidence_finding(path: str) -> BlueprintValidationFinding:
    return BlueprintValidationFinding(
        rule_id="PLAN-EVIDENCE-COVERAGE",
        severity="blocking",
        section="evidence_coverage",
        message=f"`{path}` lacks evidence references or an explicit assumption marker.",
        repair_hint="Add evidence references or mark the item as an assumption.",
    )


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_stringify(item) for pair in value.items() for item in pair)
    if isinstance(value, list | tuple | set):
        return " ".join(_stringify(item) for item in value)
    if hasattr(value, "model_dump"):
        return _stringify(value.model_dump(mode="python"))
    return str(value)
