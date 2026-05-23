# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-23
Phase: 12

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 12 - Solo Public Workflow Showcase
- Next task: BLOCKED - real prospect/customer workflow data required
- Verified baseline: 193 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-23
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
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

Task: BLOCKED - real prospect/customer workflow data required

Goal: resume real pilot proof work after a prospect supplies one real workflow
packet and a named reviewer.

Acceptance summary:

- Phase 12 public-source showcase is ready for manual outreach
- `docs/prospect_data_request_pack.md` is the next operator-facing action
- T34/T40 remain blocked until prospect/customer workflow data is reviewed as a
  real pilot

File scope:

- `docs/pilot_measurement.md`
- `docs/prospect_data_request_pack.md`

Required context:

- `docs/audit/SOLO_SHOWCASE_READINESS_REVIEW.md`
- `docs/pilot_measurement.md#prospect-data-request-gate`

## Evaluation State

Last Evaluation:

- Task: PUBLIC-TEST-1
- Date: 2026-05-23
- Eval Source: pytest -q; ruff check; ruff format --check
- Result: internet workflow fixtures recorded as public-source tests only

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked until real prospect/customer workflow data exists
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: blocked until real prospect/customer workflow data exists
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
