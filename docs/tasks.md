# Task Graph - Workflow-to-Agent Studio

Version: 1.0
Date: 2026-05-19

This file is the authoritative implementation task graph. Each task follows the structured schema in `templates/tasks_schema.md`.

---

## Phase 1: Foundation and Contracts

Business goal: create a runnable Python project with CI, smoke tests, core configuration, and typed blueprint contracts.

## T01: Project Skeleton

Owner:      codex
Phase:      1
Type:       none
Depends-On: none

Objective: |
  Create the Python package skeleton, dependency files, CLI entry point, and importable modules needed for the rest of the project.

Acceptance-Criteria:
  - id: AC-1
    description: "The package imports as `workflow_agent_studio` and exposes `__version__` as a non-empty string."
    test: "tests/unit/test_package.py::test_package_imports_with_version"
  - id: AC-2
    description: "Running `python -m workflow_agent_studio.cli --help` exits with code 0 and prints the command name `workflow-agent-studio`."
    test: "tests/unit/test_cli.py::test_cli_help_exits_zero"
  - id: AC-3
    description: "`pyproject.toml` declares Python 3.12 support and the console script `workflow-agent-studio`."
    test: "tests/unit/test_project_metadata.py::test_pyproject_declares_python_and_console_script"

Files:
  - pyproject.toml
  - requirements.txt
  - requirements-dev.txt
  - workflow_agent_studio/__init__.py
  - workflow_agent_studio/cli.py
  - tests/unit/test_package.py
  - tests/unit/test_cli.py
  - tests/unit/test_project_metadata.py

Context-Refs:
  - docs/ARCHITECTURE.md#file-layout
  - docs/IMPLEMENTATION_CONTRACT.md#mandatory-pre-task-protocol

Notes: |
  Keep the skeleton CLI-only. Do not add FastAPI, a database dependency, or retrieval libraries until the relevant tasks require them.

## T02: CI Setup

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01

Objective: |
  Configure GitHub Actions so every push and pull request runs dependency install, ruff lint, ruff format check, and pytest.

Acceptance-Criteria:
  - id: AC-1
    description: ".github/workflows/ci.yml uses Python 3.12 and runs on pushes and pull requests to `main`."
    test: "tests/unit/test_ci_config.py::test_ci_targets_python_312_and_main"
  - id: AC-2
    description: "The CI workflow installs `requirements-dev.txt` and the project in editable mode before lint and tests."
    test: "tests/unit/test_ci_config.py::test_ci_installs_dev_requirements_and_editable_package"
  - id: AC-3
    description: "The CI workflow contains separate steps for `ruff check`, `ruff format --check`, and `python -m pytest`."
    test: "tests/unit/test_ci_config.py::test_ci_runs_lint_format_and_pytest_steps"

Files:
  - .github/workflows/ci.yml
  - tests/unit/test_ci_config.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#ci-gate

Notes: |
  Do not add service containers in v1 CI until code requires them.

## T03: First Smoke Tests

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02

Objective: |
  Add the first application smoke surface: a deterministic health/status function and CLI command that prove the skeleton can run under tests.

Acceptance-Criteria:
  - id: AC-1
    description: "`get_health_status()` returns a dict with `status` equal to `ok` and `app` equal to `workflow-agent-studio`."
    test: "tests/unit/test_health.py::test_get_health_status_returns_ok"
  - id: AC-2
    description: "Running `workflow-agent-studio health` exits with code 0 and prints JSON containing `status` equal to `ok`."
    test: "tests/unit/test_cli.py::test_health_command_outputs_json"
  - id: AC-3
    description: "The smoke test baseline contains at least one passing pytest test before feature work starts."
    test: "tests/unit/test_health.py::test_smoke_baseline_has_health_test"

Files:
  - workflow_agent_studio/health.py
  - workflow_agent_studio/cli.py
  - tests/unit/test_health.py
  - tests/unit/test_cli.py

Context-Refs:
  - docs/CODEX_PROMPT.md#current-state

Notes: |
  Update `docs/CODEX_PROMPT.md` baseline after this task completes.

