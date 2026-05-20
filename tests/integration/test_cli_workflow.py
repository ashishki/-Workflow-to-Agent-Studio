import json
import subprocess
import sys
from pathlib import Path

from workflow_agent_studio.storage import AuditEventRepository, connect_database


def _run_cli(args: list[str]):
    return subprocess.run(
        [sys.executable, "-m", "workflow_agent_studio.cli", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_generates_draft_blueprint_from_sample_sop(tmp_path) -> None:
    result = _run_cli(
        [
            "run",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "run-1",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/sources/sample_sop.md",
        ]
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["blueprint_version_id"] == 1
    assert payload["source_count"] == 1
    assert payload["index_namespace"].startswith("v1-run-1-e2e")


def test_cli_returns_code_2_for_blocking_findings(tmp_path) -> None:
    source = tmp_path / "unrelated.txt"
    source.write_text("Cafeteria lunch menu and office seating notes.", encoding="utf-8")

    result = _run_cli(
        [
            "run",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "run-2",
            "--index-dir",
            str(tmp_path / "index"),
            str(source),
        ]
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 2
    assert "RAG-INSUFFICIENT-EVIDENCE" in payload["finding_ids"]


def test_cli_export_writes_blueprint_markdown(tmp_path) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_result = _run_cli(
        [
            "run",
            "--database",
            str(database),
            "--run-id",
            "run-3",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/sources/sample_sop.md",
        ]
    )
    version_id = json.loads(run_result.stdout)["blueprint_version_id"]

    export_result = _run_cli(
        [
            "export",
            "--database",
            str(database),
            "--blueprint-version-id",
            str(version_id),
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "blueprint.md",
        ]
    )

    payload = json.loads(export_result.stdout)
    markdown = Path(payload["path"]).read_text(encoding="utf-8")
    assert export_result.returncode == 0
    assert "## Workflow Summary" in markdown
    assert "## Automation Candidates" in markdown
    assert "## Eval Cases" in markdown
    assert "## Evidence Appendix" in markdown


def test_cli_review_workspace_exports_findings_evidence_comments_and_versions(tmp_path) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_result = _run_cli(
        [
            "run",
            "--database",
            str(database),
            "--run-id",
            "run-review",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/sources/sample_sop.md",
        ]
    )
    version_id = json.loads(run_result.stdout)["blueprint_version_id"]
    connection = connect_database(database)
    try:
        AuditEventRepository(connection).add_event(
            event_id="run-review:comment:1:workflow_summary",
            run_id="run-review",
            event_type="review_comment_added",
            payload={
                "blueprint_version_id": version_id,
                "section": "workflow_summary",
                "reviewer_label": "operator",
            },
        )
    finally:
        connection.close()

    review_result = _run_cli(
        [
            "review",
            "--database",
            str(database),
            "--run-id",
            "run-review",
            "--blueprint-version-id",
            str(version_id),
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "review.md",
        ]
    )

    payload = json.loads(review_result.stdout)
    markdown = Path(payload["path"]).read_text(encoding="utf-8")
    assert review_result.returncode == 0
    assert "## Version History" in markdown
    assert "## Findings" in markdown
    assert "## Evidence" in markdown
    assert "## Comments" in markdown
    assert "workflow_summary" in markdown


def test_cli_review_workspace_can_create_edited_draft_and_export(tmp_path) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_result = _run_cli(
        [
            "run",
            "--database",
            str(database),
            "--run-id",
            "run-edit",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/sources/sample_sop.md",
        ]
    )
    version_id = json.loads(run_result.stdout)["blueprint_version_id"]

    review_result = _run_cli(
        [
            "review",
            "--database",
            str(database),
            "--run-id",
            "run-edit",
            "--blueprint-version-id",
            str(version_id),
            "--set-rough-effort-band",
            "medium",
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "edited-review.md",
        ]
    )

    payload = json.loads(review_result.stdout)
    markdown = Path(payload["path"]).read_text(encoding="utf-8")
    assert review_result.returncode == 0
    assert payload["blueprint_version_id"] == 2
    assert "v1: blueprint_version_id=1" in markdown
    assert "v2: blueprint_version_id=2" in markdown
