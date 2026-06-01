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


def test_cli_roadmap_generates_hair_salon_demo_report(tmp_path) -> None:
    result = _run_cli(
        [
            "roadmap",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "salon-roadmap",
            "--business-profile",
            "docs/examples/domains/hair_salon_input.md",
            "--privacy-mode",
            "lightweight_cloud",
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "salon-roadmap.md",
        ]
    )

    payload = json.loads(result.stdout)
    markdown = Path(payload["path"]).read_text(encoding="utf-8")
    assert result.returncode == 0
    assert payload["run_id"] == "salon-roadmap"
    assert payload["privacy_mode"] == "lightweight_cloud"
    assert payload["status"] == "draft"
    assert "Status: Draft" in markdown
    assert "Appointment booking and reminder automation" in markdown
    assert "## Verification Appendix" in markdown


def test_cli_roadmap_invalid_privacy_mode_exits_nonzero(tmp_path) -> None:
    result = _run_cli(
        [
            "roadmap",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "salon-roadmap",
            "--business-profile",
            "docs/examples/domains/hair_salon_input.md",
            "--privacy-mode",
            "public_cloud",
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "salon-roadmap.md",
        ]
    )

    assert result.returncode == 2
    assert "invalid choice" in result.stderr
    assert "public_cloud" in result.stderr
    assert not (tmp_path / "exports" / "salon-roadmap.md").exists()