## T04: Configuration and Observability Foundation

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T03

Objective: |
  Implement environment-backed settings, PII-safe structured logging helpers, and the shared tracing module required by the implementation contract.

Acceptance-Criteria:
  - id: AC-1
    description: "`load_settings()` reads storage path, index directory, pattern directory, provider name, model names, and log level from environment variables with documented defaults."
    test: "tests/unit/test_config.py::test_load_settings_reads_env_and_defaults"
  - id: AC-2
    description: "`redact_observability_value()` replaces configured PII-like values with SHA-256 hashes and leaves non-sensitive labels unchanged."
    test: "tests/unit/test_observability.py::test_redact_observability_value_hashes_sensitive_values"
  - id: AC-3
    description: "`get_tracer()` is defined only in `workflow_agent_studio/observability/tracing.py` and returns an object with `start_as_current_span`."
    test: "tests/unit/test_observability.py::test_shared_tracing_module_exposes_tracer"

Files:
  - workflow_agent_studio/config.py
  - workflow_agent_studio/observability/__init__.py
  - workflow_agent_studio/observability/logging.py
  - workflow_agent_studio/observability/tracing.py
  - tests/unit/test_config.py
  - tests/unit/test_observability.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-contract
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy
  - docs/IMPLEMENTATION_CONTRACT.md#shared-tracing-module

Notes: |
  No real API keys or credentials may appear in tests.

## T05: Domain and Blueprint Schemas

Owner:      codex
Phase:      1
Type:       plan:schema
Depends-On: T01

Objective: |
  Define Pydantic schemas for workflow sources, extracted workflow maps, blueprint sections, evidence references, eval cases, review status, and implementation task plans.

Acceptance-Criteria:
  - id: AC-1
    description: "A minimal valid `AutomationBlueprint` fixture validates and includes all required v1 sections."
    test: "tests/unit/test_blueprint_schema.py::test_minimal_blueprint_fixture_validates"
  - id: AC-2
    description: "A blueprint claim without either evidence references or an assumption marker raises a validation error."
    test: "tests/unit/test_blueprint_schema.py::test_claim_requires_evidence_or_assumption"
  - id: AC-3
    description: "The plan schema version is `v1` and is serialized in exported blueprint data."
    test: "tests/unit/test_blueprint_schema.py::test_blueprint_schema_version_serializes"
  - id: AC-4
    description: "`docs/plan_eval.md` records the initial schema-validation baseline for the blueprint fixture set."
    test: "tests/eval/test_plan_eval.py::test_plan_eval_records_schema_baseline"

Files:
  - workflow_agent_studio/domain/__init__.py
  - workflow_agent_studio/domain/sources.py
  - workflow_agent_studio/domain/workflow.py
  - workflow_agent_studio/domain/blueprint.py
  - workflow_agent_studio/domain/review.py
  - tests/fixtures/blueprints/minimal_valid.json
  - tests/unit/test_blueprint_schema.py
  - tests/eval/test_plan_eval.py
  - docs/plan_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#profile-planning
  - docs/spec.md#feature-area-blueprint-generation
  - docs/IMPLEMENTATION_CONTRACT.md#profile-rules-planning

Notes: |
  This task creates the contract that later LLM outputs must satisfy. Keep fields explicit and avoid catch-all dict fields unless they are versioned.

---

## Phase 2: Ingestion, Storage, and Safety

Business goal: persist workflow runs, normalize source documents, and block unsafe source handling before any LLM synthesis.

## T06: SQLite Storage and Audit Events

Owner:      codex
Phase:      2
Type:       none
Depends-On: T04, T05

Objective: |
  Implement SQLite repositories for workflow runs, normalized source records, immutable blueprint versions, and append-only audit events.

Acceptance-Criteria:
  - id: AC-1
    description: "Creating a workflow run stores run ID, status, created timestamp, and schema version in SQLite."
    test: "tests/integration/test_storage.py::test_create_workflow_run_persists_metadata"
  - id: AC-2
    description: "Adding a blueprint version never overwrites an existing version for the same run."
    test: "tests/integration/test_storage.py::test_blueprint_versions_are_append_only"
  - id: AC-3
    description: "Deleting audit events through the repository raises `PermissionError`."
    test: "tests/integration/test_storage.py::test_audit_events_cannot_be_deleted"

