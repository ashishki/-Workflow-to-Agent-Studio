"""Forbidden blueprint claim guards."""

from __future__ import annotations

from dataclasses import dataclass

FORBIDDEN_CLAIMS = {
    "automatically builds the agent": "FORBID-AUTONOMY-CLAIM",
}


@dataclass(frozen=True)
class ForbiddenClaimFinding:
    finding_id: str
    severity: str
    claim: str
    rule_id: str


def scan_blueprint_text_for_forbidden_claims(text: str) -> list[ForbiddenClaimFinding]:
    normalized = text.casefold()
    findings: list[ForbiddenClaimFinding] = []
    for phrase, rule_id in FORBIDDEN_CLAIMS.items():
        if phrase in normalized:
            findings.append(
                ForbiddenClaimFinding(
                    finding_id=f"FORBID-{len(findings) + 1}",
                    severity="blocking",
                    claim=phrase,
                    rule_id=rule_id,
                )
            )
    return findings
