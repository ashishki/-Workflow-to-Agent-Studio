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
    assert "Approved implementation handoffs are local Markdown exports only." in guide
    assert (
        "Unapproved or validation-blocked blueprints cannot produce approved handoff exports."
        in guide
    )


def test_operator_guide_documents_supported_source_kinds() -> None:
    guide = Path("docs/operator_guide.md").read_text(encoding="utf-8")

    assert "transcripts: `.transcript`, `.transcript.txt`, `.transcript.md`" in guide
    assert "pasted notes: `.notes`, `.notes.txt`, `.notes.md`" in guide
    assert "form descriptions: `.form`, `.form.txt`, `.form.md`" in guide
    assert "integration snippets: `.integration`, `.integration.txt`, `.integration.md`" in guide
    assert "Unsupported file types fail before source records are persisted." in guide
    assert "Keep source files local" in guide
    assert "## Sanitization For Benchmarks" in guide
    assert "Sanitized or synthetic fixtures still do not count as real pilot evidence." in guide
    assert "## Public Demo Packs" in guide
    assert "docs/experiments/public_demo_pack/netbox_issue_triage/" in guide
    assert "docs/audit/PUBLIC_DATA_PRODUCT_PROOF.md" in guide
    assert "not pilot evidence" in guide


def test_open_source_research_protocol_defines_public_demo_boundaries() -> None:
    protocol = Path("docs/open_source_research_protocol.md").read_text(encoding="utf-8")
    normalized = " ".join(protocol.split())

    assert "## Allowed Sources" in protocol
    assert "public GitHub issues, discussions, PR templates" in protocol
    assert "public company FAQ/booking/support pages" in protocol
    assert "## Forbidden Sources" in protocol
    assert "private client docs, private communities, private repositories" in protocol
    assert "raw personal data, tokens, cookies" in protocol
    assert "source_url_or_locator" in protocol
    assert "captured_at" in protocol
    assert "extracted_workflow_facts" in protocol
    assert "`public_demo_only` must be true" in protocol
    assert "do not support commercial pilot pass/fail claims" in normalized


def test_operator_guide_links_open_source_research_protocol() -> None:
    guide = Path("docs/operator_guide.md").read_text(encoding="utf-8")
    normalized = " ".join(guide.split())

    assert "docs/open_source_research_protocol.md" in guide
    assert "allowed sources, forbidden sources, source register fields" in normalized
    assert "public-demo-only claim boundary" in guide


def test_lead_intake_public_source_register_has_required_protocol_fields() -> None:
    register = Path("docs/experiments/public_sources/lead_intake/source_register.md").read_text(
        encoding="utf-8"
    )
    rows = [line for line in register.splitlines() if line.startswith("| HVAC-")]

    assert len(rows) >= 20
    assert "source_url_or_locator" in register
    assert "captured_at" in register
    assert "source_type" in register
    assert "workflow_kind" in register
    assert "extracted_workflow_facts" in register
    assert "limitations" in register
    assert "public_demo_only" in register
    assert all(row.rstrip().endswith("| true |") for row in rows)
    assert "Pricing, conversion, buyer readiness, and commercial pilot claims are out" in (register)


def test_hvac_lead_intake_fixture_extracts_required_workflow_facts() -> None:
    fixture = Path("tests/fixtures/public_sources/hvac_lead_intake.notes.md").read_text(
        encoding="utf-8"
    )

    assert "Dataset kind: public-source demo only; not customer proof or pilot evidence." in (
        fixture
    )
    assert "Actors:" in fixture
    assert "Systems:" in fixture
    assert "Customer inputs:" in fixture
    assert "Qualification fields:" in fixture
    assert "Escalation points:" in fixture
    assert "Unsafe-answer boundaries:" in fixture
    assert "service-area fit" in fixture
    assert "urgent or emergency status" in fixture
    assert "no pricing, conversion, buyer-readiness, or pilot-success claim" in fixture


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
    assert "No real pilot has been reviewed yet." in measurement
    assert "Any unresolved critical missing question forces `Fail`" in measurement


def test_pilot_measurement_records_review_evidence_placeholders() -> None:
    measurement = Path("docs/pilot_measurement.md").read_text(encoding="utf-8")

    assert "reviewer_edit_summary" in measurement
    assert "critical_missing_questions" in measurement
    assert "Template only - no reviewed pilot yet" in measurement


