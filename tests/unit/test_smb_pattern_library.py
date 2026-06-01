import json
from pathlib import Path

import pytest

from workflow_agent_studio.patterns.smb import (
    DEFAULT_SMB_PATTERN_DIR,
    SMBImplementationPattern,
    load_smb_pattern,
    load_smb_patterns,
    smb_pattern_metadata,
)


def test_smb_pattern_loader_validates_every_pattern_file() -> None:
    pattern_paths = sorted(DEFAULT_SMB_PATTERN_DIR.glob("*.json"))
    patterns = load_smb_patterns()

    assert pattern_paths
    assert len(patterns) == len(pattern_paths)
    assert all(isinstance(pattern, SMBImplementationPattern) for pattern in patterns)
    assert {pattern.schema_version for pattern in patterns} == {"smb-pattern-v1"}
    assert all(pattern.workflow_signals for pattern in patterns)
    assert all(pattern.required_data for pattern in patterns)
    assert all(pattern.privacy_default for pattern in patterns)
    assert all(pattern.architecture.recommended_solution_type for pattern in patterns)
    assert all(pattern.risks for pattern in patterns)
    assert all(pattern.evaluation_metrics for pattern in patterns)
    assert all(pattern.when_not_to_use for pattern in patterns)


def test_smb_pattern_loader_returns_version_metadata() -> None:
    pattern = load_smb_pattern(DEFAULT_SMB_PATTERN_DIR / "customer_support_triage.json")

    assert smb_pattern_metadata(pattern) == {
        "pattern_id": "customer_support_triage",
        "pattern_version": "v1",
        "pattern_schema_version": "smb-pattern-v1",
    }


def test_invalid_json_pattern_fails_with_clear_error(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{not-json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid SMB pattern JSON"):
        load_smb_pattern(path)


def test_invalid_pattern_schema_fails_with_clear_error(tmp_path: Path) -> None:
    valid = json.loads(
        (DEFAULT_SMB_PATTERN_DIR / "customer_support_triage.json").read_text(encoding="utf-8")
    )
    valid.pop("workflow_signals")
    path = tmp_path / "invalid_schema.json"
    path.write_text(json.dumps(valid), encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid SMB pattern schema"):
        load_smb_pattern(path)
