# CODEX_PROMPT.md

Version: 2.1
Date: 2026-07-13
Phase: portfolio truth and CI repair

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: repair CI and prepare the repository-only rename to
  `workflow-to-agent-studio`.
- Next task: obtain green remote CI on the current slug, perform the verified
  rename, and request one consented sanitized workflow for owner review.
- Verification source: run the commands in `README.md`; do not copy a static
  passing-test count into this session state.
- Last updated: 2026-07-13.
- Open findings: remote CI is red at the unmodified source revision; T34/T40 and
  `v0.1.0` remain blocked until real observed workflow evidence exists.
- Portfolio role: standalone secondary workflow-discovery prototype, not the
  flagship, an agent runtime, or an Eval Ground Truth Lab dependency.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Implemented local mechanics include eight saved public-source fixtures,
  evidence-linked blueprints, candidate comparisons, permission/runtime
  boundaries, roadmap generation, review gates, exports, and deterministic evals.
  These artifacts prove only the exercised local paths; they do not prove user
  value, buyer demand, implementation outcomes, or production readiness.

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

Task: Client Report V2 Commercialization

Status: strategy artifact and six hand-authored Russian v2 showcase reports
complete; implementation schemas/renderers pending.

`docs/demo/CLIENT_REPORT_V2_UPGRADE_STRATEGY_RU.md` defines the new standard:
evidence boundary, target architecture, agents/API/DB bill of materials,
phase-by-phase implementation plan, role-hour estimates, RF/EU rate cards,
LLM/API infrastructure cost formulas, proof layer packaging via Entropy Core,
and AI Workflow Playbook as a repeatable delivery add-on. The six Russian demo
reports are retained as local showcase artifacts, not client evidence. Further
commercialization work stays in the backlog until the CI/rename migration is
complete and a real workflow owner supplies consented, sanitized evidence.

## Evaluation State

Last Evaluation:

- Task: P0 CI, security, truth, link, and rename preparation
- Date: 2026-07-13
- Eval Source: `docs/evidence/WORKFLOW_P0_RENAME_PREP_2026-07-13.md`
- Result: local gates pass; the evidence packet records exact commands, scope,
  counts, and the still-red remote boundary.

## Profile State

RAG: ON

- Current mode: saved public-source and synthetic local evaluation only
- Next work: one consented, sanitized observed workflow case
- Open retrieval findings: external usefulness is unverified

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1, roadmap, review, and
  deterministic evaluation contracts
- Next work: validate a before/after blueprint with the workflow's real owner
- Open planning findings: no observed owner-review result exists

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
