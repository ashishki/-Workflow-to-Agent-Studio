from workflow_agent_studio.blueprint import generate_design_candidate_portfolio
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


def test_generated_candidates_include_permission_runtime_boundaries() -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())
    portfolio = generate_design_candidate_portfolio(workflow=workflow, evidence=_evidence())

    for draft in portfolio.candidates:
        boundary = draft.candidate.permission_runtime_boundary
        assert boundary.tool_surfaces
        assert boundary.human_approval_points
        assert boundary.runtime_justification.rationale
        assert boundary.runtime_justification.mutability
        assert boundary.runtime_justification.privilege_level
        assert boundary.runtime_justification.blast_radius


def test_generated_risky_tool_surfaces_include_confirmation_or_sandbox() -> None:
    workflow = extract_workflow_map(source=_source(), evidence=_evidence())
    portfolio = generate_design_candidate_portfolio(workflow=workflow, evidence=_evidence())

    risky_surfaces = [
        surface
        for draft in portfolio.candidates
        for surface in draft.candidate.permission_runtime_boundary.tool_surfaces
        if surface.write_surfaces or surface.destructive_surfaces
    ]

    assert risky_surfaces
    assert all(
        surface.confirmation_required or surface.sandbox_recommended for surface in risky_surfaces
    )
