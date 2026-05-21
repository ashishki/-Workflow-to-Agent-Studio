"""Extracted workflow schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

WorkflowKind = Literal[
    "support_intake",
    "issue_triage",
    "kubernetes_issue_triage",
    "bug_triage",
    "incident_response",
]


class EvidenceReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    quote: str | None = None


class WorkflowStep(BaseModel):
    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    system: str | None = None
    evidence_references: list[EvidenceReference] = Field(default_factory=list)
    assumption: bool = False

    @model_validator(mode="after")
    def require_evidence_or_assumption(self) -> WorkflowStep:
        if not self.evidence_references and not self.assumption:
            raise ValueError("workflow step requires evidence references or an assumption marker")
        return self


class WorkflowMap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_id: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    steps: list[WorkflowStep] = Field(min_length=1)
