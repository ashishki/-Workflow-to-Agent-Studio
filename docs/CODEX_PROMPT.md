# CODEX_PROMPT.md

Version: 1.22
Date: 2026-05-19
Phase: 5

This file is the single source of truth for implementation session state. Every Codex agent reads it before starting work and updates it at phase boundaries.

Execution policy: development follows a nonstop Codex-only loop. Do not pause between phases after phase review/reporting; continue to the next eligible task unless a formal stop condition in `docs/IMPLEMENTATION_CONTRACT.md` applies.

---

## Current State

- Phase: 5
- Current phase: Review, Export, and End-to-End CLI
- Baseline: 76 passing tests
- Ruff: passing for `workflow_agent_studio tests/`
- Last CI: configured locally; GitHub Actions workflow not yet run remotely
- Last updated: 2026-05-19
- Session tokens (approx): not yet tracked
- Cumulative phase tokens (approx): not yet tracked

---

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Architecture: `docs/ARCHITECTURE.md`
- Task graph: `docs/tasks.md`
- Retrieval evaluation: `docs/retrieval_eval.md`
- Planning evaluation: `docs/plan_eval.md`
- Task-scoped context: read `Context-Refs` in `docs/tasks.md` before broad searching.

---

## Next Task

None — T01 through T20 are complete.

Before implementation, the orchestrator should hand Codex a narrow task digest inline:

- assignment and acceptance criteria
- file scope
- applicable contract rules only
- dependency facts from prior tasks
- immediate pipeline or flow if one matters

Only send Codex to full documents when the task is architecture-shaping, security-sensitive, ambiguous, or otherwise too risky to compress safely.

---

## Fix Queue

empty

---

## Open Findings

| ID | Sev | Description | Files | Status |
|----|-----|-------------|-------|--------|
| CODE-1 | P1 | `WorkflowStep` can validate without evidence references or an assumption marker. | `workflow_agent_studio/domain/workflow.py:26`, `tests/unit/test_blueprint_schema.py:45` | Closed — FIX-1 verified with targeted regression test |
| CODE-2 | P2 | SQLite repository operations are not wrapped in shared tracing spans. | `workflow_agent_studio/storage/repositories.py`, `tests/integration/test_storage.py` | Closed — FIX-2 verified with repository tracing regression test |

---

## Profile State: RAG

- RAG Status: ON
- Retrieval mode: text-only
- Active corpora: current workflow sources and local pattern library
- Retrieval baseline: T07 source ingestion, T09 chunking, T10 index, T11 query, and T18 end-to-end fixture baselines recorded
- Open retrieval findings: none
- Index schema version: v1 implemented by T10
- Pending reindex actions: none
- Retrieval-related next tasks: none
- Retrieval-driven tasks: T07, T09, T10, T11, and T18 completed

---

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

---

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

---

## Planning State

- Planning Profile: ON
- Plan schema version: v1 implemented by T05; FIX-1 evidence-contract repair complete; T14 synthesis coverage baseline recorded; T15 validation gate baseline recorded; T16 review-state approval baseline recorded; T18 end-to-end baseline recorded; T20 pilot template baseline recorded
- Plan validation method: deterministic Pydantic and validation-rule suite
- Open plan findings: none
- Planning-related next tasks: none

---

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

---

## NFR Baseline

- End-to-end workflow latency: not yet measured
- LLM cost per completed brief: not yet measured
- API p99 latency: n/a for CLI-first v1
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: n/a
- NFR regression open: No

---

## Evaluation State

### Last Evaluation

- Profile: Planning
- Task: T20
- Date: 2026-05-19
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric(s): pilot proof metric template coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Regression: No

### Open Evaluation Issues

none

### Evaluation History

| Date | Task | Profile | Key metric | Score | Baseline | Delta | Regression? |
|------|------|---------|------------|-------|----------|-------|-------------|
| 2026-05-19 | T05 | Planning | Schema validation pass rate | 100% | 100% | 0% | No |
| 2026-05-19 | FIX-1 | Planning | Workflow-step evidence contract regression | 100% | 100% | 0% | No |
| 2026-05-19 | T07 | RAG | Source ingestion fixture pass rate | 100% | 100% | 0% | No |
| 2026-05-19 | T09 | RAG | Chunking corpus fixture count | 3 documents / 4 chunks | 3 documents / 4 chunks | 0% | No |
| 2026-05-19 | T10 | RAG | Index metadata and namespace versioning | 100% | 100% | 0% | No |
| 2026-05-19 | T11 | RAG | hit@3 / no-answer / citation baseline | 100% | 100% | 0% | No |
| 2026-05-19 | T14 | Planning | Blueprint synthesis section coverage | 100% | 100% | 0% | No |
| 2026-05-19 | T15 | Planning | Validation fixture outcomes / blocking findings | 100%; 3 blocking findings | 100%; 3 blocking findings | 0% | No |
| 2026-05-19 | T16 | Planning | Review approval gate outcomes | 100%; 2 approvals blocked; 1 approval recorded | 100%; 2 approvals blocked; 1 approval recorded | 0% | No |
| 2026-05-19 | T18 | RAG/Planning | End-to-end CLI fixture | 100%; retrieval 1.00 | 100%; retrieval 1.00 | 0% | No |
| 2026-05-19 | T20 | Planning | Pilot proof metric template coverage | 100% | 100% | 0% | No |
| 2026-05-19 | FIX-2 | Observability | SQLite repository tracing spans | 100% | 100% | 0% | No |

