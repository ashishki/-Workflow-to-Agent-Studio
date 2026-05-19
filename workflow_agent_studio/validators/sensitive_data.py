"""Deterministic sensitive-data guards."""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass

SECRET_PATTERNS = [
    re.compile(r"\bsk-test-[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\b[A-Za-z0-9_]*api[_-]?key[A-Za-z0-9_]*\s*[:=]\s*[A-Za-z0-9_-]{12,}\b", re.I),
]


@dataclass(frozen=True)
class SensitiveDataFinding:
    finding_id: str
    severity: str
    source_id: str
    finding_type: str
    redacted_preview: str

    def log_extra(self) -> dict[str, str]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "source_id": self.source_id,
            "finding_type": self.finding_type,
        }


def scan_source_for_sensitive_data(source_id: str, text: str) -> list[SensitiveDataFinding]:
    findings: list[SensitiveDataFinding] = []
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(
                SensitiveDataFinding(
                    finding_id=f"SENS-{len(findings) + 1}",
                    severity="blocking",
                    source_id=source_id,
                    finding_type="secret_like_token",
                    redacted_preview=_redacted_preview(text, match.start(), match.end()),
                )
            )
    return findings


def log_sensitive_data_finding(
    logger: logging.Logger,
    finding: SensitiveDataFinding,
) -> None:
    logger.warning("sensitive-data-finding", extra=finding.log_extra())


def _redacted_preview(text: str, start: int, end: int) -> str:
    value = text[start:end]
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    prefix = text[max(0, start - 12) : start]
    suffix = text[end : min(len(text), end + 12)]
    return f"{prefix}sha256:{digest}{suffix}"
