from pathlib import Path

from workflow_agent_studio.roadmap.service import generate_roadmap_report


def test_every_recommendation_has_evidence_or_assumptions() -> None:
    for input_path in [
        Path("docs/examples/domains/hair_salon_input.md"),
        Path("docs/examples/domains/ecommerce_input.md"),
        Path("docs/examples/domains/legal_consultancy_input.md"),
    ]:
        report = generate_roadmap_report(input_path)

        for card in report.recommendations:
            assert card.evidence or card.assumptions
            assert card.target_workflow_step
            assert card.required_data
            assert card.fallback_option
            assert card.human_gate.required


def test_recommendation_trace_records_model_versions() -> None:
    report = generate_roadmap_report("docs/examples/domains/legal_consultancy_input.md")
    trace = report.verification_appendix.recommendation_trace[0]

    assert trace.recommendation_id == report.recommendations[0].recommendation_id
    assert trace.matched_pattern_id.startswith("legal_checklist:")
    assert trace.cost_model_version == "cost-engine-baseline-v1"
    assert trace.scoring_model_version == "priority-scoring-engine-v1"
    assert trace.privacy_model_version == "privacy-classification-v1"
    assert trace.supporting_claims
