from workflow_agent_studio.privacy.redaction import build_redaction_preview


def test_redaction_preview_masks_values_and_reports_counts() -> None:
    credential = "sk" + "_test_placeholder123"
    raw = (
        "Customer name: Jane Miller\n"
        "Email: jane@example.test\n"
        "Phone: +1 555 222 0199\n"
        "Address: 123 Market Street\n"
        "Order ID ORD-12345\n"
        "Passport: P1234567\n"
        "Card: 4111 1111 1111 1111\n"
        f"API key: {credential}\n"
        "Synthetic volume: 200 tickets/month\n"
    )

    preview = build_redaction_preview(raw)

    for raw_value in [
        "Jane Miller",
        "jane@example.test",
        "+1 555 222 0199",
        "123 Market Street",
        "ORD-12345",
        "P1234567",
        "4111 1111 1111 1111",
        credential,
    ]:
        assert raw_value not in preview.text
    assert "Customer name: [PERSON_1]" in preview.text
    assert "Email: [EMAIL_1]" in preview.text
    assert "Phone: [PHONE_1]" in preview.text
    assert "Address: [ADDRESS_1]" in preview.text
    assert "Order ID [ORDER_ID_1]" in preview.text
    assert "Passport: [PASSPORT_ID_1]" in preview.text
    assert "Card: [PAYMENT_CARD_REDACTED]" in preview.text
    assert "API key: [API_KEY_REDACTED]" in preview.text
    assert "Synthetic volume: 200 tickets/month" in preview.text
    assert preview.redaction_counts == {
        "api_key": 1,
        "payment_card": 1,
        "email": 1,
        "phone": 1,
        "address": 1,
        "passport_id": 1,
        "order_id": 1,
        "person": 1,
    }


def test_redaction_preview_uses_stable_placeholders_for_repeated_values() -> None:
    raw = "Email jane@example.test, backup jane@example.test, phone 555-222-0199."

    preview = build_redaction_preview(raw)

    assert preview.text.count("[EMAIL_1]") == 2
    assert "jane@example.test" not in preview.text
    assert "555-222-0199" not in preview.text
    assert preview.redaction_counts == {"email": 2, "phone": 1}


def test_redaction_preview_preserves_safe_workflow_meaning() -> None:
    raw = (
        "Step 1: Coordinator checks order status.\n"
        "Step 2: Manager approves escalation.\n"
        "Synthetic example: customer asks about store hours.\n"
    )

    preview = build_redaction_preview(raw)

    assert preview.text == raw
    assert preview.redaction_counts == {}
    assert preview.redaction_count == 0
