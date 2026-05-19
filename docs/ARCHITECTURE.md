# Architecture - Workflow-to-Agent Studio

Version: 1.0
Last updated: 2026-05-19
Status: Draft

---

## System Overview

Workflow-to-Agent Studio is a local-first workflow discovery and automation-spec system. It helps AI automation engineers, workflow consultants, ops leads, solution architects, and technical founders turn messy SOPs, Loom transcripts, call notes, forms, and operational notes into implementation-ready automation blueprints. The v1 system is a bounded workflow application: deterministic validators and persistence own safety-critical checks, while LLM calls synthesize structured drafts from cited source evidence.

---

## Problem Fit and Adoption Reality

### Problem-First Entry Gate

| Question | Answer |
|----------|--------|
| Concrete operational pain | Discovery for AI automation projects is slow, repetitive, and inconsistent. Stakeholders describe workflows in messy language, and engineers manually translate that into requirements, integration maps, approvals, risks, and eval plans. |
| Current workaround | Consulting calls, Loom videos, Google Docs, screenshots, manually written specs, Slack follow-ups, and engineer-created implementation plans. |
| Why existing process is insufficient | Generic notes miss edge cases, data contracts, human decisions, failure modes, evidence links, and measurable acceptance criteria. Ordinary AI summaries produce polished prose but often miss implementation boundaries and operational risks. |
| First user / operator who feels the pain | AI automation consultants, freelance AI engineers, operations teams, and technical founders creating buildable automation specs. |
| What would make v1 not worth adopting | Generated briefs are generic, miss integration details, ignore approval and risk boundaries, lack eval cases, or still require the engineer to rewrite the spec manually. |
| First proof of value | An operator turns a 10-20 minute workflow description into a decision-grade automation brief in under 30 minutes, with at least 80 percent of required sections accepted after human review. |

### Adoption Reality Gate

| Boundary | Decision |
|----------|----------|
| Work AI is expected to improve | Draft extraction, workflow mapping, missing-question generation, automation candidate identification, risk summaries, eval-case drafting, and evidence-linked blueprint synthesis. |
| Work AI will not replace | Stakeholder interviews, final scope approval, business accountability, sensitive-process judgment, legal/security review, credential handling, integration testing, and final architecture decisions. |
| Claims not allowed before evidence | "Automatically builds the agent", "replaces discovery calls", "guarantees implementation accuracy", "fully understands every business process", "production-ready agent builder". |
| Demo-to-production evidence required | Acceptance rate on required blueprint sections, evidence-link coverage, missing critical question rate, review edit rate, latency under 30 minutes per workflow, and LLM cost per completed brief. |

The project fits the playbook because the product itself is a governance and proof workflow: outputs must be structured, evidence-linked, reviewable, and bounded by human approval.

---

## Solution Shape

| Decision | Selection | Justification |
|----------|-----------|---------------|
| Primary shape | Workflow orchestration with deterministic validators and LLM synthesis | The product has a known sequence: ingest source, extract structure, validate completeness, retrieve patterns, synthesize blueprint, review, export. Open-ended runtime autonomy is not required for v1. |
| Governance level | Standard | The blast radius is medium: wrong blueprints waste engineering time and can create unsafe client expectations. Evidence links, phase gates, evals, and auditability are required, but strict privileged-runtime controls are not. |
| Runtime tier | T0 | v1 runs as a local-first CLI/service using managed LLM APIs, SQLite, and a local vector index. It does not need shell mutation, privileged actions, or long-lived autonomous workers. |

### Rejected Lower-Complexity Options

| Rejected option | Why it is insufficient |
|-----------------|------------------------|
| Deterministic-only | Messy workflow descriptions require language understanding, implicit-step extraction, and synthesis. Deterministic code still owns validation, scoring, and policy checks. |
| Generic LLM summarizer | Summaries do not enforce schema completeness, evidence links, human approval boundaries, eval cases, or implementation task quality. |
| Higher-autonomy agent | v1 does not need to contact stakeholders, mutate production systems, or run open-ended loops. Fixed workflow plus human review is enough. |
| Full BPM/process-mining platform | The first proof metric is a decision-grade blueprint, not enterprise process mining or live workflow execution. |

