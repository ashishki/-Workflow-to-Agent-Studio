"""Versioned planning price-card references."""

from __future__ import annotations

from datetime import date

from workflow_agent_studio.domain.costing import PriceCardReference

PLANNING_PRICE_CARD = PriceCardReference(
    provider="planning",
    model="usage-assumption",
    price_card_version="manual-2026-06-01",
    captured_at=date(2026, 6, 1),
    source="Manual planning placeholder; update from official provider pricing before quoting.",
)
