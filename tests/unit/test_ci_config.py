from pathlib import Path

CI_PATH = Path(".github/workflows/ci.yml")


def _ci_text() -> str:
    return CI_PATH.read_text(encoding="utf-8")


def test_ci_targets_python_312_and_main() -> None:
    ci = _ci_text()

    assert 'branches: ["main"]' in ci
    assert "actions/setup-python@v5" in ci
    assert 'python-version: "3.12"' in ci


def test_ci_installs_dev_requirements_and_editable_package() -> None:
    ci = _ci_text()

    assert "python -m pip install -r requirements-dev.txt" in ci
    assert "python -m pip install -e ." in ci


def test_ci_runs_lint_format_and_pytest_steps() -> None:
    ci = _ci_text()

    assert "name: Ruff check" in ci
    assert "run: ruff check workflow_agent_studio tests/" in ci
    assert "name: Ruff format check" in ci
    assert "run: ruff format --check workflow_agent_studio tests/" in ci
    assert "name: Pytest" in ci
    assert "run: python -m pytest tests/ -q" in ci