### Minimum Viable Control Surface

- Strict Pydantic schemas for source documents, extracted workflow maps, automation candidates, eval cases, and final blueprint.
- Deterministic completeness, evidence coverage, forbidden-claim, sensitive-data, and approval-boundary validators.
- Text-only retrieval with `insufficient_evidence` behavior and retrieval evaluation.
- Human approval before client-facing export or downstream ticket creation.
- Immutable blueprint versions and audit entries for source snippets, assumptions, human edits, and exports.

### Human Approval Boundaries

| Boundary | Human approval required? | Why |
|----------|--------------------------|-----|
| Final client-facing proposal | Yes | Business claims and scope commitments remain human-owned. |
| Implementation scope and effort estimate | Yes | Bad estimates can create contractual and operational risk. |
| Security assumptions and approval boundaries | Yes | The model can draft these, but accountability remains with the operator. |
| Markdown export to local file | No | Local draft export is reversible and low-risk. |
| Creating external execution tickets | Yes in v1 | Ticket creation can set team expectations and must be reviewed first. |
| Production workflow execution | Not supported | v1 is discovery/spec generation only. |

### Deterministic vs LLM-Owned Subproblems

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Source fingerprinting, run IDs, versioning | Deterministic | Must be reproducible and auditable. |
| Required-section checks and schema validation | Deterministic | Blueprint validity cannot depend on model judgment. |
| Evidence coverage thresholds | Deterministic | Claims need traceable source support. |
| Sensitive-data flags and forbidden claims | Deterministic | Safety policies need repeatable enforcement. |
| Integration count and complexity bands | Deterministic | Calculations and thresholds should be inspectable. |
| Workflow step extraction from messy prose | LLM | Requires language understanding and ambiguity handling. |
| Edge-case and missing-question suggestions | LLM | The model can infer likely gaps, then validators and humans review them. |
| Automation candidate drafting | LLM | Candidate framing benefits from synthesis, but final scope is human-approved. |
| Final blueprint prose | LLM | The output must be readable, evidence-linked, and schema-constrained. |

### Runtime and Isolation Model

| Property | Decision |
|----------|----------|
| Isolation boundary | T0 local process or managed service boundary. |
| Persistence model | SQLite for v1 metadata, source references, blueprint versions, and review state; vector index stored locally. |
| Network model | Outbound HTTPS to configured LLM providers and optional import APIs only. No production workflow mutation. |
| Secrets model | LLM and import API credentials come only from environment variables. Secrets are not stored in SQLite, logs, traces, or committed files. |
| Runtime mutation boundary | No shell, package, or toolchain mutation at application runtime. |
| Rollback / recovery model | Blueprint versions are immutable; failed runs preserve source references and can be regenerated. SQLite backups cover local state. |

---

## Inference / Model Strategy

| Path / Task | Model class | Why this class | Fallback / escalation | Budget / latency constraint |
|-------------|-------------|----------------|-----------------------|-----------------------------|
| Source normalization and field extraction | Small or mid-tier structured-output model | Repeated extraction should be cost-controlled and schema-constrained. | Escalate to reasoning model when schema repair fails twice or confidence is low. | Keep extraction cost below the configured workflow budget. |
| Missing questions, edge cases, and risk suggestions | Reasoning-capable text model | Ambiguity and implicit-process inference require stronger reasoning. | Return explicit assumptions and `needs_human_review` when evidence is weak. | Whole workflow brief should complete in minutes, not hours. |
| Final blueprint synthesis | Strong reasoning / long-context model | The blueprint combines evidence, retrieved patterns, validators, and human edits. | Produce partial blueprint with missing-section markers when source evidence is insufficient. | Target under 30 minutes end-to-end for v1 workflows. |
| Deterministic validators | No model | Safety and completeness checks must be repeatable. | Failing validators return actionable repair messages. | Must run interactively from stored structured data. |

