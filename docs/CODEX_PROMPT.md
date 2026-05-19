# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-19
Phase: 1

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 1 - Evidence Capture And Corpus Expansion
- Next task: T21 - Transcript Ingestion
- Verified baseline: 79 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-19
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

Task: T21 - Transcript Ingestion

Goal: add local transcript ingestion for discovery call exports while preserving source confidentiality.

Acceptance summary:

- transcript fixtures with speaker labels ingest into normalized source records
- source fingerprints remain deterministic across whitespace-only transcript changes
- raw transcript text does not appear in logs, spans, or audit labels
- `docs/retrieval_eval.md` records the transcript ingestion fixture result

File scope:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/domain/sources.py`
- `tests/integration/test_ingestion.py`
- `tests/eval/test_retrieval_eval.py`
- `docs/retrieval_eval.md`

Required context:

- `docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag`
- `docs/product_strategy.md#development-phases`
- `docs/tasks.md#t21-transcript-ingestion`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: broader source ingestion, evidence anchors, and corpus baseline
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
