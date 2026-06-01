# CODEX_PROMPT.md

Version: 2.0
Date: 2026-06-01
Phase: 14

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 14 - SMB AI Roadmap Product Layer
- Next task: T66 - Costing Domain Model
- Verified baseline: T65 pre-change baseline was 225 passing tests, 0 skipped, 0 failed; T65 completion baseline is 238 passing tests, 0 skipped, 0 failed
- Ruff: `ruff check` and `ruff format --check` pass for the full repository after T65
- Last updated: 2026-06-01
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete; T59 design candidate schema complete; T60 diverse generation flow complete; T61 Playbook export complete; T62 permission/runtime boundary pack complete; T63 framework readiness review complete; SMB AI roadmap documentation package created and indexed at `docs/AI_ROADMAP_STUDIO_INDEX.md`; T64 privacy classification schema complete; T65 recommendation card schema complete

## Active References

- Product strategy: `docs/product_strategy.md`
- SMB roadmap index: `docs/AI_ROADMAP_STUDIO_INDEX.md`
- Roadmap report contract: `docs/product/report_contract.md`
- Active task graph: `docs/tasks.md`
- Implementation contract: `docs/IMPLEMENTATION_CONTRACT.md`
- Architecture: `docs/ARCHITECTURE.md`
- Feature spec: `docs/spec.md`
- Retrieval eval: `docs/retrieval_eval.md`
- Planning eval: `docs/plan_eval.md`
- Operator guide: `docs/operator_guide.md`

## Next Task Digest

Task: T65 - Recommendation Card Schema

Status: complete.

Task: T66 - Costing Domain Model

Goal: implement cost estimate schemas with one-time/monthly ranges,
assumptions, confidence, and price-card references.

Acceptance summary:

- low, medium, and high cost ordering is validated
- estimate without assumptions fails validation
- estimate confidence supports low, medium, and high
- monthly and one-time costs can be represented separately
- unit tests cover invalid ordering and missing assumptions

File scope:

- `workflow_agent_studio/domain/costing.py`
- `tests/unit/test_costing_schema.py`

Required context:

- `docs/methodology/cost_estimation.md`
- `docs/evals/cost_estimation_eval.md`

## Evaluation State

Last Evaluation:

- Task: T65
- Date: 2026-06-01
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_recommendation_schema.py -q`
- Result: 13 passed; full repository verification passed with 238 tests

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked until real workflow data is reviewed
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1
- Next work: RoadmapReport v1, costing, scoring,
  and verification schemas for SMB implementation planning
- Open planning findings: none

Tool-Use: OFF

Agentic: OFF

Compliance: OFF

- Phase 14 adds privacy/security controls for roadmap planning, but the project
  still does not claim a named regulatory compliance framework.

## Archived State

- Completed V1 task graph: `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Completed V1 prompt state: `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- Prior long orchestrator prompt: `docs/archive/ORCHESTRATOR_V2_LONG.md`
- Original phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`
- Latest phase review: `docs/archive/CYCLE21_PHASE10_PRE_PILOT_HARDENING_REVIEW.md`