Model decisions are measured by section acceptance rate, evidence-link coverage, missing critical question rate, latency, and cost per completed workflow brief.

---

## Capability Profiles

| Profile | Status | Evaluation Artifact | Justification |
|---------|--------|---------------------|---------------|
| RAG | ON | `docs/retrieval_eval.md` | The system must retrieve prior workflow briefs, common automation patterns, integration templates, eval templates, guardrail examples, and client-specific SOP context with evidence traceability. |
| Tool-Use | OFF | `docs/tool_eval.md` | v1 integrations are deterministic adapters and exports controlled by application code, not LLM-directed tool calls. Turning this ON requires an ADR and a Tool Catalog. |
| Agentic | OFF | `docs/agent_eval.md` | v1 uses a bounded workflow and human review. It proposes missing questions but does not run an observe-decide-act loop. |
| Planning | ON | `docs/plan_eval.md` | The primary deliverable is a structured automation blueprint and implementation task plan consumed by humans and downstream execution. |
| Compliance | OFF | `docs/compliance_eval.md` | Sensitive data handling is required, but no named regulatory framework is a v1 launch gate. |

### Profile: RAG

#### RAG Architecture

Ingestion pipeline:

```text
extract -> normalize -> chunk -> embed -> index
```

| Stage | Description | Technology |
|-------|-------------|------------|
| Extract | Load pasted text, Markdown files, transcript files, SOP docs, and curated pattern templates. | Python file readers and import adapters. |
| Normalize | Convert inputs into normalized source documents with stable IDs, source type, title, text, and metadata. | Pydantic models and deterministic normalizers. |
| Chunk | Split by heading and semantic paragraph boundaries with token caps. | Local chunking module. |
| Embed | Create embeddings for normalized chunks. | Configurable embedding provider; default stable text embedding model. |
| Index | Store vectors and metadata in a local index with schema version. | SQLite-backed metadata plus local vector index. |

Query-time pipeline:

```text
query analyze -> retrieve -> filter -> assemble evidence -> answer or insufficient_evidence
```

| Stage | Description | Technology |
|-------|-------------|------------|
| Query analyze | Build retrieval queries from workflow domain, tool names, risks, and missing sections. | Deterministic query builder with optional LLM rewrite later. |
| Retrieve | Similarity search over workflow sources and pattern library. | Local vector search. |
| Filter | Enforce corpus/workspace scope and minimum evidence threshold. | Deterministic filters. |
| Assemble evidence | Provide numbered snippets with source IDs, offsets, and section labels. | Evidence assembler. |
| Answer / insufficient_evidence | Generate blueprint sections only when evidence supports them; otherwise mark missing evidence. | LLM synthesis plus deterministic guard. |

#### Corpus Description

| Property | Value |
|----------|-------|
| Source documents | Current workflow sources, prior approved blueprints, automation pattern templates, integration templates, eval templates, and guardrail examples. |
| Update frequency | Per workflow import and whenever the local pattern library changes. |
| Estimated size | v1 starts with 1-20 source documents per workflow and dozens of pattern templates. |
| Access control | Single-operator local workspace in v1; future workspaces must isolate corpora by workspace ID. |

#### Retrieval / Embedding Strategy

| Decision | Selection | Why |
|----------|-----------|-----|
| Retrieval mode | Text-only | Loom/audio is transcribed before ingestion and screenshots are manually described for v1. |
| Modalities in scope | Text and metadata only | This is the minimum sufficient mode for the first proof metric. |
| Text-only baseline considered? | Yes | Text-only is the v1 baseline. Multimodal retrieval is deferred until text evidence misses UI-specific steps. |
| Embedding provider / model | Configurable stable text embedding model | Keeps provider choice swappable while preserving index schema versioning. |
| Stability status | Stable required for client-facing output | Preview embeddings require ADR, fallback, and re-index plan. |
| Fallback / migration path | Export corpus chunks, rebuild index with new schema version, and compare against baseline retrieval eval. |

