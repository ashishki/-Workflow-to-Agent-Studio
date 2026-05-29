from workflow_agent_studio.blueprint import generate_design_candidate_portfolio
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.export import ApprovedExportBlockedError, export_playbook_artifacts
from workflow_agent_studio.extraction import extract_workflow_map
from workflow_agent_studio.retrieval import EvidenceGap, EvidenceGapReport, EvidenceSnippet


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
            "A manager approval is required before customer commitments are created."
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


def _ready_design():
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())
    return generate_design_candidate_portfolio(workflow=workflow, evidence=_evidence()).candidates[
        0
    ]


def test_playbook_export_includes_required_artifact_sections(tmp_path) -> None:
    exported = export_playbook_artifacts(
        design=_ready_design(),
        export_dir=tmp_path,
        output_path=tmp_path / "playbook.md",
        approved_by="operator",
        approved_at="2026-05-29T00:00:00+00:00",
    )

    text = exported.read_text(encoding="utf-8")
    assert "# AI Workflow Playbook Artifact Export" in text
    assert "Authority: Convenience artifact only." in text
    assert "## Runtime Tier" in text
    assert "## Tool Permission Boundaries" in text
    assert "## Human Approval Points" in text
    assert "## Implementation Contract Deltas" in text
    assert "## Eval Artifact Skeletons" in text
    assert "## Task Blocks" in text


def test_playbook_export_tasks_include_context_refs(tmp_path) -> None:
    exported = export_playbook_artifacts(
        design=_ready_design(),
        export_dir=tmp_path,
        output_path=tmp_path / "playbook.md",
        approved_by="operator",
        approved_at="2026-05-29T00:00:00+00:00",
    )

    text = exported.read_text(encoding="utf-8")
    assert "Context-Refs: src-sop#src-sop:chunk-1" in text
    assert "TASK-1: Implement Design Boundary" in text
    assert "TASK-2: Add Eval Gate" in text


def test_playbook_export_rejects_needs_review_design(tmp_path) -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())
    portfolio = generate_design_candidate_portfolio(
        workflow=workflow,
        evidence=_evidence(),
        evidence_gaps=EvidenceGapReport(
            anchors=[],
            gaps=[
                EvidenceGap(
                    section="approval_boundaries",
                    question="Who approves workflow actions?",
                    reason="No approval evidence found.",
                )
            ],
        ),
    )

    try:
        export_playbook_artifacts(
            design=portfolio.candidates[0],
            export_dir=tmp_path,
            output_path=tmp_path / "playbook.md",
            approved_by="operator",
            approved_at="2026-05-29T00:00:00+00:00",
        )
    except ApprovedExportBlockedError as error:
        assert any(
            finding.rule_id == "PLAYBOOK-DESIGN-APPROVAL-REQUIRED" for finding in error.findings
        )
    else:
        raise AssertionError("needs_review designs must not export as approved artifacts")

    assert not (tmp_path / "playbook.md").exists()
