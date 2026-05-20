# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 10

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 10 - Pre-Pilot Hardening
- Next task: T43 - Pilot Intake Checklist
- Verified baseline: 145 passing tests, 0 skipped, 0 failed
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

Task: T43 - Pilot Intake Checklist

Goal: document and validate the exact evidence needed to convert a future real pilot into a measurement row.

Acceptance summary:

- checklist enumerates required source material, reviewer actions, thresholds, and missing-question rules
- checklist distinguishes real pilot evidence from demo or synthetic fixtures
- docs tests prevent pilot proof claims while checklist inputs are incomplete

File scope:

- `docs/pilot_measurement.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`
- `docs/operator_guide.md`

Required context:

- `docs/tasks.md#t43-pilot-intake-checklist`
- `docs/pilot_measurement.md`
- `docs/evaluation_guide.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: pilot intake checklist
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: pilot intake checklist
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
