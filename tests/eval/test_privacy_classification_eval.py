from pathlib import Path

from workflow_agent_studio.roadmap.service import generate_roadmap_report
from workflow_agent_studio.validators.privacy import validate_model_mode_recommendation


def test_legal_roadmap_blocks_unrestricted_cloud_mode() -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")
    source = report.evidence_packet.source_documents[0]

    result = validate_model_mode_recommendation(
        privacy_class=source.source_privacy_class,
        redaction_status=source.redaction_status,
        recommended_mode="lightweight_cloud",
        domain="legal_consultancy",
        human_review_gate=True,
    )

    assert not result.can_recommend
    assert any(finding.rule_id == "PRIVACY-RESTRICTED-CLOUD-BLOCK" for finding in result.findings)


def test_demo_reports_include_source_and_recommendation_privacy_classes() -> None:
    for input_path in [
        Path("docs/examples/domains/hair_salon_input.md"),
        Path("docs/examples/domains/ecommerce_input.md"),
        Path("docs/examples/domains/legal_consultancy_input.md"),
    ]:
        report = generate_roadmap_report(input_path)
        source = report.evidence_packet.source_documents[0]

        assert source.source_privacy_class
        assert all(card.privacy_class for card in report.recommendations)
