"""Reusable evidence packs for blueprint sections."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from workflow_agent_studio.retrieval.embeddings import EmbeddingProvider
from workflow_agent_studio.retrieval.evidence import EvidenceSnippet
from workflow_agent_studio.retrieval.query import retrieve_evidence

EvidencePackStatus = Literal["ok", "insufficient_evidence"]

SECTION_QUERIES = {
    "workflow_summary": "workflow intake request support process",
    "actors": "operator coordinator client customer actors",
    "systems": "inbox crm tracker api systems tools",
    "current_workflow_steps": "support request follow-up task engineering review",
    "decisions": "decision whether engineering review is needed",
    "exceptions": "missing details clarification exception blocked",
    "data_fields": "customer_name request_id issue_summary account_status fields",
    "approval_boundaries": "approval approver sign-off boundary human review",
}

CANDIDATE_QUERIES = {
    "draft_follow_up_task": "draft follow-up task engineering review automation candidate",
}


@dataclass(frozen=True)
class EvidencePack:
    section: str
    query: str
    status: EvidencePackStatus
    evidence: list[EvidenceSnippet] = field(default_factory=list)


@dataclass(frozen=True)
class EvidencePackBundle:
    packs: list[EvidencePack]

    @property
    def citation_precision(self) -> float:
        evidence = [snippet for pack in self.packs for snippet in pack.evidence]
        if not evidence:
            return 0.0
        supported = [
            snippet
            for snippet in evidence
            if snippet.source_id and snippet.chunk_id and snippet.text_preview
        ]
        return len(supported) / len(evidence)


def build_evidence_packs(
    *,
    index_path: str | Path,
    sections: Sequence[str],
    candidate_automations: Sequence[str] = (),
    embedding_provider: EmbeddingProvider | None = None,
) -> EvidencePackBundle:
    packs = [
        _build_pack(
            index_path=index_path,
            section=section,
            query=SECTION_QUERIES.get(section),
            embedding_provider=embedding_provider,
        )
        for section in sections
    ]
    packs.extend(
        _build_pack(
            index_path=index_path,
            section=f"automation_candidates:{candidate}",
            query=CANDIDATE_QUERIES.get(candidate),
            embedding_provider=embedding_provider,
        )
        for candidate in candidate_automations
    )
    return EvidencePackBundle(packs=packs)


def _build_pack(
    *,
    index_path: str | Path,
    section: str,
    query: str | None,
    embedding_provider: EmbeddingProvider | None,
) -> EvidencePack:
    if query is None:
        return EvidencePack(section=section, query="", status="insufficient_evidence")
    result = retrieve_evidence(
        index_path=index_path,
        query=query,
        embedding_provider=embedding_provider,
    )
    return EvidencePack(
        section=section,
        query=query,
        status=result.status,
        evidence=result.evidence,
    )
