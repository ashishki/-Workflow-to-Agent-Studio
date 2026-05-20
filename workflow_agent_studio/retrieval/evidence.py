"""Typed retrieval evidence results."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal

from workflow_agent_studio.retrieval.chunking import SourceChunk

SPEAKER_LABEL_RE = re.compile(r"^(?P<speaker>[^:\n]{1,80}):")

DEFAULT_EVIDENCE_SECTIONS = (
    "actors",
    "systems",
    "decisions",
    "exceptions",
    "data_fields",
    "approval_boundaries",
)

SECTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "actors": ("operator", "coordinator", "client", "customer", "approver"),
    "systems": ("inbox", "crm", "tracker", "api", "form", "system"),
    "decisions": ("decide", "whether", "if ", "when ", "needs", "review"),
    "exceptions": ("missing", "exception", "clarification", "error", "blocked"),
    "data_fields": ("field", "customer_name", "request_id", "issue_summary", "account_status"),
    "approval_boundaries": ("approval", "approve", "approver", "sign-off", "boundary"),
}


@dataclass(frozen=True)
class EvidenceAnchor:
    source_id: str
    chunk_id: str
    label: str
    normalized_snippet: str


@dataclass(frozen=True)
class EvidenceGap:
    section: str
    question: str
    reason: str


@dataclass(frozen=True)
class EvidenceGapReport:
    anchors: list[EvidenceAnchor]
    gaps: list[EvidenceGap]

    @property
    def gap_count(self) -> int:
        return len(self.gaps)


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


def build_evidence_anchor_map(chunks: Sequence[SourceChunk]) -> list[EvidenceAnchor]:
    return [
        EvidenceAnchor(
            source_id=chunk.source_id,
            chunk_id=chunk.chunk_id,
            label=_anchor_label(chunk),
            normalized_snippet=_normalized_snippet(chunk.text),
        )
        for chunk in chunks
    ]


def build_evidence_gap_report(
    *,
    anchors: Sequence[EvidenceAnchor],
    required_sections: Sequence[str] = DEFAULT_EVIDENCE_SECTIONS,
) -> EvidenceGapReport:
    corpus_text = " ".join(anchor.normalized_snippet.casefold() for anchor in anchors)
    gaps = [
        EvidenceGap(
            section=section,
            question=_gap_question(section),
            reason=f"No evidence anchor matched required section `{section}`.",
        )
        for section in required_sections
        if not _section_has_evidence(section, corpus_text)
    ]
    return EvidenceGapReport(anchors=list(anchors), gaps=gaps)


def _anchor_label(chunk: SourceChunk) -> str:
    if chunk.heading_path:
        return chunk.heading_path[-1]
    first_line = chunk.text.strip().splitlines()[0] if chunk.text.strip() else ""
    match = SPEAKER_LABEL_RE.match(first_line)
    if match is not None:
        return match.group("speaker").strip()
    return "source"


def _normalized_snippet(text: str) -> str:
    return " ".join(text.split())[:240]


def _section_has_evidence(section: str, corpus_text: str) -> bool:
    return any(keyword in corpus_text for keyword in SECTION_KEYWORDS[section])


def _gap_question(section: str) -> str:
    questions = {
        "actors": "Which actors participate in this workflow?",
        "systems": "Which systems or tools does this workflow use?",
        "decisions": "Which decisions change the workflow path?",
        "exceptions": "Which exceptions or blocked states need handling?",
        "data_fields": "Which data fields are required?",
        "approval_boundaries": "Who approves workflow actions before commitments are created?",
    }
    return questions[section]
