from pathlib import Path

import pytest

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.roadmap.service import generate_roadmap_report

DOMAIN_INPUTS = [
    Path("docs/examples/domains/hair_salon_input.md"),
    Path("docs/examples/domains/ecommerce_input.md"),
    Path("docs/examples/domains/legal_consultancy_input.md"),
]


@pytest.mark.parametrize("input_path", DOMAIN_INPUTS)
def test_roadmap_service_creates_valid_report_for_demo_inputs(input_path: Path) -> None:
    report = generate_roadmap_report(input_path)

    reparsed = RoadmapReport.model_validate(report.model_dump(mode="json"))

    assert reparsed == report
    assert report.recommendations
    assert report.executive_summary.top_do_not_automate_yet_items
    assert report.do_not_automate_rationale
    assert report.executive_summary.overall_privacy_mode_recommendation
    assert report.verification_appendix.receipt.source_hashes
    assert report.verification_appendix.recommendation_trace
    assert report.verification_appendix.claims_registry


def test_legal_demo_report_requires_local_or_private_privacy_mode() -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")

    assert "Local/on-prem" in report.executive_summary.overall_privacy_mode_recommendation
    assert report.recommendations[0].privacy_class == "restricted"
    assert "Legal eligibility decisions" in report.do_not_automate_rationale
