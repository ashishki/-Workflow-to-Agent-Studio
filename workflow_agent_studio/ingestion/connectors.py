"""Read-only connector import contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from workflow_agent_studio.config import get_connector_token
from workflow_agent_studio.ingestion.readers import SourceType


class ConnectorImportError(RuntimeError):
    """Raised when a connector cannot fetch source records."""


class ConnectorCredentialError(ConnectorImportError):
    """Raised when a connector credential is not available from the environment."""


@dataclass(frozen=True)
class ConnectorSource:
    connector_id: str
    external_id: str
    source_type: SourceType
    title: str
    text: str
    metadata: dict[str, object] = field(default_factory=dict)

    def source_metadata(self) -> dict[str, object]:
        return {
            "origin": "connector",
            "connector_id": self.connector_id,
            "external_id": self.external_id,
            "read_only": True,
            **self.metadata,
        }


class ReadOnlyConnector(Protocol):
    connector_id: str

    def fetch_sources(self) -> list[ConnectorSource]:
        """Return source records without mutating the upstream system."""


def require_connector_token(
    connector_id: str,
    environ: dict[str, str] | None = None,
) -> str:
    token = get_connector_token(connector_id, environ)
    if token is None:
        raise ConnectorCredentialError(
            f"Missing environment-backed credential for connector '{connector_id}'"
        )
    return token
