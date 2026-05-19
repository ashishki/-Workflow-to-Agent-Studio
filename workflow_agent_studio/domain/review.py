"""Review state schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
