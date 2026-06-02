# CODEX_PROMPT.md

Version: 2.0
Date: 2026-06-01
Phase: 14

This file is the compact implementation-session state. It should stay short. Completed V1 history is archived at `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`.

Execution policy: continue the Codex-only loop until blocked, all active tasks are complete, or human input is required by `docs/IMPLEMENTATION_CONTRACT.md`.

---

## Current State

- Current phase: Phase 15 - Pattern Library Expansion And Frontier Discovery
- Next task: none - active task graph complete through T84
- Verified baseline: post T84 frontier opportunity discovery baseline is 364 passing tests, 0 skipped, 0 failed
- Ruff: `ruff check` and `ruff format --check` pass for the full repository after T84
- Last updated: 2026-06-02
- Open findings: T34/T40 remain blocked until real pilot evidence exists; Phase 12 may use public sources for solo showcase artifacts only.
- Latest domain contract: `WorkflowKind` lives in `workflow_agent_studio/domain/workflow.py`.
- Completed product baseline: public-data working product proof for 8 public workflow fixtures; Phase 0 / local evidence-linked MVP; T58 framework positioning refresh complete; T59 design candidate schema complete; T60 diverse generation flow complete; T61 Playbook export complete; T62 permission/runtime boundary pack complete; T63 framework readiness review complete; SMB AI roadmap documentation package created and indexed at `docs/AI_ROADMAP_STUDIO_INDEX.md`; T64 privacy classification schema complete; T65 recommendation card schema complete; T66 costing schema complete; T67 scoring schema complete; T68 verification schema complete; T69 roadmap report aggregate schema complete; T70 deterministic privacy classifier complete; T71 redaction preview complete; T72 privacy policy gate complete; T73 SMB pattern schema complete; T74 MVP SMB pattern pack complete; T75 pattern matching baseline complete; T76 cost engine complete; T77 priority scoring engine complete; T78 roadmap assembly service complete; T79 roadmap Markdown export complete; T80 roadmap CLI command complete; T81 roadmap eval suite complete; T82 roadmap review and handoff export complete; public-source roadmap demos added for HVAC lead intake, NetBox issue triage, and GitLab incident workflow; Russian accelerator application-review showcase report added for cofounder/customer demo; T83 public n8n pattern mining foundation complete with 8,824 parsed public n8n workflows and 4,963 deduplicated metadata candidates; T84 frontier opportunity discovery layer complete with validated Opus 4.6 demo run; cofounder/customer demo docs enriched with n8n provenance and frontier candidate sections

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

Task: T84 - Frontier Opportunity Discovery Layer

Status: complete.

T83 added a public n8n source register, n8n workflow metadata parser,
fingerprint/dedupe foundation, Russian methodology, mining script, and public
metadata summary. Latest mining run scanned 8,854 JSON files, parsed 8,824 n8n
workflows, collapsed 3,861 duplicates, and produced 4,963 deduplicated metadata
candidate layer and deterministic verifier boundary. Opus 4.6 demo run produced
three unapproved candidates: claim verification research assistant, post-call
structured feedback capture, and duplicate/repeat applicant detection. All
remain non-exportable until human review.

## Evaluation State

Last Evaluation:

- Task: T84
- Date: 2026-06-02
- Eval Source: `.venv/bin/python -m pytest -q`
- Result: 364 passed; `ruff check .` and `ruff format --check .` passed

## Profile State

RAG: ON

- Current mode: public-source metadata mining plus frontier candidate generation
- Next work: blocked until next task graph or human direction
- Open retrieval findings: none

Planning: ON

- Current schema: blueprint v1 plus design-candidate-v1 plus n8n metadata candidates plus frontier opportunity candidates
- Next work: active task graph complete through T84
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
