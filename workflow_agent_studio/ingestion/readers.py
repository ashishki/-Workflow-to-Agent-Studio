"""Local source readers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

SourceType = Literal["text", "markdown"]


@dataclass(frozen=True)
class RawSource:
    path: Path
    source_type: SourceType
    title: str
    text: str


def read_source_path(path: str | Path) -> RawSource:
    source_path = Path(path)
    text = source_path.read_text(encoding="utf-8")
    source_type: SourceType = (
        "markdown" if source_path.suffix.lower() in {".md", ".markdown"} else "text"
    )
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
