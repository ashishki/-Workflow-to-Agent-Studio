from workflow_agent_studio.domain.frontier import (
    FrontierDiscoveryResult,
    FrontierOpportunityCandidate,
)
from workflow_agent_studio.domain.recommendation import HumanGate
from workflow_agent_studio.roadmap.frontier import (
    verify_frontier_candidate,
    verify_frontier_discovery_result,
)


def test_frontier_candidate_is_never_exportable_without_human_review() -> None:
    candidate = _valid_candidate()

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert verification.status == "needs_human_review"
    assert not verification.exportable_as_recommendation
    assert verification.findings == []


def test_frontier_candidate_requires_evidence_or_assumptions() -> None:
    candidate = _valid_candidate().model_copy(
        update={"critical_assumptions": [], "evidence_refs": []}
    )

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert verification.status == "rejected"
    assert _finding_ids(verification) == ["frontier_evidence_or_assumption_required"]


def test_frontier_candidate_requires_human_gate() -> None:
    candidate = _valid_candidate().model_copy(
        update={
            "human_gate": HumanGate(
                required=False,
                reviewer="ops owner",
                approval_event="none",
                rationale="model suggestion only",
            )
        }
    )

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert "frontier_human_gate_required" in _finding_ids(verification)


def test_frontier_candidate_cannot_weaken_privacy_class() -> None:
    candidate = _valid_candidate().model_copy(update={"privacy_class": "public"})

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert "frontier_privacy_class_weaker_than_source" in _finding_ids(verification)


def test_frontier_high_autonomy_candidate_is_blocked() -> None:
    candidate = _valid_candidate().model_copy(
        update={"candidate_solution_type": "high_autonomy_agent_future_only"}
    )

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert "frontier_high_autonomy_not_exportable" in _finding_ids(verification)


def test_frontier_do_not_automate_text_does_not_trigger_high_impact_block() -> None:
    candidate = _valid_candidate().model_copy(
        update={
            "title": "Claim verification research assistant",
            "workflow_step": "Evidence checking after initial triage brief",
            "do_not_automate": [
                "Removing an applicant from the pipeline based on verification results"
            ],
            "reject_if": ["Reviewer cannot validate outputs before they reach the brief"],
        }
    )

    verification = verify_frontier_candidate(
        candidate=candidate,
        detected_privacy_class="sensitive",
    )

    assert verification.status == "needs_human_review"
    assert "frontier_high_impact_decision_boundary" not in _finding_ids(verification)


def test_frontier_discovery_verification_counts_blocking_findings() -> None:
    result = FrontierDiscoveryResult(
        candidates=[
            _valid_candidate(),
            _valid_candidate().model_copy(
                update={
                    "opportunity_id": "FOC-002",
                    "candidate_solution_type": "high_autonomy_agent_future_only",
                }
            ),
        ],
        rejected_candidate_titles=["Autonomous reject bot"],
    )

    verification = verify_frontier_discovery_result(
        result=result,
        detected_privacy_class="sensitive",
    )

    assert len(verification.candidate_reviews) == 2
    assert verification.blocking_finding_count == 1
    assert all(not item.exportable_as_recommendation for item in verification.candidate_reviews)


def _valid_candidate() -> FrontierOpportunityCandidate:
    return FrontierOpportunityCandidate(
        opportunity_id="FOC-001",
        title="Human-reviewed application triage assistant",
        workflow_step="Application intake and first-pass review",
        candidate_solution_type="human_in_the_loop_workflow",
        why_it_may_help=["Repeated review work can be summarized before human review."],
        why_it_may_not_help=["Low application volume may not justify integration work."],
        required_data=["application fields", "reviewer feedback"],
        evidence_refs=["n8n_cluster:crm_lead_enrichment_or_routing"],
        human_gate=HumanGate(
            required=True,
            reviewer="senior reviewer",
            approval_event="reviewer accepts or rejects draft recommendation",
            rationale="admission decisions remain human-owned",
        ),
        do_not_automate=["final accept or reject decision"],
        critical_assumptions=["historical applications are available for shadow review"],
        privacy_class="sensitive",
        privacy_notes=["founder personal data requires approved handling"],
        cost_drivers=["CRM integration", "research depth per applicant"],
        eval_cases=["suspicious traction claim", "strong founder with weak market"],
        confidence="medium",
        reject_if=["no reviewer can validate outputs"],
    )


def _finding_ids(verification) -> list[str]:
    return [finding.rule_id for finding in verification.findings]
