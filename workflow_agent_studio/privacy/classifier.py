"""Deterministic privacy classifier for SMB roadmap planning."""

from __future__ import annotations

import re
from collections.abc import Iterable

from workflow_agent_studio.domain.privacy import (
    DetectedPrivacyFlag,
    PrivacyClass,
    PrivacyClassificationResult,
    RedactionStatus,
)

_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE_RE = re.compile(r"(?:\+?\d[\d .()-]{8,}\d)")
_PAYMENT_CARD_RE = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
_PASSPORT_RE = re.compile(r"\b(?:passport|national id|id number|visa)\b", re.IGNORECASE)
_API_KEY_RE = re.compile(
    r"\b(?:api[_ -]?key|secret|token|password)\b\s*[:=]\s*[A-Za-z0-9_\-]{8,}",
    re.IGNORECASE,
)
_ORDER_ID_RE = re.compile(
    r"\b(?:order|ticket|case)[ _-]?(?:id|number|#)\s*[:#-]?\s*[A-Z0-9-]{4,}\b",
    re.IGNORECASE,
)
_NAME_CONTEXT_RE = re.compile(
    r"\b(?:customer|client|patient|candidate|student)\s+name\s*[:=]\s*"
    r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
    re.IGNORECASE,
)
_ADDRESS_RE = re.compile(
    r"\b\d{1,6}\s+[A-Za-z0-9 .'-]+\s+"
    r"(?:street|st\.?|avenue|ave\.?|road|rd\.?|lane|ln\.?|drive|dr\.?|boulevard|blvd\.?)\b",
    re.IGNORECASE,
)

_HEALTH_KEYWORDS = (
    "diagnosis",
    "patient",
    "medical record",
    "treatment plan",
    "clinic notes",
)
_LEGAL_KEYWORDS = (
    "legal status",
    "immigration",
    "asylum",
    "visa petition",
    "passport copy",
)
_TAX_KEYWORDS = ("tax filing", "tax return", "irs", "vat filing", "payroll tax")
_HR_KEYWORDS = ("candidate", "resume", "employee personal file", "background check")
_MINOR_STUDENT_KEYWORDS = ("minor", "student record", "under 18", "guardian")
_CONFIDENTIAL_KEYWORDS = ("margin", "private pricing", "vendor contract", "confidential sop")
_PUBLIC_KEYWORDS = ("public faq", "public pricing page", "published help center")

_FLAG_RANK: dict[DetectedPrivacyFlag, int] = {
    "email": 3,
    "phone": 3,
    "address": 3,
    "name_like": 3,
    "passport_or_id": 4,
    "payment_card": 4,
    "api_key_or_credential": 4,
    "health": 4,
    "legal_or_immigration": 4,
    "tax_or_accounting": 4,
    "hr_or_candidate": 4,
    "minor_or_student_data": 4,
}

_CLASS_BY_RANK: dict[int, PrivacyClass] = {
    1: "public",
    2: "internal",
    3: "sensitive",
    4: "restricted",
}


def classify_privacy(text: str) -> PrivacyClassificationResult:
    flags = _detected_flags(text)
    privacy_class = _classify(text, flags)
    redaction_status = _redaction_status(flags, privacy_class)

    return PrivacyClassificationResult(
        detected_flags=flags,
        redaction_status=redaction_status,
        source_privacy_class=privacy_class,
        recommendation_privacy_class=privacy_class,
        rationale=_rationale(flags, privacy_class, redaction_status),
    )


def _detected_flags(text: str) -> list[DetectedPrivacyFlag]:
    candidates: list[DetectedPrivacyFlag] = []
    if _EMAIL_RE.search(text):
        candidates.append("email")
    if _PHONE_RE.search(text):
        candidates.append("phone")
    if _ADDRESS_RE.search(text):
        candidates.append("address")
    if _NAME_CONTEXT_RE.search(text):
        candidates.append("name_like")
    if _PASSPORT_RE.search(text):
        candidates.append("passport_or_id")
    if _PAYMENT_CARD_RE.search(text):
        candidates.append("payment_card")
    if _API_KEY_RE.search(text):
        candidates.append("api_key_or_credential")
    if _contains_any(text, _HEALTH_KEYWORDS):
        candidates.append("health")
    if _contains_any(text, _LEGAL_KEYWORDS):
        candidates.append("legal_or_immigration")
    if _contains_any(text, _TAX_KEYWORDS):
        candidates.append("tax_or_accounting")
    if _contains_any(text, _HR_KEYWORDS):
        candidates.append("hr_or_candidate")
    if _contains_any(text, _MINOR_STUDENT_KEYWORDS):
        candidates.append("minor_or_student_data")
    return list(dict.fromkeys(candidates))


def _classify(text: str, flags: list[DetectedPrivacyFlag]) -> PrivacyClass:
    if flags:
        return _CLASS_BY_RANK[max(_FLAG_RANK[flag] for flag in flags)]
    if _contains_any(text, _PUBLIC_KEYWORDS):
        return "public"
    if _contains_any(text, _CONFIDENTIAL_KEYWORDS):
        return "confidential"
    if _ORDER_ID_RE.search(text):
        return "sensitive"
    return "internal"


def _redaction_status(
    flags: list[DetectedPrivacyFlag],
    privacy_class: PrivacyClass,
) -> RedactionStatus:
    if "api_key_or_credential" in flags or "payment_card" in flags:
        return "blocked"
    if privacy_class in {"sensitive", "restricted"}:
        return "required"
    return "not_required"


def _rationale(
    flags: list[DetectedPrivacyFlag],
    privacy_class: PrivacyClass,
    redaction_status: RedactionStatus,
) -> str:
    if flags:
        return (
            f"Detected privacy flags {', '.join(flags)}; classified as {privacy_class} "
            f"with redaction status {redaction_status}."
        )
    return f"No sensitive flags detected; classified as {privacy_class}."


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    normalized = text.lower()
    return any(keyword in normalized for keyword in keywords)
