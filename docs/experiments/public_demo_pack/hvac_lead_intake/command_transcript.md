# Command Transcript

Working directory: repository root.

## Run Pipeline

```bash
.venv/bin/workflow-agent-studio run \
  --database .data/public_demo_pack/hvac_lead_intake.sqlite3 \
  --run-id public-demo-hvac-lead-intake \
  --index-dir .data/public_demo_pack/hvac_lead_intake_index \
  tests/fixtures/public_sources/hvac_lead_intake.notes.md
```

Observed stdout:

```json
{
  "blueprint_version_id": 1,
  "chunk_count": 16,
  "exit_code": 0,
  "finding_ids": [],
  "index_namespace": "v1-public-demo-hvac-lead-intake-e2e",
  "run_id": "public-demo-hvac-lead-intake",
  "source_count": 1
}
```

## Export Draft Blueprint

```bash
.venv/bin/workflow-agent-studio export \
  --database .data/public_demo_pack/hvac_lead_intake.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/hvac_lead_intake \
  --output generated_blueprint.md
```

Observed status: draft blueprint exported to `generated_blueprint.md`.

## Export Review Workspace

```bash
.venv/bin/workflow-agent-studio review \
  --database .data/public_demo_pack/hvac_lead_intake.sqlite3 \
  --run-id public-demo-hvac-lead-intake \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/hvac_lead_intake \
  --output review_workspace.md
```

Observed stdout:

```json
{
  "blueprint_version_id": 1,
  "finding_ids": [],
  "path": "docs/experiments/public_demo_pack/hvac_lead_intake/review_workspace.md"
}
```
