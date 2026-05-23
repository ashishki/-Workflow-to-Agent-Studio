# Command Transcript

Working directory: repository root.

## Run Pipeline

```bash
.venv/bin/workflow-agent-studio run \
  --database .data/public_demo_pack/gitlab_incident_response.sqlite3 \
  --run-id public-demo-gitlab-incident-response \
  --index-dir .data/public_demo_pack/gitlab_incident_response_index \
  tests/fixtures/public_sources/gitlab_incident_workflow.notes.md
```

Observed stdout:

```json
{
  "blueprint_version_id": 1,
  "chunk_count": 16,
  "exit_code": 0,
  "finding_ids": [],
  "index_namespace": "v1-public-demo-gitlab-incident-response-e2e",
  "run_id": "public-demo-gitlab-incident-response",
  "source_count": 1
}
```

## Export Draft Blueprint

```bash
.venv/bin/workflow-agent-studio export \
  --database .data/public_demo_pack/gitlab_incident_response.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/gitlab_incident_response \
  --output generated_blueprint.md
```

Observed status: draft blueprint exported to `generated_blueprint.md`.

## Export Review Workspace

```bash
.venv/bin/workflow-agent-studio review \
  --database .data/public_demo_pack/gitlab_incident_response.sqlite3 \
  --run-id public-demo-gitlab-incident-response \
  --blueprint-version-id 1 \
  --export-dir docs/experiments/public_demo_pack/gitlab_incident_response \
  --output review_workspace.md
```

Observed stdout:

```json
{
  "blueprint_version_id": 1,
  "finding_ids": [],
  "path": "docs/experiments/public_demo_pack/gitlab_incident_response/review_workspace.md"
}
```
