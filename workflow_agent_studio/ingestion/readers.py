"""Local source readers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SourceType = Literal["text", "markdown", "transcript"]


@dataclass(frozen=True)
class RawSource:
    path: Path
    source_type: SourceType
    title: str
    text: str


def read_source_path(path: str | Path) -> RawSource:
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    source_type = _source_type_for_path(source_path, text)
    return RawSource(
        path=source_path,
        source_type=source_type,
        title=_title_from_text(source_path, text, source_type),
        text=text,
    )


def _title_from_text(path: Path, text: str, source_type: SourceType) -> str:
    if source_type == "markdown":
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped.removeprefix("# ").strip() or path.stem
    return path.stem


def _source_type_for_path(path: Path, text: str) -> SourceType:
    filename = path.name.lower()
    if filename.endswith((".transcript", ".transcript.txt", ".transcript.md")):
        return "transcript"
    if path.suffix.lower() in {".md", ".markdown"}:
        return "markdown"
    if _looks_like_transcript(text):
        return "transcript"
    return "text"


def _looks_like_transcript(text: str) -> bool:
    non_empty_lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(non_empty_lines) < 2:
        return False
    speaker_lines = [
        line
        for line in non_empty_lines
        if ":" in line and 1 <= len(line.split(":", 1)[0].strip()) <= 80
    ]
    return len(speaker_lines) >= 2 and len(speaker_lines) >= len(non_empty_lines) / 2
