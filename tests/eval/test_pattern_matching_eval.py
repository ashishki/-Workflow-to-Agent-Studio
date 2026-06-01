from workflow_agent_studio.roadmap.pattern_matching import match_smb_pattern


def test_salon_reminder_matches_appointment_pattern_not_high_autonomy_agent() -> None:
    match = match_smb_pattern(
        workflow_description="Hair salon sends appointment reminders and booking confirmations.",
        pain_point="Front desk manually checks calendar availability.",
        privacy_class="sensitive",
    )

    assert match.pattern_id == "appointment_booking"
    assert match.pattern_version == "v1"
    assert match.recommended_solution_type == "classic_script"
    assert "high_autonomy_agent" in match.blocked_anti_matches
    assert match.when_not_to_use
    assert match.privacy_compatible


def test_ecommerce_returns_match_human_in_loop_not_automatic_refund() -> None:
    match = match_smb_pattern(
        workflow_description="E-commerce returns workflow checks orders and refund policy.",
        pain_point="Support agents manually summarize return requests.",
        privacy_class="sensitive",
    )

    assert match.pattern_id == "ecommerce_returns"
    assert match.recommended_solution_type == "human_in_the_loop_workflow"
    assert "automatic_refund" in match.blocked_anti_matches
    assert match.when_not_to_use
    assert match.privacy_compatible


def test_legal_checklist_matches_private_assistant_not_legal_advice() -> None:
    match = match_smb_pattern(
        workflow_description="Legal consultancy checklist for visa document collection.",
        pain_point="Staff manually verify required documents.",
        privacy_class="restricted",
    )

    assert match.pattern_id == "legal_checklist"
    assert match.recommended_solution_type == "rag_knowledge_assistant"
    assert "legal_advice_agent" in match.blocked_anti_matches
    assert "unrestricted_cloud_bot" in match.blocked_anti_matches
    assert match.when_not_to_use
    assert match.privacy_compatible


def test_reporting_match_prefers_deterministic_pattern_when_llm_unnecessary() -> None:
    match = match_smb_pattern(
        workflow_description="Weekly spreadsheet metrics report for operations.",
        pain_point="Team manually copies dashboard numbers.",
        privacy_class="confidential",
    )

    assert match.pattern_id == "reporting_automation"
    assert match.recommended_solution_type == "classic_script"
    assert "llm_agent_for_metric_calculation" in match.blocked_anti_matches
    assert match.when_not_to_use


def test_privacy_weaker_than_detected_data_class_is_blocked() -> None:
    match = match_smb_pattern(
        workflow_description="Weekly reporting dashboard.",
        pain_point="Metrics include restricted medical records.",
        privacy_class="restricted",
    )

    assert not match.privacy_compatible
    assert "privacy_default_weaker_than_detected_data_class" in match.blocked_anti_matches
