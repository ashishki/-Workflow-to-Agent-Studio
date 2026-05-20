# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 1

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 1 - Evidence Capture And Corpus Expansion
- Next task: T24 - Real-World Corpus Fixture Baseline
- Verified baseline: 91 passing tests, 0 skipped, 0 failed
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

Task: T24 - Real-World Corpus Fixture Baseline

Goal: add a small realistic corpus pack and baseline metrics for source coverage, evidence gaps, and generated blueprint usefulness.

Acceptance summary:

- corpus fixtures include at least one transcript, one notes file, one form description, and one integration excerpt
- retrieval eval records corpus count, chunk count, and citation support metrics
- plan eval records required-section coverage and evidence-gap metrics
- README points next contributors to the corpus and eval commands

File scope:

- `tests/fixtures/sources/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`
- `README.md`
- `tests/eval/`

Required context:

- `docs/product_strategy.md#market-lens`
- `docs/evaluation_guide.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: real-world corpus baseline
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
