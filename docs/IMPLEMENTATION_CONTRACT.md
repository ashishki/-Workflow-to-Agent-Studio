# Implementation Contract

Status: IMMUTABLE - changes require an ADR filed in `docs/adr/`
Version: 1.0
Effective date: 2026-05-19

Any Codex or review agent may cite this document as the authority on implementation rules. Any violation of this contract is a P1 finding unless a rule names a higher severity.

---

## Universal Rules

These rules apply to every project using the AI Workflow Playbook. They are not changed without an ADR.

### SQL Safety

- All SQL is parameterized. Use `text()` with named params: `text("SELECT ... WHERE id = :id")`.
- Never interpolate variables into SQL strings.
- Never use string concatenation to build queries.

### Multi-Tenant Systems

- Every database call is preceded by the appropriate tenant context (`SET LOCAL app.tenant_id = :tid` or equivalent RLS setup).
- No query executes without a tenant context in multi-tenant code paths.
- V1 is single-operator and local-first. If multi-workspace or multi-tenant behavior is introduced later, this section becomes active before launch.

### Async Redis

- Redis is accessed only in `async def` functions using `redis.asyncio`.
- Never import or call the synchronous redis client in async code paths.
- Redis is not part of v1. If introduced later, these rules apply immediately.

### Authorization

- Every new route handler enforces authorization through role check, JWT validation, or equivalent.
- Authorization is never deferred to "we'll add it later."
- V1 is CLI-first. If HTTP routes are added, public routes must be explicitly documented in code and architecture.

### PII Policy

- No PII in log messages, span attributes, or metrics.
- Where identifiers must be logged, use hashes such as SHA-256.
- This applies to all observability: logs, traces, metrics, and error messages.
- Fields considered sensitive in this project include names, emails, phone numbers, customer IDs, account IDs, addresses, API keys, tokens, URLs containing secrets, pricing terms, raw workflow source text, and internal process notes.

### Credentials

- No credentials, API keys, or secrets in source code.
- Use environment variables.
- Document required environment variables in `docs/ARCHITECTURE.md` under Runtime Contract.
- Test fixtures may use placeholder strings such as `sk-test-placeholder`; real credentials are forbidden.

### Tracing

- Shared tracing module: `workflow_agent_studio/observability/tracing.py` with one `get_tracer()` function.
- No inline noop span implementations scattered across files.
- All spans use the shared module.

### CI

- CI must pass before any PR is merged.
- No exceptions. No "merge now, fix CI later."

---

## Project-Specific Rules

### Source Confidentiality

Raw workflow source text, transcript content, client notes, screenshots described as text, and API documentation excerpts are confidential by default. They must not appear in logs, spans, metric labels, CI output, or unredacted audit events.

Violation: P1.

### Evidence-Linked Blueprint Claims

Every non-obvious blueprint claim must have at least one evidence reference or an explicit assumption marker. A generated claim without either cannot be approved.

Violation: P1 if approved or exported as approved; P2 if still draft-only.

### Deterministic Validation Ownership

Completeness checks, forbidden-claim checks, sensitive-data checks, approval gating, schema validation, cost ceilings, evidence coverage thresholds, and export path checks are deterministic code paths. They must not be delegated to LLM judgment.

Violation: P1.

### Model Output Boundary

All LLM outputs must be parsed into versioned Pydantic schemas before they affect storage, validation, approval, or export. Raw model text may be stored only as a debug artifact when explicitly redacted and disabled by default.

Violation: P1.

### Local Export Boundary

V1 exports only local Markdown files. Export paths must be operator-provided and constrained to the selected export directory. External side effects such as GitHub issue creation, Slack messages, emails, or client portal publication require an ADR and human approval boundary before implementation.

Violation: P1 for external side effects without ADR; P2 for local path-boundary bugs that cannot overwrite files outside the export directory.

### No Runtime Mutation

Application runtime must not install packages, modify its toolchain, run shell commands on behalf of the model, or mutate production systems. Runtime tier is T0.

Violation: P1.

---

## Mandatory Pre-Task Protocol

1. Read `docs/IMPLEMENTATION_CONTRACT.md` before starting any task.
2. Read the orchestrator's inline task digest.
3. Read the current task entry in `docs/tasks.md` only as needed to confirm acceptance criteria, file scope, and notes.
4. Read Depends-On tasks, `Context-Refs`, and canonical docs when the task changes architecture, risky boundaries, open findings, retrieval semantics, plan validation, model routing, or interface contracts.
5. Run `pytest` to capture the pre-task baseline. Record the number: `N passing, M failed`.
6. Run `ruff check` once ruff is configured. Do not begin feature work if ruff is not clean; fix lint issues first in a separate commit.
7. Write tests before or alongside implementation. No task is complete until every acceptance criterion has a passing test.