---

## Completed Tasks

- 2026-05-19: T01 Project Skeleton ✅
  - Created Python package skeleton, CLI entry point, dependency metadata, and unit tests.
  - Baseline after task: 3 passing tests, 0 skipped, 0 failed.
  - Ruff: `workflow_agent_studio tests/` passed.
- 2026-05-19: T02 CI Setup ✅
  - Updated GitHub Actions to run Python 3.12 setup, dependency installation, editable install, ruff lint, ruff format check, and pytest.
  - Added CI configuration tests.
  - Baseline after task: 6 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T03 First Smoke Tests ✅
  - Added deterministic health status function and `workflow-agent-studio health` JSON command.
  - Baseline after task: 9 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T04 Configuration and Observability Foundation ✅
  - Added environment-backed settings, PII-safe observability redaction, and the shared tracing module.
  - Baseline after task: 12 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T05 Domain and Blueprint Schemas ✅
  - Added v1 Pydantic domain schemas, minimal valid blueprint fixture, and planning evaluation baseline.
  - Baseline after task: 16 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: FIX-1 Enforce Workflow Step Evidence Contract ✅
  - Closed CODE-1 by requiring workflow steps to include evidence references or `assumption=True`.
  - Baseline after fix: 17 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T06 SQLite Storage and Audit Events ✅
  - Added SQLite schema initialization and repositories for workflow runs, source records, blueprint versions, and audit events.
  - Baseline after task: 20 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T07 Source Ingestion and Fingerprinting ✅
  - Added local text/Markdown source ingestion, deterministic normalization, SHA-256 fingerprinting, duplicate detection, source persistence, and PII-safe ingestion audit event.
  - Updated `docs/retrieval_eval.md` with the T07 source ingestion fixture baseline.
  - Baseline after task: 24 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T08 Sensitive Data and Forbidden Claim Guards ✅
  - Added deterministic sensitive-data scanner, forbidden-claim scanner, and structured logging helper that excludes raw sensitive values.
  - Baseline after task: 27 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T09 Pattern Library and Chunking ✅
  - Added heading-aware source chunking, pattern-library Markdown templates, and pattern loader with corpus type labels.
  - Updated `docs/retrieval_eval.md` with the T09 chunking corpus fixture baseline.
  - Baseline after task: 30 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T10 Embedding and Index Schema ✅
  - Added embedding provider abstraction, deterministic fake embeddings, and local schema-versioned vector index persistence.
  - Updated `docs/retrieval_eval.md` with the T10 index metadata baseline.
  - Baseline after task: 34 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T11 Query-Time Retrieval and Insufficient Evidence ✅
  - Added typed evidence snippets, vector-aware query scoring, deterministic filtering, and `insufficient_evidence` behavior.
  - Updated `docs/retrieval_eval.md` with the T11 query metrics baseline.
  - Baseline after task: 38 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T12 Structured LLM Gateway ✅
  - Added provider-neutral structured-output gateway, fake provider, typed schema validation errors, and prompt-safe call metrics.
  - Baseline after task: 41 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T13 Workflow Extraction Service ✅
  - Added deterministic workflow extraction service with actors, systems, triggers, steps, decisions, exceptions, data fields, pain points, and missing questions.
  - Baseline after task: 44 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T14 Blueprint Synthesis Service ✅
  - Added deterministic blueprint synthesis from extracted workflow maps and retrieved evidence into the v1 automation blueprint schema.
  - Added synthesis coverage integration tests and updated the planning evaluation baseline.
  - Baseline after task: 48 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T15 Blueprint Validation Gate ✅
  - Added deterministic approval validation findings for required sections, evidence coverage, forbidden claims, eval cases, automation boundaries, and implementation task completeness.
  - Updated `docs/plan_eval.md` with validation expected-outcome and blocking-finding metrics.
  - Baseline after task: 54 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T16 Review State and Blueprint Versioning ✅
  - Added immutable edit versioning, approval records, approval audit events, and approval blocking for validation findings.
  - Fixed review-found version mismatch risk so approval validates the exact stored immutable blueprint payload.
  - Updated `docs/plan_eval.md` with review approval gate metrics.
  - Baseline after task: 59 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T17 Markdown Export ✅
  - Added local Markdown export for draft and approved blueprints with stable section order and evidence appendix.
  - Added export path boundary checks and approved-export version payload protection.
  - Baseline after task: 64 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T18 End-to-End CLI Workflow ✅
  - Wired CLI `run` and `export` commands through ingestion, local retrieval index build, evidence retrieval, extraction, synthesis, validation, versioning, and Markdown export.
  - Added insufficient-evidence exit code 2 behavior with printed finding IDs.
  - Updated retrieval and planning eval artifacts with end-to-end fixture rows.
  - Baseline after task: 68 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T19 Operator Documentation and Sample Corpus ✅
  - Added README quickstart, operator guide, evaluation guide, and pattern-library README.
  - Documented v1 non-goals, local setup, sample run/export commands, evaluation commands, and metrics.
  - Updated pattern loader to ignore README documentation files.
  - Baseline after task: 71 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: T20 Pilot Proof Metric Measurement ✅
  - Added `docs/pilot_measurement.md` template with proof metric fields and pass/fail thresholds.
  - Linked the pilot measurement artifact from the evaluation guide.
  - Updated `docs/plan_eval.md` with the T20 pilot template coverage baseline.
  - Baseline after task: 75 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.