def test_pilot_measurement_includes_real_pilot_intake_checklist() -> None:
    measurement = Path("docs/pilot_measurement.md").read_text(encoding="utf-8")

    assert "## Pilot Intake Checklist" in measurement
    assert "Real operator-provided SOP, transcript, notes, form, or integration excerpt." in (
        measurement
    )
    assert "Demo and synthetic fixtures can test mechanics only." in measurement
    assert "Any unresolved critical missing question forces `Fail`." in measurement
    assert "count accepted required blueprint sections" in measurement
    assert "confirm whether every critical missing question is resolved" in measurement
    assert "Dataset boundary: demo fixtures, synthetic benchmarks" in measurement
    assert "must not be counted as real pilot rows" in measurement


def test_pilot_measurement_defines_prospect_data_request_gate() -> None:
    measurement = Path("docs/pilot_measurement.md").read_text(encoding="utf-8")
    normalized = " ".join(measurement.split())

    assert "## Prospect Data Request Gate" in measurement
    assert "Passing this gate only authorizes a data request" in measurement
    assert "does not create a pilot row or satisfy T34/T40" in normalized
    assert "docs/experiments/public_demo_pack/netbox_issue_triage/" in measurement
    assert "public-source evals pass for pipeline mechanics" in measurement
    assert "one real SOP, transcript, pasted notes file" in measurement
    assert "no secrets, credentials, production tokens" in measurement
    assert "named reviewer who can accept sections" in measurement
    assert "docs/open_source_research_protocol.md" in measurement
    assert "cannot create the first pilot row" in measurement
    assert "docs/prospect_data_request_pack.md" in measurement


def test_prospect_data_request_pack_keeps_request_narrow_and_local() -> None:
    pack = Path("docs/prospect_data_request_pack.md").read_text(encoding="utf-8")
    normalized = " ".join(pack.split())

    assert "Status: request template; not pilot proof" in pack
    assert "one SOP" in pack
    assert "one transcript" in pack
    assert "one pasted notes file" in pack
    assert "one form description" in pack
    assert "one integration excerpt" in pack
    assert "one mixed packet" in pack
    assert "process it locally" in pack
    assert "do not need system access" in normalized
    assert "Do not request credentials" in pack
    assert "named reviewer" in pack
    assert "Optional Sanitized Benchmark Reuse" in pack
    assert "public-source demos, not buyer validation or pilot proof" in normalized


def test_solo_showcase_readiness_review_requests_prospect_data() -> None:
    review = Path("docs/audit/SOLO_SHOWCASE_READINESS_REVIEW.md").read_text(encoding="utf-8")
    normalized = " ".join(review.split())

    assert "Status: ready_to_request_prospect_data" in review
    assert "Next action: request prospect data." in review
    assert "HVAC lead intake" in review
    assert "NetBox issue triage" in review
    assert "GitLab incident response" in review
    assert "showcase_ready" in review
    assert "must not be represented as buyer validation" in normalized
    assert "T34 and T40 remain blocked" in review
    assert "docs/prospect_data_request_pack.md" in review


def test_evaluation_guide_links_pilot_measurement_artifact() -> None:
    guide = Path("docs/evaluation_guide.md").read_text(encoding="utf-8")

    assert "[`docs/pilot_measurement.md`](pilot_measurement.md)" in guide
    assert "Overall pass" in guide
    assert "time-to-reviewable blueprint under 30 minutes" in guide
    assert "no unresolved critical" in guide
    assert "missing questions" in guide
    assert "pilot intake checklist" in guide
    assert "real-pilot evidence gate" in guide
    assert "## Prospect Data Request Gate" in guide
    assert "does not satisfy T34/T40" in guide


def test_active_ai_roadmap_cover_strategy_and_engineering() -> None:
    strategy = Path("docs/product_strategy.md").read_text(encoding="utf-8")
    roadmap = Path("docs/tasks.md").read_text(encoding="utf-8")

    assert "pre-production layer for AI automation" in strategy
    assert "Phase 1: Evidence Capture And Corpus Expansion" in roadmap
    assert "Phase 4: Automation Readiness And Governance" in roadmap
    assert "Phase 6: Vertical Blueprint Packs" in roadmap
    assert "Phase 9: Learning System And Moat" in roadmap
    assert "Phase 11: Public-Source Demo Quality" in roadmap
    assert "T21: Transcript Ingestion" in roadmap
    assert "Type: rag:ingestion" in roadmap
    assert "Exit criteria" in roadmap
    assert "docs/archive/TASK_GRAPH_V1_T01_T20.md" in roadmap


