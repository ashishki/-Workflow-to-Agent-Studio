import json
import subprocess
import sys
from pathlib import Path


def test_cli_help_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "workflow_agent_studio.cli", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "workflow-agent-studio" in result.stdout


def test_health_command_outputs_json() -> None:
    command = Path(sys.executable).with_name("workflow-agent-studio")
    result = subprocess.run(
        [command, "health"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == {"app": "workflow-agent-studio", "status": "ok"}
