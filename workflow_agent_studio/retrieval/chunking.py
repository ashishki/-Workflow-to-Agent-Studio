"""Heading-aware text chunking for retrieval ingestion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceChunk:
    source_id: str
    chunk_id: str
    heading_path: tuple[str, ...]
    start_char: int
    end_char: int
    text: str


def chunk_source_document(
    *,
    source_id: str,
    text: str,
    max_chars: int = 1200,
) -> list[SourceChunk]:
    chunks: list[SourceChunk] = []
    heading_path: list[str] = []
    position = 0
    paragraph_lines: list[str] = []
    paragraph_start: int | None = None

    def flush_paragraph() -> None:
        nonlocal paragraph_lines, paragraph_start
        if paragraph_start is None:
            return
        paragraph = "\n".join(paragraph_lines).strip()
        if paragraph:
            chunks.extend(
                _split_paragraph(
                    source_id=source_id,
                    chunk_index_start=len(chunks),
                    heading_path=tuple(heading_path),
                    start_char=paragraph_start,
                    text=paragraph,
                    max_chars=max_chars,
                )
            )
        paragraph_lines = []
        paragraph_start = None

    for raw_line in text.splitlines(keepends=True):
        line_without_newline = raw_line.rstrip("\n")
        stripped = line_without_newline.strip()
        line_start = position
        position += len(raw_line)

        if _is_heading(stripped):
            flush_paragraph()
            level, title = _parse_heading(stripped)
            heading_path = heading_path[: level - 1]
            heading_path.append(title)
            continue

        if not stripped:
            flush_paragraph()
            continue

        if paragraph_start is None:
            paragraph_start = line_start
        paragraph_lines.append(line_without_newline.strip())

    flush_paragraph()
    return chunks


def _split_paragraph(
    *,
    source_id: str,
    chunk_index_start: int,
    heading_path: tuple[str, ...],
    start_char: int,
    text: str,
    max_chars: int,
) -> list[SourceChunk]:
    chunks: list[SourceChunk] = []
    offset = 0
    while offset < len(text):
        part = text[offset : offset + max_chars].strip()
        if not part:
            break
        part_start = start_char + offset
        part_end = part_start + len(part)
        chunk_number = chunk_index_start + len(chunks) + 1
        chunks.append(
            SourceChunk(
                source_id=source_id,
                chunk_id=f"{source_id}:chunk-{chunk_number}",
                heading_path=heading_path,
                start_char=part_start,
                end_char=part_end,
                text=part,
            )
        )
        offset += max_chars
    return chunks


def _is_heading(line: str) -> bool:
    return line.startswith("#") and line.lstrip("#").startswith(" ")


def _parse_heading(line: str) -> tuple[int, str]:
    marker, title = line.split(" ", 1)
    return len(marker), title.strip()