#### Index Strategy

- Embedding model: configured through `WORKFLOW_STUDIO_EMBEDDING_MODEL`; default selected in implementation.
- Chunking: heading-aware, paragraph-preserving chunks with source offsets.
- Vector representation contract: stored with index schema version and embedding model name.
- Index schema version: v1; changes require ADR and full re-index.
- Max index age: current workflow corpus must be indexed in the active run; pattern-library staleness above 30 days raises a warning.
- Evaluation plan: 10-query retrieval fixture covering workflow steps, edge cases, integrations, approval boundaries, eval cases, no-answer behavior, and prior-pattern lookup.

#### RAG Implementation Reference

Use `https://github.com/ashishki/Dream_Motif_Interpreter` as a reference-only implementation map for RAG shape and evaluation discipline. The relevant source map lives in `docs/IMPLEMENTATION_REFERENCE_MAP.md`.

Port the following patterns where they fit this project:

- separate ingestion and query-time retrieval modules
- typed source document, evidence, and `insufficient_evidence` objects
- tokenizer-aware chunking when token limits are declared
- typed embedding-provider errors and non-PII tracing
- retrieval eval history with Date, Corpus Version, Eval Source, hit@k, MRR, citation precision, no-answer accuracy, and latency
- focused regression slices for real missed-recall or false-positive reports

Do not copy dream-domain query expansion, Telegram behavior, PostgreSQL-only choices, or model constants into this project without an ADR.

#### Risks

| Risk | Mitigation |
|------|------------|
| Hallucination on weak evidence | Required `insufficient_evidence` path and evidence coverage validator. |
| Schema drift | Version index schema; ADR and re-index required for embedding, chunking, or metadata changes. |
| Stale index | Health/status output reports corpus version and pattern-library age. |
| Corpus isolation failure | v1 single workspace; future multi-workspace mode must namespace corpus and filter every query. |
| Retrieval latency regression | Retrieval eval tracks latency and hit@k. |
| Multimodal overreach | Multimodal retrieval is deferred until text-only baseline shows specific failures. |

### Profile: Planning

#### Plan Schema

The application output plan is the automation blueprint. Schema version v1 includes:

- workflow summary
- actors and systems
- triggers and inputs
- current workflow steps
- decisions and exceptions
- data fields and integration map
- pain points
- automation candidates
- human approval boundaries
- risks and assumptions
- eval cases
- observability needs
- rough effort band
- next implementation tasks
- evidence links per claim

#### Plan Validation

Every generated blueprint must pass deterministic validation before it can be approved or exported:

- required sections are present
- claims carry evidence links or explicit assumptions
- forbidden autonomy claims are absent
- unsafe automation candidates require approval boundaries
- eval cases reference measurable expected behavior
- implementation tasks have owner, dependencies, acceptance criteria, and tests or evals

#### Invalid Plan Behavior

Invalid plans stay in draft status. The system returns validator findings, missing questions, and suggested repairs. It must not silently export an invalid blueprint as approved.

#### Risks

| Risk | Mitigation |
|------|------------|
| Plan looks polished but is underspecified | Schema validation and section acceptance checklist. |
| Evidence-free claims | Evidence coverage validator blocks approval. |
| Unsafe automation scope | Approval-boundary and forbidden-claim validators. |
| Replan loop grows unbounded | v1 repair flow is human-driven; no autonomous replan loop. |

---

## Component Table

