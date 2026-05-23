from workflow_agent_studio.patterns import (
    BLUEPRINT_PROFILES,
    load_vertical_pack,
    load_vertical_packs,
    pack_metadata_for_generation,
    profile_for_workflow_kind,
    profile_for_workflow_signals,
)
from workflow_agent_studio.retrieval import load_pattern_library


def test_pattern_library_loads_markdown_templates() -> None:
    patterns = load_pattern_library("patterns")

    assert {pattern.source_id for pattern in patterns} == {
        "pattern-automation_blueprint",
        "pattern-eval_cases",
    }
    assert {pattern.corpus_type for pattern in patterns} == {"pattern"}
    assert {pattern.title for pattern in patterns} == {
        "Automation Blueprint Pattern",
        "Evaluation Case Pattern",
    }


def test_vertical_pack_contract_loads_deterministically() -> None:
    packs = load_vertical_packs("patterns")

    assert [pack.pack_id for pack in packs] == ["support_intake"]
    pack = packs[0]
    assert pack.schema_version == "vertical_pack:v1"
    assert pack.domain == "Support intake"
    assert pack.source_examples
    assert pack.extraction_hints
    assert "automation_candidates" in pack.required_blueprint_sections
    assert pack.risks
    assert pack.eval_fixtures


def test_vertical_pack_metadata_can_attach_to_generation_attempts() -> None:
    pack = load_vertical_pack("patterns/support_intake_pack.json")

    assert pack_metadata_for_generation(pack) == {
        "pack_id": "support_intake",
        "pack_schema_version": "vertical_pack:v1",
        "pack_domain": "Support intake",
    }


def test_public_workflow_blueprint_profiles_cover_public_corpus() -> None:
    assert set(BLUEPRINT_PROFILES) == {
        "support_intake",
        "issue_triage",
        "kubernetes_issue_triage",
        "bug_triage",
        "incident_response",
        "hvac_lead_intake",
    }
    assert BLUEPRINT_PROFILES["kubernetes_issue_triage"].risk_level == "high"
    assert "Incident.io" in BLUEPRINT_PROFILES["incident_response"].summary
    assert "service-area checks" in BLUEPRINT_PROFILES["hvac_lead_intake"].summary


def test_public_workflow_profile_detection_uses_workflow_signals() -> None:
    assert (
        profile_for_workflow_signals(
            systems=["Kubernetes GitHub Issues"],
            decisions=["Decide which SIG owns the issue"],
        ).kind
        == "kubernetes_issue_triage"
    )
    assert (
        profile_for_workflow_signals(
            systems=["Launchpad bug tracker"],
            decisions=["Decide whether a bug is Confirmed"],
        ).kind
        == "bug_triage"
    )
    assert (
        profile_for_workflow_signals(
            systems=["Incident.io", "PagerDuty"],
            decisions=["Decide whether an alert requires incident declaration"],
        ).kind
        == "incident_response"
    )
    assert (
        profile_for_workflow_signals(
            systems=["Service-area checker", "Dispatch calendar"],
            decisions=["Decide whether the request is urgent or emergency"],
        ).kind
        == "hvac_lead_intake"
    )


def test_public_workflow_profile_can_load_by_kind() -> None:
    assert profile_for_workflow_kind("issue_triage").kind == "issue_triage"
    assert profile_for_workflow_kind("incident_response").risk_level == "high"
    assert profile_for_workflow_kind("hvac_lead_intake").risk_level == "medium"
