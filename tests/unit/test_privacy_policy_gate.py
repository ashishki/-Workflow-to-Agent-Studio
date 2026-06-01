from pathlib import Path

from workflow_agent_studio.privacy.classifier import classify_privacy
from workflow_agent_studio.validators.privacy import validate_model_mode_recommendation


def test_restricted_legal_fixture_blocks_lightweight_cloud_without_condition() -> None:
    text = Path("tests/fixtures/smb/legal_consultancy.txt").read_text(encoding="utf-8")
    classification = classify_privacy(text)

    result = validate_model_mode_recommendation(
        privacy_class=classification.source_privacy_class,
        redaction_status=classification.redaction_status,
        recommended_mode="lightweight_cloud",
        domain="legal_consultancy",
        human_review_gate=True,
    )

    assert not result.can_recommend
    assert any(finding.rule_id == "PRIVACY-RESTRICTED-CLOUD-BLOCK" for finding in result.findings)


def test_restricted_redacted_source_can_use_cloud_when_report_states_condition() -> None:
    result = validate_model_mode_recommendation(
        privacy_class="restricted",
        redaction_status="redacted",
        recommended_mode="lightweight_cloud",
        domain="legal_consultancy",
        source_is_synthetic_or_redacted=True,
        report_condition="Use only redacted metadata and synthetic examples in cloud mode.",
        human_review_gate=True,
    )

    assert result.can_recommend


def test_sensitive_ecommerce_fixture_requires_redaction_note_for_cloud() -> None:
    classification = classify_privacy(
        "Customer email shopper@example.test and shipping address 123 Market Street "
        "for Order ID ORD-12345."
    )

    result = validate_model_mode_recommendation(
        privacy_class=classification.source_privacy_class,
        redaction_status=classification.redaction_status,
        recommended_mode="lightweight_cloud",
        domain="ecommerce",
    )

    assert not result.can_recommend
    assert any(
        finding.rule_id == "PRIVACY-SENSITIVE-CLOUD-REDACTION-NOTE" for finding in result.findings
    )


def test_salon_fixture_allows_cloud_after_redaction_note() -> None:
    text = Path("tests/fixtures/smb/salon_appointment.txt").read_text(encoding="utf-8")
    classification = classify_privacy(text)

    result = validate_model_mode_recommendation(
        privacy_class=classification.source_privacy_class,
        redaction_status="redacted",
        recommended_mode="lightweight_cloud",
        domain="hair_salon",
        report_condition=(
            "Cloud mode is allowed only after redaction preserves appointment context."
        ),
    )

    assert result.can_recommend


def test_high_risk_domains_require_human_review_gate() -> None:
    result = validate_model_mode_recommendation(
        privacy_class="confidential",
        redaction_status="not_required",
        recommended_mode="private_analysis",
        domain="finance",
        human_review_gate=False,
    )

    assert not result.can_recommend
    assert any(finding.rule_id == "PRIVACY-HIGH-RISK-HUMAN-GATE" for finding in result.findings)
