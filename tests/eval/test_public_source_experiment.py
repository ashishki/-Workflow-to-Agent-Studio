import json
import subprocess
import sys
from pathlib import Path


def test_netbox_public_source_fixture_runs_draft_pipeline(tmp_path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "run",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "public-netbox-issue-triage",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/public_sources/netbox_issue_triage.notes.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["source_count"] == 1
    assert payload["chunk_count"] >= 10
    assert payload["blueprint_version_id"] == 1
    assert payload["finding_ids"] == []
    assert payload["index_namespace"] == "v1-public-netbox-issue-triage-e2e"


def test_netbox_public_source_experiment_keeps_pilot_boundary_explicit() -> None:
    report = Path("docs/experiments/public_source_netbox_issue_triage.md").read_text(
        encoding="utf-8"
    )
    normalized_report = " ".join(report.split())
    fixture = Path("tests/fixtures/public_sources/netbox_issue_triage.notes.md").read_text(
        encoding="utf-8"
    )

    assert "public-source experiment; not real pilot evidence" in report
    assert "not counted in `docs/pilot_measurement.md`" in report
    assert "does not satisfy T34/T40" in report
    assert "template-shaped" in report
    assert "pass for pipeline mechanics" in normalized_report
    assert "fail for domain-specific draft quality" in normalized_report
    assert "Dataset kind: public-source experiment only; not operator pilot evidence." in fixture
    assert "https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow" in fixture
