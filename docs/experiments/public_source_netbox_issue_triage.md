# Public Source Experiment: NetBox Issue Triage

Status: public-source experiment; not real pilot evidence.

Source: https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow

Accessed: 2026-05-20

Local fixture:
`tests/fixtures/public_sources/netbox_issue_triage.notes.md`

## Boundary

This experiment uses a paraphrased public workflow description from the NetBox
GitHub wiki. It exercises product mechanics against a realistic open workflow,
but it is not counted in `docs/pilot_measurement.md`, does not satisfy T34/T40,
and cannot support commercial claims.

Missing proof that only a real pilot can provide:

- live workflow owner acceptance;
- reviewer edits against a real operator workflow;
- measured time to a reviewable blueprint in a real sales or delivery context;
- confirmation that critical missing questions are resolved by the operator;
- evidence that the buyer values the output enough to pay or continue.

## Procedure

The source page was reduced to a local notes file that preserves workflow facts
without copying the full public wiki page. The CLI was then run with a temporary
database and retrieval index under `.data/`.

Command:

```bash
mkdir -p .data/public_source_experiments
.venv/bin/workflow-agent-studio run \
  --database .data/public_source_experiments/netbox_issue_triage.sqlite3 \
  --run-id public-netbox-issue-triage \
  --index-dir .data/public_source_experiments/netbox_index \
  tests/fixtures/public_sources/netbox_issue_triage.notes.md
```

Observed output:

```json
{
  "blueprint_version_id": 1,
  "chunk_count": 19,
  "exit_code": 0,
  "finding_ids": [],
  "index_namespace": "v1-public-netbox-issue-triage-e2e",
  "run_id": "public-netbox-issue-triage",
  "source_count": 1
}
```

Follow-up exports:

```bash
.venv/bin/workflow-agent-studio export \
  --database .data/public_source_experiments/netbox_issue_triage.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir .data/public_source_experiments/exports \
  --output netbox_blueprint.md

.venv/bin/workflow-agent-studio review \
  --database .data/public_source_experiments/netbox_issue_triage.sqlite3 \
  --run-id public-netbox-issue-triage \
  --blueprint-version-id 1 \
  --export-dir .data/public_source_experiments/exports \
  --output netbox_review.md
```

## Findings

The pipeline successfully ingested the public-source fixture, built a local
retrieval index, generated a draft blueprint version, and exported both the
blueprint and review workspace.

The result also exposed a product gap: the current deterministic extraction and
synthesis path is template-shaped. It returns a generic support-intake blueprint
instead of preserving NetBox-specific facts such as issue templates, stale issue
handling, duplicate triage, reproducibility checks, feature request scope checks,
and maintainer canned responses.

This is acceptable for a mechanics experiment, but it is not acceptable as a
public demo outcome or pilot substitute. Before using public workflows for a
credible demo, extraction and synthesis need to preserve domain-specific actors,
systems, decisions, exceptions, and approval boundaries from the source.

## Result

Experiment result: pass for pipeline mechanics, fail for domain-specific draft
quality.

Recommended next development loop:

- add a provider-backed or rule-backed extraction fixture for public workflow
  documents;
- add an eval that checks whether NetBox-specific workflow facts survive into
  the blueprint;
- keep the real-pilot gate closed until a human operator reviews a real workflow
  source and records acceptance metrics in `docs/pilot_measurement.md`.
