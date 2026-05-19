"""Pattern-library loading for retrieval ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from workflow_agent_studio.ingestion.normalizer import fingerprint_text, normalize_text
from workflow_agent_studio.ingestion.readers import read_source_path


@dataclass(frozen=True)
class PatternTemplate:
    source_id: str
    corpus_type: Literal["pattern"]
    title: str
    fingerprint: str
    normalized_text: str


def load_pattern_library(pattern_dir: str | Path) -> list[PatternTemplate]:
    directory = Path(pattern_dir)
    templates: list[PatternTemplate] = []
    for path in sorted(directory.glob("*.md")):
        if path.name.casefold() == "readme.md":
            continue
        raw_source = read_source_path(path)
        normalized_text = normalize_text(raw_source.text)
        fingerprint = fingerprint_text(normalized_text)
        templates.append(
            PatternTemplate(
                source_id=f"pattern-{path.stem}",
                corpus_type="pattern",
                title=raw_source.title,
                fingerprint=fingerprint,
                normalized_text=normalized_text,
            )
        )
    return templates
