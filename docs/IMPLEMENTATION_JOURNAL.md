# Implementation Journal - Workflow-to-Agent Studio

Status: append-only
Date: 2026-05-19

Use this file for durable handoff context that future agents need without re-reading the whole repository.

---

## 2026-05-19 - Bootstrap Phase 1 Package

Task: bootstrap-new

Summary:

- Created the initial architecture, specification, task graph, implementation contract, session handoff, decision log, evidence index, and evaluation artifacts.
- Chose Workflow orchestration with deterministic validators and LLM synthesis.
- Activated RAG and Planning profiles; left Tool-Use, Agentic, and Compliance OFF.
- Selected CLI-first Python 3.12, SQLite, local vector index, Pydantic schemas, pytest, ruff, and GitHub Actions.
- Defined T01 as the next implementation task: Project Skeleton.

Important context:

- `docs/project_fit_guide.md` was copied into the repo because `/bootstrap-new` expects it locally.
- The execution model is Codex-only. Do not use Claude Code as the orchestrator and do not call nested `codex exec`.
- Start orchestration by resuming Codex with `docs/prompts/ORCHESTRATOR.md`.
- RAG is text-only for v1. Multimodal retrieval requires an ADR.
- External side-effecting exports are out of v1 unless an ADR adds Tool-Use controls and human approval boundaries.
- CI is configured as a real workflow but will not pass until T01-T03 create package and tests.

Next action:

- Run Codex with `docs/prompts/ORCHESTRATOR.md`; it should start at `T01: Project Skeleton`.

---

## 2026-05-19 - Add RAG Reference Project

Task: planning update

Summary:

- Inspected `https://github.com/ashishki/Dream_Motif_Interpreter` as a reference for RAG and retrieval evaluation.
- Added `docs/IMPLEMENTATION_REFERENCE_MAP.md` to map useful reference files to Workflow-to-Agent Studio targets.
- Updated RAG architecture, retrieval eval shape, and RAG task `Context-Refs` to point at the reference map.

Important context:

- Use the reference for pipeline and eval shape only: ingestion/query separation, typed evidence, `insufficient_evidence`, eval history, query types, and regression slices.
- Do not copy dream-specific query expansion, Telegram behavior, PostgreSQL-only choices, or model constants without an ADR.
