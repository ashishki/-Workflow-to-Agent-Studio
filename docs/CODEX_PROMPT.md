# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-19
Phase: 1

This file is the single source of truth for implementation session state. Every Codex agent reads it before starting work and updates it at phase boundaries.

---

## Current State

- Phase: 1
- Current phase: Foundation and Contracts
- Baseline: 0 passing tests (pre-implementation)
- Ruff: not yet configured
- Last CI: not yet configured
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

T01: Project Skeleton

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

none

---

## Profile State: RAG

- RAG Status: ON
- Retrieval mode: text-only
- Active corpora: current workflow sources and local pattern library
- Retrieval baseline: not yet measured
- Open retrieval findings: none
- Index schema version: v1 planned; not implemented
- Pending reindex actions: none
- Retrieval-related next tasks: T09, T10, T11, T18
- Retrieval-driven tasks: none

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
- Plan schema version: v1 planned; not implemented
- Plan validation method: deterministic Pydantic and validation-rule suite
- Open plan findings: none
- Planning-related next tasks: T05, T14, T15, T16, T18

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

- Profile: n/a
- Task: n/a
- Date: n/a
- Eval Source: n/a
- Metric(s): n/a
- Score: n/a
- Baseline: n/a
- Delta: n/a
- Regression: n/a

### Open Evaluation Issues

none

### Evaluation History

| Date | Task | Profile | Key metric | Score | Baseline | Delta | Regression? |
|------|------|---------|------------|-------|----------|-------|-------------|

---

## Completed Tasks

none

---

## Phase History

none

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
