"""Deterministic source normalization and fingerprinting."""

from __future__ import annotations

import hashlib


def normalize_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    normalized_lines: list[str] = []
    previous_blank = False
    for line in lines:
        blank = not line.strip()
        if blank and previous_blank:
            continue
        normalized_lines.append("" if blank else line.strip())
        previous_blank = blank
    return "\n".join(normalized_lines).strip()


def fingerprint_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
