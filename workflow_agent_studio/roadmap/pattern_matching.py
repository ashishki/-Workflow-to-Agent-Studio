"""Deterministic SMB pattern matching baseline."""

from __future__ import annotations

from dataclasses import dataclass

from workflow_agent_studio.domain.privacy import PrivacyClass
from workflow_agent_studio.domain.recommendation import SolutionType
from workflow_agent_studio.patterns.smb import SMBImplementationPattern, load_smb_patterns

_PRIVACY_RANK: dict[PrivacyClass, int] = {
    "public": 1,
    "internal": 2,
    "confidential": 3,
    "sensitive": 4,
    "restricted": 5,
}


@dataclass(frozen=True)
class PatternMatch:
    pattern_id: str
    pattern_version: str
    pattern_name: str
    recommended_solution_type: SolutionType
    privacy_default: PrivacyClass
    when_not_to_use: list[str]
    blocked_anti_matches: list[str]
    privacy_compatible: bool
    rationale: str


def match_smb_pattern(
    *,
    workflow_description: str,
    pain_point: str,
    privacy_class: PrivacyClass,
) -> PatternMatch:
    text = f"{workflow_description} {pain_point}".lower()
    patterns = {pattern.pattern_id: pattern for pattern in load_smb_patterns()}

    if _contains_any(text, ("salon", "appointment", "booking", "reminder")):
        return _match(
            patterns["appointment_booking"],
            privacy_class=privacy_class,
            blocked_anti_matches=["high_autonomy_agent"],
            rationale="Appointment workflows are mostly deterministic scheduling and reminders.",
        )
    if _contains_any(text, ("lead", "intake", "service area", "qualification")):
        return _match(
            patterns["lead_qualification"],
            privacy_class=privacy_class,
            blocked_anti_matches=["automatic_lead_rejection", "discriminatory_scoring"],
            rationale="Lead intake needs field checks, routing rules, and human approval.",
        )
    if _contains_any(text, ("return", "refund", "rma request")):
        return _match(
            patterns["ecommerce_returns"],
            privacy_class=privacy_class,
            blocked_anti_matches=["automatic_refund"],
            rationale="Returns require policy checks and a human approval gate.",
        )
    if _contains_any(text, ("legal checklist", "checklist", "visa", "immigration")):
        return _match(
            patterns["legal_checklist"],
            privacy_class=privacy_class,
            blocked_anti_matches=["legal_advice_agent", "unrestricted_cloud_bot"],
            rationale="Legal checklist work needs private review support, not advice automation.",
        )
    if _contains_any(text, ("report", "dashboard", "spreadsheet", "metrics")):
        return _match(
            patterns["reporting_automation"],
            privacy_class=privacy_class,
            blocked_anti_matches=["llm_agent_for_metric_calculation"],
            rationale="Stable reporting should prefer deterministic calculations.",
        )
    if _contains_any(text, ("incident", "runbook", "pagerduty", "slack", "incident.io")):
        return _match(
            patterns["internal_knowledge_assistant"],
            privacy_class=privacy_class,
            blocked_anti_matches=["automatic_incident_declaration", "autonomous_paging"],
            rationale=(
                "Incident response support should cite runbooks and keep response "
                "actions human-approved."
            ),
        )
    return _match(
        patterns["customer_support_triage"],
        privacy_class=privacy_class,
        blocked_anti_matches=["high_autonomy_agent"],
        rationale="Default baseline match for repeated support triage signals.",
    )


def _match(
    pattern: SMBImplementationPattern,
    *,
    privacy_class: PrivacyClass,
    blocked_anti_matches: list[str],
    rationale: str,
) -> PatternMatch:
    privacy_compatible = _PRIVACY_RANK[pattern.privacy_default] >= _PRIVACY_RANK[privacy_class]
    anti_matches = list(blocked_anti_matches)
    if not privacy_compatible:
        anti_matches.append("privacy_default_weaker_than_detected_data_class")
    return PatternMatch(
        pattern_id=pattern.pattern_id,
        pattern_version=pattern.version,
        pattern_name=pattern.pattern_name,
        recommended_solution_type=pattern.architecture.recommended_solution_type,
        privacy_default=pattern.privacy_default,
        when_not_to_use=pattern.when_not_to_use,
        blocked_anti_matches=anti_matches,
        privacy_compatible=privacy_compatible,
        rationale=rationale,
    )


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)
