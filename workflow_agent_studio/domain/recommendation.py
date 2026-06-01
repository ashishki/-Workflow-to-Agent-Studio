"""Roadmap recommendation card schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.privacy import PrivacyClass
from workflow_agent_studio.domain.workflow import EvidenceReference

SolutionType = Literal[
    "do_not_automate_yet",
    "classic_script",
    "api_integration",
    "rpa",
    "llm_assistant",
    "rag_knowledge_assistant",
    "human_in_the_loop_workflow",
    "bounded_ai_agent",
    "high_autonomy_agent_future_only",
]

ConfidenceLevel = Literal["low", "medium", "high"]


class ExpectedValue(StrictModel):
    qualitative: str = Field(min_length=1)
    quantitative_assumption: str = Field(min_length=1)


class RecommendationArchitecture(StrictModel):
    model: str = Field(min_length=1)
    deterministic_components: list[str] = Field(min_length=1)
    llm_components: list[str] = Field(default_factory=list)


class RecommendationCostEstimate(StrictModel):
    one_time_low: int = Field(ge=0)
    one_time_medium: int = Field(ge=0)
    one_time_high: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)

    @model_validator(mode="after")
    def require_ordered_cost_range(self) -> RecommendationCostEstimate:
        if not self.one_time_low <= self.one_time_medium <= self.one_time_high:
            raise ValueError("cost range must be ordered low <= medium <= high")
        return self


class RecommendationTimeEstimate(StrictModel):
    low: str = Field(min_length=1)
    medium: str = Field(min_length=1)
    high: str = Field(min_length=1)


class HumanGate(StrictModel):
    required: bool
    reviewer: str = Field(min_length=1)
    approval_event: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


class RecommendationCard(StrictModel):
    schema_version: Literal["recommendation-card-v1"] = "recommendation-card-v1"
    recommendation_id: str = Field(min_length=1)
    recommendation: str = Field(min_length=1)
    target_workflow_step: str = Field(min_length=1)
    expected_value: ExpectedValue
    required_data: list[str] = Field(min_length=1)
    privacy_class: PrivacyClass
    implementation_option: SolutionType
    architecture: RecommendationArchitecture
    estimated_cost: RecommendationCostEstimate
    estimated_time: RecommendationTimeEstimate
    required_people: list[str] = Field(min_length=1)
    dependencies: list[str] = Field(min_length=1)
    risks: list[str] = Field(min_length=1)
    validation_method: list[str] = Field(min_length=1)
    success_metrics: list[str] = Field(min_length=1)
    confidence_level: ConfidenceLevel
    assumptions: list[str] = Field(default_factory=list)
    evidence: list[EvidenceReference] = Field(default_factory=list)
    fallback_option: str = Field(min_length=1)
    human_gate: HumanGate

    @model_validator(mode="after")
    def require_evidence_or_assumptions(self) -> RecommendationCard:
        if not self.evidence and not self.assumptions:
            raise ValueError("recommendation requires evidence or assumptions")
        return self
