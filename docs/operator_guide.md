# Operator Guide

## V1 Workflow

1. Prepare local text or Markdown workflow sources.
2. Run the local CLI pipeline with `workflow-agent-studio run`.
3. Review the generated draft blueprint version ID and validation finding IDs.
4. Export a draft Markdown brief with `workflow-agent-studio export`.
5. Review the draft manually before using it for project planning or client discussion.

## Sample Source Format

Use plain text or Markdown. A useful source includes:

- actors and systems
- workflow trigger
- ordered process steps
- required data fields
- exception handling
- approval or review boundaries
- integration details

The fixture at `tests/fixtures/sources/sample_sop.md` is the canonical minimal sample.

## Safety Boundaries

V1 does not create agents.
V1 does not deploy automations.
V1 does not mutate production systems.
V1 does not create GitHub issues, send Slack messages, send email, or publish to client portals.

The tool produces local draft artifacts. Human review remains required for final scope, approval boundaries, security assumptions, and implementation decisions.

## Product Development Roadmap

The AI product development phases are documented in `docs/ai_product_development_phases.md`.

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
