from pathlib import Path


def test_retrieval_eval_records_ingestion_baseline() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")

    assert "T07 established the initial source ingestion corpus fixture baseline" in retrieval_eval
    assert (
        "| 2026-05-19 | T07 | source-fixture-v1 | n/a | "
        "pytest tests/integration/test_ingestion.py tests/eval/test_retrieval_eval.py -q |"
        in retrieval_eval
    )


def test_retrieval_eval_records_chunking_baseline() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")

    assert "T09 established the v1 chunking corpus fixture baseline" in retrieval_eval
    assert (
        "| 2026-05-19 | T09 | chunking-fixture-v1 | n/a | "
        "pytest tests/unit/test_chunking.py tests/unit/test_pattern_library.py "
        "tests/eval/test_retrieval_eval.py -q |" in retrieval_eval
    )


def test_retrieval_eval_records_index_baseline() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")

    assert "T10 established the first local vector index metadata baseline" in retrieval_eval
    assert (
        "| 2026-05-19 | T10 | index-fixture-v1 | v1 | "
        "pytest tests/unit/test_embeddings.py tests/integration/test_retrieval_index.py "
        "tests/eval/test_retrieval_eval.py -q |" in retrieval_eval
    )


def test_retrieval_hit_at_3_on_workflow_fixture(tmp_path) -> None:
    from workflow_agent_studio.retrieval import (
        FakeEmbeddingProvider,
        build_vector_index,
        chunk_source_document,
        retrieve_evidence,
    )

    chunks = chunk_source_document(
        source_id="src-sop",
        text=(
            "# Support Intake SOP\n\n"
            "Operator creates a follow-up task when engineering review is needed."
        ),
    )
    index = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=FakeEmbeddingProvider(),
        corpus_version="query-fixture-v1",
    )

    result = retrieve_evidence(index_path=index.path, query="engineering review follow-up task")

    assert result.status == "ok"
    assert result.evidence[0].source_id == "src-sop"


def test_retrieval_eval_records_query_metrics() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")

    assert "T11 established the first query-time retrieval metrics baseline" in retrieval_eval
    assert (
        "| 2026-05-19 | T11 | query-fixture-v1 | v1 | "
        "pytest tests/integration/test_retrieval_query.py tests/eval/test_retrieval_eval.py -q | "
        "1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | No |" in retrieval_eval
    )
