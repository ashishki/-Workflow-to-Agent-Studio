"""Deterministic source normalization and fingerprinting."""

from __future__ import annotations

import hashlib
import re

_WHITESPACE_RE = re.compile(r"\s+")
_SPEAKER_LINE_RE = re.compile(r"^(?P<speaker>[^:\n]{1,80}):(?P<utterance>.*)$")


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


def normalize_transcript_text(text: str) -> str:
    normalized_lines: list[str] = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        match = _SPEAKER_LINE_RE.match(stripped)
        if match is None:
            normalized_lines.append(_collapse_whitespace(stripped))
            continue
        speaker = _collapse_whitespace(match.group("speaker").strip())
        utterance = _collapse_whitespace(match.group("utterance").strip())
        normalized_lines.append(f"{speaker}: {utterance}")
    return "\n".join(normalized_lines).strip()


def fingerprint_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _collapse_whitespace(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value).strip()
