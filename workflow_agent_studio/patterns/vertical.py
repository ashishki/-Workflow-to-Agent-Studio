"""Versioned vertical workflow pack loader."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class VerticalPack(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["vertical_pack:v1"]
    pack_id: str = Field(min_length=1)
    domain: str = Field(min_length=1)
    source_examples: list[str] = Field(min_length=1)
    extraction_hints: list[str] = Field(min_length=1)
    required_blueprint_sections: list[str] = Field(min_length=1)
    risks: list[str] = Field(min_length=1)
    eval_fixtures: list[str] = Field(min_length=1)


def load_vertical_pack(path: str | Path) -> VerticalPack:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return VerticalPack.model_validate(data)


def load_vertical_packs(pattern_dir: str | Path) -> list[VerticalPack]:
    return [load_vertical_pack(path) for path in sorted(Path(pattern_dir).glob("*_pack.json"))]


def pack_metadata_for_generation(pack: VerticalPack) -> dict[str, str]:
    return {
        "pack_id": pack.pack_id,
        "pack_schema_version": pack.schema_version,
        "pack_domain": pack.domain,
    }
