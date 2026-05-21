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
from workflow_agent_studio.patterns import BlueprintProfile, profile_for_workflow_signals
from workflow_agent_studio.retrieval import EvidenceGapReport, EvidenceSnippet


def synthesize_blueprint(
    *,
    workflow: ExtractedWorkflowMap,
    evidence: list[EvidenceSnippet],
    evidence_gaps: EvidenceGapReport | None = None,
) -> AutomationBlueprint:
    """Build a typed v1 automation blueprint from extracted workflow facts."""
    reference = _first_reference(evidence)
    profile = profile_for_workflow_signals(systems=workflow.systems, decisions=workflow.decisions)
    source_system = workflow.systems[0]
    target_system = workflow.systems[-1]
    risks_and_assumptions = [
        RiskOrAssumption(
            description=profile.primary_risk,
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
            text=profile.summary,
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
                name=profile.automation_candidate_name,
                implementation_boundary=profile.implementation_boundary,
                human_approval_boundary=profile.human_approval_boundary,
                risk_level=profile.risk_level,
                evidence_references=[reference],
            )
        ],
        human_approval_boundaries=[
            ApprovalBoundary(
                decision=profile.approval_decision,
                approver=_approval_actor(workflow=workflow, profile=profile),
                reason=profile.approval_reason,
            )
        ],
        risks_and_assumptions=risks_and_assumptions,
        eval_cases=[
            EvalCase(
                name=profile.eval_case_name,
                input_condition=profile.eval_input_condition,
                expected_behavior=profile.eval_expected_behavior,
                verification_method="Inspect automation candidate and evidence link.",
                evidence_reference=reference,
            )
        ],
        observability_needs=[
            Claim(
                text=profile.observability_need,
                assumption=True,
            )
        ],
        rough_effort_band="small",
        next_implementation_tasks=[
            ImplementationTaskPlan(
                task_id="impl-1",
                owner="engineer",
                depends_on=[],
                acceptance_criteria=[profile.implementation_acceptance_criteria],
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


def _approval_actor(*, workflow: ExtractedWorkflowMap, profile: BlueprintProfile) -> str:
    for actor in workflow.actors:
        actor_text = actor.casefold()
        if any(term in actor_text for term in profile.approval_actor_terms):
            return actor
    return workflow.actors[0]