Files:
  - workflow_agent_studio/storage/__init__.py
  - workflow_agent_studio/storage/database.py
  - workflow_agent_studio/storage/repositories.py
  - workflow_agent_studio/storage/schema.sql
  - tests/integration/test_storage.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_CONTRACT.md#sql-safety

Notes: |
  Use parameterized SQL only. SQLite is single-workspace in v1.

## T07: Source Ingestion and Fingerprinting

Owner:      codex
Phase:      2
Type:       none
Depends-On: T05, T06

Objective: |
  Implement text and Markdown source ingestion with deterministic normalization, SHA-256 fingerprinting, duplicate detection, and source metadata persistence.

Acceptance-Criteria:
  - id: AC-1
    description: "Ingesting a Markdown file stores one `SourceDocument` with source type `markdown`, SHA-256 fingerprint, title, and normalized text."
    test: "tests/integration/test_ingestion.py::test_markdown_ingestion_stores_normalized_source"
  - id: AC-2
    description: "Ingesting the same content twice in one run reports the duplicate fingerprint and stores only one source document."
    test: "tests/integration/test_ingestion.py::test_duplicate_source_fingerprint_not_stored_twice"
  - id: AC-3
    description: "The ingestion command creates an audit event with run ID, source count, duplicate count, and no raw source text."
    test: "tests/integration/test_ingestion.py::test_ingestion_audit_event_excludes_raw_source_text"

Files:
  - workflow_agent_studio/ingestion/__init__.py
  - workflow_agent_studio/ingestion/readers.py
  - workflow_agent_studio/ingestion/normalizer.py
  - workflow_agent_studio/ingestion/service.py
  - workflow_agent_studio/cli.py
  - tests/fixtures/sources/sample_sop.md
  - tests/integration/test_ingestion.py

Context-Refs:
  - docs/spec.md#feature-area-source-ingestion

Notes: |
  External import adapters are deferred. Keep this task limited to local files and pasted text.

## T08: Sensitive Data and Forbidden Claim Guards

Owner:      codex
Phase:      2
Type:       none
Depends-On: T05, T07

Objective: |
  Add deterministic scanners that flag likely secrets, PII-like fields, and forbidden automation claims before source content or blueprint text can be logged, approved, or exported.

Acceptance-Criteria:
  - id: AC-1
    description: "A source containing an API-key shaped token produces a blocking sensitive-data finding with the source ID and redacted preview."
    test: "tests/unit/test_safety_guards.py::test_secret_like_token_creates_blocking_finding"
  - id: AC-2
    description: "Blueprint text containing `automatically builds the agent` produces a forbidden-claim finding."
    test: "tests/unit/test_safety_guards.py::test_forbidden_autonomy_claim_is_flagged"
  - id: AC-3
    description: "Structured logs for sensitive-data findings include finding ID and severity but exclude the raw sensitive value."
    test: "tests/unit/test_safety_guards.py::test_sensitive_finding_logs_exclude_raw_value"

Files:
  - workflow_agent_studio/validators/__init__.py
  - workflow_agent_studio/validators/sensitive_data.py
  - workflow_agent_studio/validators/forbidden_claims.py
  - tests/unit/test_safety_guards.py

Context-Refs:
  - docs/ARCHITECTURE.md#security-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules

Notes: |
  This scanner is a guardrail, not a compliance classifier.

---

## Phase 3: Text-Only Retrieval and Evidence

Business goal: ground blueprint generation in source snippets and pattern-library examples with measurable retrieval behavior.

## T09: Pattern Library and Chunking

Owner:      codex
Phase:      3
Type:       rag:ingestion
Depends-On: T05, T07

Objective: |
  Implement pattern-library loading and heading-aware chunking for workflow sources and reusable automation templates.

