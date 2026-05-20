from pathlib import Path

from workflow_agent_studio.blueprint.prompts import (
    PROMPT_REGISTRY,
    prompt_versions_for_generation,
)


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


def test_operator_guide_documents_supported_source_kinds() -> None:
    guide = Path("docs/operator_guide.md").read_text(encoding="utf-8")

    assert "transcripts: `.transcript`, `.transcript.txt`, `.transcript.md`" in guide
    assert "pasted notes: `.notes`, `.notes.txt`, `.notes.md`" in guide
    assert "form descriptions: `.form`, `.form.txt`, `.form.md`" in guide
    assert "integration snippets: `.integration`, `.integration.txt`, `.integration.md`" in guide
    assert "Unsupported file types fail before source records are persisted." in guide
    assert "Keep source files local" in guide


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


def test_active_ai_roadmap_cover_strategy_and_engineering() -> None:
    strategy = Path("docs/product_strategy.md").read_text(encoding="utf-8")
    roadmap = Path("docs/tasks.md").read_text(encoding="utf-8")

    assert "pre-production layer for AI automation" in strategy
    assert "Phase 1: Evidence Capture And Corpus Expansion" in roadmap
    assert "Phase 4: Automation Readiness And Governance" in roadmap
    assert "Phase 6: Vertical Blueprint Packs" in roadmap
    assert "Phase 9: Learning System And Moat" in roadmap
    assert "T21: Transcript Ingestion" in roadmap
    assert "Type: rag:ingestion" in roadmap
    assert "Exit criteria" in roadmap
    assert "docs/archive/TASK_GRAPH_V1_T01_T20.md" in roadmap


def test_readme_links_active_product_strategy_and_task_graph() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "docs/product_strategy.md" in readme
    assert "docs/tasks.md" in readme
    assert "docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md" in readme
    assert "Verified local baseline: 117 passing tests" in readme


def test_prompts_stay_compact_and_archive_old_versions() -> None:
    orchestrator = Path("docs/prompts/ORCHESTRATOR.md").read_text(encoding="utf-8")
    codex_prompt = Path("docs/CODEX_PROMPT.md").read_text(encoding="utf-8")

    assert "docs/archive/ORCHESTRATOR_V2_LONG.md" in codex_prompt
    assert "Do not paste large roadmap or archive content into the prompt." in orchestrator
    assert len(orchestrator.splitlines()) < 120
    assert len(codex_prompt.splitlines()) < 140


def test_prompt_registry_records_versions_for_generation_attempts() -> None:
    record = prompt_versions_for_generation(attempt_id="attempt-1")

    assert record.attempt_id == "attempt-1"
    assert record.prompt_versions == {
        "workflow_extraction": "workflow_extraction:v1",
        "blueprint_synthesis": "blueprint_synthesis:v1",
    }


def test_prompt_assets_stay_task_focused() -> None:
    forbidden_context = ("docs/tasks.md", "docs/ARCHITECTURE.md", "roadmap", "archive")

    assert set(PROMPT_REGISTRY) == {"workflow_extraction", "blueprint_synthesis"}
    for prompt in PROMPT_REGISTRY.values():
        assert prompt.version.endswith(":v1")
        assert len(prompt.template.split()) < 40
        assert not any(term in prompt.template for term in forbidden_context)
