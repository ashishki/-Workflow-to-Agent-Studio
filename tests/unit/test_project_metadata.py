import tomllib
from pathlib import Path


def test_pyproject_declares_python_and_console_script() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    assert pyproject["project"]["requires-python"] == ">=3.12"
    assert (
        pyproject["project"]["scripts"]["workflow-agent-studio"] == "workflow_agent_studio.cli:main"
    )
