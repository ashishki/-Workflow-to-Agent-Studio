from pathlib import Path

import pytest

from workflow_agent_studio.export import ExportPathError, export_draft_roadmap_report
from workflow_agent_studio.reporting.roadmap_markdown import render_roadmap_markdown
from workflow_agent_studio.roadmap.service import generate_roadmap_report


def test_roadmap_markdown_uses_stable_contract_section_order() -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")

    markdown = render_roadmap_markdown(report)

    headings = [
        "## Executive Summary",
        "## What The Agent Will Not Replace",
        "## Evidence Packet",
        "## Workflow Map",
        "## Process Inventory",
        "## Readiness And Deployment Fit",
        "## AI Opportunity Map",
        "## Recommendation Cards",
        "## Harness Candidate Cards",
        "## Use Case Card Exports",
        "## Cloud Vs Local/Private Recommendation",
        "## Build Vs Buy",
        "## Cost, Time, And Team Plan",
        "## Rollout Plan",
        "## Evaluation Plan",
        "## Governance And Maintenance",
        "## Verification Appendix",
    ]
    positions = [markdown.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "Status: Draft" in markdown
    assert "Appointment booking and reminder automation" in markdown
    assert "Realistic Autonomy Level" in markdown
    assert "Workflow-Specific Agent Myths" in markdown
    assert "Data Readiness" in markdown
    assert "Eval Readiness" in markdown
    assert "Deployment Recommendation" in markdown
    assert "ROI Proxy" in markdown


def test_roadmap_markdown_includes_claims_and_assumptions() -> None:
    report = generate_roadmap_report("docs/examples/domains/ecommerce_input.md")

    markdown = render_roadmap_markdown(report)

    claim = report.verification_appendix.claims_registry[0]
    assumption = report.verification_appendix.assumptions_registry[0]
    assert "### Claims Registry" in markdown
    assert claim.claim_id in markdown
    assert claim.claim_text in markdown
    assert "### Assumptions Registry" in markdown
    assert assumption.assumption_id in markdown
    assert assumption.text in markdown


def test_draft_roadmap_export_writes_markdown_inside_export_dir(tmp_path) -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")

    output = export_draft_roadmap_report(
        report=report,
        export_dir=tmp_path / "exports",
        output_path=Path("roadmaps/legal.md"),
    )

    markdown = output.read_text(encoding="utf-8")
    assert output == (tmp_path / "exports" / "roadmaps" / "legal.md").resolve()
    assert "# SMB AI Roadmap Report" in markdown
    assert "Status: Draft" in markdown
    assert "Local/on-prem" in markdown


def test_draft_roadmap_export_rejects_path_escape(tmp_path) -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")

    with pytest.raises(ExportPathError, match="inside the selected export directory"):
        export_draft_roadmap_report(
            report=report,
            export_dir=tmp_path / "exports",
            output_path=Path("../outside.md"),
        )

    assert not (tmp_path / "outside.md").exists()
