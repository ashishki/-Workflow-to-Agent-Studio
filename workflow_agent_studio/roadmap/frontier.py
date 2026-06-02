"""Frontier opportunity discovery verification."""

from __future__ import annotations

from workflow_agent_studio.domain.frontier import (
    FrontierCandidateVerification,
    FrontierDiscoveryResult,
    FrontierDiscoveryVerification,
    FrontierOpportunityCandidate,
    FrontierVerificationFinding,
)
from workflow_agent_studio.domain.privacy import PrivacyClass

_PRIVACY_RANK: dict[PrivacyClass, int] = {
    "public": 1,
    "internal": 2,
    "confidential": 3,
    "sensitive": 4,
    "restricted": 5,
}
_HIGH_RISK_SOLUTION_TYPES = {
    "bounded_ai_agent",
    "high_autonomy_agent_future_only",
}
_HIGH_IMPACT_DECISION_TERMS = (
    "approve",
    "reject",
    "hire",
    "fire",
    "refund",
    "charge",
    "admission",
    "investment",
    "legal advice",
    "medical advice",
)


def verify_frontier_discovery_result(
    *,
    result: FrontierDiscoveryResult,
    detected_privacy_class: PrivacyClass,
) -> FrontierDiscoveryVerification:
    """Verify frontier candidates without approving them as roadmap recommendations."""

    candidate_reviews = [
        verify_frontier_candidate(
            candidate=candidate,
            detected_privacy_class=detected_privacy_class,
        )
        for candidate in result.candidates
    ]
    blocking_count = sum(
        1
        for review in candidate_reviews
        for finding in review.findings
        if finding.severity == "blocking"
    )
    warning_count = sum(
        1
        for review in candidate_reviews
        for finding in review.findings
        if finding.severity == "warning"
    )
    return FrontierDiscoveryVerification(
        candidate_reviews=candidate_reviews,
        blocking_finding_count=blocking_count,
        warning_finding_count=warning_count,
    )


def verify_frontier_candidate(
    *,
    candidate: FrontierOpportunityCandidate,
    detected_privacy_class: PrivacyClass,
) -> FrontierCandidateVerification:
    """Apply deterministic rules to one frontier candidate."""

    findings: list[FrontierVerificationFinding] = []
    if not candidate.evidence_refs and not candidate.critical_assumptions:
        findings.append(
            _blocking(
                rule_id="frontier_evidence_or_assumption_required",
                message="Frontier candidate lacks evidence refs and explicit assumptions.",
                repair_hint="Add source references or critical assumptions before review.",
            )
        )
    if not candidate.human_gate.required:
        findings.append(
            _blocking(
                rule_id="frontier_human_gate_required",
                message="Frontier candidate lacks a required human approval gate.",
                repair_hint="Add a reviewer and approval event before roadmap consideration.",
            )
        )
    if _PRIVACY_RANK[candidate.privacy_class] < _PRIVACY_RANK[detected_privacy_class]:
        findings.append(
            _blocking(
                rule_id="frontier_privacy_class_weaker_than_source",
                message="Candidate privacy class is weaker than detected workflow privacy.",
                repair_hint="Raise candidate privacy class or switch to private/local handling.",
            )
        )
    if candidate.candidate_solution_type in _HIGH_RISK_SOLUTION_TYPES:
        findings.append(
            _blocking(
                rule_id="frontier_high_autonomy_not_exportable",
                message="High-autonomy frontier candidates cannot become roadmap recommendations.",
                repair_hint="Convert to human-in-the-loop or bounded draft-only assistance.",
            )
        )
    if _contains_high_impact_decision(candidate):
        findings.append(
            _blocking(
                rule_id="frontier_high_impact_decision_boundary",
                message="Candidate appears to automate a high-impact decision.",
                repair_hint="Move decision ownership to a human gate and draft-only assistant.",
            )
        )
    if not candidate.cost_drivers:
        findings.append(
            _blocking(
                rule_id="frontier_cost_drivers_required",
                message="Candidate lacks cost drivers.",
                repair_hint="Add integration, volume, research-depth, and privacy cost drivers.",
            )
        )
    if not candidate.do_not_automate:
        findings.append(
            _blocking(
                rule_id="frontier_do_not_automate_required",
                message="Candidate lacks do-not-automate boundaries.",
                repair_hint="Add actions that must remain human-owned.",
            )
        )

    status = "rejected" if findings else "needs_human_review"
    return FrontierCandidateVerification(
        opportunity_id=candidate.opportunity_id,
        status=status,
        exportable_as_recommendation=False,
        findings=findings,
    )


def _contains_high_impact_decision(candidate: FrontierOpportunityCandidate) -> bool:
    text = " ".join(
        [
            candidate.title,
            candidate.workflow_step,
            *candidate.why_it_may_help,
        ]
    ).lower()
    return any(term in text for term in _HIGH_IMPACT_DECISION_TERMS) and "draft" not in text


def _blocking(*, rule_id: str, message: str, repair_hint: str) -> FrontierVerificationFinding:
    return FrontierVerificationFinding(
        rule_id=rule_id,
        severity="blocking",
        message=message,
        repair_hint=repair_hint,
    )
