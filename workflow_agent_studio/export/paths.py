"""Local export path boundaries."""

from __future__ import annotations

from pathlib import Path


class ExportPathError(ValueError):
    pass


def resolve_export_path(*, export_dir: Path, output_path: Path) -> Path:
    base = export_dir.resolve()
    target = output_path if output_path.is_absolute() else base / output_path
    resolved = target.resolve()
    if resolved != base and base not in resolved.parents:
        raise ExportPathError("export path must stay inside the selected export directory")
    return resolved