def test_readme_links_active_product_strategy_and_task_graph() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    normalized = " ".join(readme.split())

    assert "docs/product_strategy.md" in readme
    assert "docs/product_strategy.md#commercial-pilot-package" in readme
    assert "docs/tasks.md" in readme
    assert "docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md" in readme
    assert (
        "No external user, observed workflow outcome, or production deployment is claimed"
        in normalized
    )
    assert "This repository currently has no open-source license" in normalized
    assert "passing tests" not in readme


def test_public_evidence_mapping_intake_is_bounded() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    guide = Path("docs/SANITIZED_INTERVIEW_FIXTURES.md").read_text(encoding="utf-8")
    form = Path(".github/ISSUE_TEMPLATE/unsupported-evidence-mapping.yml").read_text(
        encoding="utf-8"
    )
    config = Path(".github/ISSUE_TEMPLATE/config.yml").read_text(encoding="utf-8")
    normalized_guide = " ".join(guide.split()).casefold()

    assert "template=unsupported-evidence-mapping.yml" in readme
    assert "authored-from-scratch synthetic fixtures" in readme
    for marker in (
        "do not start with private material and redact or paraphrase it",
        "sanitization is not a promise of anonymity",
        "failing-then-passing deterministic regression",
        "does not establish an observed case",
        "opening an issue does not grant a license",
    ):
        assert marker in normalized_guide
    for field_id in (
        "revision",
        "defect_kind",
        "fixture",
        "expected_mapping",
        "observed_mapping",
        "reproduction",
        "execution_boundary",
        "regression",
        "confirmations",
    ):
        assert f"id: {field_id}" in form
    assert "not redacted, paraphrased, translated, or transformed" in form
    assert "blank_issues_enabled: false" in config


def test_product_strategy_documents_commercial_pilot_package() -> None:
    strategy = Path("docs/product_strategy.md").read_text(encoding="utf-8")

    assert "## Commercial Pilot Package" in strategy
    assert "Status: assumption-backed" in strategy
    assert "Buyer: AI automation consultants" in strategy
    assert "Deliverables:" in strategy
    assert "Non-goals:" in strategy
    assert "Success criteria:" in strategy
    assert "unresolved critical missing questions force a failed pilot result" in strategy
    assert "Any public sales claim must cite the pilot measurement row" in strategy


def test_product_strategy_documents_dataset_boundaries() -> None:
    strategy = Path("docs/product_strategy.md").read_text(encoding="utf-8")
    normalized = " ".join(strategy.split())

    assert "## Dataset Boundary" in strategy
    assert "Demo fixtures are not buyer proof." in strategy
    assert "Synthetic results cannot satisfy pilot proof or T34." in strategy
    assert "Real pilot evidence" in strategy
    assert "Commercial claims must use real pilot evidence." in strategy
    assert "## Prospect Data Request Strategy" in strategy
    assert "precondition for asking potential customers for real workflow data" in normalized
    assert "docs/pilot_measurement.md#prospect-data-request-gate" in strategy
    assert "Exclude secrets, credentials, private keys" in strategy
    assert "T34 and T40 remain blocked" in strategy


def test_task_graph_defines_public_source_demo_quality_gate() -> None:
    roadmap = Path("docs/tasks.md").read_text(encoding="utf-8")

    assert "Business goal: use public workflow sources to improve draft quality" in roadmap
    assert "public-source experiments do not satisfy T34/T40 or commercial pilot proof" in roadmap
    assert "T47: Public-Source Workflow Fact Eval" in roadmap
    assert "T48: Source-Grounded Extraction Upgrade" in roadmap
    assert "T49: Public Demo Pack" in roadmap
    assert "T50: Prospect Data Request Gate" in roadmap
    assert "then request real workflow" in roadmap
    assert "data from potential customers for pilot proof" in roadmap


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
