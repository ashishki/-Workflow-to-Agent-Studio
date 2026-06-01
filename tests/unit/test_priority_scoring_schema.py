import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.scoring import PriorityScore


def _priority_score_data(priority_band: str = "quick_win") -> dict:
    return {
        "scoring_model_version": "scoring-model-v1",
        "business_value": 85,
        "delivery_readiness": 80,
        "risk_penalty": 30,
        "priority_band": priority_band,
        "confidence": "medium",
        "rationale": [
            "High message volume.",
            "Clear FAQ exists.",
            "Moderate privacy risk is controlled by review.",
        ],
        "uncertainty_notes": [
            "Exact monthly volume is estimated.",
            "Refund policy needs final review.",
        ],
    }


def test_priority_score_supports_required_priority_bands() -> None:
    priority_bands = {
        "quick_win",
        "strategic_pilot",
        "prepare_first",
        "do_not_automate_yet",
        "classic_automation",
        "human_only",
    }

    scores = [
        PriorityScore.model_validate(_priority_score_data(priority_band=priority_band))
        for priority_band in priority_bands
    ]

    assert {score.priority_band for score in scores} == priority_bands


def test_priority_score_records_score_components_and_confidence() -> None:
    score = PriorityScore.model_validate(_priority_score_data())

    assert score.schema_version == "priority-score-v1"
    assert score.scoring_model_version == "scoring-model-v1"
    assert score.business_value == 85
    assert score.delivery_readiness == 80
    assert score.risk_penalty == 30
    assert score.confidence == "medium"
    assert score.rationale
    assert score.uncertainty_notes


def test_priority_score_requires_rationale() -> None:
    data = _priority_score_data()
    data["rationale"] = []

    with pytest.raises(ValidationError, match="rationale"):
        PriorityScore.model_validate(data)


def test_priority_score_requires_uncertainty_notes() -> None:
    data = _priority_score_data()
    data["uncertainty_notes"] = []

    with pytest.raises(ValidationError, match="uncertainty_notes"):
        PriorityScore.model_validate(data)


def test_priority_score_rejects_invalid_priority_band() -> None:
    data = _priority_score_data(priority_band="medium_priority")

    with pytest.raises(ValidationError, match="priority_band"):
        PriorityScore.model_validate(data)
