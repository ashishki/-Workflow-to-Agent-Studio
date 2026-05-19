"""PII-safe logging helpers."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable


def redact_observability_value(value: str, sensitive_values: Iterable[str] = ()) -> str:
    if value and value in {item for item in sensitive_values if item}:
        digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
        return f"sha256:{digest}"
    return value
