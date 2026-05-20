from workflow_agent_studio.safety import sanitize_text_for_benchmark


def test_sanitization_redacts_common_pii_and_credentials() -> None:
    raw = (
        "# Workflow\n\n"
        "- Contact jane.operator@example.com or +1 415-555-0134.\n"
        "- Customer ID: ACME-12345 and Account Number: ENT-9988.\n"
        "- Address: 1234 Market Street.\n"
        "- Token: sk-live-placeholder12345 and crm_api_key = abcdefghijklmnop.\n"
    )

    sanitized = sanitize_text_for_benchmark(raw)

    assert "jane.operator@example.com" not in sanitized.text
    assert "415-555-0134" not in sanitized.text
    assert "ACME-12345" not in sanitized.text
    assert "ENT-9988" not in sanitized.text
    assert "1234 Market Street" not in sanitized.text
    assert "sk-live-placeholder12345" not in sanitized.text
    assert "abcdefghijklmnop" not in sanitized.text
    assert sanitized.redaction_counts == {
        "email": 1,
        "phone": 1,
        "secret": 1,
        "api_key": 1,
        "customer_id": 2,
        "address": 1,
    }


def test_sanitization_preserves_eval_structure() -> None:
    raw = (
        "# Intake Workflow\n\n"
        "1. Coordinator receives request from jane@example.com.\n"
        "2. Coordinator checks Account ID: ACME-1234.\n"
        "3. Manager approves escalation.\n"
    )

    sanitized = sanitize_text_for_benchmark(raw)

    assert sanitized.text.startswith("# Intake Workflow")
    assert "1. Coordinator receives request" in sanitized.text
    assert "2. Coordinator checks Account ID: [REDACTED_CUSTOMER_ID]" in sanitized.text
    assert "3. Manager approves escalation." in sanitized.text
    assert sanitized.redaction_count == 2
