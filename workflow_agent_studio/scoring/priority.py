"""Deterministic priority scoring engine."""

from __future__ import annotations

from workflow_agent_studio.domain.recommendation import SolutionType
from workflow_agent_studio.domain.scoring import PriorityBand, PriorityScore, ScoreConfidence


def compute_priority_score(
    *,
    business_value: int,
    delivery_readiness: int,
    risk_penalty: int,
    evaluation_clarity: int,
    solution_type: SolutionType,
    confidence: ScoreConfidence,
    uncertainty_notes: list[str],
) -> PriorityScore:
    if not uncertainty_notes:
        raise ValueError("priority score requires uncertainty notes")
    priority_band = _priority_band(
        business_value=business_value,
        delivery_readiness=delivery_readiness,
        risk_penalty=risk_penalty,
        evaluation_clarity=evaluation_clarity,
        solution_type=solution_type,
    )
    return PriorityScore(
        scoring_model_version="priority-scoring-engine-v1",
        business_value=business_value,
        delivery_readiness=delivery_readiness,
        risk_penalty=risk_penalty,
        priority_band=priority_band,
        confidence=confidence,
        rationale=_rationale(
            business_value=business_value,
            delivery_readiness=delivery_readiness,
            risk_penalty=risk_penalty,
            evaluation_clarity=evaluation_clarity,
            priority_band=priority_band,
        ),
        uncertainty_notes=uncertainty_notes,
    )


def _priority_band(
    *,
    business_value: int,
    delivery_readiness: int,
    risk_penalty: int,
    evaluation_clarity: int,
    solution_type: SolutionType,
) -> PriorityBand:
    if solution_type == "classic_script" and risk_penalty <= 45 and delivery_readiness >= 60:
        return "classic_automation"
    if risk_penalty >= 80 and evaluation_clarity < 40:
        return "do_not_automate_yet"
    if risk_penalty >= 70 or delivery_readiness < 50 or evaluation_clarity < 50:
        return "prepare_first"
    if business_value >= 75 and delivery_readiness >= 75 and risk_penalty <= 40:
        return "quick_win"
    if business_value >= 70 and delivery_readiness >= 50 and risk_penalty <= 65:
        return "strategic_pilot"
    return "prepare_first"


def _rationale(
    *,
    business_value: int,
    delivery_readiness: int,
    risk_penalty: int,
    evaluation_clarity: int,
    priority_band: PriorityBand,
) -> list[str]:
    return [
        f"Business value score: {business_value}.",
        f"Delivery readiness score: {delivery_readiness}.",
        f"Risk penalty score: {risk_penalty}.",
        f"Evaluation clarity score: {evaluation_clarity}.",
        f"Priority band selected: {priority_band}.",
    ]
