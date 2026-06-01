"""Roadmap report aggregate schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.privacy import PrivacyClass, RedactionStatus
from workflow_agent_studio.domain.recommendation import RecommendationCard, SolutionType
from workflow_agent_studio.domain.verification import (
    RecommendationTrace,
    RoadmapAssumption,
    RoadmapClaim,
    RoadmapEvidenceItem,
    RoadmapVerificationReceipt,
)
from workflow_agent_studio.domain.workflow import EvidenceReference

ReportConfidence = Literal["low", "medium", "high"]


class ExecutiveSummary(StrictModel):
    company_context: str = Field(min_length=1)
    top_recommended_initiatives: list[str] = Field(default_factory=list)
    top_do_not_automate_yet_items: list[str] = Field(default_factory=list)
    roadmap_30_60_90: list[str] = Field(min_length=1)
    overall_privacy_mode_recommendation: str = Field(min_length=1)
    overall_confidence_level: ReportConfidence
    critical_assumptions: list[str] = Field(min_length=1)


class EvidenceSourceSummary(StrictModel):
    source_id: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    source_hash: str = Field(min_length=1)
    extracted_evidence_snippets: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    redaction_status: RedactionStatus
    source_privacy_class: PrivacyClass


class EvidencePacket(StrictModel):
    source_documents: list[EvidenceSourceSummary] = Field(min_length=1)


class RoadmapWorkflowMap(StrictModel):
    workflow_id: str = Field(min_length=1)
    workflow_name: str = Field(min_length=1)
    business_owner: str = Field(min_length=1)
    trigger: str = Field(min_length=1)
    actors: list[str] = Field(min_length=1)
    systems: list[str] = Field(default_factory=list)
    steps: list[str] = Field(min_length=1)
    decisions: list[str] = Field(default_factory=list)
    exceptions: list[str] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    frequency_or_volume: str = Field(min_length=1)
    pain_points: list[str] = Field(default_factory=list)
    current_tools: list[str] = Field(default_factory=list)
    current_manual_effort: str = Field(min_length=1)
    evidence_references: list[EvidenceReference] = Field(default_factory=list)


class ProcessInventoryItem(StrictModel):
    process_id: str = Field(min_length=1)
    process_name: str = Field(min_length=1)
    automation_feasibility_score: int = Field(ge=0, le=100)
    business_impact_score: int = Field(ge=0, le=100)
    privacy_sensitivity_score: int = Field(ge=0, le=100)
    security_risk_score: int = Field(ge=0, le=100)
    data_readiness_score: int = Field(ge=0, le=100)
    implementation_complexity_score: int = Field(ge=0, le=100)
    evaluation_clarity_score: int = Field(ge=0, le=100)
    recommended_solution_type: SolutionType


class RolloutPlan(StrictModel):
    stages: list[str] = Field(min_length=1)


class EvaluationPlan(StrictModel):
    golden_test_cases: list[str] = Field(min_length=1)
    shadow_mode: str = Field(min_length=1)
    human_review_sample: str = Field(min_length=1)
    acceptance_criteria: list[str] = Field(min_length=1)
    regression_tests: list[str] = Field(min_length=1)
    stop_conditions: list[str] = Field(min_length=1)


class GovernancePlan(StrictModel):
    owner: str = Field(min_length=1)
    review_cadence: str = Field(min_length=1)
    approval_rules: list[str] = Field(min_length=1)
    incident_handling: str = Field(min_length=1)
    change_policy: str = Field(min_length=1)
    data_retention: str = Field(min_length=1)
    audit_logs: str = Field(min_length=1)


class VerificationAppendix(StrictModel):
    claims_registry: list[RoadmapClaim] = Field(default_factory=list)
    assumptions_registry: list[RoadmapAssumption] = Field(default_factory=list)
    evidence_table: list[RoadmapEvidenceItem] = Field(default_factory=list)
    recommendation_trace: list[RecommendationTrace] = Field(default_factory=list)
    decision_log: list[str] = Field(default_factory=list)
    reviewer_notes: list[str] = Field(default_factory=list)
    confidence_and_uncertainty_flags: list[str] = Field(default_factory=list)
    receipt: RoadmapVerificationReceipt


class RoadmapReport(StrictModel):
    schema_version: Literal["roadmap-report-v1"] = "roadmap-report-v1"
    report_id: str = Field(min_length=1)
    executive_summary: ExecutiveSummary
    evidence_packet: EvidencePacket
    workflow_map: list[RoadmapWorkflowMap] = Field(min_length=1)
    process_inventory: list[ProcessInventoryItem] = Field(min_length=1)
    recommendations: list[RecommendationCard] = Field(default_factory=list)
    do_not_automate_rationale: list[str] = Field(default_factory=list)
    rollout_plan: RolloutPlan
    evaluation_plan: EvaluationPlan
    governance_plan: GovernancePlan
    verification_appendix: VerificationAppendix

    @model_validator(mode="after")
    def require_recommendation_or_stop_rationale(self) -> RoadmapReport:
        if not self.recommendations and not self.do_not_automate_rationale:
            raise ValueError("report requires recommendations or do-not-automate rationale")
        return self
