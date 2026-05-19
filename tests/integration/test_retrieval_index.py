from workflow_agent_studio.retrieval import (
    FakeEmbeddingProvider,
    build_vector_index,
    chunk_source_document,
    load_index_metadata,
)


def test_index_metadata_records_schema_and_corpus(tmp_path) -> None:
    chunks = chunk_source_document(source_id="src-1", text="# Intake\n\nReview the request.")

    index = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=FakeEmbeddingProvider(model_name="fake-v1"),
        corpus_version="corpus-v1",
        created_at="2026-05-19T00:00:00+00:00",
    )

    metadata = load_index_metadata(index.path)
    assert metadata.schema_version == "v1"
    assert metadata.embedding_model == "fake-v1"
    assert metadata.corpus_version == "corpus-v1"
    assert metadata.chunk_count == 1
    assert metadata.created_at == "2026-05-19T00:00:00+00:00"


def test_schema_version_change_creates_new_namespace(tmp_path) -> None:
    chunks = chunk_source_document(source_id="src-1", text="# Intake\n\nReview the request.")
    provider = FakeEmbeddingProvider(model_name="fake-v1")

    first = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=provider,
        corpus_version="corpus-v1",
        schema_version="v1",
    )
    second = build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=provider,
        corpus_version="corpus-v1",
        schema_version="v2",
    )

    assert first.namespace == "v1-corpus-v1"
    assert second.namespace == "v2-corpus-v1"
    assert first.path != second.path
    assert first.path.exists()
    assert second.path.exists()
