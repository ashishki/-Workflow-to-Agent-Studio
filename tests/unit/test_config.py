from pathlib import Path

from workflow_agent_studio.config import load_settings


def test_load_settings_reads_env_and_defaults() -> None:
    settings = load_settings(
        {
            "WORKFLOW_STUDIO_STORAGE_PATH": "custom.sqlite3",
            "WORKFLOW_STUDIO_INDEX_DIR": "custom-index",
            "WORKFLOW_STUDIO_PATTERN_DIR": "custom-patterns",
            "WORKFLOW_STUDIO_LLM_PROVIDER": "fake-provider",
            "WORKFLOW_STUDIO_LLM_MODEL": "fake-synthesis",
            "WORKFLOW_STUDIO_EXTRACTION_MODEL": "fake-extraction",
            "WORKFLOW_STUDIO_EMBEDDING_MODEL": "fake-embedding",
            "WORKFLOW_STUDIO_LOG_LEVEL": "debug",
        }
    )

    assert settings.storage_path == Path("custom.sqlite3")
    assert settings.index_dir == Path("custom-index")
    assert settings.pattern_dir == Path("custom-patterns")
    assert settings.llm_provider == "fake-provider"
    assert settings.llm_model == "fake-synthesis"
    assert settings.extraction_model == "fake-extraction"
    assert settings.embedding_model == "fake-embedding"
    assert settings.log_level == "DEBUG"

    defaults = load_settings({})
    assert defaults.storage_path == Path(".data/workflow_studio.sqlite3")
    assert defaults.index_dir == Path(".data/index")
    assert defaults.pattern_dir == Path("patterns")
    assert defaults.llm_provider == "openai"
    assert defaults.llm_model == "gpt-5.4"
    assert defaults.extraction_model == "gpt-5.4-mini"
    assert defaults.embedding_model == "text-embedding-3-small"
    assert defaults.log_level == "INFO"