---

## Nonstop Development Loop

Development must proceed in a continuous Codex-only loop:

`read state -> select next eligible item -> implement or fix -> test -> review -> update docs/state -> checkpoint -> loop`.

Phase completion is not a stopping point. A phase boundary triggers the required strategy review, deep review, archive, documentation update, and phase report, then development continues into the next phase automatically.

The only valid stop conditions are:

- a task or fix is formally marked `[!]` because Codex cannot proceed safely
- a P0 finding remains unresolved after the allowed repair attempts
- required human input is needed for an architecture, product, security, or external-side-effect decision
- provider/tool failure persists after the required retry
- API rate limit or context budget forces a clean checkpoint
- all tasks are complete

Pausing between phases without one of these stop conditions is a process violation and must be surfaced as a P1 finding.

---

## Forbidden Actions

The following actions are never permitted without explicit documented exception:

| Action | Why Forbidden |
|--------|---------------|
| String interpolation in SQL | SQL injection risk; parameterized queries are non-negotiable. |
| Session-level `SET` in multi-tenant systems | Leaks tenant context across requests; use `SET LOCAL`. |
| Skipping pre-task baseline capture | Cannot verify that implementation did not break existing tests. |
| Self-closing review findings without code verification | Findings are closed by reading the code, not by asserting the code was fixed. |
| Modifying `docs/IMPLEMENTATION_CONTRACT.md` without an ADR | The contract is immutable; changes require architectural review. |
| Deferring CI setup past Phase 1 | Every commit after Phase 1 must be CI-verified. |
| Running tests without capturing the pre-change baseline | Baseline comparison is the primary correctness signal. |
| Merging a PR with failing CI | The CI gate exists for this reason. |
| Committing credentials or secrets | Irreversible exposure risk. |
| Expanding runtime tier or adding runtime mutation without ADR | Violates the declared T0 boundary and bypasses architecture approval. |
| Exporting approved blueprints with blocking validation findings | Creates unsafe client-facing artifacts. |
| Producing external side effects from v1 exports | V1 is local-only unless an ADR changes the boundary. |
| Pausing between phases without a formal stop condition | The project must follow the nonstop Codex loop until blocked or complete. |

If any forbidden action occurs, surface it as a P1 finding in the next review cycle.

---

## Quality Process Rules

### P2 Age Cap

Any P2 finding that remains open for more than 3 consecutive review cycles must be closed, escalated to P1, or formally deferred to v2 with an ADR.

For retrieval-critical findings involving corpus isolation, `insufficient_evidence`, schema drift, or evidence/citation correctness, the age cap is 1 review cycle.

### Commit Granularity

Use one logical change per commit. Do not combine migrations, services, tests, docs, and unrelated fixes in one commit when they can be reviewed separately.

### Sandbox Isolation

Codex tasks must stay within the file scope declared in `docs/tasks.md` unless the task result explains the added file and why it was necessary.

### Evaluation Gate

A task with any of these tags is not complete until the matching evaluation artifact is updated with current results and compared to baseline:

| Tag | Artifact |
|-----|----------|
| `rag:ingestion` | `docs/retrieval_eval.md` |
| `rag:query` | `docs/retrieval_eval.md` |
| `plan:schema` | `docs/plan_eval.md` |
| `plan:validation` | `docs/plan_eval.md` |

"Tests are green" does not satisfy evaluation requirements.

---

## Continuity and Retrieval Rules

### Canonical Truth

The following documents are authoritative for implementation and review:

- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/tasks.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- ADRs in `docs/adr/`
- evaluation artifacts in `docs/retrieval_eval.md` and `docs/plan_eval.md`
- source code, tests, migrations, and CI workflow files

### Retrieval Convenience Surfaces

The following documents help agents find relevant history quickly, but they do not override canonical truth:

- `docs/DECISION_LOG.md`
- `docs/IMPLEMENTATION_JOURNAL.md`
- `docs/EVIDENCE_INDEX.md`
- task-level `Context-Refs` in `docs/tasks.md`
- audit reports in `docs/audit/`

### Mandatory Lookup Triggers

Before implementation, read scoped continuity references when a task:

- changes retrieval semantics, index schema, chunking, embedding model, corpus boundaries, or `insufficient_evidence` behavior
- changes blueprint schema, plan validation, approval rules, export behavior, or evidence requirements
- changes model routing, cost controls, secrets handling, logging, tracing, storage, or runtime boundaries
- resolves or reopens a review finding
- uses `Execution-Mode: heavy`
- changes an ADR-controlled decision

If required history is missing, stop and report a `CONTINUITY_GAP` instead of guessing.

---

## Profile Rules: RAG

