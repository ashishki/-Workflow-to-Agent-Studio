import logging

from workflow_agent_studio.validators import (
    log_sensitive_data_finding,
    scan_blueprint_text_for_forbidden_claims,
    scan_source_for_sensitive_data,
)


def test_secret_like_token_creates_blocking_finding() -> None:
    token = "sk" + "-test-placeholder-1234567890"

    findings = scan_source_for_sensitive_data("src-1", f"API token: {token}")

    assert len(findings) == 1
    assert findings[0].severity == "blocking"
    assert findings[0].source_id == "src-1"
    assert findings[0].finding_type == "secret_like_token"
    assert token not in findings[0].redacted_preview
    assert "sha256:" in findings[0].redacted_preview


def test_forbidden_autonomy_claim_is_flagged() -> None:
    findings = scan_blueprint_text_for_forbidden_claims(
        "This automatically builds the agent from the workflow."
    )

    assert len(findings) == 1
    assert findings[0].severity == "blocking"
    assert findings[0].rule_id == "FORBID-AUTONOMY-CLAIM"


def test_sensitive_finding_logs_exclude_raw_value(caplog) -> None:
    logger = logging.getLogger("workflow_agent_studio.tests")
    token = "sk" + "-test-placeholder-1234567890"
    finding = scan_source_for_sensitive_data("src-1", f"API token: {token}")[0]

    with caplog.at_level(logging.WARNING, logger=logger.name):
        log_sensitive_data_finding(logger, finding)

    record = caplog.records[0]
    assert record.finding_id == finding.finding_id
    assert record.severity == "blocking"
    assert token not in record.getMessage()
    assert token not in record.__dict__.get("redacted_preview", "")
