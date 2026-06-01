from pathlib import Path

import pytest

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.export import (
    ApprovedExportBlockedError,
    export_approved_roadmap_handoff,
)
from workflow_agent_studio.roadmap.review import build_roadmap_reviewer_output
from workflow_agent_studio.roadmap.service import generate_roadmap_report


def test_approved_roadmap_handoff_includes_tasks_evals_risks_and_gates(tmp_path) -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")
    review = build_roadmap_reviewer_output(
        report,
        reviewer_label="operator",
        approve=True,
    )

    output = export_approved_roadmap_handoff(
        report=report,
        review=review,
        export_dir=tmp_path / "exports",
        output_path=Path("legal-handoff.md"),
    )

    markdown = output.read_text(encoding="utf-8")
    assert "# Roadmap Implementation Handoff" in markdown
    assert "Status: Approved" in markdown
    assert "## Implementation Tasks" in markdown
    assert "## Acceptance Criteria" in markdown
    assert "## Eval Cases" in markdown
    assert "## Risks" in markdown
    assert "## Owner" in markdown
    assert "## Privacy Mode" in markdown
    assert "Local/on-prem" in markdown
    assert "## Human Gates" in markdown
    assert "Legal eligibility decisions" in markdown


def test_unapproved_roadmap_cannot_export_approved_handoff(tmp_path) -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")
    review = build_roadmap_reviewer_output(
        report,
        reviewer_label="operator",
        approve=False,
    )

    with pytest.raises(ApprovedExportBlockedError) as blocked:
        export_approved_roadmap_handoff(
            report=report,
            review=review,
            export_dir=tmp_path / "exports",
            output_path=Path("handoff.md"),
        )

    assert any(
        finding.rule_id == "ROADMAP-HANDOFF-APPROVAL-REQUIRED" for finding in blocked.value.findings
    )
    assert not (tmp_path / "exports" / "handoff.md").exists()


def test_blocked_roadmap_cannot_export_approved_handoff(tmp_path) -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")
    payload = report.model_dump(mode="json")
    payload["verification_appendix"]["receipt"]["blocking_finding_count"] = 1
    blocked_report = RoadmapReport.model_validate(payload)
    review = build_roadmap_reviewer_output(
        blocked_report,
        reviewer_label="operator",
        approve=True,
    )

    with pytest.raises(ApprovedExportBlockedError) as blocked:
        export_approved_roadmap_handoff(
            report=blocked_report,
            review=review,
            export_dir=tmp_path / "exports",
            output_path=Path("handoff.md"),
        )

    assert any(
        finding.rule_id == "ROADMAP-REVIEW-BLOCKING-FINDINGS" for finding in blocked.value.findings
    )
    assert not (tmp_path / "exports" / "handoff.md").exists()
