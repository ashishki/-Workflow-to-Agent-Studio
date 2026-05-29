# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-29
Phase: 13

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 13 - Workflow-To-Agent Framework Upgrade
- Next task: T59 - Design Diversity Candidate Set
- Verified baseline: 199 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`; ruff format check passing
- Last updated: 2026-05-29
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete

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

Task: T59 - Design Diversity Candidate Set

Goal: add a candidate design model that can represent several bounded
agent/workflow architectures for the same source evidence.

Acceptance summary:

- candidate schema supports deterministic-first, human-in-the-loop,
  bounded-agent, high-autonomy, compliance-heavy, and low-cost MVP variants
- each candidate records autonomy level, required tools, human approvals,
  runtime tier, eval needs, risks, cost posture, and evidence gaps
- validators reject candidates that lack approval boundaries or eval plan
- tests cover schema validation and missing-field rejection

File scope:

- `workflow_agent_studio/domain/`
- `workflow_agent_studio/validators/`
- `tests/unit/`
- `docs/plan_eval.md`
- `docs/CODEX_PROMPT.md`

Required context:

- `docs/tasks.md#phase-13-workflow-to-agent-framework-upgrade`
- `docs/PROJECT_PLAN.md#near-term-roadmap`
- `docs/ARCHITECTURE.md#solution-shape-selection`

## Evaluation State

Last Evaluation:

- Task: T58
- Date: 2026-05-29
- Eval Source: .venv/bin/pytest -q; .venv/bin/ruff check workflow_agent_studio tests/; .venv/bin/ruff format --check workflow_agent_studio tests/
- Result: framework positioning refresh complete; customer proof still blocked

## Profile State

RAG: ON

- Current mode: text-only
- Next work: T59 design diversity schema
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: T59 design diversity candidate schema and T60 generation flow
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
