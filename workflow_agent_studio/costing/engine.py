"""Deterministic cost range engine for roadmap planning."""

from __future__ import annotations

from typing import Literal

from workflow_agent_studio.costing.price_cards import PLANNING_PRICE_CARD
from workflow_agent_studio.domain.costing import CostConfidence, CostEstimate, CostRange
from workflow_agent_studio.patterns.smb import SMBImplementationPattern, load_smb_patterns

ScopeSize = Literal["small", "medium", "large"]
PrivacyMode = Literal["lightweight_cloud", "private_analysis", "local_on_prem"]

_SCOPE_MULTIPLIER: dict[ScopeSize, float] = {
    "small": 1.0,
    "medium": 1.5,
    "large": 2.0,
}

_PATTERN_BASE_RANGES: dict[str, tuple[CostRange, CostRange]] = {
    "appointment_booking": (
        CostRange(low=500, medium=1500, high=3000),
        CostRange(low=20, medium=100, high=300),
    ),
    "customer_support_triage": (
        CostRange(low=3000, medium=10000, high=20000),
        CostRange(low=50, medium=500, high=1000),
    ),
    "document_extraction": (
        CostRange(low=15000, medium=40000, high=80000),
        CostRange(low=500, medium=2000, high=5000),
    ),
}

_DEFAULT_BASE_RANGE = (
    CostRange(low=2000, medium=7000, high=15000),
    CostRange(low=50, medium=300, high=900),
)


def estimate_pattern_cost(
    *,
    pattern_id: str,
    scope: ScopeSize,
    privacy_mode: PrivacyMode,
    monthly_volume: int,
    assumptions: list[str],
    confidence: CostConfidence,
) -> CostEstimate:
    if not assumptions:
        raise ValueError("cost estimate requires assumptions")
    pattern = _pattern_by_id(pattern_id)
    one_time_base, monthly_base = _PATTERN_BASE_RANGES.get(pattern_id, _DEFAULT_BASE_RANGE)
    scope_multiplier = _SCOPE_MULTIPLIER[scope]
    volume_multiplier = _volume_multiplier(monthly_volume)
    privacy_multiplier = _privacy_multiplier(privacy_mode)

    one_time = _scale_range(one_time_base, scope_multiplier * privacy_multiplier)
    monthly = _scale_range(monthly_base, volume_multiplier * privacy_multiplier)
    maintenance = _maintenance_range(one_time=one_time, privacy_mode=privacy_mode)
    human_review = _human_review_range(monthly_volume=monthly_volume, privacy_mode=privacy_mode)
    integration = _integration_range(pattern=pattern, scope=scope)

    return CostEstimate(
        one_time=one_time,
        monthly=monthly,
        maintenance_monthly=maintenance,
        human_review_monthly=human_review,
        integration_subscription_monthly=integration,
        currency="USD",
        assumptions=assumptions,
        confidence=confidence,
        price_card_references=[PLANNING_PRICE_CARD] if pattern.architecture.llm_owned_steps else [],
    )


def _pattern_by_id(pattern_id: str) -> SMBImplementationPattern:
    patterns = {pattern.pattern_id: pattern for pattern in load_smb_patterns()}
    try:
        return patterns[pattern_id]
    except KeyError as exc:
        raise ValueError(f"Unknown SMB pattern: {pattern_id}") from exc


def _volume_multiplier(monthly_volume: int) -> float:
    if monthly_volume <= 500:
        return 1.0
    if monthly_volume <= 5000:
        return 1.5
    return 2.0


def _privacy_multiplier(privacy_mode: PrivacyMode) -> float:
    if privacy_mode == "private_analysis":
        return 1.35
    if privacy_mode == "local_on_prem":
        return 2.0
    return 1.0


def _scale_range(cost_range: CostRange, multiplier: float) -> CostRange:
    return CostRange(
        low=round(cost_range.low * multiplier),
        medium=round(cost_range.medium * multiplier),
        high=round(cost_range.high * multiplier),
    )


def _maintenance_range(*, one_time: CostRange, privacy_mode: PrivacyMode) -> CostRange:
    base = CostRange(
        low=max(100, round(one_time.low * 0.05)),
        medium=max(300, round(one_time.medium * 0.1)),
        high=max(700, round(one_time.high * 0.15)),
    )
    if privacy_mode in {"private_analysis", "local_on_prem"}:
        return CostRange(low=base.low + 300, medium=base.medium + 1000, high=base.high + 3000)
    return base


def _human_review_range(*, monthly_volume: int, privacy_mode: PrivacyMode) -> CostRange:
    base = max(50, round(monthly_volume * 0.05))
    if privacy_mode in {"private_analysis", "local_on_prem"}:
        base *= 2
    return CostRange(low=base, medium=base * 3, high=base * 6)


def _integration_range(*, pattern: SMBImplementationPattern, scope: ScopeSize) -> CostRange:
    has_integration = any(
        "lookup" in step or "integration" in step
        for step in [*pattern.architecture.deterministic_steps, pattern.cost_range.lower()]
    )
    if not has_integration:
        return CostRange(low=0, medium=0, high=0)
    multiplier = _SCOPE_MULTIPLIER[scope]
    return _scale_range(CostRange(low=50, medium=250, high=1000), multiplier)
