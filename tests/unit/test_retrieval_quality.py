from collections.abc import Sequence

from workflow_agent_studio.retrieval import (
    FakeEmbeddingProvider,
    ScoredEntry,
    build_vector_index,
    chunk_source_document,
    retrieve_evidence,
)


def _index_path(tmp_path):
    chunks = [
        *chunk_source_document(
            source_id="src-first",
            text=(
                "# Intake\n\n"
                "The coordinator reviews support requests and checks CRM account status."
            ),
        ),
        *chunk_source_document(
            source_id="src-second",
            text=(
                "# Follow-up\n\n"
                "The coordinator drafts a follow-up task when engineering review is needed."
            ),
        ),
    ]
    index = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=FakeEmbeddingProvider(),
        corpus_version="retrieval-quality-fixture-v1",
    )
    return index.path


def test_retrieval_threshold_controls_low_confidence_no_answer(tmp_path) -> None:
    index_path = _index_path(tmp_path)

    supported = retrieve_evidence(
        index_path=index_path,
        query="engineering review follow-up task",
        min_score=0.1,
    )
    low_confidence = retrieve_evidence(
        index_path=index_path,
        query="engineering review follow-up task",
        min_score=1.01,
    )

    assert supported.status == "ok"
    assert low_confidence.status == "insufficient_evidence"
    assert low_confidence.evidence == []


def test_retrieval_reranker_can_be_faked_deterministically(tmp_path) -> None:
    class PreferFirstSourceLast:
        def rerank(self, entries: Sequence[ScoredEntry]) -> list[ScoredEntry]:
            return sorted(entries, key=lambda item: item.entry["source_id"], reverse=True)

    result = retrieve_evidence(
        index_path=_index_path(tmp_path),
        query="coordinator review",
        min_score=0.1,
        top_k=2,
        reranker=PreferFirstSourceLast(),
    )

    assert result.status == "ok"
    assert result.evidence[0].source_id == "src-second"


def test_retrieval_unsupported_query_returns_no_answer(tmp_path) -> None:
    result = retrieve_evidence(
        index_path=_index_path(tmp_path),
        query="production credential extraction deployment",
        min_score=0.1,
    )

    assert result.status == "insufficient_evidence"
    assert result.evidence == []
    assert result.answer_text is None
