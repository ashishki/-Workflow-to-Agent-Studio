"""Workflow-to-agent design candidate schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

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


class ToolSurfaceBoundary(StrictModel):
    tool_name: str = Field(min_length=1)
    read_surfaces: list[str] = Field(default_factory=list)
    write_surfaces: list[str] = Field(default_factory=list)
    destructive_surfaces: list[str] = Field(default_factory=list)
    confirmation_required: bool = False
    sandbox_recommended: bool = False
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def require_control_for_risky_surfaces(self) -> ToolSurfaceBoundary:
        if (self.write_surfaces or self.destructive_surfaces) and not (
            self.confirmation_required or self.sandbox_recommended
        ):
            raise ValueError(
                "write or destructive tool surfaces require confirmation or sandbox recommendation"
            )
        return self


class RuntimeTierJustification(StrictModel):
    runtime_tier: RuntimeTier
    mutability: Literal["read_only", "draft_only", "writes_allowed", "destructive"]
    privilege_level: Literal["none", "low", "medium", "high"]
    blast_radius: Literal["local", "team", "customer", "production"]
    rationale: str = Field(min_length=1)


class PermissionRuntimeBoundary(StrictModel):
    runtime_tier: RuntimeTier
    runtime_justification: RuntimeTierJustification
    tool_surfaces: list[ToolSurfaceBoundary] = Field(min_length=1)
    human_approval_points: list[str] = Field(min_length=1)


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
    permission_runtime_boundary: PermissionRuntimeBoundary
    human_approvals: list[ApprovalBoundary] = Field(min_length=1)
    runtime_tier: RuntimeTier
    eval_needs: list[EvalNeed] = Field(min_length=1)
    risks: list[RiskOrAssumption] = Field(min_length=1)
    cost_posture: CostPosture
    evidence_gaps: list[EvidenceGap]
    evidence_references: list[EvidenceReference] = Field(min_length=1)
