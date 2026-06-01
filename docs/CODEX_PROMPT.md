# CODEX_PROMPT.md

Version: 2.0
Date: 2026-06-01
Phase: 14

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 14 - SMB AI Roadmap Product Layer
- Next task: T73 - SMB Implementation Pattern Schema
- Verified baseline: T72 pre-change baseline was 297 passing tests, 0 skipped, 0 failed; T72 completion baseline is 302 passing tests, 0 skipped, 0 failed
- Ruff: `ruff check` and `ruff format --check` pass for the full repository after T72
- Last updated: 2026-06-01
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete; T59 design candidate schema complete; T60 diverse generation flow complete; T61 Playbook export complete; T62 permission/runtime boundary pack complete; T63 framework readiness review complete; SMB AI roadmap documentation package created and indexed at `docs/AI_ROADMAP_STUDIO_INDEX.md`; T64 privacy classification schema complete; T65 recommendation card schema complete; T66 costing schema complete; T67 scoring schema complete; T68 verification schema complete; T69 roadmap report aggregate schema complete; T70 deterministic privacy classifier complete; T71 redaction preview complete; T72 privacy policy gate complete

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

Task: T72 - Cloud Private Local Policy Gate

Status: complete.

Task: T73 - SMB Implementation Pattern Schema

Goal: implement schema and loader for versioned SMB implementation patterns.

Acceptance summary:

- pattern schema validates pattern ID, version, signals, required data, privacy
  default, architecture, risks, eval metrics, and when-not-to-use
- invalid JSON pattern fails with a clear validation error
- loader returns pattern version metadata
- unit tests validate every pattern file

File scope:

- `workflow_agent_studio/patterns/smb.py`
- `workflow_agent_studio/patterns/smb/`
- `tests/unit/test_smb_pattern_library.py`

Required context:

- `docs/methodology/implementation_patterns.md`

## Evaluation State

Last Evaluation:

- Task: T72
- Date: 2026-06-01
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_privacy_policy_gate.py -q`
- Result: 5 passed; full repository verification passed with 302 tests

## Profile State

RAG: ON

- Current mode: text-only
- Next work: blocked until real workflow data is reviewed
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1
- Next work: SMB implementation patterns for roadmap planning
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
