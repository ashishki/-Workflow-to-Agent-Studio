from pathlib import Path

import pytest

from workflow_agent_studio.export import ExportPathError, resolve_export_path


def test_export_rejects_paths_outside_export_directory(tmp_path) -> None:
    export_dir = tmp_path / "exports"
    export_dir.mkdir()

    with pytest.raises(ExportPathError, match="inside the selected export directory"):
        resolve_export_path(export_dir=export_dir, output_path=Path("../outside.md"))


def test_export_accepts_relative_path_inside_export_directory(tmp_path) -> None:
    export_dir = tmp_path / "exports"
    export_dir.mkdir()

    resolved = resolve_export_path(
        export_dir=export_dir,
        output_path=Path("nested/blueprint.md"),
    )

    assert resolved == (export_dir / "nested" / "blueprint.md").resolve()
