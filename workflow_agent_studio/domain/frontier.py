"""Frontier-model opportunity candidate schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.privacy import PrivacyClass
from workflow_agent_studio.domain.recommendation import HumanGate, SolutionType

FrontierConfidence = Literal["low", "medium", "high"]
FrontierCandidateStatus = Literal["unapproved", "needs_human_review", "rejected"]


class FrontierOpportunityCandidate(StrictModel):
    """Unapproved roadmap opportunity proposed by a frontier model."""

    schema_version: Literal["frontier-opportunity-candidate-v1"] = (
        "frontier-opportunity-candidate-v1"
    )
    opportunity_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    workflow_step: str = Field(min_length=1)
    candidate_solution_type: SolutionType
    why_it_may_help: list[str] = Field(min_length=1)
    why_it_may_not_help: list[str] = Field(min_length=1)
    required_data: list[str] = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    human_gate: HumanGate
    do_not_automate: list[str] = Field(min_length=1)
    critical_assumptions: list[str] = Field(default_factory=list)
    privacy_class: PrivacyClass
    privacy_notes: list[str] = Field(min_length=1)
    cost_drivers: list[str] = Field(min_length=1)
    eval_cases: list[str] = Field(min_length=1)
    confidence: FrontierConfidence
    reject_if: list[str] = Field(min_length=1)
    status: FrontierCandidateStatus = "unapproved"


class FrontierDiscoveryResult(StrictModel):
    """Structured output expected from frontier opportunity discovery."""

    schema_version: Literal["frontier-discovery-result-v1"] = "frontier-discovery-result-v1"
    candidates: list[FrontierOpportunityCandidate] = Field(min_length=1)
    rejected_candidate_titles: list[str] = Field(default_factory=list)
    model_notes: list[str] = Field(default_factory=list)


class FrontierVerificationFinding(StrictModel):
    """Deterministic verifier finding for a frontier candidate."""

    rule_id: str = Field(min_length=1)
    severity: Literal["blocking", "warning"]
    message: str = Field(min_length=1)
    repair_hint: str = Field(min_length=1)


class FrontierCandidateVerification(StrictModel):
    """Verification result for one unapproved frontier candidate."""

    opportunity_id: str = Field(min_length=1)
    status: FrontierCandidateStatus
    exportable_as_recommendation: bool = False
    findings: list[FrontierVerificationFinding] = Field(default_factory=list)


class FrontierDiscoveryVerification(StrictModel):
    """Verification result for a complete frontier discovery payload."""

    schema_version: Literal["frontier-discovery-verification-v1"] = (
        "frontier-discovery-verification-v1"
    )
    candidate_reviews: list[FrontierCandidateVerification] = Field(min_length=1)
    blocking_finding_count: int = Field(ge=0)
    warning_finding_count: int = Field(ge=0)
