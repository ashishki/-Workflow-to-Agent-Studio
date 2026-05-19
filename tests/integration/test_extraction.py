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


def test_extraction_returns_required_workflow_fields() -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())

    assert workflow.actors == ["Operator"]
    assert workflow.systems == ["Inbox", "CRM", "Task Tracker"]
    assert workflow.triggers == ["Inbound support request"]
    assert workflow.steps
    assert workflow.decisions
    assert workflow.exceptions
    assert workflow.data_fields
    assert workflow.pain_points


def test_extracted_steps_have_evidence_or_assumption() -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())

    for step in workflow.steps:
        assert step.evidence_references or step.assumption


def test_extraction_returns_missing_questions_for_absent_details() -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())

    assert workflow.missing_questions
    assert workflow.missing_questions[0].section == "approval_boundaries"
    assert "approves" in workflow.missing_questions[0].question
