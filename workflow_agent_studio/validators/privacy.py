"""Privacy policy gates for roadmap model-mode recommendations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from workflow_agent_studio.domain.privacy import PrivacyClass, RedactionStatus

ModelMode = Literal["lightweight_cloud", "private_analysis", "local_on_prem"]

_HIGH_RISK_DOMAINS = {
    "legal",
    "legal_consultancy",
    "medical",
    "health",
    "healthcare",
    "financial",
    "finance",
    "accounting",
    "hr",
    "human_resources",
    "identity",
}


@dataclass(frozen=True)
class PrivacyPolicyFinding:
    rule_id: str
    severity: Literal["blocking", "warning"]
    section: str
    message: str
    repair_hint: str


@dataclass(frozen=True)
class PrivacyPolicyResult:
    findings: list[PrivacyPolicyFinding]

    @property
    def blocking_count(self) -> int:
        return sum(finding.severity == "blocking" for finding in self.findings)

    @property
    def can_recommend(self) -> bool:
        return self.blocking_count == 0


def validate_model_mode_recommendation(
    *,
    privacy_class: PrivacyClass,
    redaction_status: RedactionStatus,
    recommended_mode: ModelMode,
    domain: str,
    source_is_synthetic_or_redacted: bool = False,
    report_condition: str = "",
    human_review_gate: bool = False,
) -> PrivacyPolicyResult:
    findings: list[PrivacyPolicyFinding] = []
    findings.extend(
        _restricted_cloud_findings(
            privacy_class=privacy_class,
            recommended_mode=recommended_mode,
            source_is_synthetic_or_redacted=source_is_synthetic_or_redacted,
            report_condition=report_condition,
        )
    )
    findings.extend(
        _sensitive_cloud_findings(
            privacy_class=privacy_class,
            redaction_status=redaction_status,
            recommended_mode=recommended_mode,
            report_condition=report_condition,
        )
    )
    findings.extend(_high_risk_review_findings(domain=domain, human_review_gate=human_review_gate))
    return PrivacyPolicyResult(findings=findings)


def _restricted_cloud_findings(
    *,
    privacy_class: PrivacyClass,
    recommended_mode: ModelMode,
    source_is_synthetic_or_redacted: bool,
    report_condition: str,
) -> list[PrivacyPolicyFinding]:
    if privacy_class != "restricted" or recommended_mode != "lightweight_cloud":
        return []
    if source_is_synthetic_or_redacted and report_condition:
        return []
    return [
        PrivacyPolicyFinding(
            rule_id="PRIVACY-RESTRICTED-CLOUD-BLOCK",
            severity="blocking",
            section="cloud_private_local_policy",
            message="Restricted data cannot use lightweight cloud analysis by default.",
            repair_hint=(
                "Recommend local/on-prem or strict private analysis, or use only "
                "synthetic/redacted source data and state that condition in the report."
            ),
        )
    ]


def _sensitive_cloud_findings(
    *,
    privacy_class: PrivacyClass,
    redaction_status: RedactionStatus,
    recommended_mode: ModelMode,
    report_condition: str,
) -> list[PrivacyPolicyFinding]:
    if privacy_class != "sensitive" or recommended_mode != "lightweight_cloud":
        return []
    redaction_done_or_planned = redaction_status in {"redacted", "partially_redacted", "required"}
    if redaction_done_or_planned and "redact" in report_condition.lower():
        return []
    return [
        PrivacyPolicyFinding(
            rule_id="PRIVACY-SENSITIVE-CLOUD-REDACTION-NOTE",
            severity="blocking",
            section="cloud_private_local_policy",
            message="Sensitive data requires a redaction condition for lightweight cloud mode.",
            repair_hint="State the redaction requirement or recommend private analysis.",
        )
    ]


def _high_risk_review_findings(
    *,
    domain: str,
    human_review_gate: bool,
) -> list[PrivacyPolicyFinding]:
    normalized = domain.lower().replace("-", "_").replace(" ", "_")
    if normalized not in _HIGH_RISK_DOMAINS or human_review_gate:
        return []
    return [
        PrivacyPolicyFinding(
            rule_id="PRIVACY-HIGH-RISK-HUMAN-GATE",
            severity="blocking",
            section="human_review_gate",
            message="High-risk domains require an explicit human review gate.",
            repair_hint="Add an accountable human approval gate before recommendation approval.",
        )
    ]
