"""Synthetic benchmark fixture loading and coverage reporting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SyntheticBenchmarkFixture(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["synthetic_benchmark:v1"]
    benchmark_id: str = Field(min_length=1)
    dataset_kind: Literal["synthetic"]
    not_pilot_evidence: Literal[True]
    domain: str = Field(min_length=1)
    source_summary: str = Field(min_length=1)
    retrieval_queries: list[str] = Field(min_length=1)
    required_blueprint_sections: list[str] = Field(min_length=1)
    expected_feedback_categories: list[str] = Field(min_length=1)


class BenchmarkCoverageReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    fixture_count: int
    retrieval_query_count: int
    required_section_count: int
    feedback_category_count: int
    dataset_kind: Literal["synthetic"]
    not_pilot_evidence: Literal[True]


def load_synthetic_benchmark_fixtures(
    benchmark_dir: str | Path,
) -> list[SyntheticBenchmarkFixture]:
    return [
        _load_synthetic_benchmark_fixture(path)
        for path in sorted(Path(benchmark_dir).glob("synthetic_*.json"))
    ]


def synthetic_benchmark_coverage(
    fixtures: list[SyntheticBenchmarkFixture],
) -> BenchmarkCoverageReport:
    return BenchmarkCoverageReport(
        fixture_count=len(fixtures),
        retrieval_query_count=sum(len(fixture.retrieval_queries) for fixture in fixtures),
        required_section_count=len(
            {section for fixture in fixtures for section in fixture.required_blueprint_sections}
        ),
        feedback_category_count=len(
            {category for fixture in fixtures for category in fixture.expected_feedback_categories}
        ),
        dataset_kind="synthetic",
        not_pilot_evidence=True,
    )


def _load_synthetic_benchmark_fixture(path: Path) -> SyntheticBenchmarkFixture:
    data = json.loads(path.read_text(encoding="utf-8"))
    return SyntheticBenchmarkFixture.model_validate(data)
