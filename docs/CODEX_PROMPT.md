# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 8

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 8 - Integrations And Controlled Handoff
- Next task: T37 - Controlled Import Connectors
- Verified baseline: 127 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34 and T40 currently form a dependency cycle; tracked as Cycle 19 P2.
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

Task: T37 - Controlled Import Connectors

Goal: add connector architecture for read-only imports while preserving local confidentiality and auditability.

Acceptance summary:

- connector credentials are environment-backed and never persisted
- imports are read-only and produce source records with connector metadata
- connector failures do not corrupt existing runs

File scope:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/config.py`
- `docs/ARCHITECTURE.md`
- `tests/integration/`

Required context:

- `docs/tasks.md#t37-controlled-import-connectors`
- `docs/IMPLEMENTATION_CONTRACT.md#credentials`
- `docs/IMPLEMENTATION_CONTRACT.md#source-confidentiality`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: read-only connector imports with local corpus isolation
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: controlled handoff export after approved pilot gates
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
- Latest phase review: `docs/archive/CYCLE19_PHASE7_PILOT_PACKAGE_REVIEW.md`
