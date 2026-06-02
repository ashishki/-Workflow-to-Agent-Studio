"""n8n workflow mining helpers for public-template pattern research."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel

_AI_INTEGRATION_MARKERS = (
    "openai",
    "anthropic",
    "langchain",
    "lmchat",
    "agent",
    "embeddings",
    "vectorstore",
)
_TRIGGER_MARKERS = ("trigger", "webhook", "cron", "schedule", "manual")
_REVIEW_INTEGRATIONS = {"slack", "telegram", "gmail", "email", "discord", "microsoftteams"}
_RISKY_OPERATION_MARKERS = (
    "send",
    "post",
    "create",
    "update",
    "delete",
    "refund",
    "charge",
    "publish",
    "message",
)
_SENSITIVE_INTEGRATIONS = {
    "gmail": "personal_or_customer_messages",
    "email": "personal_or_customer_messages",
    "hubspot": "crm_or_lead_data",
    "salesforce": "crm_or_lead_data",
    "pipedrive": "crm_or_lead_data",
    "stripe": "payment_or_financial_data",
    "quickbooks": "payment_or_financial_data",
    "xero": "payment_or_financial_data",
    "googlesheets": "spreadsheet_business_data",
    "notion": "workspace_or_internal_notes",
    "slack": "internal_messages",
    "telegram": "personal_or_customer_messages",
}


class N8nNodeSignal(StrictModel):
    """Normalized signal extracted from an n8n node."""

    name: str
    node_type: str
    integration: str
    operation: str | None = None
    resource: str | None = None
    is_trigger: bool = False
    is_ai_node: bool = False


class N8nPatternCandidate(StrictModel):
    """Deduplicated pattern candidate derived from a public n8n workflow."""

    source_locator: str = Field(min_length=1)
    source_locators: list[str] = Field(default_factory=list)
    workflow_name: str
    workflow_fingerprint: str = Field(min_length=12)
    integrations: list[str]
    trigger_integrations: list[str]
    action_integrations: list[str]
    node_types: list[str]
    ai_node_count: int
    human_gate_signals: list[str]
    risky_action_signals: list[str]
    data_sensitivity_signals: list[str]
    suggested_archetype: str
    review_required: bool = True


def load_n8n_workflow(
    path: str | Path,
    *,
    source_locator: str | None = None,
) -> N8nPatternCandidate:
    """Load one n8n workflow JSON file and return a normalized candidate."""

    workflow_path = Path(path)
    data = json.loads(workflow_path.read_text(encoding="utf-8"))
    return extract_n8n_pattern_candidate(
        data,
        source_locator=source_locator or str(workflow_path),
    )


def extract_n8n_pattern_candidate(
    workflow: dict[str, Any],
    *,
    source_locator: str,
) -> N8nPatternCandidate:
    """Extract product-pattern signals from an n8n workflow object."""

    node_signals = [_node_signal(node) for node in workflow.get("nodes", [])]
    node_signals = [signal for signal in node_signals if signal is not None]
    integrations = _unique_sorted(signal.integration for signal in node_signals)
    trigger_integrations = _unique_sorted(
        signal.integration for signal in node_signals if signal.is_trigger
    )
    action_integrations = _unique_sorted(
        signal.integration for signal in node_signals if not signal.is_trigger
    )
    node_types = _unique_sorted(signal.node_type for signal in node_signals)
    human_gate_signals = _human_gate_signals(node_signals)
    risky_action_signals = _risky_action_signals(node_signals)
    data_sensitivity_signals = _data_sensitivity_signals(integrations)
    fingerprint = _workflow_fingerprint(
        node_signals=node_signals,
        connections=workflow.get("connections", {}),
    )
    source_locators = [source_locator]
    return N8nPatternCandidate(
        source_locator=source_locator,
        source_locators=source_locators,
        workflow_name=str(workflow.get("name") or "Untitled n8n workflow"),
        workflow_fingerprint=fingerprint,
        integrations=integrations,
        trigger_integrations=trigger_integrations,
        action_integrations=action_integrations,
        node_types=node_types,
        ai_node_count=sum(1 for signal in node_signals if signal.is_ai_node),
        human_gate_signals=human_gate_signals,
        risky_action_signals=risky_action_signals,
        data_sensitivity_signals=data_sensitivity_signals,
        suggested_archetype=_suggest_archetype(
            integrations=integrations,
            node_signals=node_signals,
        ),
    )


def dedupe_n8n_candidates(candidates: Iterable[N8nPatternCandidate]) -> list[N8nPatternCandidate]:
    """Collapse duplicate workflow candidates by stable fingerprint."""

    by_fingerprint: dict[str, N8nPatternCandidate] = {}
    for candidate in candidates:
        existing = by_fingerprint.get(candidate.workflow_fingerprint)
        if existing is None:
            by_fingerprint[candidate.workflow_fingerprint] = candidate
            continue
        source_locators = _unique_sorted(
            [*existing.source_locators, candidate.source_locator, *candidate.source_locators]
        )
        by_fingerprint[candidate.workflow_fingerprint] = existing.model_copy(
            update={"source_locators": source_locators}
        )
    return sorted(by_fingerprint.values(), key=lambda item: item.workflow_fingerprint)


def _node_signal(node: dict[str, Any]) -> N8nNodeSignal | None:
    node_type = str(node.get("type") or "").strip()
    name = str(node.get("name") or node_type or "unnamed").strip()
    if not node_type:
        return None
    integration = _integration_from_type(node_type)
    parameters = node.get("parameters") if isinstance(node.get("parameters"), dict) else {}
    operation = _string_or_none(parameters.get("operation"))
    resource = _string_or_none(parameters.get("resource"))
    lowered = " ".join(
        item.lower()
        for item in (node_type, name, integration, operation or "", resource or "")
        if item
    )
    return N8nNodeSignal(
        name=name,
        node_type=node_type,
        integration=integration,
        operation=operation,
        resource=resource,
        is_trigger=any(marker in lowered for marker in _TRIGGER_MARKERS),
        is_ai_node=any(marker in lowered for marker in _AI_INTEGRATION_MARKERS),
    )


def _integration_from_type(node_type: str) -> str:
    integration = node_type.rsplit(".", maxsplit=1)[-1]
    integration = integration.removesuffix("Trigger")
    return integration.replace("-", "").replace("_", "").lower()


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _human_gate_signals(node_signals: list[N8nNodeSignal]) -> list[str]:
    signals: list[str] = []
    integrations = {signal.integration for signal in node_signals}
    node_text = " ".join(
        f"{signal.name} {signal.node_type} {signal.operation or ''}".lower()
        for signal in node_signals
    )
    if integrations & _REVIEW_INTEGRATIONS:
        signals.append("messaging_or_email_review_channel_present")
    if "wait" in integrations or "approval" in node_text or "review" in node_text:
        signals.append("explicit_wait_or_approval_signal")
    return _unique_sorted(signals)


def _risky_action_signals(node_signals: list[N8nNodeSignal]) -> list[str]:
    signals: list[str] = []
    for signal in node_signals:
        action_text = " ".join(
            item.lower()
            for item in (
                signal.integration,
                signal.operation or "",
                signal.resource or "",
                signal.name,
            )
        )
        if signal.is_trigger:
            continue
        if any(marker in action_text for marker in _RISKY_OPERATION_MARKERS):
            signals.append(f"{signal.integration}:{signal.operation or 'action'}")
    return _unique_sorted(signals)


def _data_sensitivity_signals(integrations: list[str]) -> list[str]:
    return _unique_sorted(
        sensitivity
        for integration, sensitivity in _SENSITIVE_INTEGRATIONS.items()
        if integration in integrations
    )


def _suggest_archetype(*, integrations: list[str], node_signals: list[N8nNodeSignal]) -> str:
    integration_set = set(integrations)
    if {"hubspot", "salesforce", "pipedrive"} & integration_set:
        return "crm_lead_enrichment_or_routing"
    if {"zendesk", "intercom", "freshdesk"} & integration_set:
        return "customer_support_triage"
    if {"gmail", "email"} & integration_set and any(signal.is_ai_node for signal in node_signals):
        return "ai_email_assistant"
    if {"slack", "telegram", "discord"} & integration_set:
        return "internal_notification_or_approval_workflow"
    if {"googlesheets", "airtable", "notion"} & integration_set:
        return "backoffice_data_sync_or_reporting"
    if any(signal.is_ai_node for signal in node_signals):
        return "ai_assisted_workflow"
    return "automation_workflow_candidate"


def _workflow_fingerprint(
    *,
    node_signals: list[N8nNodeSignal],
    connections: dict[str, Any],
) -> str:
    canonical_nodes = sorted(
        (
            signal.node_type,
            signal.integration,
            signal.operation or "",
            signal.resource or "",
            signal.is_trigger,
        )
        for signal in node_signals
    )
    canonical_edges = _canonical_edges(connections)
    payload = json.dumps(
        {"edges": canonical_edges, "nodes": canonical_nodes},
        ensure_ascii=True,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _canonical_edges(connections: dict[str, Any]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for source_name, source_connections in connections.items():
        if not isinstance(source_connections, dict):
            continue
        for output_group in source_connections.values():
            if not isinstance(output_group, list):
                continue
            for connection_group in output_group:
                if not isinstance(connection_group, list):
                    continue
                for connection in connection_group:
                    if isinstance(connection, dict) and connection.get("node"):
                        edges.append((str(source_name), str(connection["node"])))
    return sorted(edges)


def _unique_sorted(values: Iterable[str]) -> list[str]:
    return sorted({value for value in values if value})
