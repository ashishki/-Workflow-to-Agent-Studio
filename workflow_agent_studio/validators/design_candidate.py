"""Deterministic validators for workflow-to-agent design candidates."""

from __future__ import annotations

from workflow_agent_studio.domain.design_candidate import AgentDesignCandidate
from workflow_agent_studio.validators.blueprint import (
    BlueprintValidationFinding,
    BlueprintValidationResult,
)


def validate_design_candidate_for_approval(
    candidate: AgentDesignCandidate,
) -> BlueprintValidationResult:
    findings: list[BlueprintValidationFinding] = []
    if not candidate.human_approvals:
        findings.append(
            BlueprintValidationFinding(
                rule_id="PLAN-DESIGN-CANDIDATE-APPROVALS",
                severity="blocking",
                section="design_candidates.human_approvals",
                message=f"Design candidate `{candidate.name}` lacks approval boundaries.",
                repair_hint="Add at least one human approval boundary before review.",
            )
        )
    if not candidate.eval_needs:
        findings.append(
            BlueprintValidationFinding(
                rule_id="PLAN-DESIGN-CANDIDATE-EVALS",
                severity="blocking",
                section="design_candidates.eval_needs",
                message=f"Design candidate `{candidate.name}` lacks an eval plan.",
                repair_hint="Add at least one eval need with expected behavior and verification.",
            )
        )
    return BlueprintValidationResult(findings=findings)


def validate_design_candidate_set_for_approval(
    candidates: list[AgentDesignCandidate],
) -> BlueprintValidationResult:
    findings: list[BlueprintValidationFinding] = []
    for candidate in candidates:
        findings.extend(validate_design_candidate_for_approval(candidate).findings)
    return BlueprintValidationResult(findings=findings)
