import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.verification import (
    RecommendationTrace,
    RoadmapAssumption,
    RoadmapClaim,
    RoadmapEvidenceItem,
    RoadmapVerificationReceipt,
)


def _claim_data() -> dict:
    return {
        "claim_id": "CLM-001",
        "claim_text": "Support requests are manually triaged in Gmail.",
        "claim_type": "observation",
        "source_refs": [{"source_id": "SRC-001", "chunk_id": "CH-002"}],
        "evidence_level": "direct",
        "confidence": "high",
        "created_by": "workflow_decomposer:v1",
        "status": "accepted",
    }


def _assumption_data() -> dict:
    return {
        "assumption_id": "ASM-001",
        "text": "The company receives at least 50 support messages per week.",
        "impact_if_wrong": "Automation may not be worth implementing.",
        "verification_method": "Ask owner for weekly support volume.",
        "owner": "business_owner",
        "expires_at_stage": "before_implementation",
        "status": "unresolved",
    }


def _trace_data() -> dict:
    return {
        "recommendation_id": "REC-003",
        "target_step_id": "WF-RETURNS-04",
        "matched_pattern_id": "customer_support_triage:v1",
        "supporting_claims": ["CLM-004", "CLM-009"],
        "cost_model_version": "cost_model:v1",
        "scoring_model_version": "priority_model:v1",
        "privacy_model_version": "privacy_model:v1",
        "decision_log_id": "DEC-002",
        "review_status": "needs_human_review",
    }


def _receipt_data() -> dict:
    return {
        "report_schema_version": "roadmap_report:v1",
        "source_hashes": ["sha256:source-001"],
        "prompt_versions": {"roadmap": "roadmap_prompt:v1"},
        "model_metadata": {
            "provider": "fake",
            "model": "deterministic-fixture",
            "prompt_version": "roadmap_prompt:v1",
            "generation_mode": "deterministic_demo",
        },
        "pattern_library_version": "smb_patterns:v1",
        "privacy_model_version": "privacy_model:v1",
        "cost_model_version": "cost_model:v1",
        "scoring_model_version": "priority_model:v1",
        "claim_count": 1,
        "assumption_count": 1,
        "blocking_finding_count": 0,
        "review_status": "draft",
        "recommendation_traces": [_trace_data()],
    }


def test_minimal_valid_verification_receipt_and_registries() -> None:
    claim = RoadmapClaim.model_validate(_claim_data())
    assumption = RoadmapAssumption.model_validate(_assumption_data())
    evidence = RoadmapEvidenceItem.model_validate(
        {
            "evidence_id": "EVD-001",
            "source_id": "SRC-001",
            "chunk_id": "CH-002",
            "source_hash": "sha256:source-001",
            "evidence_summary": "Redacted support triage workflow evidence.",
            "redacted": True,
        }
    )
    trace = RecommendationTrace.model_validate(_trace_data())
    receipt = RoadmapVerificationReceipt.model_validate(_receipt_data())

    assert claim.claim_type == "observation"
    assert claim.evidence_level == "direct"
    assert claim.confidence == "high"
    assert claim.status == "accepted"
    assert assumption.impact_if_wrong
    assert assumption.verification_method
    assert assumption.owner == "business_owner"
    assert assumption.status == "unresolved"
    assert evidence.source_hash == "sha256:source-001"
    assert trace.cost_model_version == "cost_model:v1"
    assert trace.scoring_model_version == "priority_model:v1"
    assert trace.privacy_model_version == "privacy_model:v1"
    assert receipt.report_schema_version == "roadmap_report:v1"
    assert receipt.source_hashes == ["sha256:source-001"]
    assert receipt.model_metadata.model == "deterministic-fixture"
    assert receipt.blocking_finding_count == 0


@pytest.mark.parametrize("field", ["claim_type", "evidence_level", "confidence", "status"])
def test_claim_requires_verification_fields(field: str) -> None:
    data = _claim_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RoadmapClaim.model_validate(data)


@pytest.mark.parametrize("field", ["impact_if_wrong", "verification_method", "owner", "status"])
def test_assumption_requires_verification_fields(field: str) -> None:
    data = _assumption_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RoadmapAssumption.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["matched_pattern_id", "cost_model_version", "scoring_model_version", "privacy_model_version"],
)
def test_recommendation_trace_requires_model_versions(field: str) -> None:
    data = _trace_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RecommendationTrace.model_validate(data)


@pytest.mark.parametrize(
    "field",
    ["source_hashes", "report_schema_version", "model_metadata", "blocking_finding_count"],
)
def test_verification_receipt_requires_reproducibility_fields(field: str) -> None:
    data = _receipt_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RoadmapVerificationReceipt.model_validate(data)
