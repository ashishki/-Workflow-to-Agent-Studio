# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-23
Phase: 12

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 12 - Solo Public Workflow Showcase
- Next task: T53 Three Public Blueprint Showcase Packs
- Verified baseline: 179 passing tests, 0 skipped, 0 failed
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

Task: T53 Three Public Blueprint Showcase Packs

Goal: produce three reproducible public-source demo packs that show the product
can turn public workflow evidence into useful automation blueprints.

Acceptance summary:

- one pack covers lead intake
- one pack covers public issue/support triage
- one pack covers an operations workflow such as onboarding, invoice approval,
  or incident response
- each pack includes source fixture/register, command transcript, generated
  blueprint, review workspace, gap summary, and boundary label

File scope:

- `docs/experiments/public_demo_pack/`
- `tests/fixtures/public_sources/`
- `docs/evaluation_guide.md`

Required context:

- `docs/tasks.md#phase-12-solo-public-workflow-showcase`
- `docs/open_source_research_protocol.md`
- `docs/experiments/public_sources/lead_intake/source_register.md`

## Evaluation State

Last Evaluation:

- Task: T52
- Date: 2026-05-23
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_retrieval_eval.py tests/eval/test_plan_eval.py -q
- Result: HVAC lead-intake public corpus coverage recorded in retrieval and planning evals

## Profile State

RAG: ON

- Current mode: text-only
- Next work: three public blueprint showcase packs
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: three public blueprint showcase packs
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