Acceptance-Criteria:
  - id: AC-1
    description: "Chunking preserves source ID, chunk ID, heading path, character offsets, and text for each source document."
    test: "tests/unit/test_chunking.py::test_chunks_preserve_source_metadata"
  - id: AC-2
    description: "The pattern-library loader reads Markdown templates from `patterns/` and labels them as corpus type `pattern`."
    test: "tests/unit/test_pattern_library.py::test_pattern_library_loads_markdown_templates"
  - id: AC-3
    description: "`docs/retrieval_eval.md` includes the v1 chunking corpus fixture count and corpus version row."
    test: "tests/eval/test_retrieval_eval.py::test_retrieval_eval_records_chunking_baseline"

Files:
  - workflow_agent_studio/retrieval/__init__.py
  - workflow_agent_studio/retrieval/chunking.py
  - workflow_agent_studio/retrieval/patterns.py
  - patterns/automation_blueprint.md
  - patterns/eval_cases.md
  - tests/unit/test_chunking.py
  - tests/unit/test_pattern_library.py
  - tests/eval/test_retrieval_eval.py
  - docs/retrieval_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#profile-rag
  - docs/spec.md#feature-area-retrieval
  - docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag
  - docs/IMPLEMENTATION_REFERENCE_MAP.md#recommended-use-by-task

Execution-Mode: heavy
Evidence:
  - docs/retrieval_eval.md baseline row for chunking fixture corpus
  - tests/eval/test_retrieval_eval.py::test_retrieval_eval_records_chunking_baseline
Verifier-Focus: |
  Confirm ingestion and query-time retrieval remain separate and that chunk metadata supports citation traceability.

## T10: Embedding and Index Schema

Owner:      codex
Phase:      3
Type:       rag:ingestion
Depends-On: T09

Objective: |
  Implement embedding provider abstraction, local vector index persistence, index schema versioning, and full re-index behavior for text-only retrieval.

Acceptance-Criteria:
  - id: AC-1
    description: "Index metadata stores schema version, embedding model name, corpus version, chunk count, and created timestamp."
    test: "tests/integration/test_retrieval_index.py::test_index_metadata_records_schema_and_corpus"
  - id: AC-2
    description: "Changing the index schema version causes the index builder to create a new index namespace instead of mixing old and new chunks."
    test: "tests/integration/test_retrieval_index.py::test_schema_version_change_creates_new_namespace"
  - id: AC-3
    description: "The fake embedding provider used in tests returns deterministic vectors for identical chunk text."
    test: "tests/unit/test_embeddings.py::test_fake_embedding_provider_is_deterministic"
  - id: AC-4
    description: "`docs/retrieval_eval.md` records the first index baseline with corpus version and retrieval latency placeholder."
    test: "tests/eval/test_retrieval_eval.py::test_retrieval_eval_records_index_baseline"

Files:
  - workflow_agent_studio/retrieval/embeddings.py
  - workflow_agent_studio/retrieval/index.py
  - workflow_agent_studio/storage/repositories.py
  - tests/unit/test_embeddings.py
  - tests/integration/test_retrieval_index.py
  - tests/eval/test_retrieval_eval.py
  - docs/retrieval_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#index-strategy
  - docs/IMPLEMENTATION_CONTRACT.md#index-schema-versioning
  - docs/IMPLEMENTATION_REFERENCE_MAP.md#recommended-use-by-task

Execution-Mode: heavy
Evidence:
  - docs/retrieval_eval.md index baseline row
  - tests/integration/test_retrieval_index.py::test_schema_version_change_creates_new_namespace
Verifier-Focus: |
  Confirm schema changes cannot silently mix incompatible embeddings or chunks.

## T11: Query-Time Retrieval and Insufficient Evidence

Owner:      codex
Phase:      3
Type:       rag:query
Depends-On: T10

Objective: |
  Implement query-time retrieval that returns scoped evidence snippets, filters low-confidence results, and emits `insufficient_evidence` when support is inadequate.

