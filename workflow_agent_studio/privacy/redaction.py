"""Deterministic redaction preview for privacy-sensitive roadmap inputs."""

from __future__ import annotations

import re
from dataclasses import dataclass
from re import Match, Pattern


@dataclass(frozen=True)
class RedactionPreview:
    text: str
    redaction_counts: dict[str, int]

    @property
    def redaction_count(self) -> int:
        return sum(self.redaction_counts.values())


@dataclass(frozen=True)
class _Rule:
    name: str
    pattern: Pattern[str]
    placeholder_prefix: str | None = None
    fixed_placeholder: str | None = None
    preserve_prefix_group: bool = False


_RULES: tuple[_Rule, ...] = (
    _Rule(
        name="api_key",
        pattern=re.compile(
            r"\b(?P<prefix>(?:api[_ -]?key|secret|token|password)\s*[:=]\s*)"
            r"(?P<value>[A-Za-z0-9_\-]{8,})",
            re.IGNORECASE,
        ),
        fixed_placeholder="[API_KEY_REDACTED]",
        preserve_prefix_group=True,
    ),
    _Rule(
        name="payment_card",
        pattern=re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        fixed_placeholder="[PAYMENT_CARD_REDACTED]",
    ),
    _Rule(
        name="email",
        pattern=re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        placeholder_prefix="EMAIL",
    ),
    _Rule(
        name="phone",
        pattern=re.compile(r"(?:\+?\d[\d .()-]{8,}\d)"),
        placeholder_prefix="PHONE",
    ),
    _Rule(
        name="address",
        pattern=re.compile(
            r"\b\d{1,6}\s+[A-Za-z0-9 .'-]+\s+"
            r"(?:street|st\.?|avenue|ave\.?|road|rd\.?|lane|ln\.?|drive|dr\.?|boulevard|blvd\.?)\b",
            re.IGNORECASE,
        ),
        placeholder_prefix="ADDRESS",
    ),
    _Rule(
        name="passport_id",
        pattern=re.compile(
            r"\b(?P<prefix>(?:passport|national id|id number)\s*[:#]?\s*)"
            r"(?P<value>[A-Z0-9-]{5,})\b",
            re.IGNORECASE,
        ),
        placeholder_prefix="PASSPORT_ID",
        preserve_prefix_group=True,
    ),
    _Rule(
        name="order_id",
        pattern=re.compile(
            r"\b(?P<prefix>(?:order|ticket|case)[ _-]?(?:id|number|#)\s*[:#-]?\s*)"
            r"(?P<value>[A-Z0-9-]{4,})\b",
            re.IGNORECASE,
        ),
        placeholder_prefix="ORDER_ID",
        preserve_prefix_group=True,
    ),
    _Rule(
        name="person",
        pattern=re.compile(
            r"\b(?P<prefix>(?:customer|client|patient|candidate|student)\s+name\s*[:=]\s*)"
            r"(?P<value>[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+)+)",
            re.IGNORECASE,
        ),
        placeholder_prefix="PERSON",
        preserve_prefix_group=True,
    ),
)


def build_redaction_preview(text: str) -> RedactionPreview:
    redacted = text
    counts: dict[str, int] = {}
    placeholders: dict[str, dict[str, str]] = {}

    for rule in _RULES:
        redacted, count = rule.pattern.subn(
            lambda match, current_rule=rule: _replacement(match, current_rule, placeholders),
            redacted,
        )
        if count:
            counts[rule.name] = count

    return RedactionPreview(text=redacted, redaction_counts=counts)


def _replacement(
    match: Match[str],
    rule: _Rule,
    placeholders: dict[str, dict[str, str]],
) -> str:
    value = match.group("value") if "value" in match.groupdict() else match.group(0)
    if rule.fixed_placeholder is not None:
        placeholder = rule.fixed_placeholder
    else:
        placeholder = _stable_placeholder(rule, value, placeholders)

    if rule.preserve_prefix_group:
        return f"{match.group('prefix')}{placeholder}"
    return placeholder


def _stable_placeholder(
    rule: _Rule,
    value: str,
    placeholders: dict[str, dict[str, str]],
) -> str:
    if rule.placeholder_prefix is None:
        raise ValueError("numbered redaction rule requires a placeholder prefix")
    rule_placeholders = placeholders.setdefault(rule.name, {})
    if value not in rule_placeholders:
        rule_placeholders[value] = f"[{rule.placeholder_prefix}_{len(rule_placeholders) + 1}]"
    return rule_placeholders[value]
