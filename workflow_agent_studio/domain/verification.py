"""Verification schemas for roadmap report audit artifacts."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.workflow import EvidenceReference

ClaimType = Literal[
    "observation",
    "inference",
    "recommendation",
    "cost_estimate",
    "risk_assessment",
    "privacy_classification",
    "priority_score",
    "implementation_assumption",
]

EvidenceLevel = Literal[
    "direct",
    "inferred_from_multiple_sources",
    "pattern_based",
    "assumption_only",
    "unsupported_blocked",
]

VerificationConfidence = Literal["low", "medium", "high"]
ClaimStatus = Literal["draft", "accepted", "needs_review", "blocked", "rejected"]
AssumptionStatus = Literal["unresolved", "verified", "rejected", "expired"]
ReviewStatus = Literal["draft", "needs_human_review", "approved", "blocked"]


class RoadmapClaim(StrictModel):
    claim_id: str = Field(min_length=1)
    claim_text: str = Field(min_length=1)
    claim_type: ClaimType
    source_refs: list[EvidenceReference] = Field(default_factory=list)
    evidence_level: EvidenceLevel
    confidence: VerificationConfidence
    created_by: str = Field(min_length=1)
    status: ClaimStatus
    reviewer_notes: list[str] = Field(default_factory=list)


class RoadmapAssumption(StrictModel):
    assumption_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    impact_if_wrong: str = Field(min_length=1)
    verification_method: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    expires_at_stage: str = Field(min_length=1)
    status: AssumptionStatus


class RoadmapEvidenceItem(StrictModel):
    evidence_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    evidence_summary: str = Field(min_length=1)
    redacted: bool


class RecommendationTrace(StrictModel):
    recommendation_id: str = Field(min_length=1)
    target_step_id: str = Field(min_length=1)
    matched_pattern_id: str = Field(min_length=1)
    supporting_claims: list[str] = Field(default_factory=list)
    cost_model_version: str = Field(min_length=1)
    scoring_model_version: str = Field(min_length=1)
    privacy_model_version: str = Field(min_length=1)
    decision_log_id: str = Field(min_length=1)
    review_status: ReviewStatus


class ModelMetadata(StrictModel):
    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    generation_mode: str = Field(min_length=1)


class RoadmapVerificationReceipt(StrictModel):
    schema_version: Literal["roadmap-verification-receipt-v1"] = "roadmap-verification-receipt-v1"
    report_schema_version: str = Field(min_length=1)
    source_hashes: list[str] = Field(min_length=1)
    prompt_versions: dict[str, str] = Field(default_factory=dict)
    model_metadata: ModelMetadata
    pattern_library_version: str = Field(min_length=1)
    privacy_model_version: str = Field(min_length=1)
    cost_model_version: str = Field(min_length=1)
    scoring_model_version: str = Field(min_length=1)
    claim_count: int = Field(ge=0)
    assumption_count: int = Field(ge=0)
    blocking_finding_count: int = Field(ge=0)
    review_status: ReviewStatus
    recommendation_traces: list[RecommendationTrace] = Field(default_factory=list)
