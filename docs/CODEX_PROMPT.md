# CODEX_PROMPT.md

Version: 2.0
Date: 2026-05-23
Phase: 12

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 12 - Solo Public Workflow Showcase
- Next task: T56 Solo Prospect Data Request Pack
- Verified baseline: 186 passing tests, 0 skipped, 0 failed
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

Task: T56 Solo Prospect Data Request Pack

Goal: create a lightweight request pack a solo operator can send manually to
prospects, asking for one narrow workflow packet without broad system access.

Acceptance summary:

- request asks for one SOP, transcript, notes file, form description,
  integration excerpt, or mixed packet
- request explains local processing, confidentiality boundaries, human review,
  and optional sanitized benchmark reuse
- request includes the public demo pack as demo material, not proof

File scope:

- `docs/prospect_data_request_pack.md`
- `docs/pilot_measurement.md`

Required context:

- `docs/tasks.md#phase-12-solo-public-workflow-showcase`
- `docs/experiments/public_demo_pack/hvac_lead_intake/`
- `docs/pilot_measurement.md#prospect-data-request-gate`

## Evaluation State

Last Evaluation:

- Task: T55
- Date: 2026-05-23
- Eval Source: pytest tests/eval/test_public_source_experiment.py -q
- Result: Lead Response SLA Agent handoff is source-bounded and safe-reply scoped

## Profile State

RAG: ON

- Current mode: text-only
- Next work: solo prospect data request pack
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1
- Next work: solo prospect data request pack
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
