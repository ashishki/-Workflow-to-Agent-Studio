# Public Data Product Proof

Status: public_data_working_product_proof
Date: 2026-05-23

Public-data proof means technical workflow proof, not customer proof. It proves
the local product can turn public workflow descriptions into evidence-linked,
validated, reviewable automation blueprints. It does not prove demand, buyer
value, conversion, customer acceptance, or pilot success.

## Proof Claim

This is enough to say the product works on public workflow data:

- It ingests local public-source workflow notes.
- It chunks and indexes the source for evidence-backed retrieval.
- It extracts workflow-specific actors, systems, decisions, steps, exceptions,
  data fields, and missing questions.
- It generates a typed automation blueprint with human approval boundaries,
  eval cases, implementation tasks, and risk assumptions.
- It validates the draft with `finding_ids=[]`.
- It exports a local Markdown draft for review.
- It rejects the generic support-intake fallback for domain-specific public
  workflows.
- It preserves public-vs-pilot boundary labels.

## Public Data Coverage

Current coverage: 8 public workflow fixtures.

| Fixture | Source type | Product proof |
|---|---|---|
| NetBox issue triage | public project workflow | run + export + domain fact preservation |
| Kubernetes issue triage | public project workflow | run + export + domain fact preservation |
| OpenStack bug triage | public project workflow | run + export + domain fact preservation |
| GitLab incident response | public runbook workflow | run + export + domain fact preservation |
| HVAC lead intake | public business workflow | run + export + domain fact preservation |
| Django ticket triage | public project workflow | run + export + domain fact preservation |
| Mozilla Bugzilla triage | public project workflow | run + export + domain fact preservation |
| Apache Airflow issue triage | public project workflow | run + export + domain fact preservation |

Showcase coverage: 3 showcase-ready public demo packs.

- `docs/experiments/public_demo_pack/hvac_lead_intake/`
- `docs/experiments/public_demo_pack/netbox_issue_triage/`
- `docs/experiments/public_demo_pack/gitlab_incident_response/`

## Regression Gates

Public-data proof is guarded by:

- `tests/eval/test_public_source_experiment.py`
- `tests/unit/test_public_workflow_extraction_profiles.py`
- `tests/eval/test_plan_eval.py`
- `tests/eval/test_retrieval_eval.py`

The internet workflow examples must pass `workflow_agent_studio.cli run` and
`workflow_agent_studio.cli export`, return `finding_ids=[]`, preserve
domain-specific terms, and avoid the generic sentence `Support intake workflow
routes customer requests`.

Support intake generic fallback rejected for Django ticket triage, Mozilla
Bugzilla triage, and Apache Airflow issue triage.

## Boundary

This public-data proof supports demo and technical product claims only:

- allowed: "The product works locally on public workflow data."
- allowed: "The product can generate reviewable automation blueprints from
  public workflow examples."
- forbidden: "Customers validated this."
- forbidden: "A buyer accepted this."
- forbidden: "This satisfies pilot evidence."

T34 and T40 remain blocked until a real prospect/customer workflow packet and
named reviewer are recorded in `docs/pilot_measurement.md`.