- 2026-05-19: FIX-2 Close SQLite Repository Tracing Gap ✅
  - Closed CODE-2 by wrapping SQLite repository operations in shared tracing spans.
  - Added a regression test that monkeypatches the shared tracer and verifies repository span names.
  - Baseline after fix: 76 passing tests, 0 skipped, 0 failed.
  - Ruff check and format check passed.

---

## Phase History

- 2026-05-19: Phase 1 Foundation and Contracts complete.
  - Built package skeleton, CI, smoke health command, settings/observability foundation, and v1 blueprint schema.
  - Deep review Cycle 1 archived at `docs/archive/PHASE1_REVIEW.md`.
  - CODE-1 P1 found and resolved by FIX-1 before Phase 2.
  - Baseline entering Phase 2: 17 passing tests.
- 2026-05-19: Phase 2 Ingestion, Storage, and Safety complete.
  - Built SQLite storage/audit events, source ingestion/fingerprinting, and sensitive-data/forbidden-claim guards.
  - Deep review Cycle 3 archived at `docs/archive/PHASE2_REVIEW.md`.
  - Open P2 CODE-2: DB operations need shared tracing spans.
  - Baseline entering Phase 3: 27 passing tests.
- 2026-05-19: Phase 3 Text-Only Retrieval and Evidence complete.
  - Built chunking, pattern loading, fake embeddings, schema-versioned local index, query-time evidence retrieval, and `insufficient_evidence`.
  - Deep review Cycle 6 archived at `docs/archive/PHASE3_REVIEW.md`.
  - Open P2 CODE-2 carried forward.
  - Baseline entering Phase 4: 38 passing tests.
- 2026-05-19: Phase 4 Extraction, Synthesis, and Validation complete.
  - Built structured-output gateway, deterministic workflow extraction, blueprint synthesis, and deterministic approval validation gate.
  - Deep review Cycle 8 archived at `docs/archive/PHASE4_REVIEW.md`.
  - Open P2 CODE-2 carried forward.
  - Baseline entering Phase 5: 54 passing tests.
- 2026-05-19: Phase 5 Review, Export, and End-to-End CLI complete.
  - Built review/versioning, local Markdown export, end-to-end CLI workflow, operator docs, and pilot measurement template.
  - Deep review Cycle 12 archived at `docs/archive/PHASE5_REVIEW.md`.
  - CODE-2 P2 was closed by FIX-2 after phase completion.
  - Final baseline after FIX-2: 76 passing tests.

---

## Compaction Protocol

Trigger compaction before implementation work when either threshold is met:

- Completed task entries exceed 20.
- Phase history summaries exceed 5.

Compaction keeps the latest active state, open findings, Fix Queue, next task, and evaluation summary in this file. Older detail moves to archived sections or dedicated audit reports.

---

## Instructions for Codex

1. Read the orchestrator's inline task digest first.
2. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
3. Read the full task definition in `docs/tasks.md` before writing code.
4. Read all Depends-On tasks to understand interface contracts.
5. Read task `Context-Refs` and relevant continuity artifacts when the task depends on prior decisions, findings, or evidence.
6. Run `pytest` to capture the current baseline before making changes.
7. Run `ruff check` before implementation once ruff is configured. Fix ruff issues first, in a separate commit.
8. Write tests before or alongside implementation. Every acceptance criterion has a passing test.
9. Update this file at every phase boundary and whenever the next task or baseline changes.
10. Commit with format `type(scope): description`; use one logical change per commit.
11. When done, return `IMPLEMENTATION_RESULT: DONE` with the new baseline and what changed.
12. When blocked, return `IMPLEMENTATION_RESULT: BLOCKED` with the exact blocker.
