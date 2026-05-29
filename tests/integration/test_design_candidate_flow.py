from dataclasses import replace

from workflow_agent_studio.blueprint import generate_design_candidate_portfolio
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.export import export_design_candidate_portfolio
from workflow_agent_studio.extraction import MissingQuestion, extract_workflow_map
from workflow_agent_studio.retrieval import (
    EvidenceAnchor,
    EvidenceGap,
    EvidenceGapReport,
    EvidenceSnippet,
)


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


def _workflow():
    return extract_workflow_map(source=_source(), evidence=_evidence())


def test_design_candidate_flow_generates_candidate_portfolio() -> None:
    portfolio = generate_design_candidate_portfolio(workflow=_workflow(), evidence=_evidence())

    assert len(portfolio.candidates) >= 3
    assert {draft.candidate.variant for draft in portfolio.candidates} >= {
        "deterministic_first",
        "human_in_the_loop",
        "bounded_agent",
    }
    assert all(draft.status == "ready" for draft in portfolio.candidates)


def test_design_candidates_cite_evidence_and_record_assumptions_separately() -> None:
    workflow = replace(
        _workflow(),
        missing_questions=[
            MissingQuestion(
                section="approval_boundaries",
                question="Which manager approves customer commitments?",
                reason="Approver title is not explicit.",
            )
        ],
    )

    portfolio = generate_design_candidate_portfolio(workflow=workflow, evidence=_evidence())
    draft = portfolio.candidates[0]

    assert draft.candidate.evidence_references[0].source_id == "src-sop"
    assert draft.assumptions
    assert any(item.kind == "assumption" for item in draft.assumptions)


def test_tradeoff_comparison_keeps_consolidation_explicit() -> None:
    portfolio = generate_design_candidate_portfolio(workflow=_workflow(), evidence=_evidence())

    assert portfolio.consolidated_blueprint.workflow_summary.text
    assert len(portfolio.tradeoff_comparison) == len(portfolio.candidates)
    assert {item.variant for item in portfolio.tradeoff_comparison} == {
        draft.candidate.variant for draft in portfolio.candidates
    }
    assert len({item.autonomy_level for item in portfolio.tradeoff_comparison}) > 1
    assert len({item.cost_posture for item in portfolio.tradeoff_comparison}) > 1


def test_insufficient_evidence_keeps_candidates_in_needs_review_status() -> None:
    evidence_gap_report = EvidenceGapReport(
        anchors=[
            EvidenceAnchor(
                source_id="src-sop",
                chunk_id="src-sop:chunk-1",
                label="Support Intake SOP",
                normalized_snippet="Create a follow-up task.",
            )
        ],
        gaps=[
            EvidenceGap(
                section="approval_boundaries",
                question="Who approves workflow actions before commitments are created?",
                reason="No evidence anchor matched required section `approval_boundaries`.",
            )
        ],
    )

    portfolio = generate_design_candidate_portfolio(
        workflow=_workflow(),
        evidence=_evidence(),
        evidence_gaps=evidence_gap_report,
    )

    assert all(draft.status == "needs_review" for draft in portfolio.candidates)
    assert all(draft.candidate.evidence_gaps for draft in portfolio.candidates)
    assert all(draft.assumptions for draft in portfolio.candidates)


def test_design_candidate_portfolio_export_includes_tradeoffs(tmp_path) -> None:
    portfolio = generate_design_candidate_portfolio(workflow=_workflow(), evidence=_evidence())

    exported = export_design_candidate_portfolio(
        portfolio=portfolio,
        export_dir=tmp_path,
        output_path=tmp_path / "portfolio.md",
    )

    text = exported.read_text(encoding="utf-8")
    assert "## Tradeoff Comparison" in text
    assert "deterministic_first" in text
    assert "bounded_agent" in text
    assert "## Consolidated Blueprint" in text
