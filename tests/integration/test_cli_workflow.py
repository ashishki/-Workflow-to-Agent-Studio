import json
import subprocess
import sys
from pathlib import Path


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
