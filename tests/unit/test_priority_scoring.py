import pytest

from workflow_agent_studio.scoring.priority import compute_priority_score


def test_high_value_high_readiness_low_risk_maps_to_quick_win() -> None:
    score = compute_priority_score(
        business_value=90,
        delivery_readiness=85,
        risk_penalty=25,
        evaluation_clarity=80,
        solution_type="llm_assistant",
        confidence="high",
        uncertainty_notes=["Exact monthly volume should be confirmed."],
    )

    assert score.priority_band == "quick_win"
    assert score.confidence == "high"
    assert score.rationale
    assert score.uncertainty_notes


def test_high_privacy_risk_and_low_eval_clarity_blocks_or_prepares_first() -> None:
    score = compute_priority_score(
        business_value=85,
        delivery_readiness=60,
        risk_penalty=90,
        evaluation_clarity=30,
        solution_type="rag_knowledge_assistant",
        confidence="low",
        uncertainty_notes=["Restricted data path and eval set are unresolved."],
    )

    assert score.priority_band == "do_not_automate_yet"


def test_deterministic_reminder_maps_to_classic_automation() -> None:
    score = compute_priority_score(
        business_value=70,
        delivery_readiness=80,
        risk_penalty=20,
        evaluation_clarity=85,
        solution_type="classic_script",
        confidence="medium",
        uncertainty_notes=["Calendar API access still needs confirmation."],
    )

    assert score.priority_band == "classic_automation"


def test_priority_score_requires_uncertainty_notes() -> None:
    with pytest.raises(ValueError, match="uncertainty notes"):
        compute_priority_score(
            business_value=90,
            delivery_readiness=85,
            risk_penalty=25,
            evaluation_clarity=80,
            solution_type="llm_assistant",
            confidence="high",
            uncertainty_notes=[],
        )
