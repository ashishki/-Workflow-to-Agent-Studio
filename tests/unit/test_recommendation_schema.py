import pytest
from pydantic import ValidationError

from workflow_agent_studio.domain.recommendation import RecommendationCard


def _recommendation_data() -> dict:
    return {
        "recommendation_id": "REC-001",
        "recommendation": "Customer support triage assistant",
        "target_workflow_step": "Inbound message classification",
        "expected_value": {
            "qualitative": "Faster response and fewer missed requests.",
            "quantitative_assumption": "Reduce manual triage time by 30-50 percent.",
        },
        "required_data": ["support messages", "order status", "FAQ/SOP"],
        "privacy_class": "sensitive",
        "implementation_option": "llm_assistant",
        "architecture": {
            "model": "Cloud LLM API or private mode depending on customer data.",
            "deterministic_components": ["routing rules", "refund approval gate"],
            "llm_components": ["message summarization", "intent classification draft"],
        },
        "estimated_cost": {
            "one_time_low": 2000,
            "one_time_medium": 7000,
            "one_time_high": 20000,
            "currency": "USD",
        },
        "estimated_time": {
            "low": "2 weeks",
            "medium": "4 weeks",
            "high": "8 weeks",
        },
        "required_people": [
            "AI automation engineer",
            "business process owner",
            "reviewer/support lead",
        ],
        "dependencies": ["clean FAQ", "support inbox access", "refund policy"],
        "risks": ["hallucinated policy answer", "exposure of customer data"],
        "validation_method": [
            "golden support tickets",
            "human review of first 100 classifications",
        ],
        "success_metrics": [
            "first response time",
            "escalation accuracy",
            "manual handling time",
        ],
        "confidence_level": "medium",
        "assumptions": ["Support requests are repetitive enough."],
        "evidence": [{"source_id": "SRC-001", "chunk_id": "CH-004"}],
        "fallback_option": "Deterministic canned replies and manual routing.",
        "human_gate": {
            "required": True,
            "reviewer": "Support lead",
            "approval_event": "Approve first production rollout.",
            "rationale": "Customer-facing support drafts require accountable review.",
        },
    }


def test_recommendation_card_accepts_happy_path() -> None:
    card = RecommendationCard.model_validate(_recommendation_data())

    assert card.schema_version == "recommendation-card-v1"
    assert card.target_workflow_step == "Inbound message classification"
    assert card.privacy_class == "sensitive"
    assert card.estimated_cost.one_time_medium == 7000
    assert card.estimated_time.medium == "4 weeks"
    assert card.validation_method
    assert card.success_metrics
    assert card.human_gate.required


def test_recommendation_without_target_workflow_step_fails_validation() -> None:
    data = _recommendation_data()
    data.pop("target_workflow_step")

    with pytest.raises(ValidationError, match="target_workflow_step"):
        RecommendationCard.model_validate(data)


def test_recommendation_without_evidence_and_assumptions_fails_validation() -> None:
    data = _recommendation_data()
    data["evidence"] = []
    data["assumptions"] = []

    with pytest.raises(ValidationError, match="evidence or assumptions"):
        RecommendationCard.model_validate(data)


def test_recommendation_without_fallback_fails_validation() -> None:
    data = _recommendation_data()
    data.pop("fallback_option")

    with pytest.raises(ValidationError, match="fallback_option"):
        RecommendationCard.model_validate(data)


@pytest.mark.parametrize(
    "field",
    [
        "privacy_class",
        "estimated_cost",
        "estimated_time",
        "risks",
        "validation_method",
        "success_metrics",
        "required_data",
        "dependencies",
        "human_gate",
    ],
)
def test_recommendation_requires_planning_fields(field: str) -> None:
    data = _recommendation_data()
    data.pop(field)

    with pytest.raises(ValidationError, match=field):
        RecommendationCard.model_validate(data)
