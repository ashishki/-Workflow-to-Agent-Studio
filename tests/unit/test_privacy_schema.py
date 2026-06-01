import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.privacy import PrivacyClassificationResult


def _classification_data(
    source_privacy_class: str = "sensitive",
    recommendation_privacy_class: str = "confidential",
) -> dict:
    return {
        "detected_flags": ["email", "address", "api_key_or_credential"],
        "redaction_status": "required",
        "source_privacy_class": source_privacy_class,
        "recommendation_privacy_class": recommendation_privacy_class,
        "rationale": "Customer contact fields and credentials require redaction before planning.",
    }


def test_privacy_schema_accepts_required_privacy_classes() -> None:
    privacy_classes = {
        "public",
        "internal",
        "confidential",
        "sensitive",
        "restricted",
    }

    source_results = [
        PrivacyClassificationResult.model_validate(
            _classification_data(source_privacy_class=privacy_class)
        )
        for privacy_class in privacy_classes
    ]
    recommendation_results = [
        PrivacyClassificationResult.model_validate(
            _classification_data(recommendation_privacy_class=privacy_class)
        )
        for privacy_class in privacy_classes
    ]

    assert {result.source_privacy_class for result in source_results} == privacy_classes
    assert {
        result.recommendation_privacy_class for result in recommendation_results
    } == privacy_classes


def test_privacy_schema_records_flags_redaction_and_classes() -> None:
    result = PrivacyClassificationResult.model_validate(_classification_data())

    assert result.schema_version == "privacy-classification-v1"
    assert result.detected_flags == ["email", "address", "api_key_or_credential"]
    assert result.redaction_status == "required"
    assert result.source_privacy_class == "sensitive"
    assert result.recommendation_privacy_class == "confidential"
    assert result.rationale


def test_privacy_schema_rejects_unknown_source_privacy_class() -> None:
    data = _classification_data(source_privacy_class="moderate")

    with pytest.raises(ValidationError, match="source_privacy_class"):
        PrivacyClassificationResult.model_validate(data)


def test_privacy_schema_rejects_unknown_recommendation_privacy_class() -> None:
    data = _classification_data(recommendation_privacy_class="moderate")

    with pytest.raises(ValidationError, match="recommendation_privacy_class"):
        PrivacyClassificationResult.model_validate(data)
