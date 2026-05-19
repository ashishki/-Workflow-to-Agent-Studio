import json
import subprocess
import sys
from pathlib import Path

from workflow_agent_studio.ingestion import fingerprint_text, ingest_source_paths, normalize_text
from workflow_agent_studio.storage import (
    AuditEventRepository,
    SourceDocumentRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)

SAMPLE_SOURCE = Path("tests/fixtures/sources/sample_sop.md")


def _connection(tmp_path):
    connection = connect_database(tmp_path / "workflow_studio.sqlite3")
    initialize_database(connection)
    WorkflowRunRepository(connection).create_run("run-1")
    return connection


def test_markdown_ingestion_stores_normalized_source(tmp_path) -> None:
    connection = _connection(tmp_path)
    try:
        result = ingest_source_paths(connection, run_id="run-1", paths=[SAMPLE_SOURCE])
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    normalized = normalize_text(SAMPLE_SOURCE.read_text(encoding="utf-8"))
    assert result.source_count == 1
    assert len(sources) == 1
    assert sources[0].source_type == "markdown"
    assert sources[0].title == "Support Intake SOP"
    assert sources[0].normalized_text == normalized
    assert sources[0].fingerprint == fingerprint_text(normalized)


def test_duplicate_source_fingerprint_not_stored_twice(tmp_path) -> None:
    connection = _connection(tmp_path)
    try:
        result = ingest_source_paths(
            connection,
            run_id="run-1",
            paths=[SAMPLE_SOURCE, SAMPLE_SOURCE],
        )
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    assert result.source_count == 1
    assert result.duplicate_count == 1
    assert len(result.duplicate_fingerprints) == 1
    assert len(sources) == 1


def test_ingestion_audit_event_excludes_raw_source_text(tmp_path) -> None:
    database_path = tmp_path / "workflow_studio.sqlite3"
    command = Path(sys.executable).with_name("workflow-agent-studio")

    result = subprocess.run(
        [
            command,
            "ingest",
            "--database",
            str(database_path),
            "--run-id",
            "run-1",
            str(SAMPLE_SOURCE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout)["source_count"] == 1

    connection = connect_database(database_path)
    try:
        events = AuditEventRepository(connection).list_events("run-1")
    finally:
        connection.close()

    assert len(events) == 1
    payload = json.loads(events[0]["payload_json"])
    assert payload == {"duplicate_count": 0, "run_id": "run-1", "source_count": 1}
    assert "Operator reviews each inbound support request" not in events[0]["payload_json"]
