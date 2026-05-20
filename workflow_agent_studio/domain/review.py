"""Review state schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReviewFeedbackCategory = Literal[
    "missing_evidence",
    "wrong_boundary",
    "weak_eval",
    "wrong_integration",
    "unclear_risk",
    "unsupported_claim",
]

REVIEW_FEEDBACK_CATEGORIES: tuple[ReviewFeedbackCategory, ...] = (
    "missing_evidence",
    "wrong_boundary",
    "weak_eval",
    "wrong_integration",
    "unclear_risk",
    "unsupported_claim",
)


class ReviewFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    severity: Literal["blocking", "warning"]
    section: str = Field(min_length=1)
    message: str = Field(min_length=1)
    repair_hint: str = Field(min_length=1)


class ReviewStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["draft", "approved", "rejected"] = "draft"
    findings: list[ReviewFinding] = Field(default_factory=list)


class ReviewFeedback(BaseModel):
    model_config = ConfigDict(extra="forbid")

    feedback_id: str = Field(min_length=1)
    blueprint_version_id: int
    category: ReviewFeedbackCategory
    section: str = Field(min_length=1)
    reviewer_label: str = Field(min_length=1)
    summary: str = Field(min_length=1)


class ReviewFeedbackAnalytics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_count: int
    by_category: dict[ReviewFeedbackCategory, int] = Field(default_factory=dict)
    by_section: dict[str, int] = Field(default_factory=dict)
    by_blueprint_version_id: dict[int, int] = Field(default_factory=dict)
