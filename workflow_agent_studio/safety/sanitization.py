"""Deterministic sanitization for benchmark and pilot artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Pattern


@dataclass(frozen=True)
class SanitizedText:
    text: str
    redaction_counts: dict[str, int]

    @property
    def redaction_count(self) -> int:
        return sum(self.redaction_counts.values())


_REDACTION_RULES: tuple[tuple[str, Pattern[str], str], ...] = (
    (
        "email",
        re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "[REDACTED_EMAIL]",
    ),
    (
        "phone",
        re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"),
        "[REDACTED_PHONE]",
    ),
    (
        "secret",
        re.compile(r"\bsk-[A-Za-z0-9_-]{8,}\b"),
        "[REDACTED_SECRET]",
    ),
    (
        "api_key",
        re.compile(
            r"\b([A-Za-z0-9_]*api[_-]?key[A-Za-z0-9_]*\s*[:=]\s*)[A-Za-z0-9_-]{12,}\b", re.I
        ),
        r"\1[REDACTED_SECRET]",
    ),
    (
        "customer_id",
        re.compile(
            r"\b((?:customer|account)[ _-]?(?:id|number)?\s*[:#]\s*)[A-Z0-9][A-Z0-9_-]{3,}\b",
            re.I,
        ),
        r"\1[REDACTED_CUSTOMER_ID]",
    ),
    (
        "address",
        re.compile(
            r"\b\d{3,5}\s+[A-Z][A-Za-z0-9.'-]*(?:\s+[A-Z][A-Za-z0-9.'-]*){0,4}\s+"
            r"(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Ln|Lane|Dr|Drive)\b"
        ),
        "[REDACTED_ADDRESS]",
    ),
)


def sanitize_text_for_benchmark(text: str) -> SanitizedText:
    sanitized = text
    counts: dict[str, int] = {}
    for name, pattern, replacement in _REDACTION_RULES:
        sanitized, count = pattern.subn(replacement, sanitized)
        if count:
            counts[name] = count
    return SanitizedText(text=sanitized, redaction_counts=counts)
