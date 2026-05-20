# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 10

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 10 - Pre-Pilot Hardening
- Next task: T41 - Synthetic Benchmark Harness
- Verified baseline: 139 passing tests, 0 skipped, 0 failed
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

Task: T41 - Synthetic Benchmark Harness

Goal: create a synthetic-only benchmark harness for regression testing without satisfying real-pilot evidence gates.

Acceptance summary:

- synthetic benchmark fixtures are explicitly labeled as not pilot evidence
- harness reports retrieval and planning fixture coverage deterministically
- eval docs state synthetic results cannot satisfy T34 or commercial pilot proof

File scope:

- `tests/fixtures/benchmarks/`
- `workflow_agent_studio/eval/`
- `tests/eval/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

Required context:

- `docs/tasks.md#t41-synthetic-benchmark-harness`
- `docs/pilot_measurement.md`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: synthetic benchmark harness
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: synthetic benchmark harness
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
