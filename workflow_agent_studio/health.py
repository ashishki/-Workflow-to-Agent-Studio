"""Deterministic application health surface."""

from __future__ import annotations


def get_health_status() -> dict[str, str]:
    return {"app": "workflow-agent-studio", "status": "ok"}
