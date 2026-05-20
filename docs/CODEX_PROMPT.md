# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 10

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 10 - Pre-Pilot Hardening
- Next task: T44 - Vertical Pack Dry-Run Evaluation
- Verified baseline: 147 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34/T40 remain blocked until real pilot evidence exists; synthetic fixtures cannot satisfy pilot proof.
- Completed product baseline: Phase 0 / local evidence-linked MVP

## Active References

- Product strategy: `docs/product_strategy.md`
- Active task graph: `docs/tasks.md`
- Implementation contract: `docs/IMPLEMENTATION_CONTRACT.md`
- Architecture: `docs/ARCHITECTURE.md`
- Feature spec: `docs/spec.md`
- Retrieval eval: `docs/retrieval_eval.md`
- Planning eval: `docs/plan_eval.md`
- Operator guide: `docs/operator_guide.md`

## Next Task Digest

Task: T44 - Vertical Pack Dry-Run Evaluation

Goal: evaluate vertical-pack mechanics on synthetic fixtures without claiming a real wedge.

Acceptance summary:

- dry-run compares generic and vertical-pack expectations on synthetic fixtures
- results are labeled not pilot evidence
- T34 remains blocked until real pilot evidence exists

File scope:

- `patterns/`
- `tests/fixtures/benchmarks/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

Required context:

- `docs/tasks.md#t44-vertical-pack-dry-run-evaluation`
- `docs/tasks.md#t34-first-vertical-pack-from-pilot-evidence`
- `tests/fixtures/benchmarks/`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: vertical pack dry-run evaluation
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: vertical pack dry-run evaluation
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
- Latest phase review: `docs/archive/CYCLE20_PHASE8_INTEGRATIONS_HANDOFF_REVIEW.md`