| Component | File / Directory | Responsibility |
|-----------|------------------|----------------|
| CLI entry point | `workflow_agent_studio/cli.py` | Accept source paths or pasted text, run workflows, export Markdown. |
| Configuration | `workflow_agent_studio/config.py` | Load environment settings, model names, storage paths, and feature flags. |
| Domain schemas | `workflow_agent_studio/domain/` | Pydantic models for sources, workflow maps, blueprint schema, eval cases, and review state. |
| Source ingestion | `workflow_agent_studio/ingestion/` | Load text/transcript/Markdown inputs, fingerprint sources, normalize documents. |
| Retrieval ingestion | `workflow_agent_studio/retrieval/ingest.py` | Chunk, embed, and index normalized source documents and pattern templates. |
| Retrieval query | `workflow_agent_studio/retrieval/query.py` | Retrieve evidence snippets with corpus filters and no-answer behavior. |
| LLM gateway | `workflow_agent_studio/llm/` | Structured-output model calls, retries, budget tracking, and schema repair. |
| Workflow extraction | `workflow_agent_studio/extraction/` | Extract actors, systems, steps, fields, decisions, exceptions, and pain points. |
| Blueprint synthesis | `workflow_agent_studio/blueprint/` | Compose evidence-linked automation blueprint sections. |
| Validators | `workflow_agent_studio/validators/` | Deterministic completeness, evidence, forbidden-claim, sensitive-data, and plan validators. |
| Persistence | `workflow_agent_studio/storage/` | SQLite repositories for runs, source refs, blueprint versions, review status, and audit events. |
| Export | `workflow_agent_studio/export/` | Markdown export and future downstream export adapters. |
| Observability | `workflow_agent_studio/observability/` | Shared tracing, metrics, structured logs, and PII-safe reporting. |
| Tests | `tests/` | Unit, integration, retrieval eval, and plan eval tests. |

---

## Data Flow

1. Operator provides source text or file paths through the CLI.
2. Ingestion normalizes each source into a `SourceDocument` with fingerprint and metadata.
3. Sensitive-data scanner flags likely secrets, credentials, and PII before logs or exports.
4. Retrieval ingestion chunks and indexes source documents and local pattern templates.
5. Extraction LLM produces structured workflow facts with source evidence references.
6. Deterministic validators check schema, required sections, evidence coverage, and forbidden claims.
7. Query-time retrieval adds relevant prior patterns, integration templates, and eval templates.
8. Blueprint synthesis generates the automation blueprint with evidence links and assumptions.
9. Plan validators block approval until required sections, eval cases, risks, and task contracts pass.
10. Human reviews, edits, approves, and exports the blueprint as Markdown.
11. Persistence stores immutable blueprint versions, source references, review status, and audit events.

---

## Tech Stack

| Component | Technology Choice | Rationale |
|-----------|-------------------|-----------|
| Language | Python 3.12 | Strong ecosystem for CLI apps, Pydantic, LLM integrations, retrieval, and tests. |
| Interface | CLI-first with service-ready modules | Fastest route to proof metric; keeps web UI optional. |
| Schemas | Pydantic v2 | Strict structured outputs and validation. |
| Persistence | SQLite | Local-first, simple backup, no server dependency for v1. |
| Retrieval | Local vector index plus SQLite metadata | Enough for dozens to hundreds of docs without external infrastructure. |
| LLM calls | Provider adapter with structured-output validation | Keeps model/provider changes isolated. |
| Testing | pytest | Standard Python test runner. |
| Lint/format | ruff | Fast static checks and formatting. |
| CI | GitHub Actions | Enforces tests and lint from Phase 1. |
| Observability | Standard logging plus shared tracing wrapper | PII-safe logs and future OpenTelemetry upgrade path. |

---

## Security Boundaries

- v1 is single-operator and local-first; no multi-tenant access is implemented in v1.
- If client-facing workspaces are added, workspace-scoped authorization and corpus isolation become mandatory before launch.
- Source files are confidential by default.
- Logs, traces, metrics, and errors must not include raw workflow content, credentials, customer records, or pricing details.
- Potential PII fields include names, emails, phone numbers, customer IDs, account IDs, addresses, API keys, tokens, URLs containing secrets, pricing terms, and internal process notes.
- Local exports are drafts until human approval marks them approved.
- External side-effecting exports such as GitHub issue creation are out of v1 implementation unless added by ADR with approval controls.

