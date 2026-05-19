# Decision Log - Workflow-to-Agent Studio

Status: append-only index
Date: 2026-05-19

This file is a retrieval index. Canonical decisions live in `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, ADRs, and evaluation artifacts.

| ID | Date | Decision | Canonical Source | Rationale | Superseded By |
|----|------|----------|------------------|-----------|---------------|
| D-001 | 2026-05-19 | Use Workflow orchestration with deterministic validators and LLM synthesis as the primary solution shape. | `docs/ARCHITECTURE.md#solution-shape` | The workflow steps are known and reviewable; higher autonomy is not needed for v1. | n/a |
| D-002 | 2026-05-19 | Set governance level to Standard. | `docs/ARCHITECTURE.md#solution-shape` | Wrong blueprints have medium blast radius and need evidence, evals, and auditability. | n/a |
| D-003 | 2026-05-19 | Set runtime tier to T0. | `docs/ARCHITECTURE.md#runtime-and-isolation-model` | v1 needs local process execution, managed LLM APIs, SQLite, and no runtime mutation. | n/a |
| D-004 | 2026-05-19 | Activate RAG profile with text-only retrieval. | `docs/ARCHITECTURE.md#profile-rag` | Blueprint claims must be grounded in source snippets and prior pattern templates. | n/a |
| D-005 | 2026-05-19 | Activate Planning profile. | `docs/ARCHITECTURE.md#profile-planning` | The primary deliverable is a structured automation blueprint and implementation plan. | n/a |
| D-006 | 2026-05-19 | Keep Tool-Use, Agentic, and Compliance profiles OFF for v1. | `docs/ARCHITECTURE.md#capability-profiles` | v1 uses deterministic adapters, no observe-decide-act loop, and no named regulatory launch gate. | n/a |
| D-007 | 2026-05-19 | Start CLI-first with service-ready modules. | `docs/ARCHITECTURE.md#tech-stack` | This is the fastest route to the proof metric while keeping web UI optional. | n/a |
| D-008 | 2026-05-19 | Use SQLite and local vector index for v1 persistence and retrieval. | `docs/ARCHITECTURE.md#tech-stack` | Local-first proof does not need PostgreSQL or external vector infrastructure. | n/a |
| D-009 | 2026-05-19 | Make source confidentiality and evidence-linked claims project-specific contract rules. | `docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules` | The product handles sensitive workflow material and client-facing scope claims. | n/a |
| D-010 | 2026-05-19 | Use `Dream_Motif_Interpreter` as a reference-only RAG and retrieval-eval implementation source. | `docs/IMPLEMENTATION_REFERENCE_MAP.md` | The repo contains a mature RAG/eval shape, but its dream-domain and PostgreSQL-specific decisions are not canonical for this project. | n/a |

## ADR Triggers

Create an ADR before changing any of these decisions:

- RAG profile ON/OFF status, retrieval mode, embedding model class, chunking contract, or index schema.
- Planning profile ON/OFF status, blueprint schema breaking changes, or approval/export validation contract.
- Runtime tier escalation from T0.
- Adding LLM-directed external tool calls or MCP-backed tools.
- Adding multi-workspace, multi-tenant, or client-facing auth.
- Adding external side-effecting exports such as GitHub issue creation, Slack messages, email, or client portal publishing.
