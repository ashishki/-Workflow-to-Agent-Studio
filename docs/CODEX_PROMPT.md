# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 9

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 9 - Learning System And Moat
- Next task: BLOCKED - T34/T40 dependency cycle
- Verified baseline: 139 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34 depends on T40 and T40 depends on T34; human task-graph decision required.
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

Task: BLOCKED - T34/T40 dependency cycle

Goal: unblock the remaining vertical-pack and learning-system tasks.

Acceptance summary:

- T34 requires T40 before implementation
- T40 requires T34 before implementation
- no remaining task is eligible without changing the task graph or dependency interpretation

File scope:

- `docs/tasks.md`

Required context:

- `docs/tasks.md#t34-first-vertical-pack-from-pilot-evidence`
- `docs/tasks.md#t40-pattern-learning-and-benchmark-corpus`
- `docs/IMPLEMENTATION_CONTRACT.md#nonstop-development-loop`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked pending task-graph decision
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: blocked pending task-graph decision
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
