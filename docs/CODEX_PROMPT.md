# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 1

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 1 - Evidence Capture And Corpus Expansion
- Next task: T22 - Notes, Forms, And Integration Snippet Ingestion
- Verified baseline: 83 passing tests, 0 skipped, 0 failed
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

Task: T22 - Notes, Forms, And Integration Snippet Ingestion

Goal: support common discovery artifacts beyond transcripts: pasted notes, form descriptions, and API or integration excerpts.

Acceptance summary:

- each supported source kind is represented in source metadata
- unsupported file types fail with a clear nonzero CLI error and no partial persisted source
- fixtures cover notes, form descriptions, and integration snippets
- ingestion docs explain supported source kinds and local-only boundaries

File scope:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/cli.py`
- `docs/operator_guide.md`
- `tests/integration/test_ingestion.py`
- `tests/unit/test_docs.py`

Required context:

- `docs/spec.md#feature-area-source-ingestion`
- `docs/IMPLEMENTATION_CONTRACT.md#source-confidentiality`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: notes/forms/integration snippet ingestion, evidence anchors, and corpus baseline
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
