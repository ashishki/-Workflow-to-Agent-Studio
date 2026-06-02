import json

from workflow_agent_studio.patterns.n8n import (
    dedupe_n8n_candidates,
    extract_n8n_pattern_candidate,
)


def test_extract_n8n_pattern_candidate_normalizes_workflow_signals() -> None:
    candidate = extract_n8n_pattern_candidate(
        _lead_routing_workflow(),
        source_locator="github://example/repo/workflows/lead.json",
    )

    assert candidate.review_required
    assert candidate.workflow_name == "Inbound lead routing"
    assert candidate.integrations == ["hubspot", "openai", "slack", "webhook"]
    assert candidate.trigger_integrations == ["webhook"]
    assert candidate.action_integrations == ["hubspot", "openai", "slack"]
    assert candidate.ai_node_count == 1
    assert candidate.suggested_archetype == "crm_lead_enrichment_or_routing"
    assert "messaging_or_email_review_channel_present" in candidate.human_gate_signals
    assert "crm_or_lead_data" in candidate.data_sensitivity_signals
    assert "internal_messages" in candidate.data_sensitivity_signals
    assert "hubspot:create" in candidate.risky_action_signals
    assert "slack:post" in candidate.risky_action_signals
    assert len(candidate.workflow_fingerprint) == 16


def test_n8n_fingerprint_is_stable_when_node_order_changes() -> None:
    workflow = _lead_routing_workflow()
    reordered = {
        **workflow,
        "nodes": list(reversed(workflow["nodes"])),
    }

    first = extract_n8n_pattern_candidate(workflow, source_locator="source-a")
    second = extract_n8n_pattern_candidate(reordered, source_locator="source-b")

    assert first.workflow_fingerprint == second.workflow_fingerprint


def test_dedupe_n8n_candidates_preserves_source_locators() -> None:
    first = extract_n8n_pattern_candidate(_lead_routing_workflow(), source_locator="source-a")
    duplicate = extract_n8n_pattern_candidate(_lead_routing_workflow(), source_locator="source-b")
    different = extract_n8n_pattern_candidate(
        _email_summary_workflow(),
        source_locator="source-c",
    )

    deduped = dedupe_n8n_candidates([first, duplicate, different])

    assert len(deduped) == 2
    duplicate_group = [
        candidate
        for candidate in deduped
        if candidate.workflow_fingerprint == first.workflow_fingerprint
    ][0]
    assert duplicate_group.source_locators == ["source-a", "source-b"]


def test_extract_n8n_pattern_candidate_accepts_plain_json_payloads() -> None:
    payload = json.loads(json.dumps(_email_summary_workflow()))

    candidate = extract_n8n_pattern_candidate(payload, source_locator="source-json")

    assert candidate.suggested_archetype == "ai_email_assistant"
    assert candidate.ai_node_count == 1
    assert "personal_or_customer_messages" in candidate.data_sensitivity_signals


def _lead_routing_workflow() -> dict:
    return {
        "name": "Inbound lead routing",
        "nodes": [
            {
                "name": "New lead webhook",
                "type": "n8n-nodes-base.webhook",
                "parameters": {},
            },
            {
                "name": "Summarize lead",
                "type": "@n8n/n8n-nodes-langchain.openAi",
                "parameters": {"operation": "chat"},
            },
            {
                "name": "Create HubSpot contact",
                "type": "n8n-nodes-base.hubspot",
                "parameters": {"resource": "contact", "operation": "create"},
            },
            {
                "name": "Post review note",
                "type": "n8n-nodes-base.slack",
                "parameters": {"resource": "message", "operation": "post"},
            },
        ],
        "connections": {
            "New lead webhook": {"main": [[{"node": "Summarize lead"}]]},
            "Summarize lead": {"main": [[{"node": "Create HubSpot contact"}]]},
            "Create HubSpot contact": {"main": [[{"node": "Post review note"}]]},
        },
    }


def _email_summary_workflow() -> dict:
    return {
        "name": "Email summary",
        "nodes": [
            {
                "name": "New email",
                "type": "n8n-nodes-base.gmailTrigger",
                "parameters": {},
            },
            {
                "name": "Draft answer",
                "type": "n8n-nodes-base.openAi",
                "parameters": {"operation": "chat"},
            },
            {
                "name": "Send draft",
                "type": "n8n-nodes-base.gmail",
                "parameters": {"resource": "message", "operation": "send"},
            },
        ],
        "connections": {
            "New email": {"main": [[{"node": "Draft answer"}]]},
            "Draft answer": {"main": [[{"node": "Send draft"}]]},
        },
    }
