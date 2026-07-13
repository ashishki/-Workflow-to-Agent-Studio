#!/usr/bin/env python3
"""Run optional Anthropic frontier opportunity discovery against mined n8n metadata."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from json import JSONDecodeError
from pathlib import Path

from pydantic import ValidationError

from workflow_agent_studio.domain.frontier import FrontierDiscoveryResult
from workflow_agent_studio.roadmap.frontier import verify_frontier_discovery_result

ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-opus-4-6"
PROMPT_VERSION = "frontier-opportunity-discovery-v1"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mining-summary",
        default="docs/experiments/n8n_template_mining_summary.md",
        help="Public n8n metadata summary to send as context.",
    )
    parser.add_argument(
        "--workflow-context",
        default="docs/demo/ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md",
        help="Workflow/customer context file to send as context.",
    )
    parser.add_argument(
        "--output",
        default=".data/frontier/frontier_opportunity_candidates.json",
        help="Output JSON path for model candidates and verifier result.",
    )
    parser.add_argument(
        "--detected-privacy-class",
        default="sensitive",
        choices=["public", "internal", "confidential", "sensitive", "restricted"],
        help="Deterministic privacy class used by the verifier.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Anthropic model ID. Defaults to ANTHROPIC_MODEL or claude-opus-4-6.",
    )
    parser.add_argument("--max-tokens", type=int, default=4000)
    parser.add_argument(
        "--env-check",
        action="store_true",
        help="Print API key/model availability without calling the provider.",
    )
    return parser


def main() -> int:
    _load_dotenv(Path(".env"))
    args = build_parser().parse_args()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = args.model or os.getenv("ANTHROPIC_MODEL") or DEFAULT_MODEL
    if args.env_check:
        print(
            json.dumps(
                {
                    "anthropic_api_key": "present" if api_key else "missing",
                    "model": model,
                },
                sort_keys=True,
            )
        )
        return 0
    if not api_key:
        print(
            json.dumps(
                {
                    "error": "ANTHROPIC_API_KEY missing",
                    "hint": "export ANTHROPIC_API_KEY=... or put it in .env",
                },
                sort_keys=True,
            )
        )
        return 2
    prompt = _build_prompt(
        mining_summary=Path(args.mining_summary).read_text(encoding="utf-8"),
        workflow_context=Path(args.workflow_context).read_text(encoding="utf-8"),
    )
    payload = _call_anthropic(
        api_key=api_key,
        model=model,
        prompt=prompt,
        max_tokens=args.max_tokens,
    )
    raw_text = _extract_text_payload(payload)
    try:
        discovery_payload = json.loads(_extract_json_object(raw_text))
    except JSONDecodeError as error:
        raw_output = Path(args.output).with_suffix(".raw.txt")
        raw_output.parent.mkdir(parents=True, exist_ok=True)
        raw_output.write_text(raw_text, encoding="utf-8")
        print(
            json.dumps(
                {
                    "error": "invalid JSON from model",
                    "raw_output": str(raw_output),
                    "json_error": str(error),
                },
                sort_keys=True,
            )
        )
        return 3
    try:
        discovery = FrontierDiscoveryResult.model_validate(discovery_payload)
    except ValidationError as error:
        invalid_output = Path(args.output).with_suffix(".invalid.json")
        invalid_output.parent.mkdir(parents=True, exist_ok=True)
        invalid_output.write_text(
            json.dumps(discovery_payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "error": "model JSON failed schema validation",
                    "invalid_output": str(invalid_output),
                    "validation_error_count": error.error_count(),
                },
                sort_keys=True,
            )
        )
        return 4
    verification = verify_frontier_discovery_result(
        result=discovery,
        detected_privacy_class=args.detected_privacy_class,  # type: ignore[arg-type]
    )
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "model": model,
                "prompt_version": PROMPT_VERSION,
                "discovery": discovery.model_dump(mode="json"),
                "verification": verification.model_dump(mode="json"),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "blocking_findings": verification.blocking_finding_count,
                "candidate_count": len(discovery.candidates),
                "model": model,
                "output": str(output_path),
                "warning_findings": verification.warning_finding_count,
            },
            sort_keys=True,
        )
    )
    return 0


def _build_prompt(*, mining_summary: str, workflow_context: str) -> str:
    contract = Path("docs/prompts/frontier_opportunity_discovery.md").read_text(encoding="utf-8")
    return f"""
{contract}

Return only valid JSON matching `frontier-discovery-result-v1`.
Do not wrap the JSON in Markdown.
Use double-quoted JSON keys and strings only.
Do not include comments, trailing commas, YAML, prose, or Markdown.
Return exactly three candidates.
Keep every list field to at most three strings.
Use confidence values only from: low, medium, high.
Use candidate_solution_type values only from: do_not_automate_yet, classic_script,
api_integration, rpa, llm_assistant, rag_knowledge_assistant,
human_in_the_loop_workflow, bounded_ai_agent, high_autonomy_agent_future_only.
Every candidate must include privacy_class using only: public, internal,
confidential, sensitive, restricted.
Every human_gate object must include: required, reviewer, approval_event, rationale.
model_notes must be an array of strings.
The top-level JSON object must contain:
schema_version, candidates, rejected_candidate_titles, model_notes.

Workflow/customer context:
{workflow_context[:12000]}

Public n8n mining metadata summary:
{mining_summary[:12000]}
""".strip()


def _call_anthropic(
    *,
    api_key: str,
    model: str,
    prompt: str,
    max_tokens: int,
) -> dict:
    body = json.dumps(
        {
            "model": model,
            "max_tokens": max_tokens,
            "system": (
                "You produce strict JSON for unapproved AI roadmap opportunity "
                "candidates. You do not approve recommendations."
            ),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        ANTHROPIC_MESSAGES_URL,
        data=body,
        headers={
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
            "x-api-key": api_key,
        },
        method="POST",
    )
    try:
        # The Request URL is the module-owned, fixed HTTPS Anthropic endpoint;
        # callers cannot supply a file or custom scheme.
        with urllib.request.urlopen(request, timeout=120) as response:  # nosec B310
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Anthropic API error {error.code}: {detail}") from error


def _extract_text_payload(payload: dict) -> str:
    content = payload.get("content", [])
    if not content or not isinstance(content, list):
        raise ValueError("Anthropic response has no content blocks")
    text_parts = [block.get("text", "") for block in content if isinstance(block, dict)]
    return "\n".join(part for part in text_parts if part).strip()


def _extract_json_object(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        stripped = stripped.removeprefix("json").strip()
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return stripped
    return stripped[start : end + 1]


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", maxsplit=1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


if __name__ == "__main__":
    raise SystemExit(main())
