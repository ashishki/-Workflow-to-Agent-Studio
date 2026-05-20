# Command Transcript

Working directory: repository root.

## Run Pipeline

```bash
mkdir -p .data/public_demo_pack docs/experiments/public_demo_pack/netbox_issue_triage
.venv/bin/workflow-agent-studio run \
  --database .data/public_demo_pack/netbox_issue_triage.sqlite3 \
  --run-id public-demo-netbox-issue-triage \
  --index-dir .data/public_demo_pack/netbox_index \
  tests/fixtures/public_sources/netbox_issue_triage.notes.md
```

Observed stdout:

```json
{
  "blueprint_version_id": 1,
  "chunk_count": 19,
  "exit_code": 0,
  "finding_ids": [],
  "index_namespace": "v1-public-demo-netbox-issue-triage-e2e",
  "run_id": "public-demo-netbox-issue-triage",
  "source_count": 1
}
```

## Export Draft Blueprint

```bash
.venv/bin/workflow-agent-studio export \
  --database .data/public_demo_pack/netbox_issue_triage.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/netbox_issue_triage \
  --output generated_blueprint.md
```

Observed status: draft blueprint exported to `generated_blueprint.md`.

## Export Review Workspace

```bash
.venv/bin/workflow-agent-studio review \
  --database .data/public_demo_pack/netbox_issue_triage.sqlite3 \
  --run-id public-demo-netbox-issue-triage \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/netbox_issue_triage \
  --output review_workspace.md
```

Observed status: review workspace exported to `review_workspace.md` with no
validation findings.
