# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 6

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 7 - Pilot Proof And Commercial Packaging
- Next task: T35 - Real Pilot Measurement Row
- Verified baseline: 125 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34 and T40 currently form a dependency cycle, so T35 is the next eligible task.
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

Task: T35 - Real Pilot Measurement Row

Goal: record the first real pilot measurement without overstating product maturity.

Acceptance summary:

- `docs/pilot_measurement.md` contains one reviewed real pilot row or explicitly remains template-only
- pass/fail result is based on time-to-blueprint and required-section acceptance thresholds
- reviewer edits and critical missing questions are recorded

File scope:

- `docs/pilot_measurement.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`

Required context:

- `docs/tasks.md#t35-real-pilot-measurement-row`
- `docs/evaluation_guide.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: pilot evidence and later vertical-pack validation
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: pilot measurement thresholds and evidence-backed validation
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
