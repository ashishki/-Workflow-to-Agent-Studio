"""Versioned SMB implementation pattern loader."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Literal

from pydantic import Field, ValidationError

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.privacy import PrivacyClass
from workflow_agent_studio.domain.recommendation import SolutionType

DEFAULT_SMB_PATTERN_DIR = Path(__file__).with_name("smb")


class SMBPatternArchitecture(StrictModel):
    recommended_solution_type: SolutionType
    llm_owned_steps: list[str] = Field(default_factory=list)
    deterministic_steps: list[str] = Field(default_factory=list)


class SMBImplementationPattern(StrictModel):
    schema_version: Literal["smb-pattern-v1"] = "smb-pattern-v1"
    pattern_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    pattern_name: str = Field(min_length=1)
    business_problem: str = Field(min_length=1)
    suitable_company_type: list[str] = Field(min_length=1)
    workflow_signals: list[str] = Field(min_length=1)
    required_data: list[str] = Field(min_length=1)
    privacy_default: PrivacyClass
    architecture: SMBPatternArchitecture
    estimated_implementation_time: str = Field(min_length=1)
    cost_range: str = Field(min_length=1)
    required_roles: list[str] = Field(min_length=1)
    risks: list[str] = Field(min_length=1)
    evaluation_metrics: list[str] = Field(min_length=1)
    when_not_to_use: list[str] = Field(min_length=1)


def load_smb_pattern(path: str | Path) -> SMBImplementationPattern:
    pattern_path = Path(path)
    try:
        data = json.loads(pattern_path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        raise ValueError(f"Invalid SMB pattern JSON in {pattern_path}: {exc.msg}") from exc
    try:
        return SMBImplementationPattern.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Invalid SMB pattern schema in {pattern_path}: {exc}") from exc


def load_smb_patterns(
    pattern_dir: str | Path = DEFAULT_SMB_PATTERN_DIR,
) -> list[SMBImplementationPattern]:
    return [load_smb_pattern(path) for path in sorted(Path(pattern_dir).glob("*.json"))]


def smb_pattern_metadata(pattern: SMBImplementationPattern) -> dict[str, str]:
    return {
        "pattern_id": pattern.pattern_id,
        "pattern_version": pattern.version,
        "pattern_schema_version": pattern.schema_version,
    }
