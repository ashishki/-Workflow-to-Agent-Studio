"""Privacy classification schemas for roadmap recommendations."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel

PrivacyClass = Literal[
    "public",
    "internal",
    "confidential",
    "sensitive",
    "restricted",
]

DetectedPrivacyFlag = Literal[
    "email",
    "phone",
    "address",
    "name_like",
    "passport_or_id",
    "payment_card",
    "api_key_or_credential",
    "health",
    "legal_or_immigration",
    "tax_or_accounting",
    "hr_or_candidate",
    "minor_or_student_data",
]

RedactionStatus = Literal[
    "not_required",
    "required",
    "partially_redacted",
    "redacted",
    "blocked",
]


class PrivacyClassificationResult(StrictModel):
    schema_version: Literal["privacy-classification-v1"] = "privacy-classification-v1"
    detected_flags: list[DetectedPrivacyFlag] = Field(default_factory=list)
    redaction_status: RedactionStatus
    source_privacy_class: PrivacyClass
    recommendation_privacy_class: PrivacyClass
    rationale: str = Field(min_length=1)