Acceptance-Criteria:
  - id: AC-1
    description: "A query matching the workflow fixture retrieves the expected source chunk in the top 3 results."
    test: "tests/eval/test_retrieval_eval.py::test_retrieval_hit_at_3_on_workflow_fixture"
  - id: AC-2
    description: "A query outside the corpus returns `insufficient_evidence` with no generated answer text."
    test: "tests/integration/test_retrieval_query.py::test_query_without_support_returns_insufficient_evidence"
  - id: AC-3
    description: "Each returned evidence snippet includes source ID, chunk ID, score, text preview, and heading path."
    test: "tests/integration/test_retrieval_query.py::test_evidence_snippet_contains_trace_fields"
  - id: AC-4
    description: "`docs/retrieval_eval.md` records hit@3, no-answer accuracy, citation precision, latency, and corpus version for this task."
    test: "tests/eval/test_retrieval_eval.py::test_retrieval_eval_records_query_metrics"

Files:
  - workflow_agent_studio/retrieval/query.py
  - workflow_agent_studio/retrieval/evidence.py
  - tests/integration/test_retrieval_query.py
  - tests/eval/test_retrieval_eval.py
  - docs/retrieval_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#query-time-pipeline
  - docs/IMPLEMENTATION_CONTRACT.md#insufficient_evidence-path
  - docs/IMPLEMENTATION_REFERENCE_MAP.md#recommended-use-by-task

Execution-Mode: heavy
Evidence:
  - docs/retrieval_eval.md query metrics row
  - tests/integration/test_retrieval_query.py::test_query_without_support_returns_insufficient_evidence
Verifier-Focus: |
  Confirm unsupported questions cannot be converted into fabricated evidence or generated claims.

---

## Phase 4: Extraction, Synthesis, and Validation

Business goal: produce validated, evidence-linked automation blueprints from ingested sources and retrieved patterns.

## T12: Structured LLM Gateway

Owner:      codex
Phase:      4
Type:       none
Depends-On: T04, T05

Objective: |
  Implement a provider-neutral LLM gateway that requests structured outputs, validates responses against Pydantic schemas, tracks aggregate cost and latency, and returns typed errors on schema failure.

Acceptance-Criteria:
  - id: AC-1
    description: "The fake LLM provider can return a valid structured payload that validates into the requested Pydantic model."
    test: "tests/unit/test_llm_gateway.py::test_fake_provider_returns_valid_structured_output"
  - id: AC-2
    description: "A malformed provider response returns `SchemaValidationError` with model name and validation error count."
    test: "tests/unit/test_llm_gateway.py::test_malformed_response_returns_schema_validation_error"
  - id: AC-3
    description: "LLM call metrics record provider, model, latency milliseconds, token counts when supplied, and no prompt text."
    test: "tests/unit/test_llm_gateway.py::test_llm_metrics_exclude_prompt_text"

Files:
  - workflow_agent_studio/llm/__init__.py
  - workflow_agent_studio/llm/gateway.py
  - workflow_agent_studio/llm/providers.py
  - workflow_agent_studio/llm/errors.py
  - tests/unit/test_llm_gateway.py

Context-Refs:
  - docs/ARCHITECTURE.md#inference--model-strategy
  - docs/IMPLEMENTATION_CONTRACT.md#model-output-boundary

Notes: |
  Tests must use fake providers only.

## T13: Workflow Extraction Service

Owner:      codex
Phase:      4
Type:       none
Depends-On: T07, T11, T12

Objective: |
  Implement extraction that turns normalized sources and retrieved snippets into typed workflow maps with evidence references and missing-question entries.

Acceptance-Criteria:
  - id: AC-1
    description: "The extraction service returns actors, systems, triggers, steps, decisions, exceptions, data fields, and pain points for the sample SOP fixture."
    test: "tests/integration/test_extraction.py::test_extraction_returns_required_workflow_fields"
  - id: AC-2
    description: "Each extracted workflow step includes at least one evidence reference or an assumption marker."
    test: "tests/integration/test_extraction.py::test_extracted_steps_have_evidence_or_assumption"
  - id: AC-3
    description: "When required source details are absent, extraction returns missing questions with section, question text, and reason."
    test: "tests/integration/test_extraction.py::test_extraction_returns_missing_questions_for_absent_details"

