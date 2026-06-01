"""Priority scoring schemas for roadmap recommendations."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel

PriorityBand = Literal[
    "quick_win",
    "strategic_pilot",
    "prepare_first",
    "do_not_automate_yet",
    "classic_automation",
    "human_only",
]

ScoreConfidence = Literal["low", "medium", "high"]


class PriorityScore(StrictModel):
    schema_version: Literal["priority-score-v1"] = "priority-score-v1"
    scoring_model_version: str = Field(min_length=1)
    business_value: int = Field(ge=0, le=100)
    delivery_readiness: int = Field(ge=0, le=100)
    risk_penalty: int = Field(ge=0, le=100)
    priority_band: PriorityBand
    confidence: ScoreConfidence
    rationale: list[str] = Field(min_length=1)
    uncertainty_notes: list[str] = Field(min_length=1)
