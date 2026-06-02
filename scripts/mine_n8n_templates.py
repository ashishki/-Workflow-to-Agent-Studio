#!/usr/bin/env python3
"""Mine local public n8n template repositories into pattern-candidate summaries."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from workflow_agent_studio.patterns.n8n import (
    N8nMiningResult,
    discover_n8n_json_paths,
    mine_n8n_workflow_paths,
    n8n_candidate_summary_counts,
)

_UTILITY_INTEGRATIONS = {
    "code",
    "cron",
    "filter",
    "function",
    "httprequest",
    "if",
    "manual",
    "merge",
    "noop",
    "schedule",
    "set",
    "splitinbatches",
    "splitout",
    "stickynote",
    "switch",
    "webhook",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        default=".data/n8n_sources",
        help="Directory containing local public n8n repository clones.",
    )
    parser.add_argument(
        "--json-output",
        default=".data/n8n_mining/n8n_pattern_candidates.json",
        help="Output JSON path for deduplicated metadata candidates.",
    )
    parser.add_argument(
        "--markdown-output",
        default="docs/experiments/n8n_template_mining_summary.md",
        help="Output Markdown summary path.",
    )
    parser.add_argument(
        "--top",
        default=40,
        type=int,
        help="Maximum candidates to include in the Markdown table.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    source_root = Path(args.source_root)
    json_paths = discover_n8n_json_paths(source_root)
    result = mine_n8n_workflow_paths(json_paths, source_root=source_root)
    _write_json(result=result, output_path=Path(args.json_output))
    _write_markdown(result=result, output_path=Path(args.markdown_output), top=args.top)
    print(
        json.dumps(
            {
                "candidates": len(result.candidates),
                "duplicates": result.duplicate_workflows,
                "json_output": args.json_output,
                "markdown_output": args.markdown_output,
                "parsed_workflows": result.parsed_workflows,
                "scanned_json_files": result.scanned_json_files,
                "skipped_json_files": result.skipped_json_files,
            },
            sort_keys=True,
        )
    )
    return 0


def _write_json(*, result: N8nMiningResult, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result.model_dump(), ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _write_markdown(*, result: N8nMiningResult, output_path: Path, top: int) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    archetype_counts = n8n_candidate_summary_counts(result.candidates)
    integration_counts = Counter(
        integration for candidate in result.candidates for integration in candidate.integrations
    )
    ai_candidate_count = sum(1 for candidate in result.candidates if candidate.ai_node_count)
    risky_candidate_count = sum(
        1 for candidate in result.candidates if candidate.risky_action_signals
    )
    sensitive_candidate_count = sum(
        1 for candidate in result.candidates if candidate.data_sensitivity_signals
    )
    cluster_counts = _cluster_counts(result)
    top_candidates = _balanced_review_queue(result=result, top=top)
    lines = [
        "# n8n Template Mining Summary",
        "",
        "Status: public-source metadata mining; not buyer proof",
        "",
        "## Claim Boundary",
        "",
        "This artifact summarizes extracted metadata from local clones of public",
        "n8n template repositories. It does not commit raw third-party workflow JSON",
        "and does not prove ROI, customer demand, or implementation safety.",
        "",
        "## Run Summary",
        "",
        f"- source roots: {', '.join(result.source_roots)}",
        f"- scanned JSON files: {result.scanned_json_files}",
        f"- parsed n8n workflows: {result.parsed_workflows}",
        f"- skipped JSON files: {result.skipped_json_files}",
        f"- duplicate workflows collapsed: {result.duplicate_workflows}",
        f"- deduplicated candidates: {len(result.candidates)}",
        f"- candidates with AI nodes: {ai_candidate_count}",
        f"- candidates with risky action signals: {risky_candidate_count}",
        f"- candidates with data sensitivity signals: {sensitive_candidate_count}",
        "",
        "## Archetype Counts",
        "",
        "| Archetype | Candidates |",
        "|---|---:|",
        *[f"| `{name}` | {count} |" for name, count in archetype_counts.items()],
        "",
        "## Top Integrations",
        "",
        "| Integration | Candidates |",
        "|---|---:|",
        *[f"| `{name}` | {count} |" for name, count in integration_counts.most_common(20)],
        "",
        "## Top Candidate Clusters",
        "",
        "| Archetype | Business integrations | Candidates |",
        "|---|---|---:|",
        *[
            f"| `{archetype}` | {integrations} | {count} |"
            for (archetype, integrations), count in cluster_counts[:30]
        ],
        "",
        "## Review Queue Sample",
        "",
        "| Archetype | Workflow | AI nodes | Risk signals | Sensitivity | Sources |",
        "|---|---|---:|---|---|---:|",
    ]
    for candidate in top_candidates:
        lines.append(
            "| "
            f"`{candidate.suggested_archetype}` | "
            f"{_escape_table(candidate.workflow_name)} | "
            f"{candidate.ai_node_count} | "
            f"{_join_or_dash(candidate.risky_action_signals)} | "
            f"{_join_or_dash(candidate.data_sensitivity_signals)} | "
            f"{len(candidate.source_locators)} |"
        )
    lines.extend(
        [
            "",
            "## Next Review Step",
            "",
            "1. Cluster candidates by archetype and integration set.",
            "2. Reject unsafe high-autonomy candidates before pattern generation.",
            "3. Ask the frontier model for missed opportunities and risks using",
            "   `docs/prompts/frontier_opportunity_discovery.md`.",
            "4. Convert accepted candidates into draft SMB pattern JSON only after",
            "   human review.",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _join_or_dash(values: list[str]) -> str:
    if not values:
        return "-"
    return ", ".join(f"`{value}`" for value in values[:3])


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _balanced_review_queue(*, result: N8nMiningResult, top: int):
    by_archetype: dict[str, list] = {}
    for candidate in result.candidates:
        by_archetype.setdefault(candidate.suggested_archetype, []).append(candidate)
    selected = []
    per_archetype = max(3, top // max(1, len(by_archetype)))
    for archetype in sorted(by_archetype):
        selected.extend(
            sorted(
                by_archetype[archetype],
                key=lambda item: (
                    -_candidate_priority(item),
                    item.workflow_name.lower(),
                    item.workflow_fingerprint,
                ),
            )[:per_archetype]
        )
    return selected[:top]


def _candidate_priority(candidate) -> int:
    return (
        min(candidate.ai_node_count, 5) * 3
        + len(candidate.human_gate_signals) * 2
        + len(candidate.risky_action_signals)
        + len(candidate.data_sensitivity_signals)
        + min(len(_business_integrations(candidate.integrations)), 5)
    )


def _cluster_counts(result: N8nMiningResult):
    counts = Counter(
        (
            candidate.suggested_archetype,
            _join_or_dash(_business_integrations(candidate.integrations)),
        )
        for candidate in result.candidates
    )
    return counts.most_common()


def _business_integrations(integrations: list[str]) -> list[str]:
    return sorted(
        integration for integration in integrations if integration not in _UTILITY_INTEGRATIONS
    )


if __name__ == "__main__":
    raise SystemExit(main())
