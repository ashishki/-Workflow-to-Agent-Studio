# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 11

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 11 - Public-Source Demo Quality
- Next task: T50 - Prospect Data Request Gate
- Verified baseline: 161 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34/T40 remain blocked until real pilot evidence exists; use public sources for demo-quality stabilization only.
- Latest public-source demo pack: `docs/experiments/public_demo_pack/netbox_issue_triage/`.
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

Task: T50 - Prospect Data Request Gate

Goal: define when public-source quality is stable enough to ask potential customers for real workflow data.

Acceptance summary:

- gate requires stable public-source evals before prospect data requests
- request checklist states minimum safe source types and confidentiality boundary
- T34/T40 remain blocked until prospect/customer data is reviewed as a real pilot

File scope:

- `docs/pilot_measurement.md`
- `docs/product_strategy.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`

Required context:

- `docs/tasks.md#t50-prospect-data-request-gate`
- `docs/experiments/public_demo_pack/netbox_issue_triage/`
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
