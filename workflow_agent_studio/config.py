"""Environment-backed application settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# These are environment-variable name fragments, never credential values.
CONNECTOR_TOKEN_PREFIX = "WORKFLOW_STUDIO_CONNECTOR_"  # nosec B105
CONNECTOR_TOKEN_SUFFIX = "_TOKEN"  # nosec B105


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
    retrieval_min_score: float
    retrieval_top_k: int
    connector_token_env_vars: tuple[str, ...]


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
        retrieval_min_score=float(env.get("WORKFLOW_STUDIO_RETRIEVAL_MIN_SCORE", "0.1")),
        retrieval_top_k=int(env.get("WORKFLOW_STUDIO_RETRIEVAL_TOP_K", "3")),
        connector_token_env_vars=tuple(sorted(_connector_token_env_vars(env))),
    )


def connector_token_env_var(connector_id: str) -> str:
    normalized = connector_id.upper().replace("-", "_")
    return f"{CONNECTOR_TOKEN_PREFIX}{normalized}{CONNECTOR_TOKEN_SUFFIX}"


def get_connector_token(
    connector_id: str,
    environ: dict[str, str] | None = None,
) -> str | None:
    env = os.environ if environ is None else environ
    return env.get(connector_token_env_var(connector_id))


def _connector_token_env_vars(environ: dict[str, str]) -> list[str]:
    return [
        key
        for key in environ
        if key.startswith(CONNECTOR_TOKEN_PREFIX) and key.endswith(CONNECTOR_TOKEN_SUFFIX)
    ]
