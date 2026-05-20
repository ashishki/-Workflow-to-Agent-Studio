# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-20
Phase: 9

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 9 - Learning System And Moat
- Next task: T39 - Reviewer Feedback Taxonomy
- Verified baseline: 136 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`
- Last updated: 2026-05-20
- Open findings: T34 and T40 currently form a dependency cycle; tracked as Cycle 20 P2.
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

Task: T39 - Reviewer Feedback Taxonomy

Goal: classify reviewer edits into reusable feedback categories.

Acceptance summary:

- taxonomy captures missing evidence, wrong boundary, weak eval, wrong integration, unclear risk, and unsupported claim
- feedback is stored without raw confidential source text
- plan eval records feedback category coverage

File scope:

- `workflow_agent_studio/blueprint/review.py`
- `workflow_agent_studio/domain/review.py`
- `docs/plan_eval.md`
- `tests/integration/test_review_state.py`

Required context:

- `docs/tasks.md#t39-reviewer-feedback-taxonomy`
- `docs/IMPLEMENTATION_CONTRACT.md#source-confidentiality`
- `docs/plan_eval.md`

## Profile State

RAG: ON

- Current mode: text-only
- Next work: learning-system fixtures after feedback taxonomy
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: reviewer feedback taxonomy
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
