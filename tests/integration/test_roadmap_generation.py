from pathlib import Path

import pytest

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.roadmap.service import generate_roadmap_report

DOMAIN_INPUTS = [
    Path("docs/examples/domains/hair_salon_input.md"),
    Path("docs/examples/domains/ecommerce_input.md"),
    Path("docs/examples/domains/legal_consultancy_input.md"),
]

PUBLIC_SOURCE_INPUTS = [
    Path("tests/fixtures/public_sources/hvac_lead_intake.notes.md"),
    Path("tests/fixtures/public_sources/netbox_issue_triage.notes.md"),
    Path("tests/fixtures/public_sources/gitlab_incident_workflow.notes.md"),
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
    assert report.agent_expectation_check.what_agent_will_not_replace
    assert report.agent_expectation_check.workflow_specific_myths
    assert report.verification_appendix.receipt.source_hashes
    assert report.verification_appendix.recommendation_trace
    assert report.verification_appendix.claims_registry


def test_legal_demo_report_requires_local_or_private_privacy_mode() -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")

    assert "Local/on-prem" in report.executive_summary.overall_privacy_mode_recommendation
    assert report.recommendations[0].privacy_class == "restricted"
    assert "Legal eligibility decisions" in report.do_not_automate_rationale
    assert report.agent_expectation_check.realistic_autonomy_level == "human_in_the_loop"
    assert "Sensitive or high-impact decisions" in " ".join(
        report.agent_expectation_check.workflow_specific_myths
    )


@pytest.mark.parametrize("input_path", PUBLIC_SOURCE_INPUTS)
def test_roadmap_service_creates_valid_report_for_public_source_inputs(
    input_path: Path,
) -> None:
    report = generate_roadmap_report(input_path)

    reparsed = RoadmapReport.model_validate(report.model_dump(mode="json"))

    assert reparsed == report
    assert report.evidence_packet.source_documents[0].source_type == "public_source_markdown"
    assert report.agent_expectation_check.proof_gates_before_rollout
    assert report.recommendations
    assert report.do_not_automate_rationale
    assert report.verification_appendix.recommendation_trace


def test_public_hvac_report_uses_public_source_lead_intake_pattern() -> None:
    report = generate_roadmap_report("tests/fixtures/public_sources/hvac_lead_intake.notes.md")

    assert report.report_id == "RPT-HVAC-001"
    assert "lead_qualification:v1" in (
        report.verification_appendix.recommendation_trace[0].matched_pattern_id
    )
    assert "automatic lead rejection" in report.do_not_automate_rationale


def test_public_incident_report_keeps_incident_actions_human_approved() -> None:
    report = generate_roadmap_report(
        "tests/fixtures/public_sources/gitlab_incident_workflow.notes.md"
    )

    assert "Private analysis" in report.executive_summary.overall_privacy_mode_recommendation
    assert "paging responders" in report.do_not_automate_rationale
    assert report.recommendations[0].human_gate.required
    assert report.recommendations[0].human_gate.reviewer == "Incident manager"
    assert "live incident" in report.recommendations[0].human_gate.approval_event
    assert report.agent_expectation_check.realistic_autonomy_level == "human_in_the_loop"
    assert "autonomous paging blocker" in report.agent_expectation_check.proof_gates_before_rollout