---

## External Integrations

| Integration | v1 Status | Use |
|-------------|-----------|-----|
| LLM provider APIs | Required | Structured extraction and blueprint synthesis. |
| Embedding provider | Required when retrieval tasks are implemented | Text-only vector embeddings. |
| Google Drive / Docs | Deferred | Future source import adapter. |
| Notion | Deferred | Future source import adapter. |
| Loom transcript export | Deferred | Future transcript import adapter. |
| Slack | Deferred | Future intake channel. |
| GitHub Issues | Deferred and human-gated | Future export target for approved implementation tasks. |
| Airtable / Sheets | Deferred | Future source and export adapter. |
| Mermaid diagrams | Optional later | Deterministic diagram export from workflow schema. |

---

## File Layout

```text
workflow_agent_studio/
  __init__.py
  cli.py
  config.py
  domain/
  ingestion/
  retrieval/
  llm/
  extraction/
  blueprint/
  validators/
  storage/
  export/
  observability/
tests/
  unit/
  integration/
  eval/
docs/
  ARCHITECTURE.md
  spec.md
  tasks.md
  CODEX_PROMPT.md
  IMPLEMENTATION_CONTRACT.md
  DECISION_LOG.md
  IMPLEMENTATION_JOURNAL.md
  EVIDENCE_INDEX.md
  retrieval_eval.md
  plan_eval.md
  audit/
  adr/
.github/workflows/ci.yml
pyproject.toml
requirements.txt
requirements-dev.txt
```

---

## Runtime Contract

| Name | Description | Example Value |
|------|-------------|---------------|
| `WORKFLOW_STUDIO_STORAGE_PATH` | SQLite database path. | `.data/workflow_studio.sqlite3` |
| `WORKFLOW_STUDIO_INDEX_DIR` | Local vector index directory. | `.data/index` |
| `WORKFLOW_STUDIO_PATTERN_DIR` | Local pattern/template corpus path. | `patterns/` |
| `WORKFLOW_STUDIO_LLM_PROVIDER` | LLM provider adapter name. | `openai` |
| `WORKFLOW_STUDIO_LLM_MODEL` | Default synthesis model. | `gpt-5.4` |
| `WORKFLOW_STUDIO_EXTRACTION_MODEL` | Lower-cost extraction model. | `gpt-5.4-mini` |
| `WORKFLOW_STUDIO_EMBEDDING_MODEL` | Text embedding model name. | `text-embedding-3-small` |
| `OPENAI_API_KEY` | Provider API key when using OpenAI. | `sk-test-placeholder` |
| `WORKFLOW_STUDIO_MAX_LLM_COST_USD` | Optional per-run budget ceiling. | `5.00` |
| `WORKFLOW_STUDIO_LOG_LEVEL` | Logging verbosity. | `INFO` |

Real secrets must come from the environment and must never be committed.

---

## Continuity and Retrieval Model

Canonical truth:

- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- ADRs in `docs/adr/`
- evaluation artifacts in `docs/retrieval_eval.md` and `docs/plan_eval.md`
- code, tests, migrations, and CI

Retrieval convenience:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- task-level `Context-Refs`

Scoped retrieval is mandatory when a task changes retrieval semantics, blueprint schema, plan validation, source confidentiality, model routing, export behavior, approval boundaries, or any open finding.

---

## Non-Goals

- Build or deploy the automation agent automatically.
- Replace stakeholder discovery or final human approval.
- Execute customer workflows or mutate production systems.
- Provide enterprise BPM/process mining.
- Support multimodal retrieval in v1.
- Support multi-tenant client workspaces in v1.
- Create GitHub issues without explicit human approval and a future Tool-Use profile decision.
- Treat LLM output as authoritative without schema validation and evidence links.
