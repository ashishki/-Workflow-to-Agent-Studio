"""Automation blueprint schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowStep


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Claim(StrictModel):
    text: str = Field(min_length=1)
    evidence_references: list[EvidenceReference] = Field(default_factory=list)
    assumption: bool = False

    @model_validator(mode="after")
    def require_evidence_or_assumption(self) -> Claim:
        if not self.evidence_references and not self.assumption:
            raise ValueError("claim requires evidence references or an assumption marker")
        return self


class Actor(StrictModel):
    name: str = Field(min_length=1)
    role: str = Field(min_length=1)


class SystemRef(StrictModel):
    name: str = Field(min_length=1)
    purpose: str = Field(min_length=1)


class DataField(StrictModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    source: str = Field(min_length=1)


class Integration(StrictModel):
    source_system: str = Field(min_length=1)
    target_system: str = Field(min_length=1)
    data_fields: list[str] = Field(min_length=1)


class AutomationCandidate(StrictModel):
    name: str = Field(min_length=1)
    implementation_boundary: str = Field(min_length=1)
    human_approval_boundary: str = Field(min_length=1)
    risk_level: Literal["low", "medium", "high"]
    evidence_references: list[EvidenceReference] = Field(min_length=1)


class ApprovalBoundary(StrictModel):
    decision: str = Field(min_length=1)
    approver: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class RiskOrAssumption(StrictModel):
    description: str = Field(min_length=1)
    kind: Literal["risk", "assumption"]
    evidence_references: list[EvidenceReference] = Field(default_factory=list)


class EvalCase(StrictModel):
    name: str = Field(min_length=1)
    input_condition: str = Field(min_length=1)
    expected_behavior: str = Field(min_length=1)
    verification_method: str = Field(min_length=1)
    evidence_reference: EvidenceReference


class ImplementationTaskPlan(StrictModel):
    task_id: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    depends_on: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(min_length=1)
    tests_or_evals: list[str] = Field(min_length=1)


class AutomationBlueprint(StrictModel):
    schema_version: Literal["v1"] = "v1"
    workflow_summary: Claim
    actors: list[Actor] = Field(min_length=1)
    systems: list[SystemRef] = Field(min_length=1)
    triggers: list[Claim] = Field(min_length=1)
    inputs: list[DataField] = Field(min_length=1)
    current_workflow_steps: list[WorkflowStep] = Field(min_length=1)
    decisions: list[Claim] = Field(min_length=1)
    exceptions: list[Claim] = Field(min_length=1)
    data_fields: list[DataField] = Field(min_length=1)
    integration_map: list[Integration] = Field(min_length=1)
    pain_points: list[Claim] = Field(min_length=1)
    automation_candidates: list[AutomationCandidate] = Field(min_length=1)
    human_approval_boundaries: list[ApprovalBoundary] = Field(min_length=1)
    risks_and_assumptions: list[RiskOrAssumption] = Field(min_length=1)
    eval_cases: list[EvalCase] = Field(min_length=1)
    observability_needs: list[Claim] = Field(min_length=1)
    rough_effort_band: str = Field(min_length=1)
    next_implementation_tasks: list[ImplementationTaskPlan] = Field(min_length=1)
