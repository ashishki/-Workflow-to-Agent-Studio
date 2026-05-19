"""Typed retrieval evidence results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class EvidenceSnippet:
    source_id: str
    chunk_id: str
    score: float
    text_preview: str
    heading_path: tuple[str, ...]


@dataclass(frozen=True)
class RetrievalResult:
    status: Literal["ok", "insufficient_evidence"]
    evidence: list[EvidenceSnippet] = field(default_factory=list)
    answer_text: str | None = None
