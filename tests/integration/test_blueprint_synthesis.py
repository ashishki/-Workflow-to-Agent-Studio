from workflow_agent_studio.blueprint import synthesize_blueprint
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.extraction import extract_workflow_map
from workflow_agent_studio.retrieval import EvidenceSnippet


def _source() -> SourceDocument:
    return SourceDocument(
        source_id="src-sop",
        source_type="markdown",
        title="Support Intake SOP",
        fingerprint="abc123",
        normalized_text=(
            "Operator reviews inbound support requests. "
            "Check the CRM for account status. "
            "Create a follow-up task when engineering review is needed. "
            "If details are missing, ask the customer for clarification."
        ),
    )


def _evidence() -> list[EvidenceSnippet]:
    return [
        EvidenceSnippet(
            source_id="src-sop",
            chunk_id="src-sop:chunk-1",
            score=1.0,
            text_preview="Create a follow-up task when engineering review is needed.",
            heading_path=("Support Intake SOP",),
        )
    ]


def _blueprint():
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())
    return synthesize_blueprint(workflow=workflow, evidence=_evidence())


def test_synthesis_produces_all_required_sections() -> None:
    blueprint = _blueprint()

    assert blueprint.schema_version == "v1"
    assert blueprint.workflow_summary
    assert blueprint.actors
    assert blueprint.systems
    assert blueprint.triggers
    assert blueprint.inputs
    assert blueprint.current_workflow_steps
    assert blueprint.decisions
    assert blueprint.exceptions
    assert blueprint.data_fields
    assert blueprint.integration_map
    assert blueprint.pain_points
    assert blueprint.automation_candidates
    assert blueprint.human_approval_boundaries
    assert blueprint.risks_and_assumptions
    assert blueprint.eval_cases
    assert blueprint.observability_needs
    assert blueprint.rough_effort_band
    assert blueprint.next_implementation_tasks


def test_automation_candidates_include_boundaries_risk_and_evidence() -> None:
    candidate = _blueprint().automation_candidates[0]

    assert candidate.implementation_boundary
    assert candidate.human_approval_boundary
    assert candidate.risk_level in {"low", "medium", "high"}
    assert candidate.evidence_references


def test_eval_cases_include_measurable_verification() -> None:
    eval_case = _blueprint().eval_cases[0]

    assert eval_case.input_condition
    assert eval_case.expected_behavior
    assert eval_case.evidence_reference.source_id == "src-sop"
    assert "Inspect" in eval_case.verification_method
