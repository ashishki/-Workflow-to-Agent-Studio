"""Blueprint synthesis service."""

from __future__ import annotations

from workflow_agent_studio.domain.blueprint import (
    Actor,
    ApprovalBoundary,
    AutomationBlueprint,
    AutomationCandidate,
    Claim,
    DataField,
    EvalCase,
    ImplementationTaskPlan,
    Integration,
    RiskOrAssumption,
    SystemRef,
)
from workflow_agent_studio.domain.workflow import EvidenceReference
from workflow_agent_studio.extraction import ExtractedWorkflowMap, MissingQuestion
from workflow_agent_studio.retrieval import EvidenceGapReport, EvidenceSnippet


def synthesize_blueprint(
    *,
    workflow: ExtractedWorkflowMap,
    evidence: list[EvidenceSnippet],
    evidence_gaps: EvidenceGapReport | None = None,
) -> AutomationBlueprint:
    """Build a typed v1 automation blueprint from extracted workflow facts."""
    reference = _first_reference(evidence)
    workflow_kind = _workflow_kind(workflow)
    source_system = workflow.systems[0]
    target_system = workflow.systems[-1]
    risks_and_assumptions = [
        RiskOrAssumption(
            description=_primary_risk(workflow_kind),
            kind="risk",
            evidence_references=[reference],
        )
    ]
    risks_and_assumptions.extend(
        _missing_question_to_assumption(question) for question in workflow.missing_questions
    )
    if evidence_gaps is not None:
        risks_and_assumptions.extend(
            RiskOrAssumption(description=gap.question, kind="assumption")
            for gap in evidence_gaps.gaps
        )

    return AutomationBlueprint(
        workflow_summary=Claim(
            text=_workflow_summary(workflow, workflow_kind),
            evidence_references=[reference],
        ),
        actors=[Actor(name=actor, role="Workflow participant") for actor in workflow.actors],
        systems=[SystemRef(name=system, purpose="Workflow system") for system in workflow.systems],
        triggers=[
            Claim(text=trigger, evidence_references=[reference]) for trigger in workflow.triggers
        ],
        inputs=[
            DataField(
                name=field,
                description=f"Input field: {field}",
                source=source_system,
            )
            for field in workflow.data_fields
        ],
        current_workflow_steps=workflow.steps,
        decisions=[
            Claim(text=decision, evidence_references=[reference]) for decision in workflow.decisions
        ],
        exceptions=[
            Claim(text=exception, evidence_references=[reference])
            for exception in workflow.exceptions
        ],
        data_fields=[
            DataField(
                name=field,
                description=f"Workflow data field: {field}",
                source=source_system,
            )
            for field in workflow.data_fields
        ],
        integration_map=[
            Integration(
                source_system=source_system,
                target_system=target_system,
                data_fields=workflow.data_fields,
            )
        ],
        pain_points=[
            Claim(text=pain_point, evidence_references=[reference])
            for pain_point in workflow.pain_points
        ],
        automation_candidates=[
            AutomationCandidate(
                name=_automation_candidate_name(workflow_kind),
                implementation_boundary=_automation_candidate_boundary(workflow_kind),
                human_approval_boundary=_human_approval_boundary(workflow_kind),
                risk_level=_risk_level(workflow_kind),
                evidence_references=[reference],
            )
        ],
        human_approval_boundaries=[
            ApprovalBoundary(
                decision=_approval_decision(workflow_kind),
                approver=_approval_actor(workflow),
                reason=_approval_reason(workflow_kind),
            )
        ],
        risks_and_assumptions=risks_and_assumptions,
        eval_cases=[
            EvalCase(
                name=_eval_case_name(workflow_kind),
                input_condition=_eval_input_condition(workflow_kind),
                expected_behavior=_eval_expected_behavior(workflow_kind),
                verification_method="Inspect automation candidate and evidence link.",
                evidence_reference=reference,
            )
        ],
        observability_needs=[
            Claim(
                text=_observability_need(workflow_kind),
                assumption=True,
            )
        ],
        rough_effort_band="small",
        next_implementation_tasks=[
            ImplementationTaskPlan(
                task_id="impl-1",
                owner="engineer",
                depends_on=[],
                acceptance_criteria=[_implementation_acceptance_criteria(workflow_kind)],
                tests_or_evals=["Blueprint synthesis integration test."],
            )
        ],
    )


def _first_reference(evidence: list[EvidenceSnippet]) -> EvidenceReference:
    if not evidence:
        raise ValueError("blueprint synthesis requires at least one evidence snippet")
    first = evidence[0]
    return EvidenceReference(source_id=first.source_id, chunk_id=first.chunk_id)


def _missing_question_to_assumption(question: MissingQuestion) -> RiskOrAssumption:
    return RiskOrAssumption(description=question.question, kind="assumption")


def _workflow_kind(workflow: ExtractedWorkflowMap) -> str:
    systems = " ".join(workflow.systems).casefold()
    decisions = " ".join(workflow.decisions).casefold()
    if "github issues" in systems and "duplicate" in decisions:
        return "issue_triage"
    return "support_intake"


def _workflow_summary(workflow: ExtractedWorkflowMap, workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return (
            "GitHub Issues triage workflow routes public issue submissions through "
            "template checks, duplicate and scope review, reproducibility checks, "
            "stale handling, and engineering ownership decisions."
        )
    return "Support intake workflow routes customer requests to follow-up tasks."


def _primary_risk(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Missing issue details can lead to incorrect closure or delayed engineering review."
    return "Missing request details can block automation."


def _automation_candidate_name(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Draft issue triage recommendation"
    return "Draft follow-up task"


def _automation_candidate_boundary(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return (
            "Draft triage recommendation only; do not close, label, or route issues automatically."
        )
    return "Draft task only; do not create external commitments."


def _human_approval_boundary(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return (
            "Maintainer approves before issue status, labels, closure, "
            "or engineering routing change."
        )
    return "Operator approves before task creation."


def _risk_level(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "high"
    return "medium"


def _approval_decision(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Approve issue triage recommendation"
    return "Approve follow-up task"


def _approval_actor(workflow: ExtractedWorkflowMap) -> str:
    for actor in workflow.actors:
        if "maintainer" in actor.casefold():
            return actor
    return workflow.actors[0]


def _approval_reason(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Triage changes can close public issues or create engineering commitments."
    return "Task creation changes team expectations."


def _eval_case_name(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Issue triage recommendation"
    return "Follow-up task candidate"


def _eval_input_condition(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Issue includes template fields, version, reproduction details, and scope context."
    return "Request includes enough details for engineering review."


def _eval_expected_behavior(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return (
            "Blueprint recommends a maintainer-reviewed triage action without mutating "
            "GitHub issue state automatically."
        )
    return "Blueprint recommends a draft follow-up task."


def _observability_need(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return (
            "Track draft triage recommendations, maintainer overrides, "
            "stale decisions, and blocked cases."
        )
    return "Track generated draft task count and validation failures."


def _implementation_acceptance_criteria(workflow_kind: str) -> str:
    if workflow_kind == "issue_triage":
        return "Draft triage recommendation is generated from source evidence."
    return "Draft task candidate is generated from source evidence."