Files:
  - workflow_agent_studio/extraction/__init__.py
  - workflow_agent_studio/extraction/prompts.py
  - workflow_agent_studio/extraction/service.py
  - tests/integration/test_extraction.py

Context-Refs:
  - docs/spec.md#feature-area-workflow-extraction
  - docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems

Notes: |
  The extraction service may call the LLM gateway but must not approve or export blueprints.

## T14: Blueprint Synthesis Service

Owner:      codex
Phase:      4
Type:       plan:schema
Depends-On: T11, T12, T13

Objective: |
  Implement blueprint synthesis that combines extracted workflow maps, retrieved pattern evidence, assumptions, and missing questions into the v1 automation blueprint schema.

Acceptance-Criteria:
  - id: AC-1
    description: "Synthesizing from the complete workflow fixture produces all required blueprint sections in schema version v1."
    test: "tests/integration/test_blueprint_synthesis.py::test_synthesis_produces_all_required_sections"
  - id: AC-2
    description: "Automation candidates include implementation boundary, human approval boundary, risk level, and evidence references."
    test: "tests/integration/test_blueprint_synthesis.py::test_automation_candidates_include_boundaries_risk_and_evidence"
  - id: AC-3
    description: "Eval cases include input condition, expected behavior, evidence reference, and measurable verification method."
    test: "tests/integration/test_blueprint_synthesis.py::test_eval_cases_include_measurable_verification"
  - id: AC-4
    description: "`docs/plan_eval.md` records the first blueprint synthesis fixture result and section-coverage score."
    test: "tests/eval/test_plan_eval.py::test_plan_eval_records_synthesis_coverage"

Files:
  - workflow_agent_studio/blueprint/__init__.py
  - workflow_agent_studio/blueprint/prompts.py
  - workflow_agent_studio/blueprint/service.py
  - tests/integration/test_blueprint_synthesis.py
  - tests/eval/test_plan_eval.py
  - docs/plan_eval.md

Context-Refs:
  - docs/spec.md#feature-area-blueprint-generation
  - docs/ARCHITECTURE.md#profile-planning

Notes: |
  Keep the blueprint as a typed draft until T15 validation passes.

## T15: Blueprint Validation Gate

Owner:      codex
Phase:      4
Type:       plan:validation
Depends-On: T08, T14

Objective: |
  Implement the deterministic validation gate that blocks approval and approved export until blueprint completeness, evidence coverage, forbidden-claim, eval-case, and approval-boundary rules pass.

Acceptance-Criteria:
  - id: AC-1
    description: "A blueprint missing approval boundaries receives a blocking validation finding with section `approval_boundaries`."
    test: "tests/unit/test_blueprint_validators.py::test_missing_approval_boundaries_blocks_approval"
  - id: AC-2
    description: "A blueprint claim without evidence or assumption receives a blocking evidence-coverage finding."
    test: "tests/unit/test_blueprint_validators.py::test_unsupported_claim_blocks_approval"
  - id: AC-3
    description: "A blueprint with zero eval cases receives a blocking validation finding with section `eval_cases`."
    test: "tests/unit/test_blueprint_validators.py::test_missing_eval_cases_blocks_approval"
  - id: AC-4
    description: "`docs/plan_eval.md` records validation pass rate and blocking-finding counts for the fixture set."
    test: "tests/eval/test_plan_eval.py::test_plan_eval_records_validation_gate_metrics"

Files:
  - workflow_agent_studio/validators/blueprint.py
  - workflow_agent_studio/blueprint/service.py
  - tests/unit/test_blueprint_validators.py
  - tests/eval/test_plan_eval.py
  - docs/plan_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#plan-validation
  - docs/IMPLEMENTATION_CONTRACT.md#profile-rules-planning

Execution-Mode: heavy
Evidence:
  - docs/plan_eval.md validation gate metrics row
  - tests/unit/test_blueprint_validators.py::test_unsupported_claim_blocks_approval
