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


def test_netbox_public_source_blueprint_preserves_domain_facts(tmp_path) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "run",
            "--database",
            str(database),
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
    version_id = json.loads(run_result.stdout)["blueprint_version_id"]

    export_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "export",
            "--database",
            str(database),
            "--blueprint-version-id",
            str(version_id),
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "netbox_blueprint.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    export_payload = json.loads(export_result.stdout)
    markdown = Path(export_payload["path"]).read_text(encoding="utf-8")
    assert export_result.returncode == 0
    assert "GitHub Issues" in markdown
    assert "Issue templates" in markdown
    assert "Reporter" in markdown
    assert "Maintainer or triager" in markdown
    assert "duplicate" in markdown
    assert "stale" in markdown
    assert "reproduc" in markdown
    assert "Support intake workflow routes customer requests" not in markdown


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
    assert "current result preserves NetBox-specific actors" in report
    assert "pass for pipeline mechanics" in normalized_report
    assert "pass for domain-specific draft quality" in normalized_report
    assert "still blocked for real-pilot proof" in normalized_report
    assert "Dataset kind: public-source experiment only; not operator pilot evidence." in fixture
    assert "https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow" in fixture
