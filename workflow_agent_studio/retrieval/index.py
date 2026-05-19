"""Local vector index persistence."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from workflow_agent_studio.retrieval.chunking import SourceChunk
from workflow_agent_studio.retrieval.embeddings import EmbeddingProvider

INDEX_SCHEMA_VERSION = "v1"


@dataclass(frozen=True)
class IndexMetadata:
    schema_version: str
    embedding_model: str
    corpus_version: str
    chunk_count: int
    created_at: str
    namespace: str


@dataclass(frozen=True)
class VectorIndex:
    namespace: str
    path: Path
    metadata: IndexMetadata


def build_vector_index(
    *,
    chunks: list[SourceChunk],
    index_dir: str | Path,
    embedding_provider: EmbeddingProvider,
    corpus_version: str,
    schema_version: str = INDEX_SCHEMA_VERSION,
    created_at: str | None = None,
) -> VectorIndex:
    namespace = f"{schema_version}-{corpus_version}"
    namespace_dir = Path(index_dir) / namespace
    namespace_dir.mkdir(parents=True, exist_ok=True)

    vectors = embedding_provider.embed_texts([chunk.text for chunk in chunks])
    metadata = IndexMetadata(
        schema_version=schema_version,
        embedding_model=embedding_provider.model_name,
        corpus_version=corpus_version,
        chunk_count=len(chunks),
        created_at=created_at or datetime.now(UTC).isoformat(),
        namespace=namespace,
    )
    (namespace_dir / "metadata.json").write_text(
        json.dumps(asdict(metadata), sort_keys=True, indent=2),
        encoding="utf-8",
    )
    (namespace_dir / "vectors.json").write_text(
        json.dumps(
            [
                {
                    "chunk_id": chunk.chunk_id,
                    "source_id": chunk.source_id,
                    "heading_path": list(chunk.heading_path),
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char,
                    "text": chunk.text,
                    "vector": vector,
                }
                for chunk, vector in zip(chunks, vectors, strict=True)
            ],
            sort_keys=True,
            indent=2,
        ),
        encoding="utf-8",
    )
    return VectorIndex(namespace=namespace, path=namespace_dir, metadata=metadata)


def load_index_metadata(index_path: str | Path) -> IndexMetadata:
    data = json.loads((Path(index_path) / "metadata.json").read_text(encoding="utf-8"))
    return IndexMetadata(**data)
