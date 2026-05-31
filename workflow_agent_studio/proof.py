"""Entropy Core-compatible proof receipts for blueprint exports."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.domain.workflow import EvidenceReference

PROOF_RECEIPT_SCHEMA_VERSION = "entropy_core.product_receipt.v1"
PRODUCT_ID = "workflow-to-agent-studio"
SHA256_HEX_LENGTH = 64


class BlueprintProofEvidenceRef(BaseModel):
    model_config = ConfigDict(frozen=True)

    source_id: str = Field(min_length=1)
    chunk_id: str = Field(min_length=1)
    supports: str = Field(min_length=1)
    quote_sha256: str | None = Field(
        default=None, min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )

    @field_validator("quote_sha256")
    @classmethod
    def quote_hash_must_be_sha256(cls, value: str | None) -> str | None:
        if value is not None and any(char not in "0123456789abcdef" for char in value):
            raise ValueError("quote_sha256 must be lowercase hexadecimal")
        return value


class BlueprintProofReceipt(BaseModel):
    model_config = ConfigDict(frozen=True)

    type: Literal["blueprint_proof_receipt"] = "blueprint_proof_receipt"
    schema_version: Literal["entropy_core.product_receipt.v1"] = PROOF_RECEIPT_SCHEMA_VERSION
    product_id: Literal["workflow-to-agent-studio"] = PRODUCT_ID
    blueprint_schema_version: str = Field(min_length=1)
    artifact_ref: str = Field(min_length=1)
    artifact_sha256: str = Field(min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH)
    generated_at: datetime
    evidence_refs: tuple[BlueprintProofEvidenceRef, ...] = Field(min_length=1)
    assumption_count: int = Field(ge=0)
    verifier_status: Literal["passed", "needs_review", "failed"]
    verifier_notes: tuple[str, ...] = ()
    entropy_core_level: Literal["schema_compatible", "evidence_lookup_compatible"] = (
        "schema_compatible"
    )

    @field_validator("artifact_sha256")
    @classmethod
    def artifact_hash_must_be_sha256(cls, value: str) -> str:
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("artifact_sha256 must be lowercase hexadecimal")
        return value

    @model_validator(mode="after")
    def non_passed_status_requires_notes(self) -> BlueprintProofReceipt:
        if self.verifier_status != "passed" and not self.verifier_notes:
            raise ValueError("non-passed proof receipts require verifier_notes")
        return self

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=True)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    def receipt_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


def build_blueprint_proof_receipt(
    *,
    blueprint: AutomationBlueprint,
    artifact_ref: Path | str,
    artifact_payload: str | None = None,
    generated_at: datetime | None = None,
) -> BlueprintProofReceipt:
    payload = artifact_payload or blueprint.model_dump_json()
    evidence_refs = _collect_blueprint_evidence_refs(blueprint)
    assumption_count = _count_assumptions(blueprint)
    verifier_status: Literal["passed", "needs_review", "failed"] = (
        "passed" if evidence_refs else "failed"
    )
    notes = () if evidence_refs else ("blueprint has no evidence references",)
    return BlueprintProofReceipt(
        blueprint_schema_version=blueprint.schema_version,
        artifact_ref=str(artifact_ref),
        artifact_sha256=hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        generated_at=generated_at or datetime.now(UTC),
        evidence_refs=evidence_refs,
        assumption_count=assumption_count,
        verifier_status=verifier_status,
        verifier_notes=notes,
    )


def _collect_blueprint_evidence_refs(
    blueprint: AutomationBlueprint,
) -> tuple[BlueprintProofEvidenceRef, ...]:
    refs: list[BlueprintProofEvidenceRef] = []
    seen: set[tuple[str, str, str]] = set()

    def add(items: list[EvidenceReference], supports: str) -> None:
        for item in items:
            key = (item.source_id, item.chunk_id, supports)
            if key in seen:
                continue
            seen.add(key)
            refs.append(
                BlueprintProofEvidenceRef(
                    source_id=item.source_id,
                    chunk_id=item.chunk_id,
                    supports=supports,
                    quote_sha256=(
                        hashlib.sha256(item.quote.encode("utf-8")).hexdigest()
                        if item.quote
                        else None
                    ),
                )
            )

    add(blueprint.workflow_summary.evidence_references, "workflow_summary")
    for index, claim in enumerate(blueprint.triggers):
        add(claim.evidence_references, f"trigger:{index}")
    for step in blueprint.current_workflow_steps:
        add(step.evidence_references, f"workflow_step:{step.step_id}")
    for index, claim in enumerate(blueprint.decisions):
        add(claim.evidence_references, f"decision:{index}")
    for index, claim in enumerate(blueprint.exceptions):
        add(claim.evidence_references, f"exception:{index}")
    for index, claim in enumerate(blueprint.pain_points):
        add(claim.evidence_references, f"pain_point:{index}")
    for candidate in blueprint.automation_candidates:
        add(candidate.evidence_references, f"automation_candidate:{candidate.name}")
    for index, item in enumerate(blueprint.risks_and_assumptions):
        add(item.evidence_references, f"risk_or_assumption:{index}")
    for case in blueprint.eval_cases:
        add([case.evidence_reference], f"eval_case:{case.name}")
    for index, claim in enumerate(blueprint.observability_needs):
        add(claim.evidence_references, f"observability_need:{index}")
    return tuple(refs)


def _count_assumptions(blueprint: AutomationBlueprint) -> int:
    return sum(
        [
            int(blueprint.workflow_summary.assumption),
            *(int(item.assumption) for item in blueprint.triggers),
            *(int(item.assumption) for item in blueprint.current_workflow_steps),
            *(int(item.assumption) for item in blueprint.decisions),
            *(int(item.assumption) for item in blueprint.exceptions),
            *(int(item.assumption) for item in blueprint.pain_points),
            *(int(item.kind == "assumption") for item in blueprint.risks_and_assumptions),
            *(int(item.assumption) for item in blueprint.observability_needs),
        ]
    )
