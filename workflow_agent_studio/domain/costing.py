"""Cost estimate schemas for SMB roadmap planning."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import Field, model_validator

from workflow_agent_studio.domain.blueprint import StrictModel

CostConfidence = Literal["low", "medium", "high"]


class CostRange(StrictModel):
    low: int = Field(ge=0)
    medium: int = Field(ge=0)
    high: int = Field(ge=0)

    @model_validator(mode="after")
    def require_ordered_range(self) -> CostRange:
        if not self.low <= self.medium <= self.high:
            raise ValueError("cost range must be ordered low <= medium <= high")
        return self


class PriceCardReference(StrictModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    price_card_version: str = Field(min_length=1)
    captured_at: date
    source: str = Field(min_length=1)


class CostEstimate(StrictModel):
    schema_version: Literal["cost-estimate-v1"] = "cost-estimate-v1"
    one_time: CostRange
    monthly: CostRange
    maintenance_monthly: CostRange
    human_review_monthly: CostRange
    integration_subscription_monthly: CostRange
    currency: str = Field(min_length=3, max_length=3)
    assumptions: list[str] = Field(min_length=1)
    confidence: CostConfidence
    price_card_references: list[PriceCardReference] = Field(default_factory=list)
