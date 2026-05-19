import json
from contextlib import contextmanager

import pytest

from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintVersionRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
    repositories,
)


@pytest.fixture()
def connection(tmp_path):
    database = connect_database(tmp_path / "workflow_studio.sqlite3")
    initialize_database(database)
    try:
        yield database
    finally:
        database.close()


def test_create_workflow_run_persists_metadata(connection) -> None:
    repository = WorkflowRunRepository(connection)

    repository.create_run(
        "run-1",
        status="created",
        schema_version="v1",
        created_at="2026-05-19T00:00:00+00:00",
    )

    row = connection.execute(
        """
        SELECT run_id, status, created_at, schema_version
        FROM workflow_runs
        WHERE run_id = :run_id
        """,
        {"run_id": "run-1"},
    ).fetchone()
    assert dict(row) == {
        "run_id": "run-1",
        "status": "created",
        "created_at": "2026-05-19T00:00:00+00:00",
        "schema_version": "v1",
    }


def test_blueprint_versions_are_append_only(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    repository = BlueprintVersionRepository(connection)

    first = repository.add_version(run_id="run-1", blueprint={"summary": "first"})
    second = repository.add_version(run_id="run-1", blueprint={"summary": "second"})

    versions = repository.list_versions("run-1")
    assert [version.version_number for version in versions] == [1, 2]
    assert json.loads(first.blueprint_json) == {"summary": "first"}
    assert json.loads(second.blueprint_json) == {"summary": "second"}


def test_audit_events_cannot_be_deleted(connection) -> None:
    WorkflowRunRepository(connection).create_run("run-1")
    repository = AuditEventRepository(connection)
    repository.add_event(event_id="evt-1", run_id="run-1", event_type="run_created", payload={})

    with pytest.raises(PermissionError, match="append-only"):
        repository.delete_event("evt-1")


def test_repository_operations_use_shared_tracing_spans(connection, monkeypatch) -> None:
    span_names: list[str] = []

    class RecordingTracer:
        @contextmanager
        def start_as_current_span(self, name: str):
            span_names.append(name)
            yield

    monkeypatch.setattr(repositories.tracing, "get_tracer", lambda: RecordingTracer())

    WorkflowRunRepository(connection).create_run("run-1")
    WorkflowRunRepository(connection).get_run("run-1")
    BlueprintVersionRepository(connection).add_version(
        run_id="run-1",
        blueprint={"summary": "first"},
    )
    AuditEventRepository(connection).add_event(
        event_id="evt-1",
        run_id="run-1",
        event_type="run_created",
        payload={},
    )
    AuditEventRepository(connection).list_events("run-1")

    assert "storage.workflow_runs.create_run" in span_names
    assert "storage.workflow_runs.get_run" in span_names
    assert "storage.blueprint_versions.add_version" in span_names
    assert "storage.blueprint_versions.get_version" in span_names
    assert "storage.audit_events.add_event" in span_names
    assert "storage.audit_events.list_events" in span_names
