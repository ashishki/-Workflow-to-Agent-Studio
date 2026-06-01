# CODEX_PROMPT.md

Version: 2.0
Date: 2026-06-01
Phase: 14

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 14 - SMB AI Roadmap Product Layer
- Next task: T64 - Privacy Domain Model
- Verified baseline: 216 passing tests, 0 skipped, 0 failed from the prior framework loop; current documentation prep check passed with `tests/unit/test_docs.py` at 24 passing tests
- Ruff: previously passing for `workflow_agent_studio tests/`; rerun focused ruff after T64 code changes
- Last updated: 2026-06-01
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete; T59 design candidate schema complete; T60 diverse generation flow complete; T61 Playbook export complete; T62 permission/runtime boundary pack complete; T63 framework readiness review complete; SMB AI roadmap documentation package created and indexed at `docs/AI_ROADMAP_STUDIO_INDEX.md`

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

Task: T64 - Privacy Domain Model

Goal: add typed privacy classes and classification result schemas used by
roadmap recommendations and policy gates.

Acceptance summary:

- privacy classes include public, internal, confidential, sensitive, and
  restricted
- unknown privacy classes fail Pydantic validation
- schema can represent detected flags, redaction status, source privacy class,
  and recommendation privacy class
- unit tests cover valid classes and invalid class rejection

File scope:

- `workflow_agent_studio/domain/privacy.py`
- `tests/unit/test_privacy_schema.py`

Required context:

- `docs/security/data_classification.md`
- `docs/security/privacy_modes.md`
- `docs/product/report_contract.md`

## Evaluation State

Last Evaluation:

- Task: roadmap documentation prep
- Date: 2026-06-01
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_docs.py -q`
- Result: 24 passed; full pytest and ruff should be rerun after the first Phase 14 code task

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked until real workflow data is reviewed
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1
- Next work: RoadmapReport v1, RecommendationCard, privacy, costing, scoring,
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
