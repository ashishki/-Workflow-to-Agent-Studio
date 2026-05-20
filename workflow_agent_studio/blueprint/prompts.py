"""Versioned prompt registry for extraction and synthesis."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PromptAsset:
    prompt_id: str
    version: str
    template: str


@dataclass(frozen=True)
class PromptVersionRecord:
    attempt_id: str
    prompt_versions: dict[str, str]


WORKFLOW_EXTRACTION_PROMPT = (
    "Extract v1 workflow facts from the supplied source text. Return only schema-valid "
    "structured data with evidence references or explicit missing questions."
)

BLUEPRINT_SYNTHESIS_PROMPT = (
    "Synthesize a v1 automation blueprint from extracted workflow facts and evidence. "
    "Use evidence-backed claims or mark assumptions explicitly."
)

PROMPT_REGISTRY = {
    "workflow_extraction": PromptAsset(
        prompt_id="workflow_extraction",
        version="workflow_extraction:v1",
        template=WORKFLOW_EXTRACTION_PROMPT,
    ),
    "blueprint_synthesis": PromptAsset(
        prompt_id="blueprint_synthesis",
        version="blueprint_synthesis:v1",
        template=BLUEPRINT_SYNTHESIS_PROMPT,
    ),
}


def get_prompt(prompt_id: str) -> PromptAsset:
    return PROMPT_REGISTRY[prompt_id]


def prompt_versions_for_generation(
    *,
    attempt_id: str,
    prompt_ids: tuple[str, ...] = ("workflow_extraction", "blueprint_synthesis"),
) -> PromptVersionRecord:
    return PromptVersionRecord(
        attempt_id=attempt_id,
        prompt_versions={prompt_id: get_prompt(prompt_id).version for prompt_id in prompt_ids},
    )
