"""Source ingestion package."""

from workflow_agent_studio.ingestion.connectors import (
    ConnectorCredentialError,
    ConnectorImportError,
    ConnectorSource,
    ReadOnlyConnector,
    require_connector_token,
)
from workflow_agent_studio.ingestion.normalizer import (
    fingerprint_text,
    normalize_text,
    normalize_transcript_text,
)
from workflow_agent_studio.ingestion.readers import UnsupportedSourceType
from workflow_agent_studio.ingestion.service import (
    IngestionResult,
    ingest_connector_sources,
    ingest_source_paths,
)

__all__ = [
    "ConnectorCredentialError",
    "ConnectorImportError",
    "ConnectorSource",
    "IngestionResult",
    "ReadOnlyConnector",
    "UnsupportedSourceType",
    "fingerprint_text",
    "ingest_connector_sources",
    "ingest_source_paths",
    "normalize_text",
    "normalize_transcript_text",
    "require_connector_token",
]
