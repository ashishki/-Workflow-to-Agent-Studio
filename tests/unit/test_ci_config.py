from pathlib import Path

import yaml

CI_PATH = Path(".github/workflows/ci.yml")
CI_TEMPLATE_PATH = Path("ci/ci.yml")
GITLEAKS_IGNORE_PATH = Path(".gitleaksignore")


def _ci_text() -> str:
    return CI_PATH.read_text(encoding="utf-8")


def test_ci_targets_python_312_and_main() -> None:
    ci = _ci_text()

    assert 'branches: ["main"]' in ci
    assert "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0 # v7.0.0" in ci
    assert "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1 # v6.3.0" in ci
    assert 'python-version: "3.12"' in ci


def test_ci_uses_a_read_only_bounded_checkout() -> None:
    ci = _ci_text()

    assert "permissions:\n  contents: read" in ci
    assert "fetch-depth: 0" in ci
    assert "persist-credentials: false" in ci
    assert "timeout-minutes: 20" in ci
    assert "cancel-in-progress: true" in ci


def test_ci_scans_full_history_with_a_checksum_verified_gitleaks_binary() -> None:
    ci = _ci_text()
    checksum = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"

    assert 'GITLEAKS_VERSION: "8.30.1"' in ci
    assert f'GITLEAKS_ARCHIVE_SHA256: "{checksum}"' in ci
    assert "sha256sum --check" in ci
    assert 'gitleaks" git --no-banner --redact=100 .' in ci


def test_gitleaks_allowlist_is_limited_to_exact_historical_fingerprints() -> None:
    fingerprints = [
        line
        for line in GITLEAKS_IGNORE_PATH.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#")
    ]

    assert len(fingerprints) == 7
    for fingerprint in fingerprints:
        commit, path, rule, line = fingerprint.split(":")
        assert len(commit) == 40
        assert all(character in "0123456789abcdef" for character in commit)
        assert path.startswith("tests/unit/test_")
        assert rule in {"generic-api-key", "stripe-access-token"}
        assert line.isdigit()


def test_ci_and_template_are_valid_yaml() -> None:
    for path in (CI_PATH, CI_TEMPLATE_PATH):
        document = yaml.compose(path.read_text(encoding="utf-8"))

        assert document is not None


def test_ci_and_template_pin_every_action_to_a_full_commit_sha() -> None:
    for path in (CI_PATH, CI_TEMPLATE_PATH):
        uses_lines = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if "uses:" in line
        ]

        assert uses_lines
        for line in uses_lines:
            revision = line.partition("@")[2].split()[0]
            assert len(revision) == 40
            assert all(character in "0123456789abcdef" for character in revision)


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
