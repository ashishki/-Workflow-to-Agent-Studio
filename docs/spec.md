# Specification - Workflow-to-Agent Studio

Version: 1.0
Date: 2026-05-19
Status: Draft

---

## Overview

Workflow-to-Agent Studio turns raw workflow discovery material into an evidence-linked automation blueprint. v1 is a local-first CLI workflow that ingests text and transcript sources, extracts workflow structure, retrieves relevant prior patterns, generates a structured blueprint, validates completeness and risk boundaries, and exports a human-reviewed Markdown brief.

---

## User Roles

| Role | Responsibilities |
|------|------------------|
| Operator | Imports workflow sources, reviews extracted structure, answers missing questions, approves or rejects blueprint sections, and exports Markdown. |
| Reviewer | Checks whether generated blueprints are specific, evidence-linked, safe, and ready for implementation planning. |
| Future client stakeholder | Provides source materials and approves final scope outside the application. |

---

## Feature Area: Source Ingestion

Description: The operator can create a workflow run from pasted text, Markdown files, transcript files, SOP notes, and structured samples. The system normalizes each source into a stable source document with fingerprint, metadata, and source text.

Acceptance criteria:

1. The CLI accepts at least one text or Markdown source path and creates a workflow run with a stable run ID.
2. Each source document stores source type, title, fingerprint, text length, and created timestamp.
3. Duplicate source content in the same run is detected by fingerprint and reported without creating a second document.
4. Likely credentials or secrets in source text are flagged before any export or log output.

Out of scope for v1:

- Direct Google Docs, Notion, Loom, Slack, Airtable, or Sheets import.
- OCR or multimodal screenshot parsing.
- Audio/video transcription.

---

## Feature Area: Workflow Extraction

Description: The system extracts actors, systems, triggers, inputs, workflow steps, decisions, exceptions, data fields, pain points, and candidate automation boundaries from messy source text.

Acceptance criteria:

1. Extraction returns a typed workflow map that passes Pydantic validation.
2. Every extracted workflow step includes a source evidence reference or an explicit assumption marker.
3. Missing critical fields produce structured missing-question entries.
4. Extraction failures preserve the source run and return actionable errors without dropping source references.

Out of scope for v1:

- Autonomous stakeholder outreach.
- Final business-process approval.
- Fully automatic architecture decisions.

---

## Feature Area: Retrieval

Description: The system retrieves relevant current-run source snippets and local pattern-library examples to ground blueprint synthesis.

Retrieval mode: text-only for v1.

Sources indexed:

- Current workflow source chunks from pasted text, Markdown files, transcripts, SOP notes, and structured samples.
- Local pattern-library chunks for automation blueprint structure, approval boundaries, integration checklists, eval cases, and guardrail examples.

Expected query types:

- current workflow steps, actors, systems, fields, decisions, exceptions, and risks
- reusable automation patterns and approval-boundary examples
- eval-case and observability templates
- no-answer queries where the corpus does not contain support

Evidence and citation format:

- Every evidence snippet includes source ID, chunk ID, corpus type, heading path, score, text preview, and character offsets when available.
- Blueprint sections cite evidence by source ID and chunk ID.
- Claims without evidence must be marked as explicit assumptions and remain reviewable.

`insufficient_evidence` behavior:

- Query-time retrieval returns `insufficient_evidence` when no retrieved snippet satisfies the configured support threshold.
- Blueprint synthesis must not turn `insufficient_evidence` into a supported claim.

Acceptance criteria:

1. Retrieval indexes normalized source chunks and pattern templates with index schema version v1.
2. Query-time retrieval returns numbered evidence snippets with source ID, chunk ID, and score.
3. Queries without enough evidence return `insufficient_evidence` instead of fabricated support.
4. Retrieval eval records hit@k, no-answer accuracy, citation precision, and latency for the v1 fixture set.

Out of scope for v1:

- Multimodal retrieval.
- Cross-workspace corpus sharing.
- Live web search.

---

## Feature Area: Blueprint Generation

Description: The system synthesizes a structured automation blueprint from extracted workflow facts, retrieved evidence, deterministic validators, and operator edits.

Acceptance criteria:

1. A generated blueprint includes summary, actors, systems, triggers, steps, decisions, exceptions, data fields, integration map, pain points, automation candidates, approval boundaries, risks, assumptions, eval cases, observability needs, effort band, and next implementation tasks.
2. Every non-obvious claim includes evidence references or an explicit assumption marker.
3. Forbidden claims such as automatic production agent building are blocked by validation.
4. Draft blueprints cannot be marked approved until required sections and validators pass.

Out of scope for v1:

- Automatic agent implementation.
- Autonomous deployment.
- Direct production execution.

---

## Feature Area: Review and Approval

Description: The operator can review generated sections, see validation findings, edit the blueprint, answer missing questions, and mark the blueprint approved.

Acceptance criteria:

1. Validation findings identify the section, rule, severity, and repair hint.
2. Operator edits create a new immutable blueprint version.
3. Approval requires zero blocking validator findings.
4. Approval status, reviewer identity placeholder, and timestamp are stored in the audit log.

Out of scope for v1:

- Multi-user approval workflows.
- Role-based access control.
- Electronic signatures.

---

## Feature Area: Markdown Export

Description: The operator can export approved or draft blueprints to Markdown. Draft exports must be labeled as drafts.

Acceptance criteria:

1. Markdown export includes all blueprint sections in a stable order.
2. Draft exports include a visible draft status and unresolved findings section.
3. Approved exports include source/evidence appendix and blueprint version ID.
4. Export writes only to local paths selected by the operator.

Out of scope for v1:

- GitHub issue creation.
- Client portal publishing.
- Email or Slack sending.

---

## Feature Area: Observability and Audit

Description: The system records safe operational events and evaluation metrics without leaking source content or secrets.

Acceptance criteria:

1. Every run, source import, generation attempt, validation result, approval, and export creates an audit event.
2. Logs and spans never include raw source text, secrets, or PII-like field values.
3. The health/status command reports storage availability, index schema version, and pattern-library age.
4. Cost, latency, and model usage are recorded at aggregate level for each workflow run.

Out of scope for v1:

- Centralized telemetry service.
- Production incident alerting.
- Compliance certification evidence.
