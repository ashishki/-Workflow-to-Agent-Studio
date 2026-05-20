import json
from pathlib import Path

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.validators import (
    compute_automation_readiness,
    validate_blueprint_for_approval,
)


def _valid_blueprint() -> AutomationBlueprint:
    data = json.loads(
        Path("tests/fixtures/blueprints/minimal_valid.json").read_text(encoding="utf-8")
    )
    return AutomationBlueprint.model_validate(data)


def test_valid_blueprint_can_be_approved() -> None:
    result = validate_blueprint_for_approval(_valid_blueprint())

    assert result.can_approve
    assert result.blocking_count == 0


def test_missing_approval_boundaries_blocks_approval() -> None:
    blueprint = _valid_blueprint().model_copy(update={"human_approval_boundaries": []})

    result = validate_blueprint_for_approval(blueprint)

    assert not result.can_approve
    assert any(
        finding.severity == "blocking" and finding.section == "approval_boundaries"
        for finding in result.findings
    )


def test_unsupported_claim_blocks_approval() -> None:
    valid = _valid_blueprint()
    unsupported_claim = valid.workflow_summary.model_copy(
        update={"evidence_references": [], "assumption": False}
    )
    blueprint = valid.model_copy(update={"workflow_summary": unsupported_claim})

    result = validate_blueprint_for_approval(blueprint)

    assert not result.can_approve
    assert any(
        finding.severity == "blocking"
        and finding.section == "evidence_coverage"
        and finding.rule_id == "PLAN-EVIDENCE-COVERAGE"
        for finding in result.findings
    )


def test_missing_eval_cases_blocks_approval() -> None:
    blueprint = _valid_blueprint().model_copy(update={"eval_cases": []})

    result = validate_blueprint_for_approval(blueprint)

    assert not result.can_approve
    assert any(
        finding.severity == "blocking" and finding.section == "eval_cases"
        for finding in result.findings
    )


def test_forbidden_claim_blocks_approval() -> None:
    valid = _valid_blueprint()
    forbidden_summary = valid.workflow_summary.model_copy(
        update={"text": "This automatically builds the agent."}
    )
    blueprint = valid.model_copy(update={"workflow_summary": forbidden_summary})

    result = validate_blueprint_for_approval(blueprint)

    assert not result.can_approve
    assert any(
        finding.severity == "blocking"
        and finding.section == "forbidden_claims"
        and finding.rule_id == "FORBID-AUTONOMY-CLAIM"
        for finding in result.findings
    )


def test_readiness_explains_risks_and_next_questions() -> None:
    readiness = compute_automation_readiness(_valid_blueprint())

    assert readiness.status == "needs_review"
    assert readiness.score == 80
    assert readiness.blockers == []
    assert any("Medium-risk automation candidate" in risk for risk in readiness.risks)
    assert any("Confirm assumption" in question for question in readiness.next_questions)


def test_readiness_score_cannot_override_blocking_validation_findings() -> None:
    blueprint = _valid_blueprint().model_copy(update={"eval_cases": []})

    readiness = compute_automation_readiness(blueprint)

    assert readiness.status == "blocked"
    assert readiness.score == 0
    assert any("eval_cases" in blocker for blocker in readiness.blockers)
