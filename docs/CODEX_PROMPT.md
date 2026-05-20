# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 5

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 5 - Review Workspace And Human Editing
- Next task: T32 - Review Workspace Interface
- Verified baseline: 119 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: none
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

Task: T32 - Review Workspace Interface

Goal: provide the smallest useful local review interface, CLI or UI, for editing and approving blueprint sections.

Acceptance summary:

- reviewer can inspect findings, evidence, comments, and version history
- reviewer can create an edited draft and export it locally
- interface documentation stays operator-focused and does not claim autonomous deployment

File scope:

- `workflow_agent_studio/cli.py`
- `docs/operator_guide.md`
- `tests/integration/`

Required context:

- `docs/ARCHITECTURE.md#profile-planning`
- `docs/plan_eval.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: review comments, diffs, and local review interface
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: evidence gaps and readiness validation in later phases
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
