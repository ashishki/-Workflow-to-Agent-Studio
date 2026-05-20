# Operator Guide

## V1 Workflow

1. Prepare local workflow sources.
2. Run the local CLI pipeline with `workflow-agent-studio run`.
3. Review the generated draft blueprint version ID and validation finding IDs.
4. Export a draft Markdown brief with `workflow-agent-studio export`.
5. Review the draft manually before using it for project planning or client discussion.

## Sample Source Format

Supported local source kinds:

- plain text: `.txt`
- Markdown: `.md`, `.markdown`
- transcripts: `.transcript`, `.transcript.txt`, `.transcript.md`
- pasted notes: `.notes`, `.notes.txt`, `.notes.md`
- form descriptions: `.form`, `.form.txt`, `.form.md`
- integration snippets: `.integration`, `.integration.txt`, `.integration.md`

Unsupported file types fail before source records are persisted. Keep source files local;
V1 does not import from SaaS tools, external APIs, cloud drives, audio, video, or images.

A useful source includes:

- actors and systems
- workflow trigger
- ordered process steps
- required data fields
- exception handling
- approval or review boundaries
- integration details

The fixture at `tests/fixtures/sources/sample_sop.md` is the canonical minimal sample.

## Public Demo Packs

Public demo packs use open workflow sources to demonstrate product mechanics and
draft quality before prospect data is available. They are not pilot evidence and
must not be used as customer proof.

The current public demo pack is
`docs/experiments/public_demo_pack/netbox_issue_triage/`. It includes the source
fixture reference, command transcript, generated draft blueprint, review
workspace, and gap summary.

## Sanitization For Benchmarks

Benchmark and future pilot artifacts must be sanitized before they are reused outside
the local source context. The deterministic sanitizer redacts common emails, phone
numbers, credential-like tokens, customer/account IDs, and street-address patterns
while preserving headings, ordered steps, and section structure for eval usefulness.
Sanitized or synthetic fixtures still do not count as real pilot evidence.

## Safety Boundaries

V1 does not create agents.
V1 does not deploy automations.
V1 does not mutate production systems.
V1 does not create GitHub issues, send Slack messages, send email, or publish to client portals.

The tool produces local draft artifacts. Human review remains required for final scope, approval boundaries, security assumptions, and implementation decisions.

Governance reports are local Markdown exports for reviewer handoff. They summarize
evidence coverage, assumptions, approval boundaries, readiness, risks, and unresolved
validation findings. Approved governance exports remain blocked when validation has
blocking findings, and output paths stay constrained to the selected export directory.

Approved implementation handoffs are local Markdown exports only. They require an
approved blueprint version and include implementation tasks, eval cases, automation
boundaries, human approval boundaries, assumptions, risks, and an evidence appendix.
Unapproved or validation-blocked blueprints cannot produce approved handoff exports.
External side effects such as issue creation, Slack messages, email, or portal
publication remain disabled unless a future ADR changes the boundary.

## Product Development Roadmap

The active development roadmap is `docs/tasks.md`. Product strategy is summarized in `docs/product_strategy.md`.

## Local Commands

```bash
workflow-agent-studio run \
  --database .data/workflow_studio.sqlite3 \
  --run-id sample-sop \
  --index-dir .data/index \
  tests/fixtures/sources/sample_sop.md
```

```bash
workflow-agent-studio export \
  --database .data/workflow_studio.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir .data/exports \
  --output sample-sop-blueprint.md
```

```bash
workflow-agent-studio review \
  --database .data/workflow_studio.sqlite3 \
  --run-id sample-sop \
  --blueprint-version-id 1 \
  --export-dir .data/exports \
  --output sample-sop-review.md
```

Use `workflow-agent-studio review --set-rough-effort-band medium` when a reviewer needs
to create an edited draft version while exporting the local review workspace. The review
workspace is a local Markdown file for inspecting findings, evidence, comment metadata,
and version history; it does not deploy or execute automation.
