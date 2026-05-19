"""Query-time retrieval over a local vector index."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from workflow_agent_studio.retrieval.embeddings import EmbeddingProvider, FakeEmbeddingProvider
from workflow_agent_studio.retrieval.evidence import EvidenceSnippet, RetrievalResult

TOKEN_PATTERN = re.compile(r"[a-z0-9]+")


def retrieve_evidence(
    *,
    index_path: str | Path,
    query: str,
    top_k: int = 3,
    min_score: float = 0.1,
    embedding_provider: EmbeddingProvider | None = None,
) -> RetrievalResult:
    entries = json.loads((Path(index_path) / "vectors.json").read_text(encoding="utf-8"))
    query_tokens = _tokens(query)
    provider = embedding_provider or FakeEmbeddingProvider()
    query_vector = provider.embed_texts([query])[0]
    scored = [(_combined_score(query_tokens, query_vector, entry), entry) for entry in entries]
    evidence = [
        _to_evidence(score, entry)
        for score, entry in sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]
        if score >= min_score
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
