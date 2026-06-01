import pytest

from workflow_agent_studio.costing.engine import estimate_pattern_cost


def test_cost_engine_estimates_deterministic_reminder_range() -> None:
    estimate = estimate_pattern_cost(
        pattern_id="appointment_booking",
        scope="small",
        privacy_mode="lightweight_cloud",
        monthly_volume=200,
        assumptions=["Calendar access is available.", "Booking rules are stable."],
        confidence="medium",
    )

    assert estimate.one_time.low == 500
    assert estimate.one_time.high == 3000
    assert estimate.monthly.low == 20
    assert estimate.monthly.high == 300
    assert estimate.assumptions
    assert estimate.confidence == "medium"


def test_cost_engine_estimates_support_assistant_with_price_card() -> None:
    estimate = estimate_pattern_cost(
        pattern_id="customer_support_triage",
        scope="medium",
        privacy_mode="lightweight_cloud",
        monthly_volume=2000,
        assumptions=["Support volume is known.", "Cloud mode is allowed after redaction."],
        confidence="medium",
    )

    assert estimate.one_time.low == 4500
    assert estimate.one_time.high == 30000
    assert estimate.monthly.medium == 750
    assert estimate.price_card_references


def test_cost_engine_private_document_assistant_includes_overhead() -> None:
    private_estimate = estimate_pattern_cost(
        pattern_id="document_extraction",
        scope="medium",
        privacy_mode="local_on_prem",
        monthly_volume=1000,
        assumptions=["Local/private model path is required.", "Human review is required."],
        confidence="low",
    )

    cloud_estimate = estimate_pattern_cost(
        pattern_id="document_extraction",
        scope="medium",
        privacy_mode="lightweight_cloud",
        monthly_volume=1000,
        assumptions=["Synthetic fixture only."],
        confidence="low",
    )

    assert private_estimate.one_time.low > cloud_estimate.one_time.low
    assert private_estimate.monthly.low > cloud_estimate.monthly.low
    assert private_estimate.maintenance_monthly.low > cloud_estimate.maintenance_monthly.low


def test_cost_engine_requires_assumptions() -> None:
    with pytest.raises(ValueError, match="requires assumptions"):
        estimate_pattern_cost(
            pattern_id="appointment_booking",
            scope="small",
            privacy_mode="lightweight_cloud",
            monthly_volume=200,
            assumptions=[],
            confidence="medium",
        )
