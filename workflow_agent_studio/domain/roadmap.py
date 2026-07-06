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
AutonomyLevel = Literal[
    "assistive",
    "human_in_the_loop",
    "bounded_agent_with_human_gate",
    "high_autonomy_not_recommended",
]
RiskLevel = Literal["low", "medium", "high", "regulated"]
ReadinessStatus = Literal["ready", "prepare_first", "blocked"]
TcoComplexity = Literal["low", "medium", "high"]
AutonomyFitMode = Literal["deterministic", "workflow", "bounded_agent", "autonomous_routine"]
DeploymentTarget = Literal[
    "local",
    "github_action",
    "hosted_sandbox",
    "self_hosted_worker",
    "cloud_function",
    "not_recommended",
]
DeploymentFit = Literal[
    "not_recommended",
    "manual_only",
    "scheduled_routine_candidate",
    "event_driven_candidate",
    "bounded_worker_candidate",
]


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


class AgentExpectationCheck(StrictModel):
    realistic_autonomy_level: AutonomyLevel
    autonomy_rationale: str = Field(min_length=1)
    what_agent_will_not_replace: list[str] = Field(min_length=1)
    workflow_specific_myths: list[str] = Field(min_length=1)
    required_human_capabilities: list[str] = Field(min_length=1)
    proof_gates_before_rollout: list[str] = Field(min_length=1)


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


class RoiProxy(StrictModel):
    fte_minutes_saved: str = Field(default="not estimated", min_length=1)
    cycle_time_delta: str = Field(default="not estimated", min_length=1)
    error_rate_delta: str = Field(default="not estimated", min_length=1)
    throughput_delta: str = Field(default="not estimated", min_length=1)
    service_delta: str = Field(default="not estimated", min_length=1)
    evidence_basis: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def reject_unsupported_roi_claims(self) -> RoiProxy:
        values = [
            self.fte_minutes_saved,
            self.cycle_time_delta,
            self.error_rate_delta,
            self.throughput_delta,
            self.service_delta,
        ]
        text = " ".join(values).casefold()
        forbidden = ("guaranteed", "guarantee", "proven roi", "certain payback")
        if any(term in text for term in forbidden):
            raise ValueError("roi_proxy cannot contain guaranteed or proven ROI claims")
        estimated_values = {
            "not estimated",
            "unknown",
            "tbd",
            "not estimated from demo evidence",
        }
        if not self.evidence_basis and any(
            value.casefold() not in estimated_values for value in values
        ):
            raise ValueError("roi_proxy requires evidence_basis for specific value claims")
        return self


class AutonomyFit(StrictModel):
    deterministic: str = Field(min_length=1)
    workflow: str = Field(min_length=1)
    bounded_agent: str = Field(min_length=1)
    autonomous_routine: str = Field(min_length=1)
    recommended_mode: AutonomyFitMode


class WorkflowCandidateScore(StrictModel):
    schema_version: Literal["workflow-candidate-score-v1"] = "workflow-candidate-score-v1"
    process_id: str = Field(min_length=1)
    recommendation_id: str = Field(min_length=1)
    feasibility: int = Field(ge=1, le=5)
    data_readiness: int = Field(ge=1, le=5)
    eval_readiness: int = Field(ge=1, le=5)
    risk_level: RiskLevel
    tco_complexity: TcoComplexity
    roi_proxy: RoiProxy
    autonomy_fit: AutonomyFit
    deployment_fit: DeploymentTarget
    evidence: list[EvidenceReference] = Field(default_factory=list)
    caveats: list[str] = Field(min_length=1)


class DataReadinessReport(StrictModel):
    schema_version: Literal["data-readiness-report-v1"] = "data-readiness-report-v1"
    status: ReadinessStatus
    score: int = Field(ge=0, le=100)
    ready_sources: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    required_next_questions: list[str] = Field(min_length=1)
    evidence: list[EvidenceReference] = Field(default_factory=list)


class EvalReadinessReport(StrictModel):
    schema_version: Literal["eval-readiness-report-v1"] = "eval-readiness-report-v1"
    status: ReadinessStatus
    score: int = Field(ge=0, le=100)
    golden_cases: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    required_next_questions: list[str] = Field(min_length=1)
    evidence: list[EvidenceReference] = Field(default_factory=list)


class HarnessCandidateCard(StrictModel):
    schema_version: Literal["harness-candidate-card-v1"] = "harness-candidate-card-v1"
    recommendation_id: str = Field(min_length=1)
    harness_boundary: str = Field(min_length=1)
    tools: list[str] = Field(default_factory=list)
    memory_policy: str = Field(min_length=1)
    retry_recovery_policy: str = Field(min_length=1)
    permission_policy: str = Field(min_length=1)
    human_handoff: str = Field(min_length=1)
    trace_requirements: list[str] = Field(min_length=1)
    eval_required: list[str] = Field(min_length=1)


class AutonomousDeploymentRecommendation(StrictModel):
    schema_version: Literal["autonomous-deployment-recommendation-v1"] = (
        "autonomous-deployment-recommendation-v1"
    )
    recommendation_id: str = Field(min_length=1)
    fit: DeploymentFit
    trigger_contract: str = Field(min_length=1)
    runtime_target: DeploymentTarget
    idempotency_key: str = Field(min_length=1)
    secrets_boundary: str = Field(min_length=1)
    fallback_policy: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    blockers: list[str] = Field(default_factory=list)


class UseCaseCardExport(StrictModel):
    schema_version: Literal["use-case-card-export-v1"] = "use-case-card-export-v1"
    use_case_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    problem: str = Field(min_length=1)
    current_workflow: str = Field(min_length=1)
    ai_opportunity: str = Field(min_length=1)
    data_required: list[str] = Field(min_length=1)
    risk_privacy: list[str] = Field(min_length=1)
    human_in_loop: str = Field(min_length=1)
    eval_plan: list[str] = Field(min_length=1)
    tco_complexity: TcoComplexity
    mvp_scope: str = Field(min_length=1)
    production_hardening: list[str] = Field(min_length=1)
    evidence: list[EvidenceReference] = Field(default_factory=list)


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
    agent_expectation_check: AgentExpectationCheck
    evidence_packet: EvidencePacket
    workflow_map: list[RoadmapWorkflowMap] = Field(min_length=1)
    process_inventory: list[ProcessInventoryItem] = Field(min_length=1)
    workflow_candidate_scores: list[WorkflowCandidateScore] = Field(default_factory=list)
    data_readiness_report: DataReadinessReport | None = None
    eval_readiness_report: EvalReadinessReport | None = None
    harness_candidate_cards: list[HarnessCandidateCard] = Field(default_factory=list)
    autonomous_deployment_recommendations: list[AutonomousDeploymentRecommendation] = Field(
        default_factory=list
    )
    use_case_card_exports: list[UseCaseCardExport] = Field(default_factory=list)
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
