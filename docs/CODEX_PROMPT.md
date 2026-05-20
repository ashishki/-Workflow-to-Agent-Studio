# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 10

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 10 - Pre-Pilot Hardening
- Next task: BLOCKED - Real pilot evidence required for T34/T40
- Verified baseline: 156 passing tests, 0 skipped, 0 failed
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

Task: BLOCKED - Real pilot evidence required for T34/T40

Goal: complete remaining vertical-pack and learning-system tasks when real pilot evidence exists.

Acceptance summary:

- T34 needs real pilot evidence to identify the strongest wedge
- T40 needs approved sanitized outcomes from a real pilot
- demo, synthetic, dry-run, and sanitized-only fixtures cannot satisfy pilot proof

File scope:

- `docs/pilot_measurement.md`

Required context:

- `docs/tasks.md#t34-first-vertical-pack-from-pilot-evidence`
- `docs/tasks.md#t40-pattern-learning-and-benchmark-corpus`
- `docs/pilot_measurement.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked pending real pilot evidence or a new task graph extension
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: blocked pending real pilot evidence or a new task graph extension
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
- Latest phase review: `docs/archive/CYCLE21_PHASE10_PRE_PILOT_HARDENING_REVIEW.md`
