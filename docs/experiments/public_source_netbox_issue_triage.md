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
  --database .data/public_source_experiments/netbox_issue_triage_v2.sqlite3 \
  --run-id public-netbox-issue-triage-v2 \
  --index-dir .data/public_source_experiments/netbox_index_v2 \
  tests/fixtures/public_sources/netbox_issue_triage.notes.md
```

Observed output:

```json
{
  "blueprint_version_id": 1,
  "chunk_count": 19,
  "exit_code": 0,
  "finding_ids": [],
  "index_namespace": "v1-public-netbox-issue-triage-v2-e2e",
  "run_id": "public-netbox-issue-triage-v2",
  "source_count": 1
}
```

Follow-up exports:

```bash
.venv/bin/workflow-agent-studio export \
  --database .data/public_source_experiments/netbox_issue_triage_v2.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir .data/public_source_experiments/exports_v2 \
  --output netbox_blueprint.md

.venv/bin/workflow-agent-studio review \
  --database .data/public_source_experiments/netbox_issue_triage_v2.sqlite3 \
  --run-id public-netbox-issue-triage-v2 \
  --blueprint-version-id 1 \
  --export-dir .data/public_source_experiments/exports_v2 \
  --output netbox_review.md
```

## Findings

The pipeline successfully ingested the public-source fixture, built a local
retrieval index, generated a draft blueprint version, and exported both the
blueprint and review workspace.

The initial result exposed a product gap: deterministic extraction and synthesis
were template-shaped and returned a generic support-intake blueprint instead of
preserving NetBox-specific facts.

The current result preserves NetBox-specific actors, systems, decisions,
exceptions, data fields, automation boundary, and approval boundary. The exported
draft includes GitHub Issues, issue templates, reporter and maintainer roles,
duplicate handling, stale handling, reproducibility checks, and maintainer
approval before issue state changes.

This is acceptable as a public-source demo quality signal, but it is still not a
pilot substitute.

## Result

Experiment result: pass for pipeline mechanics, pass for domain-specific draft
quality, still blocked for real-pilot proof.

Recommended next development loop:

- package the public-source demo output into a reproducible demo pack;
- add at least one more public workflow source to test stability across domains;
- keep the real-pilot gate closed until a human operator reviews a real workflow
  source and records acceptance metrics in `docs/pilot_measurement.md`.
