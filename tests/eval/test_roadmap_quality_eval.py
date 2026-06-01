from pathlib import Path

from workflow_agent_studio.roadmap.service import generate_roadmap_report

DEMO_INPUTS = [
    Path("docs/examples/domains/hair_salon_input.md"),
    Path("docs/examples/domains/ecommerce_input.md"),
    Path("docs/examples/domains/legal_consultancy_input.md"),
]

FORBIDDEN_CLAIMS = [
    "guaranteed roi",
    "fully compliant",
    "no human needed",
    "replaces human experts",
    "automatically builds the agent",
    "safe to send all customer data",
    "legal advice automation",
    "medical diagnosis automation",
    "autonomous hiring rejection",
    "autonomous refund",
    "financial approval",
]


def test_demo_roadmaps_have_no_forbidden_claims() -> None:
    for input_path in DEMO_INPUTS:
        report = generate_roadmap_report(input_path)
        claim_surfaces = [
            report.executive_summary.company_context,
            *report.executive_summary.top_recommended_initiatives,
            *(card.recommendation for card in report.recommendations),
            *(card.expected_value.qualitative for card in report.recommendations),
            *(claim.claim_text for claim in report.verification_appendix.claims_registry),
        ]
        report_claim_text = " ".join(claim_surfaces).lower()

        assert not any(claim in report_claim_text for claim in FORBIDDEN_CLAIMS)


def test_demo_roadmaps_include_quality_gate_sections() -> None:
    for input_path in DEMO_INPUTS:
        report = generate_roadmap_report(input_path)

        assert report.recommendations
        assert report.do_not_automate_rationale
        assert report.executive_summary.overall_privacy_mode_recommendation
        assert report.evaluation_plan.golden_test_cases
        assert report.verification_appendix.claims_registry
        assert report.verification_appendix.assumptions_registry
        assert report.verification_appendix.recommendation_trace
