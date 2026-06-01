import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.roadmap import RoadmapReport

FIXTURE_PATH = Path("tests/fixtures/roadmaps/minimal_valid_roadmap.json")


def _roadmap_data() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def test_minimal_valid_roadmap_report_fixture_round_trips() -> None:
    report = RoadmapReport.model_validate(_roadmap_data())
    dumped = report.model_dump(mode="json")
    reparsed = RoadmapReport.model_validate(dumped)

    assert report.schema_version == "roadmap-report-v1"
    assert reparsed == report
    assert report.executive_summary.company_context
    assert report.evidence_packet.source_documents[0].source_hash == "sha256:source-001"
    assert report.workflow_map[0].workflow_name == "Support triage"
    assert report.process_inventory[0].recommended_solution_type == "llm_assistant"
    assert report.recommendations[0].recommendation_id == "REC-001"
    assert report.rollout_plan.stages
    assert report.evaluation_plan.stop_conditions
    assert report.governance_plan.owner == "Support lead"
    assert report.verification_appendix.receipt.blocking_finding_count == 0


@pytest.mark.parametrize(
    "field",
    [
        "executive_summary",
        "evidence_packet",
        "workflow_map",
        "process_inventory",
        "rollout_plan",
        "evaluation_plan",
        "governance_plan",
        "verification_appendix",
    ],
)
def test_roadmap_report_requires_core_sections(field: str) -> None:
    data = _roadmap_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RoadmapReport.model_validate(data)


def test_roadmap_report_blocks_empty_recommendations_without_stop_rationale() -> None:
    data = _roadmap_data()
    data["recommendations"] = []
    data["do_not_automate_rationale"] = []

    with pytest.raises(ValidationError, match="recommendations or do-not-automate"):
        RoadmapReport.model_validate(data)


def test_roadmap_report_allows_empty_recommendations_with_stop_rationale() -> None:
    data = _roadmap_data()
    data["recommendations"] = []
    data["do_not_automate_rationale"] = ["Evidence is insufficient for automation."]
    data["executive_summary"]["top_recommended_initiatives"] = []

    report = RoadmapReport.model_validate(data)

    assert report.recommendations == []
    assert report.do_not_automate_rationale == ["Evidence is insufficient for automation."]
