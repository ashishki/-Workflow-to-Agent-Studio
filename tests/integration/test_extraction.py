import pytest

from workflow_agent_studio.config import load_settings
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.extraction import (
    extract_workflow_map,
    extract_workflow_map_provider_backed,
    extract_workflow_map_with_provider,
    extraction_provider_payload,
)
from workflow_agent_studio.llm import FakeStructuredOutputProvider, SchemaValidationError
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

    assert workflow.workflow_kind == "support_intake"
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


def test_provider_backed_extraction_parses_versioned_schema() -> None:
    source = _source()
    evidence = _evidence()
    provider = FakeStructuredOutputProvider(
        payload=extraction_provider_payload(source=source, evidence=evidence)
    )

    workflow = extract_workflow_map_with_provider(
        source=source,
        evidence=evidence,
        provider=provider,
    )

    assert workflow.actors == ["Operator"]
    assert workflow.workflow_kind == "support_intake"
    assert workflow.steps[0].evidence_references[0].source_id == "src-sop"
    assert workflow.missing_questions[0].section == "approval_boundaries"


def test_provider_selection_defaults_to_fake_provider_in_tests() -> None:
    workflow = extract_workflow_map_provider_backed(
        source=_source(),
        evidence=_evidence(),
        settings=load_settings(
            {
                "WORKFLOW_STUDIO_LLM_PROVIDER": "fake",
                "WORKFLOW_STUDIO_EXTRACTION_MODEL": "fake-extraction-model",
            }
        ),
    )

    assert workflow.systems == ["Inbox", "CRM", "Task Tracker"]


def test_provider_schema_errors_exclude_raw_source_text() -> None:
    raw_phrase = "Create a follow-up task when engineering review is needed"
    provider = FakeStructuredOutputProvider(
        payload={"schema_version": "v1", "actors": []},
        model_name="bad-extraction-model",
    )

    with pytest.raises(SchemaValidationError) as error:
        extract_workflow_map_with_provider(
            source=_source(),
            evidence=_evidence(),
            provider=provider,
        )

    assert error.value.model_name == "bad-extraction-model"
    assert raw_phrase not in str(error.value)
