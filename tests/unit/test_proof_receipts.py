from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.proof import (
    BlueprintProofReceipt,
    build_blueprint_proof_receipt,
)

FIXTURE_PATH = Path("tests/fixtures/blueprints/minimal_valid.json")


def test_blueprint_proof_receipt_links_artifact_evidence_and_assumptions() -> None:
    payload = FIXTURE_PATH.read_text(encoding="utf-8")
    blueprint = AutomationBlueprint.model_validate(json.loads(payload))

    receipt = build_blueprint_proof_receipt(
        blueprint=blueprint,
        artifact_ref="exports/blueprints/minimal.md",
        artifact_payload=payload,
        generated_at=datetime(2026, 5, 31, tzinfo=UTC),
    )

    assert receipt.type == "blueprint_proof_receipt"
    assert receipt.schema_version == "entropy_core.product_receipt.v1"
    assert receipt.product_id == "workflow-to-agent-studio"
    assert receipt.blueprint_schema_version == "v1"
    assert receipt.artifact_ref == "exports/blueprints/minimal.md"
    assert len(receipt.artifact_sha256) == 64
    assert receipt.verifier_status == "passed"
    assert receipt.assumption_count == 2
    assert any(ref.supports == "workflow_step:step-1" for ref in receipt.evidence_refs)
    assert len(receipt.receipt_sha256()) == 64


def test_blueprint_proof_receipt_rejects_missing_evidence_refs() -> None:
    with pytest.raises(ValidationError):
        BlueprintProofReceipt(
            blueprint_schema_version="v1",
            artifact_ref="exports/blueprints/empty.md",
            artifact_sha256="a" * 64,
            generated_at=datetime(2026, 5, 31, tzinfo=UTC),
            evidence_refs=[],
            assumption_count=0,
            verifier_status="failed",
            verifier_notes=("no evidence",),
        )


def test_blueprint_proof_receipt_requires_notes_for_review_status() -> None:
    with pytest.raises(ValidationError, match="verifier_notes"):
        BlueprintProofReceipt(
            blueprint_schema_version="v1",
            artifact_ref="exports/blueprints/review.md",
            artifact_sha256="a" * 64,
            generated_at=datetime(2026, 5, 31, tzinfo=UTC),
            evidence_refs=[
                {
                    "source_id": "src-1",
                    "chunk_id": "chk-1",
                    "supports": "workflow_summary",
                }
            ],
            assumption_count=1,
            verifier_status="needs_review",
        )
