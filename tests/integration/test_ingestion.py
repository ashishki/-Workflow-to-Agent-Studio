import json
import subprocess
import sys
from pathlib import Path

from workflow_agent_studio.ingestion import (
    fingerprint_text,
    ingest_source_paths,
    normalize_text,
    normalize_transcript_text,
)
from workflow_agent_studio.observability import tracing
from workflow_agent_studio.storage import (
    AuditEventRepository,
    SourceDocumentRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)

SAMPLE_SOURCE = Path("tests/fixtures/sources/sample_sop.md")
TRANSCRIPT_SOURCE = Path("tests/fixtures/sources/discovery_call.transcript.txt")
NOTES_SOURCE = Path("tests/fixtures/sources/discovery_notes.notes.txt")
FORM_SOURCE = Path("tests/fixtures/sources/intake_form.form.md")
INTEGRATION_SOURCE = Path("tests/fixtures/sources/crm_integration.integration.txt")


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


def test_transcript_ingestion_stores_normalized_source_record(tmp_path) -> None:
    connection = _connection(tmp_path)
    try:
        result = ingest_source_paths(connection, run_id="run-1", paths=[TRANSCRIPT_SOURCE])
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    normalized = normalize_transcript_text(TRANSCRIPT_SOURCE.read_text(encoding="utf-8"))
    assert result.source_count == 1
    assert len(sources) == 1
    assert sources[0].source_type == "transcript"
    assert sources[0].title == "discovery_call.transcript"
    assert sources[0].normalized_text == normalized
    assert sources[0].fingerprint == fingerprint_text(normalized)
    assert "Consultant: Walk me through the intake process." in sources[0].normalized_text


def test_common_discovery_artifacts_store_source_kind_metadata(tmp_path) -> None:
    connection = _connection(tmp_path)
    try:
        result = ingest_source_paths(
            connection,
            run_id="run-1",
            paths=[NOTES_SOURCE, FORM_SOURCE, INTEGRATION_SOURCE],
        )
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    assert result.source_count == 3
    assert {source.source_type for source in sources} == {"notes", "form", "integration"}
    assert {source.title for source in sources} == {
        "crm_integration.integration",
        "discovery_notes.notes",
        "intake_form.form",
    }


def test_transcript_fingerprint_ignores_whitespace_only_changes(tmp_path) -> None:
    first = tmp_path / "first.transcript.txt"
    second = tmp_path / "second.transcript.txt"
    first.write_text(
        "Consultant: Walk me through intake.\nClient: The coordinator checks the CRM.\n",
        encoding="utf-8",
    )
    second.write_text(
        "\n  Consultant:   Walk   me through intake.  \n\n"
        "Client: The coordinator   checks the CRM.   \n",
        encoding="utf-8",
    )
    connection = _connection(tmp_path)
    try:
        result = ingest_source_paths(connection, run_id="run-1", paths=[first, second])
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    assert result.source_count == 1
    assert result.duplicate_count == 1
    assert len(sources) == 1
    assert sources[0].source_type == "transcript"


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


def test_unsupported_source_file_fails_without_partial_persisted_source(tmp_path) -> None:
    database_path = tmp_path / "workflow_studio.sqlite3"
    unsupported_source = tmp_path / "source.pdf"
    unsupported_source.write_text("Raw unsupported discovery source text", encoding="utf-8")
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
            str(unsupported_source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 2
    assert "Unsupported source file type" in result.stderr
    assert "Raw unsupported discovery source text" not in result.stderr

    connection = connect_database(database_path)
    try:
        sources = SourceDocumentRepository(connection).list_by_run("run-1")
    finally:
        connection.close()

    assert sources == []


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


def test_transcript_ingestion_observability_excludes_raw_transcript_text(
    tmp_path, monkeypatch
) -> None:
    raw_phrase = "A coordinator reviews each request in the shared inbox"
    span_names: list[str] = []

    class CapturingTracer:
        def start_as_current_span(self, name: str):
            span_names.append(name)
            return tracing.NoopTracer().start_as_current_span(name)

    monkeypatch.setattr(tracing, "get_tracer", lambda: CapturingTracer())

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
            str(TRANSCRIPT_SOURCE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert raw_phrase not in result.stdout
    assert raw_phrase not in result.stderr

    span_connection = connect_database(tmp_path / "span_workflow_studio.sqlite3")
    initialize_database(span_connection)
    WorkflowRunRepository(span_connection).create_run("run-spans")
    try:
        ingest_source_paths(span_connection, run_id="run-spans", paths=[TRANSCRIPT_SOURCE])
    finally:
        span_connection.close()

    assert span_names
    assert all(raw_phrase not in span_name for span_name in span_names)

    connection = connect_database(database_path)
    try:
        events = AuditEventRepository(connection).list_events("run-1")
    finally:
        connection.close()

    assert events
    assert raw_phrase not in events[0]["event_type"]
    assert raw_phrase not in events[0]["payload_json"]
