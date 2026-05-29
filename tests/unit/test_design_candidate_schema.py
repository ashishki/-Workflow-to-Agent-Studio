import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.design_candidate import AgentDesignCandidate
from workflow_agent_studio.validators import (
    validate_design_candidate_for_approval,
    validate_design_candidate_set_for_approval,
)


def _candidate_data(variant: str = "bounded_agent") -> dict:
    return {
        "variant": variant,
        "name": f"{variant} candidate",
        "summary": "Draft a bounded workflow-to-agent design.",
        "autonomy_level": "bounded",
        "required_tools": [
            {
                "name": "CRM",
                "permission_boundary": "Read records and draft updates only.",
                "evidence_references": [{"source_id": "src-1", "chunk_id": "chk-1"}],
            }
        ],
        "human_approvals": [
            {
                "decision": "Approve generated CRM update",
                "approver": "Operator",
                "reason": "CRM writes affect customer-facing records.",
            }
        ],
        "runtime_tier": "T0",
        "eval_needs": [
            {
                "name": "CRM update draft",
                "expected_behavior": "The design drafts an update without writing to CRM.",
                "verification_method": "Inspect the candidate permission boundary.",
                "evidence_references": [{"source_id": "src-1", "chunk_id": "chk-2"}],
            }
        ],
        "risks": [
            {
                "description": "CRM field mapping may be incomplete.",
                "kind": "risk",
                "evidence_references": [{"source_id": "src-1", "chunk_id": "chk-3"}],
            }
        ],
        "cost_posture": "medium",
        "evidence_gaps": [
            {
                "section": "tool_permissions",
                "question": "Which CRM fields may be updated?",
                "impact": "Write permissions cannot be approved until fields are known.",
            }
        ],
        "evidence_references": [{"source_id": "src-1", "chunk_id": "chk-1"}],
    }


def test_schema_supports_required_design_candidate_variants() -> None:
    variants = {
        "deterministic_first",
        "human_in_the_loop",
        "bounded_agent",
        "high_autonomy",
        "compliance_heavy",
        "low_cost_mvp",
    }

    candidates = [
        AgentDesignCandidate.model_validate(_candidate_data(variant)) for variant in variants
    ]

    assert {candidate.variant for candidate in candidates} == variants
    assert all(candidate.schema_version == "design-candidate-v1" for candidate in candidates)


def test_design_candidate_records_required_tradeoff_fields() -> None:
    candidate = AgentDesignCandidate.model_validate(_candidate_data())

    assert candidate.autonomy_level == "bounded"
    assert candidate.required_tools[0].permission_boundary
    assert candidate.human_approvals[0].approver == "Operator"
    assert candidate.runtime_tier == "T0"
    assert candidate.eval_needs[0].verification_method
    assert candidate.risks[0].description
    assert candidate.cost_posture == "medium"
    assert candidate.evidence_gaps[0].question


def test_design_candidate_schema_rejects_missing_approval_boundaries() -> None:
    data = _candidate_data()
    data["human_approvals"] = []

    with pytest.raises(ValidationError, match="human_approvals"):
        AgentDesignCandidate.model_validate(data)


def test_design_candidate_schema_rejects_missing_eval_plan() -> None:
    data = _candidate_data()
    data["eval_needs"] = []

    with pytest.raises(ValidationError, match="eval_needs"):
        AgentDesignCandidate.model_validate(data)


def test_design_candidate_validator_blocks_missing_approval_boundaries() -> None:
    candidate = AgentDesignCandidate.model_validate(_candidate_data()).model_copy(
        update={"human_approvals": []}
    )

    result = validate_design_candidate_for_approval(candidate)

    assert not result.can_approve
    assert any(
        finding.rule_id == "PLAN-DESIGN-CANDIDATE-APPROVALS" and finding.severity == "blocking"
        for finding in result.findings
    )


def test_design_candidate_validator_blocks_missing_eval_plan() -> None:
    candidate = AgentDesignCandidate.model_validate(_candidate_data()).model_copy(
        update={"eval_needs": []}
    )

    result = validate_design_candidate_set_for_approval([candidate])

    assert not result.can_approve
    assert any(
        finding.rule_id == "PLAN-DESIGN-CANDIDATE-EVALS" and finding.severity == "blocking"
        for finding in result.findings
    )