Applies because `docs/ARCHITECTURE.md` declares RAG Status ON.

### Corpus Isolation

- Every retrieval query must be scoped to the active local workflow run and permitted pattern library.
- Future multi-workspace mode must namespace corpora by workspace and filter every query by workspace ID.
- Cross-corpus retrieval is treated as a data leak.

### insufficient_evidence Path

- Every query-time retrieval handler must implement `insufficient_evidence`.
- When retrieved evidence does not meet minimum support, the system returns `insufficient_evidence` instead of fabricating an answer.
- This path must have explicit tests.

### Index Schema Versioning

- The index schema is versioned.
- Changing embedding model, chunking strategy, metadata fields, vector representation, or retrieval mode requires an ADR and full re-index.
- Partial indexes mixing old and new schema versions are forbidden.

### Text-Only Retrieval Mode

- V1 retrieval mode is text-only.
- Multimodal retrieval requires an ADR, text-only baseline comparison, fallback plan, cost/latency analysis, and updated evaluation artifact.

### Max Index Age

- Current workflow source chunks must be indexed in the active run before query-time retrieval uses them.
- Pattern-library index age above 30 days must produce a warning in health/status output.
- A pattern-library index age above 60 days is a P2 finding until refreshed or explicitly accepted by the human reviewer.

### Embedding Strategy Declaration

- The active embedding model name, retrieval mode, vector representation contract, and index schema version must be recorded in `docs/ARCHITECTURE.md` and `docs/retrieval_eval.md`.
- Changing embedding model, dimensions, provider, representation contract, or retrieval mode requires an ADR and full re-index before production use.
- Preview or experimental embedding models require a documented stable fallback and migration plan before any client-facing workflow uses them.

### Retrieval Evaluation Gate

A retrieval task is not complete unless:

1. `docs/retrieval_eval.md` is updated with current metrics.
2. Current metrics are compared to baseline.
3. Any regression is documented and either justified or escalated as P1.
4. The evaluation history row records corpus version.
5. Retrieval answer behavior includes an `insufficient_evidence` test.

---

## Profile Rules: Planning

Applies because `docs/ARCHITECTURE.md` declares Planning Status ON.

### Plan Schema Versioning

- The automation blueprint schema is versioned.
- Schema changes require tests and a `docs/plan_eval.md` update.
- Breaking schema changes after implementation starts require an ADR.

### Plan Validation Gate

- Every blueprint must pass schema validation before storage as a versioned blueprint.
- Every blueprint must pass deterministic validation before approval.
- A draft with blocking findings may be exported only when clearly labeled as draft with unresolved findings.
- An approved export with blocking findings is forbidden.

### Invalid Plan Behavior

- Invalid blueprints remain in draft status.
- Validation returns structured findings with rule ID, severity, section, message, and repair hint.
- No autonomous replan loop is allowed in v1; repair is human-driven.

### Plan Evaluation Gate

A task tagged `plan:schema` or `plan:validation` is not complete unless:

1. `docs/plan_eval.md` records current schema or validation metrics.
2. Results are compared to the current baseline.
3. Any regression is documented and either justified or escalated as P1.

---

## Control Surface and Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | Only configured provider adapters may read relevant API keys from environment variables. No code stores secrets. |
| Network egress | Outbound HTTPS to configured LLM and embedding providers only in v1. External import APIs are deferred. |
| Privileged actions | None in v1. Client-facing approval and external side effects are human-gated and deferred. |
| Runtime mutation | No shell, package, toolchain, service, or production system mutation at application runtime. |
| Persistence | SQLite and local vector index persist local workspace state. Blueprint versions and audit events are append-only. |
| Auditability | Runs, imports, generation attempts, validation results, approvals, and exports produce PII-safe audit events. |

---

## Governing Documents

| Document | Role |
|----------|------|
| `docs/ARCHITECTURE.md` | System design, profiles, runtime, security, and data flow. |
| `docs/spec.md` | Product feature specification and v1 acceptance criteria. |
| `docs/tasks.md` | Authoritative implementation task graph. |
| `docs/CODEX_PROMPT.md` | Current session state, baseline, next task, findings, and profile state. |
| `docs/retrieval_eval.md` | RAG quality and regression evidence. |
| `docs/plan_eval.md` | Blueprint schema and validation quality evidence. |
| `docs/DECISION_LOG.md` | Decision index pointing to canonical sources. |
| `docs/IMPLEMENTATION_JOURNAL.md` | Append-only continuity log for implementation sessions. |
| `docs/EVIDENCE_INDEX.md` | Index of proof artifacts, evals, reviews, and heavy-task evidence. |
| `docs/adr/` | Immutable architectural decision records. |
| `docs/audit/` | Review prompts, audit index, and review reports. |