Verifier-Focus: |
  Confirm polished but underspecified blueprints cannot be approved or exported as approved.

---

## Phase 5: Review, Export, and End-to-End CLI

Business goal: complete the operator workflow from source import to reviewable blueprint and local Markdown export.

## T16: Review State and Blueprint Versioning

Owner:      codex
Phase:      5
Type:       plan:validation
Depends-On: T06, T15

Objective: |
  Implement review state transitions, immutable blueprint versions, approval blocking on validator findings, and audit events for edits and approvals.

Acceptance-Criteria:
  - id: AC-1
    description: "Editing a blueprint creates a new version and leaves the previous version unchanged."
    test: "tests/integration/test_review_state.py::test_blueprint_edit_creates_new_version"
  - id: AC-2
    description: "Attempting to approve a blueprint with blocking findings raises `ApprovalBlockedError`."
    test: "tests/integration/test_review_state.py::test_blocking_findings_prevent_approval"
  - id: AC-3
    description: "Approving a valid blueprint stores reviewer label, timestamp, version ID, and audit event."
    test: "tests/integration/test_review_state.py::test_valid_blueprint_approval_records_audit_event"

Files:
  - workflow_agent_studio/blueprint/review.py
  - workflow_agent_studio/storage/repositories.py
  - tests/integration/test_review_state.py
  - docs/plan_eval.md

Context-Refs:
  - docs/spec.md#feature-area-review-and-approval

Notes: |
  Reviewer identity can be a local operator label in v1.

## T17: Markdown Export

Owner:      codex
Phase:      5
Type:       none
Depends-On: T15, T16

Objective: |
  Implement local Markdown export for draft and approved blueprints with stable section order, evidence appendix, draft markers, and unresolved findings.

Acceptance-Criteria:
  - id: AC-1
    description: "Exporting a draft blueprint writes Markdown with `Status: Draft` and an unresolved findings section."
    test: "tests/integration/test_markdown_export.py::test_draft_export_includes_status_and_findings"
  - id: AC-2
    description: "Exporting an approved blueprint writes Markdown with blueprint version ID and evidence appendix."
    test: "tests/integration/test_markdown_export.py::test_approved_export_includes_version_and_evidence_appendix"
  - id: AC-3
    description: "The exporter rejects output paths outside the operator-provided export directory."
    test: "tests/unit/test_export_paths.py::test_export_rejects_paths_outside_export_directory"

Files:
  - workflow_agent_studio/export/__init__.py
  - workflow_agent_studio/export/markdown.py
  - workflow_agent_studio/export/paths.py
  - tests/integration/test_markdown_export.py
  - tests/unit/test_export_paths.py

Context-Refs:
  - docs/spec.md#feature-area-markdown-export
  - docs/IMPLEMENTATION_CONTRACT.md#local-export-boundary

Notes: |
  Do not add GitHub issue creation in this task.

## T18: End-to-End CLI Workflow

Owner:      codex
Phase:      5
Type:       rag:query plan:validation
Depends-On: T07, T11, T13, T15, T17

Objective: |
  Wire the CLI workflow so an operator can create a run from local sources, build the retrieval index, generate a draft blueprint, validate it, and export Markdown.

Acceptance-Criteria:
  - id: AC-1
    description: "Running the CLI on the sample SOP fixture creates a run, stores sources, generates a draft blueprint, and prints the blueprint version ID."
    test: "tests/integration/test_cli_workflow.py::test_cli_generates_draft_blueprint_from_sample_sop"
  - id: AC-2
    description: "The CLI exits with code 2 and prints validator finding IDs when the generated blueprint has blocking findings."
    test: "tests/integration/test_cli_workflow.py::test_cli_returns_code_2_for_blocking_findings"
  - id: AC-3
    description: "The CLI export command writes a Markdown file containing workflow summary, automation candidates, eval cases, and evidence appendix."
    test: "tests/integration/test_cli_workflow.py::test_cli_export_writes_blueprint_markdown"
  - id: AC-4
    description: "`docs/retrieval_eval.md` and `docs/plan_eval.md` contain current evaluation rows for the end-to-end fixture run."
    test: "tests/eval/test_end_to_end_eval.py::test_eval_artifacts_record_end_to_end_fixture"

