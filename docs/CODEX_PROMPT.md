# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-29
Phase: 13

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 13 - Workflow-To-Agent Framework Upgrade
- Next task: none - Phase 13 active task graph complete
- Verified baseline: 216 passing tests, 0 skipped, 0 failed
- Ruff: passing for `workflow_agent_studio tests/`; ruff format check passing
- Last updated: 2026-05-29
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete; T59 design candidate schema complete; T60 diverse generation flow complete; T61 Playbook export complete; T62 permission/runtime boundary pack complete; T63 framework readiness review complete

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

Task: none - Phase 13 complete

Goal: stop under the contract condition that all active tasks are complete.

Acceptance summary:

- constrained framework demo is allowed
- real pilot, buyer proof, T34, and T40 remain blocked until human-reviewed real
  workflow data is recorded
- next operator-facing action remains `docs/prospect_data_request_pack.md`

File scope:

- `docs/CODEX_PROMPT.md`

Required context:

- `docs/audit/FRAMEWORK_READINESS_REVIEW.md`
- `docs/prospect_data_request_pack.md`

## Evaluation State

Last Evaluation:

- Task: T63
- Date: 2026-05-29
- Eval Source: .venv/bin/pytest -q; .venv/bin/ruff check workflow_agent_studio tests/; .venv/bin/ruff format --check workflow_agent_studio tests/
- Result: framework ready for constrained demo; customer proof still blocked

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked until real workflow data is reviewed
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1
- Next work: blocked until real workflow data is reviewed
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
