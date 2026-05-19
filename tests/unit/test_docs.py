from pathlib import Path


def test_readme_contains_setup_and_sample_commands() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "python3.12 -m venv .venv" in readme
    assert "Required environment variables" in readme
    assert "WORKFLOW_STUDIO_STORAGE_PATH" in readme
    assert "workflow-agent-studio run" in readme
    assert "workflow-agent-studio export" in readme


def test_operator_guide_states_v1_non_goals() -> None:
    guide = Path("docs/operator_guide.md").read_text(encoding="utf-8")

    assert "V1 does not create agents." in guide
    assert "V1 does not deploy automations." in guide
    assert "V1 does not mutate production systems." in guide


def test_evaluation_guide_lists_eval_commands_and_metrics() -> None:
    guide = Path("docs/evaluation_guide.md").read_text(encoding="utf-8")

    assert "tests/integration/test_retrieval_query.py tests/eval/test_retrieval_eval.py" in guide
    assert "tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py" in guide
    assert "hit@3" in guide
    assert "citation precision" in guide
    assert "blocking finding count" in guide


def test_pilot_measurement_defines_proof_metric_fields() -> None:
    measurement = Path("docs/pilot_measurement.md").read_text(encoding="utf-8")

    assert "workflow_source_duration_minutes" in measurement
    assert "time_to_reviewable_blueprint_minutes" in measurement
    assert "required_section_acceptance_rate_percent" in measurement
    assert "reviewer_edit_count" in measurement
    assert "critical_missing_question_count" in measurement


def test_pilot_measurement_includes_v1_thresholds() -> None:
    measurement = Path("docs/pilot_measurement.md").read_text(encoding="utf-8")

    assert "Pass if under 30 minutes." in measurement
    assert "Pass if at least 80 percent after human review." in measurement
    assert "template only" in measurement


def test_evaluation_guide_links_pilot_measurement_artifact() -> None:
    guide = Path("docs/evaluation_guide.md").read_text(encoding="utf-8")

    assert "[`docs/pilot_measurement.md`](pilot_measurement.md)" in guide
