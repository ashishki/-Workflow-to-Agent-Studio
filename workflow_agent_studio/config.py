"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    storage_path: Path
    index_dir: Path
    pattern_dir: Path
    llm_provider: str
    llm_model: str
    extraction_model: str
    embedding_model: str
    log_level: str


def load_settings(environ: dict[str, str] | None = None) -> Settings:
    env = os.environ if environ is None else environ
    return Settings(
        storage_path=Path(env.get("WORKFLOW_STUDIO_STORAGE_PATH", ".data/workflow_studio.sqlite3")),
        index_dir=Path(env.get("WORKFLOW_STUDIO_INDEX_DIR", ".data/index")),
        pattern_dir=Path(env.get("WORKFLOW_STUDIO_PATTERN_DIR", "patterns")),
        llm_provider=env.get("WORKFLOW_STUDIO_LLM_PROVIDER", "openai"),
        llm_model=env.get("WORKFLOW_STUDIO_LLM_MODEL", "gpt-5.4"),
        extraction_model=env.get("WORKFLOW_STUDIO_EXTRACTION_MODEL", "gpt-5.4-mini"),
        embedding_model=env.get("WORKFLOW_STUDIO_EMBEDDING_MODEL", "text-embedding-3-small"),
        log_level=env.get("WORKFLOW_STUDIO_LOG_LEVEL", "INFO").upper(),
    )