Files:
  - workflow_agent_studio/cli.py
  - workflow_agent_studio/pipeline.py
  - tests/integration/test_cli_workflow.py
  - tests/eval/test_end_to_end_eval.py
  - docs/retrieval_eval.md
  - docs/plan_eval.md

Context-Refs:
  - docs/ARCHITECTURE.md#data-flow
  - docs/spec.md#overview
  - docs/retrieval_eval.md#evaluation-history
  - docs/plan_eval.md#evaluation-history
  - docs/IMPLEMENTATION_REFERENCE_MAP.md#recommended-use-by-task

Execution-Mode: heavy
Evidence:
  - tests/integration/test_cli_workflow.py::test_cli_generates_draft_blueprint_from_sample_sop
  - docs/retrieval_eval.md end-to-end row
  - docs/plan_eval.md end-to-end row
Verifier-Focus: |
  Confirm the full workflow remains bounded and review-first: no external side effects, no approved export without validation, and no fabricated evidence.

## T19: Operator Documentation and Sample Corpus

Owner:      codex
Phase:      5
Type:       none
Depends-On: T18

Objective: |
  Document the v1 operator workflow, local setup, sample corpus format, safety boundaries, evaluation commands, and known non-goals.

Acceptance-Criteria:
  - id: AC-1
    description: "`README.md` includes setup commands, required environment variables, a sample run command, and the local export command."
    test: "tests/unit/test_docs.py::test_readme_contains_setup_and_sample_commands"
  - id: AC-2
    description: "`docs/operator_guide.md` states that v1 does not create agents, deploy automations, or mutate production systems."
    test: "tests/unit/test_docs.py::test_operator_guide_states_v1_non_goals"
  - id: AC-3
    description: "`docs/evaluation_guide.md` lists the retrieval and plan eval commands and the metrics each command updates."
    test: "tests/unit/test_docs.py::test_evaluation_guide_lists_eval_commands_and_metrics"

Files:
  - README.md
  - docs/operator_guide.md
  - docs/evaluation_guide.md
  - patterns/README.md
  - tests/unit/test_docs.py

Context-Refs:
  - docs/ARCHITECTURE.md#non-goals
  - docs/retrieval_eval.md
  - docs/plan_eval.md

Notes: |
  Keep documentation factual. Do not add pre-evidence claims that the system replaces discovery calls or builds production agents.

## T20: Pilot Proof Metric Measurement

Owner:      codex
Phase:      5
Type:       plan:validation
Depends-On: T18, T19

Objective: |
  Add a pilot measurement artifact that records time-to-blueprint, required-section acceptance rate, reviewer edits, and critical missing-question count for the first real workflow brief.

Acceptance-Criteria:
  - id: AC-1
    description: "`docs/pilot_measurement.md` defines fields for workflow source duration, time-to-reviewable-blueprint, required-section acceptance rate, reviewer edit count, and critical missing-question count."
    test: "tests/unit/test_docs.py::test_pilot_measurement_defines_proof_metric_fields"
  - id: AC-2
    description: "The pilot measurement template includes pass/fail thresholds for under 30 minutes and at least 80 percent required-section acceptance after human review."
    test: "tests/unit/test_docs.py::test_pilot_measurement_includes_v1_thresholds"
  - id: AC-3
    description: "`docs/evaluation_guide.md` links to `docs/pilot_measurement.md` as the artifact for the first proof metric."
    test: "tests/unit/test_docs.py::test_evaluation_guide_links_pilot_measurement_artifact"

Files:
  - docs/pilot_measurement.md
  - docs/evaluation_guide.md
  - tests/unit/test_docs.py

Context-Refs:
  - docs/ARCHITECTURE.md#problem-fit-and-adoption-reality
  - docs/EVIDENCE_INDEX.md

Notes: |
  This task records the first adoption proof metric. It does not claim the metric has passed until a real pilot row is filled after human review.
