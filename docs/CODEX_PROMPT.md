# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-21
Phase: 11

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 11 - Public-Source Demo Quality
- Next task: BLOCKED - Real prospect/customer workflow data required
- Verified baseline: 171 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-21
- Open findings: T34/T40 remain blocked until real pilot evidence exists; use public sources for demo-quality stabilization only.
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

Task: BLOCKED - Real prospect/customer workflow data required

Goal: resume pilot proof work after a potential customer supplies a real workflow source and reviewer.

Acceptance summary:

- public-source corpus now covers NetBox, Kubernetes, OpenStack, and GitLab workflows
- public-source demo pack and prospect data request gate are complete
- T34/T40 remain blocked until prospect/customer data is reviewed as a real pilot
- first real pilot row requires a named reviewer, measured thresholds, edits, and critical missing-question count

File scope:

- `docs/pilot_measurement.md`

Required context:

- `docs/pilot_measurement.md#prospect-data-request-gate`
- `docs/pilot_measurement.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: public-source workflow fact preservation evals
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: public-source workflow fact preservation evals
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
