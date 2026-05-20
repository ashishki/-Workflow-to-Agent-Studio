from workflow_agent_studio.blueprint import synthesize_blueprint
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.extraction import extract_workflow_map
from workflow_agent_studio.retrieval import (
    EvidenceSnippet,
    build_evidence_anchor_map,
    build_evidence_gap_report,
    chunk_source_document,
)
from workflow_agent_studio.validators import validate_evidence_gap_report


def test_evidence_anchors_include_source_chunk_label_and_normalized_snippet() -> None:
    markdown_chunks = chunk_source_document(
        source_id="src-notes",
        text="# Intake Notes\n\nCoordinator checks the CRM account status.",
    )
    transcript_chunks = chunk_source_document(
        source_id="src-transcript",
        text="Consultant: Walk me through intake.\nClient: It starts in the inbox.",
    )

    anchors = build_evidence_anchor_map([*markdown_chunks, *transcript_chunks])

    assert anchors[0].source_id == "src-notes"
    assert anchors[0].chunk_id == "src-notes:chunk-1"
    assert anchors[0].label == "Intake Notes"
    assert anchors[0].normalized_snippet == "Coordinator checks the CRM account status."
    assert anchors[1].source_id == "src-transcript"
    assert anchors[1].label == "Consultant"
    assert anchors[1].normalized_snippet == (
        "Consultant: Walk me through intake. Client: It starts in the inbox."
    )


def test_evidence_gap_report_lists_missing_required_sections() -> None:
    chunks = chunk_source_document(
        source_id="src-transcript",
        text="Consultant: Workflow source has no implementation details.",
    )
    anchors = build_evidence_anchor_map(chunks)

    report = build_evidence_gap_report(anchors=anchors)
    validation = validate_evidence_gap_report(report)

    assert {gap.section for gap in report.gaps} == {
        "actors",
        "systems",
        "decisions",
        "exceptions",
        "data_fields",
        "approval_boundaries",
    }
    assert report.gap_count == 6
    assert validation.blocking_count == 6
    assert not validation.can_approve


def test_blueprint_synthesis_records_structured_evidence_gaps_as_assumptions() -> None:
    chunks = chunk_source_document(
        source_id="src-transcript",
        text="Consultant: Workflow source has no implementation details.",
    )
    anchors = build_evidence_anchor_map(chunks)
    report = build_evidence_gap_report(anchors=anchors)
    evidence = [
        EvidenceSnippet(
            source_id=anchors[0].source_id,
            chunk_id=anchors[0].chunk_id,
            score=1.0,
            text_preview=anchors[0].normalized_snippet,
            heading_path=(),
        )
    ]
    source = SourceDocument(
        source_id="src-transcript",
        source_type="transcript",
        title="Discovery call",
        fingerprint="abc123",
        normalized_text=chunks[0].text,
    )
    workflow = extract_workflow_map(source=source, evidence=evidence)

    blueprint = synthesize_blueprint(
        workflow=workflow,
        evidence=evidence,
        evidence_gaps=report,
    )

    assumption_text = {item.description for item in blueprint.risks_and_assumptions}
    assert "Which actors participate in this workflow?" in assumption_text
    assert "Who approves workflow actions before commitments are created?" in assumption_text
    assert all(item.kind in {"risk", "assumption"} for item in blueprint.risks_and_assumptions)
