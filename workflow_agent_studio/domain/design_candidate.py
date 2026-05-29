"""Workflow-to-agent design candidate schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import ApprovalBoundary, RiskOrAssumption, StrictModel
from workflow_agent_studio.domain.workflow import EvidenceReference

DesignCandidateVariant = Literal[
    "deterministic_first",
    "human_in_the_loop",
    "bounded_agent",
    "high_autonomy",
    "compliance_heavy",
    "low_cost_mvp",
]

AutonomyLevel = Literal["none", "assisted", "bounded", "high"]
RuntimeTier = Literal["T0", "T1", "T2"]
CostPosture = Literal["low", "medium", "high", "variable"]


class ToolRequirement(StrictModel):
    name: str = Field(min_length=1)
    permission_boundary: str = Field(min_length=1)
    evidence_references: list[EvidenceReference] = Field(default_factory=list)


class EvalNeed(StrictModel):
    name: str = Field(min_length=1)
    expected_behavior: str = Field(min_length=1)
    verification_method: str = Field(min_length=1)
    evidence_references: list[EvidenceReference] = Field(default_factory=list)


class EvidenceGap(StrictModel):
    section: str = Field(min_length=1)
    question: str = Field(min_length=1)
    impact: str = Field(min_length=1)


class AgentDesignCandidate(StrictModel):
    schema_version: Literal["design-candidate-v1"] = "design-candidate-v1"
    variant: DesignCandidateVariant
    name: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    autonomy_level: AutonomyLevel
    required_tools: list[ToolRequirement]
    human_approvals: list[ApprovalBoundary] = Field(min_length=1)
    runtime_tier: RuntimeTier
    eval_needs: list[EvalNeed] = Field(min_length=1)
    risks: list[RiskOrAssumption] = Field(min_length=1)
    cost_posture: CostPosture
    evidence_gaps: list[EvidenceGap]
    evidence_references: list[EvidenceReference] = Field(min_length=1)
