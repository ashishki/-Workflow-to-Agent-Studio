from workflow_agent_studio.health import get_health_status


def test_get_health_status_returns_ok() -> None:
    assert get_health_status() == {"app": "workflow-agent-studio", "status": "ok"}


def test_smoke_baseline_has_health_test() -> None:
    assert get_health_status()["status"] == "ok"
