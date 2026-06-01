from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.roadmap.review import build_roadmap_reviewer_output
from workflow_agent_studio.roadmap.service import generate_roadmap_report


def test_roadmap_reviewer_output_includes_required_checklist_fields() -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")

    review = build_roadmap_reviewer_output(
        report,
        reviewer_label="operator",
        approve=True,
    )

    item = review.recommendation_reviews[0]
    assert review.review_status == "approved"
    assert item.accepted
    assert item.reason
    assert item.missing_evidence == []
    assert item.cost_realism == "medium"
    assert item.privacy_concern
    assert item.would_show_to_client
    assert item.required_changes == []


def test_roadmap_reviewer_output_blocks_unresolved_findings() -> None:
    report = generate_roadmap_report("docs/examples/domains/hair_salon_input.md")
    payload = report.model_dump(mode="json")
    payload["verification_appendix"]["receipt"]["blocking_finding_count"] = 1
    blocked_report = RoadmapReport.model_validate(payload)

    review = build_roadmap_reviewer_output(
        blocked_report,
        reviewer_label="operator",
        approve=True,
    )

    assert review.review_status == "blocked"
    assert any(
        finding.rule_id == "ROADMAP-REVIEW-BLOCKING-FINDINGS"
        for finding in review.blocking_findings
    )
