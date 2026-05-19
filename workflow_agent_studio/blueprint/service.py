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
from workflow_agent_studio.extraction import ExtractedWorkflowMap
from workflow_agent_studio.retrieval import EvidenceSnippet


def synthesize_blueprint(
    *,
    workflow: ExtractedWorkflowMap,
    evidence: list[EvidenceSnippet],
) -> AutomationBlueprint:
    """Build a typed v1 automation blueprint from extracted workflow facts."""
    reference = _first_reference(evidence)
    risks_and_assumptions = [
        RiskOrAssumption(
            description="Missing request details can block automation.",
            kind="risk",
            evidence_references=[reference],
        )
    ]
    risks_and_assumptions.extend(
        RiskOrAssumption(description=question.question, kind="assumption")
        for question in workflow.missing_questions
    )

    return AutomationBlueprint(
        workflow_summary=Claim(
            text="Support intake workflow routes customer requests to follow-up tasks.",
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
                source="Support intake source",
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
                source="Source SOP",
            )
            for field in workflow.data_fields
        ],
        integration_map=[
            Integration(
                source_system="Inbox",
                target_system="Task Tracker",
                data_fields=workflow.data_fields,
            )
        ],
        pain_points=[
            Claim(text=pain_point, evidence_references=[reference])
            for pain_point in workflow.pain_points
        ],
        automation_candidates=[
            AutomationCandidate(
                name="Draft follow-up task",
                implementation_boundary=("Draft task only; do not create external commitments."),
                human_approval_boundary="Operator approves before task creation.",
                risk_level="medium",
                evidence_references=[reference],
            )
        ],
        human_approval_boundaries=[
            ApprovalBoundary(
                decision="Approve follow-up task",
                approver="Operator",
                reason="Task creation changes team expectations.",
            )
        ],
        risks_and_assumptions=risks_and_assumptions,
        eval_cases=[
            EvalCase(
                name="Follow-up task candidate",
                input_condition="Request includes enough details for engineering review.",
                expected_behavior="Blueprint recommends a draft follow-up task.",
                verification_method="Inspect automation candidate and evidence link.",
                evidence_reference=reference,
            )
        ],
        observability_needs=[
            Claim(
                text="Track generated draft task count and validation failures.",
                assumption=True,
            )
        ],
        rough_effort_band="small",
        next_implementation_tasks=[
            ImplementationTaskPlan(
                task_id="impl-1",
                owner="engineer",
                depends_on=[],
                acceptance_criteria=["Draft task candidate is generated from source evidence."],
                tests_or_evals=["Blueprint synthesis integration test."],
            )
        ],
    )


def _first_reference(evidence: list[EvidenceSnippet]) -> EvidenceReference:
    if not evidence:
        raise ValueError("blueprint synthesis requires at least one evidence snippet")
    first = evidence[0]
    return EvidenceReference(source_id=first.source_id, chunk_id=first.chunk_id)
