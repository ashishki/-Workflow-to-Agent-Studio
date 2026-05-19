"""SQLite repositories for workflow state."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from workflow_agent_studio.observability import tracing


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _repository_span(name: str):
    return tracing.get_tracer().start_as_current_span(f"storage.{name}")


@dataclass(frozen=True)
class WorkflowRunRecord:
    run_id: str
    status: str
    created_at: str
    schema_version: str


@dataclass(frozen=True)
class BlueprintVersionRecord:
    blueprint_version_id: int
    run_id: str
    version_number: int
    blueprint_json: str
    created_at: str


@dataclass(frozen=True)
class BlueprintApprovalRecord:
    blueprint_version_id: int
    run_id: str
    reviewer_label: str
    approved_at: str
    status: str


@dataclass(frozen=True)
class SourceDocumentRecord:
    source_id: str
    run_id: str
    source_type: str
    title: str
    fingerprint: str
    normalized_text: str
    created_at: str


class WorkflowRunRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def create_run(
        self,
        run_id: str,
        *,
        status: str = "created",
        schema_version: str = "v1",
        created_at: str | None = None,
    ) -> WorkflowRunRecord:
        timestamp = created_at or _now()
        with _repository_span("workflow_runs.create_run"):
            self._connection.execute(
                """
                INSERT INTO workflow_runs (run_id, status, created_at, schema_version)
                VALUES (:run_id, :status, :created_at, :schema_version)
                """,
                {
                    "run_id": run_id,
                    "status": status,
                    "created_at": timestamp,
                    "schema_version": schema_version,
                },
            )
            self._connection.commit()
        return WorkflowRunRecord(run_id, status, timestamp, schema_version)

    def get_run(self, run_id: str) -> WorkflowRunRecord | None:
        with _repository_span("workflow_runs.get_run"):
            row = self._connection.execute(
                """
                SELECT run_id, status, created_at, schema_version
                FROM workflow_runs
                WHERE run_id = :run_id
                """,
                {"run_id": run_id},
            ).fetchone()
        if row is None:
            return None
        return WorkflowRunRecord(**dict(row))


class SourceDocumentRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add_source(
        self,
        *,
        source_id: str,
        run_id: str,
        source_type: str,
        title: str,
        fingerprint: str,
        normalized_text: str,
        created_at: str | None = None,
    ) -> SourceDocumentRecord:
        timestamp = created_at or _now()
        with _repository_span("source_documents.add_source"):
            self._connection.execute(
                """
                INSERT INTO source_documents (
                    source_id, run_id, source_type, title, fingerprint, normalized_text, created_at
                )
                VALUES (
                    :source_id, :run_id, :source_type, :title, :fingerprint, :normalized_text,
                    :created_at
                )
                """,
                {
                    "source_id": source_id,
                    "run_id": run_id,
                    "source_type": source_type,
                    "title": title,
                    "fingerprint": fingerprint,
                    "normalized_text": normalized_text,
                    "created_at": timestamp,
                },
            )
            self._connection.commit()
        return SourceDocumentRecord(
            source_id=source_id,
            run_id=run_id,
            source_type=source_type,
            title=title,
            fingerprint=fingerprint,
            normalized_text=normalized_text,
            created_at=timestamp,
        )

    def get_by_fingerprint(self, *, run_id: str, fingerprint: str) -> SourceDocumentRecord | None:
        with _repository_span("source_documents.get_by_fingerprint"):
            row = self._connection.execute(
                """
                SELECT
                    source_id, run_id, source_type, title, fingerprint, normalized_text, created_at
                FROM source_documents
                WHERE run_id = :run_id AND fingerprint = :fingerprint
                """,
                {"run_id": run_id, "fingerprint": fingerprint},
            ).fetchone()
        if row is None:
            return None
        return SourceDocumentRecord(**dict(row))

    def list_by_run(self, run_id: str) -> list[SourceDocumentRecord]:
        with _repository_span("source_documents.list_by_run"):
            rows = self._connection.execute(
                """
                SELECT
                    source_id, run_id, source_type, title, fingerprint, normalized_text, created_at
                FROM source_documents
                WHERE run_id = :run_id
                ORDER BY created_at, source_id
                """,
                {"run_id": run_id},
            ).fetchall()
        return [SourceDocumentRecord(**dict(row)) for row in rows]


class BlueprintVersionRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add_version(
        self,
        *,
        run_id: str,
        blueprint: dict[str, Any],
        created_at: str | None = None,
    ) -> BlueprintVersionRecord:
        with _repository_span("blueprint_versions.add_version"):
            version_row = self._connection.execute(
                """
                SELECT COALESCE(MAX(version_number), 0) + 1 AS next_version
                FROM blueprint_versions
                WHERE run_id = :run_id
                """,
                {"run_id": run_id},
            ).fetchone()
            version_number = int(version_row["next_version"])
            cursor = self._connection.execute(
                """
                INSERT INTO blueprint_versions (run_id, version_number, blueprint_json, created_at)
                VALUES (:run_id, :version_number, :blueprint_json, :created_at)
                """,
                {
                    "run_id": run_id,
                    "version_number": version_number,
                    "blueprint_json": json.dumps(blueprint, sort_keys=True),
                    "created_at": created_at or _now(),
                },
            )
            self._connection.commit()
        return self.get_version(int(cursor.lastrowid))

    def get_version(self, blueprint_version_id: int) -> BlueprintVersionRecord:
        with _repository_span("blueprint_versions.get_version"):
            row = self._connection.execute(
                """
                SELECT blueprint_version_id, run_id, version_number, blueprint_json, created_at
                FROM blueprint_versions
                WHERE blueprint_version_id = :blueprint_version_id
                """,
                {"blueprint_version_id": blueprint_version_id},
            ).fetchone()
        if row is None:
            raise LookupError(f"Blueprint version not found: {blueprint_version_id}")
        return BlueprintVersionRecord(**dict(row))

    def list_versions(self, run_id: str) -> list[BlueprintVersionRecord]:
        with _repository_span("blueprint_versions.list_versions"):
            rows = self._connection.execute(
                """
                SELECT blueprint_version_id, run_id, version_number, blueprint_json, created_at
                FROM blueprint_versions
                WHERE run_id = :run_id
                ORDER BY version_number
                """,
                {"run_id": run_id},
            ).fetchall()
        return [BlueprintVersionRecord(**dict(row)) for row in rows]


class BlueprintApprovalRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def approve(
        self,
        *,
        blueprint_version_id: int,
        run_id: str,
        reviewer_label: str,
        approved_at: str | None = None,
    ) -> BlueprintApprovalRecord:
        timestamp = approved_at or _now()
        with _repository_span("blueprint_approvals.approve"):
            self._connection.execute(
                """
                INSERT INTO blueprint_approvals (
                    blueprint_version_id, run_id, reviewer_label, approved_at, status
                )
                VALUES (
                    :blueprint_version_id, :run_id, :reviewer_label, :approved_at, :status
                )
                """,
                {
                    "blueprint_version_id": blueprint_version_id,
                    "run_id": run_id,
                    "reviewer_label": reviewer_label,
                    "approved_at": timestamp,
                    "status": "approved",
                },
            )
            self._connection.commit()
        return BlueprintApprovalRecord(
            blueprint_version_id=blueprint_version_id,
            run_id=run_id,
            reviewer_label=reviewer_label,
            approved_at=timestamp,
            status="approved",
        )

    def get_approval(self, blueprint_version_id: int) -> BlueprintApprovalRecord | None:
        with _repository_span("blueprint_approvals.get_approval"):
            row = self._connection.execute(
                """
                SELECT blueprint_version_id, run_id, reviewer_label, approved_at, status
                FROM blueprint_approvals
                WHERE blueprint_version_id = :blueprint_version_id
                """,
                {"blueprint_version_id": blueprint_version_id},
            ).fetchone()
        if row is None:
            return None
        return BlueprintApprovalRecord(**dict(row))


class AuditEventRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def add_event(
        self,
        *,
        event_id: str,
        run_id: str,
        event_type: str,
        payload: dict[str, Any],
        created_at: str | None = None,
    ) -> None:
        with _repository_span("audit_events.add_event"):
            self._connection.execute(
                """
                INSERT INTO audit_events (event_id, run_id, event_type, payload_json, created_at)
                VALUES (:event_id, :run_id, :event_type, :payload_json, :created_at)
                """,
                {
                    "event_id": event_id,
                    "run_id": run_id,
                    "event_type": event_type,
                    "payload_json": json.dumps(payload, sort_keys=True),
                    "created_at": created_at or _now(),
                },
            )
            self._connection.commit()

    def delete_event(self, event_id: str) -> None:
        raise PermissionError(f"Audit events are append-only: {event_id}")

    def list_events(self, run_id: str) -> list[sqlite3.Row]:
        with _repository_span("audit_events.list_events"):
            return self._connection.execute(
                """
                SELECT event_id, run_id, event_type, payload_json, created_at
                FROM audit_events
                WHERE run_id = :run_id
                ORDER BY created_at, event_id
                """,
                {"run_id": run_id},
            ).fetchall()
