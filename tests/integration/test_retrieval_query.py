from workflow_agent_studio.retrieval import (
    FakeEmbeddingProvider,
    build_vector_index,
    chunk_source_document,
    retrieve_evidence,
)


def _index_path(tmp_path):
    text = (
        "# Support Intake SOP\n\n"
        "Operator reviews inbound support requests and creates a follow-up task when "
        "engineering review is needed."
    )
    chunks = chunk_source_document(source_id="src-sop", text=text)
    index = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=FakeEmbeddingProvider(),
        corpus_version="query-fixture-v1",
    )
    return index.path


def test_query_without_support_returns_insufficient_evidence(tmp_path) -> None:
    result = retrieve_evidence(
        index_path=_index_path(tmp_path),
        query="production deployment credential extraction",
    )

    assert result.status == "insufficient_evidence"
    assert result.evidence == []
    assert result.answer_text is None


def test_evidence_snippet_contains_trace_fields(tmp_path) -> None:
    result = retrieve_evidence(
        index_path=_index_path(tmp_path),
        query="engineering review follow-up task",
    )

    assert result.status == "ok"
    snippet = result.evidence[0]
    assert snippet.source_id == "src-sop"
    assert snippet.chunk_id
    assert snippet.score > 0
    assert "engineering review" in snippet.text_preview
    assert snippet.heading_path == ("Support Intake SOP",)
