from pathlib import Path

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.roadmap.service import generate_roadmap_report


def test_demo_roadmap_costs_are_ranges_with_assumptions() -> None:
    for input_path in [
        Path("docs/examples/domains/hair_salon_input.md"),
        Path("docs/examples/domains/ecommerce_input.md"),
        Path("docs/examples/domains/legal_consultancy_input.md"),
    ]:
        report = generate_roadmap_report(input_path)

        assert _single_point_cost_ids(report) == []
        assert all(card.assumptions for card in report.recommendations)
        assert all(
            card.confidence_level in {"low", "medium", "high"} for card in report.recommendations
        )


def test_cost_eval_flags_single_point_estimates() -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")
    payload = report.model_dump(mode="json")
    payload["recommendations"][0]["estimated_cost"].update(
        {
            "one_time_low": 1000,
            "one_time_medium": 1000,
            "one_time_high": 1000,
        }
    )
    edited = RoadmapReport.model_validate(payload)

    assert _single_point_cost_ids(edited) == ["REC-SALON-001"]


def _single_point_cost_ids(report: RoadmapReport) -> list[str]:
    single_point_ids: list[str] = []
    for card in report.recommendations:
        cost = card.estimated_cost
        if cost.one_time_low == cost.one_time_medium == cost.one_time_high:
            single_point_ids.append(card.recommendation_id)
    return single_point_ids
