"""Query-time retrieval over a local vector index."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from workflow_agent_studio.config import load_settings
from workflow_agent_studio.retrieval.embeddings import EmbeddingProvider, FakeEmbeddingProvider
from workflow_agent_studio.retrieval.evidence import EvidenceSnippet, RetrievalResult

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ScoredEntry:
    score: float
    entry: dict[str, Any]


class EvidenceReranker(Protocol):
    def rerank(self, entries: Sequence[ScoredEntry]) -> list[ScoredEntry]: ...


def retrieve_evidence(
    *,
    index_path: str | Path,
    query: str,
    top_k: int | None = None,
    min_score: float | None = None,
    embedding_provider: EmbeddingProvider | None = None,
    reranker: EvidenceReranker | None = None,
) -> RetrievalResult:
    settings = load_settings()
    effective_top_k = top_k if top_k is not None else settings.retrieval_top_k
    effective_min_score = min_score if min_score is not None else settings.retrieval_min_score
    entries = json.loads((Path(index_path) / "vectors.json").read_text(encoding="utf-8"))
    query_tokens = _tokens(query)
    provider = embedding_provider or FakeEmbeddingProvider()
    query_vector = provider.embed_texts([query])[0]
    scored = [
        ScoredEntry(score=_combined_score(query_tokens, query_vector, entry), entry=entry)
        for entry in entries
    ]
    ordered = (
        reranker.rerank(scored)
        if reranker is not None
        else sorted(scored, key=lambda item: item.score, reverse=True)
    )
    evidence = [
        _to_evidence(scored_entry.score, scored_entry.entry)
        for scored_entry in ordered[:effective_top_k]
        if scored_entry.score >= effective_min_score
    ]
    if not evidence:
        return RetrievalResult(status="insufficient_evidence", evidence=[], answer_text=None)
    return RetrievalResult(status="ok", evidence=evidence, answer_text=None)


def _tokens(text: str) -> set[str]:
    return set(TOKEN_PATTERN.findall(text.casefold()))


def _lexical_score(query_tokens: set[str], entry_tokens: set[str]) -> float:
    if not query_tokens:
        return 0.0
    return len(query_tokens & entry_tokens) / len(query_tokens)


def _combined_score(
    query_tokens: set[str],
    query_vector: list[float],
    entry: dict[str, Any],
) -> float:
    lexical = _lexical_score(query_tokens, _tokens(entry["text"]))
    if lexical == 0:
        return 0.0
    return (lexical + _cosine_similarity(query_vector, entry["vector"])) / 2


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(
        left_value * right_value for left_value, right_value in zip(left, right, strict=True)
    )
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def _to_evidence(score: float, entry: dict[str, Any]) -> EvidenceSnippet:
    return EvidenceSnippet(
        source_id=entry["source_id"],
        chunk_id=entry["chunk_id"],
        score=score,
        text_preview=entry["text"][:240],
        heading_path=tuple(entry["heading_path"]),
    )
