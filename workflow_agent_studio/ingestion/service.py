"""Source ingestion service."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from workflow_agent_studio.ingestion.normalizer import (
    fingerprint_text,
    normalize_text,
    normalize_transcript_text,
)
from workflow_agent_studio.ingestion.readers import RawSource, read_source_path
from workflow_agent_studio.storage.repositories import (
    AuditEventRepository,
    SourceDocumentRepository,
)


@dataclass(frozen=True)
class IngestionResult:
    run_id: str
    source_count: int
    duplicate_count: int
    duplicate_fingerprints: list[str] = field(default_factory=list)


def ingest_source_paths(
    connection: sqlite3.Connection,
    *,
    run_id: str,
    paths: list[str | Path],
) -> IngestionResult:
    source_repository = SourceDocumentRepository(connection)
    duplicate_fingerprints: list[str] = []
    stored_count = 0

    for path in paths:
        raw_source = read_source_path(path)
        normalized_text = _normalize_source_text(raw_source)
        fingerprint = fingerprint_text(normalized_text)
        existing = source_repository.get_by_fingerprint(run_id=run_id, fingerprint=fingerprint)
        if existing is not None:
            duplicate_fingerprints.append(fingerprint)
            continue
        source_repository.add_source(
            source_id=f"src-{run_id}-{fingerprint[:16]}",
            run_id=run_id,
            source_type=raw_source.source_type,
            title=raw_source.title,
            fingerprint=fingerprint,
            normalized_text=normalized_text,
        )
        stored_count += 1

    result = IngestionResult(
        run_id=run_id,
        source_count=stored_count,
        duplicate_count=len(duplicate_fingerprints),
        duplicate_fingerprints=duplicate_fingerprints,
    )
    AuditEventRepository(connection).add_event(
        event_id=f"evt-{uuid4()}",
        run_id=run_id,
        event_type="source_ingested",
        payload={
            "run_id": run_id,
            "source_count": result.source_count,
            "duplicate_count": result.duplicate_count,
        },
    )
    return result


def _normalize_source_text(raw_source: RawSource) -> str:
    if raw_source.source_type == "transcript":
        return normalize_transcript_text(raw_source.text)
    return normalize_text(raw_source.text)
