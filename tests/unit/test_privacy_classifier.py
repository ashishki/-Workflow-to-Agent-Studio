from pathlib import Path

import pytest

from workflow_agent_studio.privacy.classifier import classify_privacy


@pytest.mark.parametrize(
    ("text", "flag"),
    [
        ("Contact support at customer@example.test", "email"),
        ("Call +1 555 222 0199 before dispatch.", "phone"),
        ("Ship to 123 Market Street tomorrow.", "address"),
        ("Customer name: Jane Miller", "name_like"),
        ("Order ID ORD-12345 needs review.", None),
        ("Passport copy is attached.", "passport_or_id"),
        ("Payment card 4111 1111 1111 1111 was pasted.", "payment_card"),
        ("API key: sk_test_placeholder123", "api_key_or_credential"),
        ("Immigration legal status review is needed.", "legal_or_immigration"),
        ("Diagnosis notes are part of the intake.", "health"),
        ("Tax filing workflow uses IRS documents.", "tax_or_accounting"),
        ("Candidate resume review includes background check.", "hr_or_candidate"),
        ("Student record mentions a guardian for a minor.", "minor_or_student_data"),
    ],
)
def test_classifier_covers_required_privacy_eval_categories(text: str, flag: str | None) -> None:
    result = classify_privacy(text)

    if flag is not None:
        assert flag in result.detected_flags
    assert result.source_privacy_class in {"sensitive", "restricted"}


def test_public_internal_and_confidential_examples_classify_without_sensitive_flags() -> None:
    assert classify_privacy("Public FAQ text for store hours.").source_privacy_class == "public"
    assert classify_privacy("Internal SOP for queue handoff.").source_privacy_class == "internal"
    assert (
        classify_privacy("Private pricing and margin review process.").source_privacy_class
        == "confidential"
    )


def test_secret_like_values_are_blocked_from_export() -> None:
    result = classify_privacy("API key: sk_test_placeholder123")

    assert result.source_privacy_class == "restricted"
    assert result.redaction_status == "blocked"
    assert "api_key_or_credential" in result.detected_flags


def test_legal_consultancy_fixture_is_restricted() -> None:
    text = Path("tests/fixtures/smb/legal_consultancy.txt").read_text(encoding="utf-8")

    result = classify_privacy(text)

    assert result.source_privacy_class == "restricted"
    assert "passport_or_id" in result.detected_flags
    assert "legal_or_immigration" in result.detected_flags


def test_salon_fixture_is_sensitive_not_restricted() -> None:
    text = Path("tests/fixtures/smb/salon_appointment.txt").read_text(encoding="utf-8")

    result = classify_privacy(text)

    assert result.source_privacy_class == "sensitive"
    assert result.source_privacy_class != "restricted"
    assert {"email", "phone", "name_like"}.issubset(result.detected_flags)


def test_false_positive_fixture_stays_internal_or_confidential() -> None:
    text = Path("tests/fixtures/smb/false_positive_internal.txt").read_text(encoding="utf-8")

    result = classify_privacy(text)

    assert result.source_privacy_class in {"internal", "confidential"}
    assert result.source_privacy_class != "restricted"
