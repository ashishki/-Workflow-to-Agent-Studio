"""Source ingestion package."""

from workflow_agent_studio.ingestion.normalizer import (
    fingerprint_text,
    normalize_text,
    normalize_transcript_text,
)
from workflow_agent_studio.ingestion.readers import UnsupportedSourceType
from workflow_agent_studio.ingestion.service import IngestionResult, ingest_source_paths

__all__ = [
    "IngestionResult",
    "UnsupportedSourceType",
    "fingerprint_text",
    "ingest_source_paths",
    "normalize_text",
    "normalize_transcript_text",
]
