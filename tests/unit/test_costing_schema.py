import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.costing import CostEstimate


def _cost_range(low: int = 100, medium: int = 500, high: int = 1000) -> dict:
    return {"low": low, "medium": medium, "high": high}


def _cost_estimate_data(confidence: str = "medium") -> dict:
    return {
        "one_time": _cost_range(3000, 10000, 20000),
        "monthly": _cost_range(50, 500, 1000),
        "maintenance_monthly": _cost_range(300, 1000, 2000),
        "human_review_monthly": _cost_range(200, 700, 1500),
        "integration_subscription_monthly": _cost_range(0, 100, 500),
        "currency": "USD",
        "assumptions": [
            "Support volume is known.",
            "Cloud LLM is allowed after redaction.",
            "Human review is required during pilot.",
        ],
        "confidence": confidence,
        "price_card_references": [
            {
                "provider": "OpenAI",
                "model": "gpt-example",
                "price_card_version": "2026-06-01",
                "captured_at": "2026-06-01",
                "source": "manual source note for test fixture",
            }
        ],
    }


def test_cost_estimate_supports_required_ranges_and_price_cards() -> None:
    estimate = CostEstimate.model_validate(_cost_estimate_data())

    assert estimate.schema_version == "cost-estimate-v1"
    assert estimate.one_time.medium == 10000
    assert estimate.monthly.medium == 500
    assert estimate.maintenance_monthly.high == 2000
    assert estimate.human_review_monthly.low == 200
    assert estimate.integration_subscription_monthly.medium == 100
    assert estimate.currency == "USD"
    assert estimate.assumptions
    assert estimate.confidence == "medium"
    assert estimate.price_card_references[0].price_card_version == "2026-06-01"


def test_cost_estimate_confidence_supports_low_medium_and_high() -> None:
    confidence_levels = {"low", "medium", "high"}

    estimates = [
        CostEstimate.model_validate(_cost_estimate_data(confidence=confidence))
        for confidence in confidence_levels
    ]

    assert {estimate.confidence for estimate in estimates} == confidence_levels


def test_cost_estimate_rejects_invalid_one_time_ordering() -> None:
    data = _cost_estimate_data()
    data["one_time"] = _cost_range(low=10000, medium=3000, high=20000)

    with pytest.raises(ValidationError, match="cost range must be ordered"):
        CostEstimate.model_validate(data)


def test_cost_estimate_rejects_invalid_monthly_ordering() -> None:
    data = _cost_estimate_data()
    data["monthly"] = _cost_range(low=50, medium=1000, high=500)

    with pytest.raises(ValidationError, match="cost range must be ordered"):
        CostEstimate.model_validate(data)


def test_cost_estimate_without_assumptions_fails_validation() -> None:
    data = _cost_estimate_data()
    data["assumptions"] = []

    with pytest.raises(ValidationError, match="assumptions"):
        CostEstimate.model_validate(data)
