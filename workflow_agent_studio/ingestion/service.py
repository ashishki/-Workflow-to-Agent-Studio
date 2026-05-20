"""Source ingestion service."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

from workflow_agent_studio.ingestion.connectors import ConnectorSource, ReadOnlyConnector
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
    raw_sources = [read_source_path(path) for path in paths]
    return _ingest_raw_sources(
        connection,
        run_id=run_id,
        raw_sources=raw_sources,
        event_type="source_ingested",
    )


def ingest_connector_sources(
    connection: sqlite3.Connection,
    *,
    run_id: str,
    connector: ReadOnlyConnector,
) -> IngestionResult:
    connector_sources = connector.fetch_sources()
    raw_sources = [_raw_source_from_connector(source) for source in connector_sources]
    return _ingest_raw_sources(
        connection,
        run_id=run_id,
        raw_sources=raw_sources,
        event_type="connector_sources_imported",
        event_payload={"connector_id": connector.connector_id},
    )


def _ingest_raw_sources(
    connection: sqlite3.Connection,
    *,
    run_id: str,
    raw_sources: list[RawSource],
    event_type: str,
    event_payload: dict[str, object] | None = None,
) -> IngestionResult:
    source_repository = SourceDocumentRepository(connection)
    duplicate_fingerprints: list[str] = []
    stored_count = 0

    for raw_source in raw_sources:
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
            metadata=raw_source.metadata,
        )
        stored_count += 1

    result = IngestionResult(
        run_id=run_id,
        source_count=stored_count,
        duplicate_count=len(duplicate_fingerprints),
        duplicate_fingerprints=duplicate_fingerprints,
    )
    payload: dict[str, object] = {
        "run_id": run_id,
        "source_count": result.source_count,
        "duplicate_count": result.duplicate_count,
    }
    if event_payload:
        payload.update(event_payload)
    AuditEventRepository(connection).add_event(
        event_id=f"evt-{uuid4()}",
        run_id=run_id,
        event_type=event_type,
        payload=payload,
    )
    return result


def _raw_source_from_connector(source: ConnectorSource) -> RawSource:
    return RawSource(
        path=Path(f"{source.connector_id}-{source.external_id}"),
        source_type=source.source_type,
        title=source.title,
        text=source.text,
        metadata=source.source_metadata(),
    )


def _normalize_source_text(raw_source: RawSource) -> str:
    if raw_source.source_type == "transcript":
        return normalize_transcript_text(raw_source.text)
    return normalize_text(raw_source.text)
