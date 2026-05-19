from workflow_agent_studio.observability.logging import redact_observability_value
from workflow_agent_studio.observability.tracing import get_tracer


def test_redact_observability_value_hashes_sensitive_values() -> None:
    sensitive = "customer@example.test"

    redacted = redact_observability_value(sensitive, sensitive_values=[sensitive])

    assert redacted.startswith("sha256:")
    assert sensitive not in redacted
    assert (
        redact_observability_value("workflow_status", sensitive_values=[sensitive])
        == "workflow_status"
    )


def test_shared_tracing_module_exposes_tracer() -> None:
    tracer = get_tracer()

    assert hasattr(tracer, "start_as_current_span")
    with tracer.start_as_current_span("unit-test"):
        assert True
