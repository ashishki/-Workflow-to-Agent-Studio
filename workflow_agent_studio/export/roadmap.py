"""Roadmap report local export helpers."""

from __future__ import annotations

from pathlib import Path

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.export.paths import resolve_export_path
from workflow_agent_studio.reporting.roadmap_markdown import render_roadmap_markdown


def export_draft_roadmap_report(
    *,
    report: RoadmapReport,
    export_dir: Path,
    output_path: Path,
) -> Path:
    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_roadmap_markdown(report, status="Draft"), encoding="utf-8")
    return target
