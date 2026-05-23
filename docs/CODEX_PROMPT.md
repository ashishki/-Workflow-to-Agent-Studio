# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-23
Phase: 12

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 12 - Solo Public Workflow Showcase
- Next task: T57 Solo Showcase Readiness Review
- Verified baseline: 187 passing tests, 0 skipped, 0 failed
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

Task: T57 Solo Showcase Readiness Review

Goal: decide whether the public-source showcase is ready to show manually to
prospects and whether the next work is prospect data collection or another
public-source quality pass.

Acceptance summary:

- review cites all three public demo packs and their rubric results
- review confirms public-source artifacts are not represented as buyer proof
- review records next action: request prospect data, improve demo quality, or
  pause

File scope:

- `docs/audit/SOLO_SHOWCASE_READINESS_REVIEW.md`
- `docs/CODEX_PROMPT.md`

Required context:

- `docs/tasks.md#phase-12-solo-public-workflow-showcase`
- `docs/experiments/public_demo_pack/hvac_lead_intake/`
- `docs/experiments/public_demo_pack/netbox_issue_triage/`
- `docs/experiments/public_demo_pack/gitlab_incident_response/`
- `docs/prospect_data_request_pack.md`

## Evaluation State

Last Evaluation:

- Task: T56
- Date: 2026-05-23
- Eval Source: pytest tests/unit/test_docs.py -q
- Result: prospect data request pack keeps request narrow, local, and demo-only

## Profile State

RAG: ON

- Current mode: text-only
- Next work: solo showcase readiness review
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: solo showcase readiness review
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
