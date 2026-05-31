# Entropy Core And Gensyn Integration

Status: receipt wired into approved export loop; Core runtime not adopted
Last updated: 2026-05-31

## Purpose

Workflow-To-Agent Studio can use Entropy Core vocabulary to make generated agent
blueprints auditable. Gensyn is a design reference for diverse candidate designs
and evaluator/referee roles, not a runtime dependency.

Before building custom Gensyn-shaped logic, run the Gensyn OSS reuse gate from
`repo://AI_workflow_playbook/docs/entropy_core_and_gensyn_reference_policy.md`.
Check official Gensyn repos first and record whether the result is dependency,
vendored component, adapted code, pattern-only reuse, or rejection.

## Entropy Core Use

Default level: schema-compatible for blueprint proof receipts.

Local artifacts:

- `blueprint_proof_receipt` implemented in `workflow_agent_studio/proof.py`
- `permission_boundary_receipt`
- `agent_design_referee_verdict`
- `playbook_export_receipt`

Example:

```yaml
type: workflow_blueprint_receipt
source_project: workflow-to-agent-studio
workflow_id: wf-example
artifact_path: docs/blueprints/wf-example.yml
evidence:
  - path: docs/discovery/wf-example.md
  - path: docs/blueprints/wf-example.yml
verifier:
  method: human_review
  status: pending
entropy_core:
  use_level: receipt_compatible
  runtime_dependency: false
```

## Required Context-Refs

Tasks that introduce or change receipt behavior should include:

```yaml
Context-Refs:
  - repo://AI_workflow_playbook/docs/entropy_core_and_gensyn_reference_policy.md
  - repo://Entropy_Protocol/docs/ENTROPY_CORE_AND_GENSYN_REFERENCES.md
  - repo://Entropy_Protocol/products/entropy-core/docs/tasks.md#T123
```

## Gensyn-Inspired Pattern

Allowed adaptation:

```text
multiple blueprint candidates -> critic/evaluator pass -> referee verdict -> selected design
```

Use it for high-impact workflow designs where one generated blueprint may miss a
better permission model or failure boundary.

## Proof Layer Implementation

Workflow-to-Agent Studio should use Entropy Core to prove blueprint decisions,
not to generate blueprints.

Implemented now:

- `build_blueprint_proof_receipt(...)` hashes the blueprint artifact payload,
  records schema version, collects source/chunk evidence refs across blueprint
  sections, and counts explicit assumptions.
- Receipts fail validation when no evidence refs exist.
- Approved blueprint, approved governance report, and approved implementation
  handoff exports write a `*.proof_receipt.json` sidecar that hashes the
  exported Markdown artifact.
- Implementation handoff export is blocked when the proof receipt cannot pass
  validation.
- `tests/unit/test_proof_receipts.py` covers artifact hash, evidence refs,
  assumption count, receipt hash, and missing-evidence rejection.

Next implementation tasks:

1. Use schema compatibility before changing exported blueprint or receipt
   formats.
2. Add evidence lookup refs for discovery notes, SOP excerpts, risk findings,
   and approval decisions.
3. Keep workflow synthesis, UI, client editing, and export behavior
   product-local.
4. Extend export-to-implementation blocking beyond receipt validation when
   reviewer verdict metadata and permission-boundary receipts exist.

Core value here: prevent impressive but ungrounded agent blueprints from being
treated as implementation-ready.

Not adopted:

- decentralized training;
- token incentives;
- on-chain coordination;
- P2P swarm runtime;
- model weight updates.

## Code Reuse Boundary

Do not copy Gensyn code into this project casually. If the reuse gate finds a
fit, create an ADR or task note with license, commit, file refs, attribution,
security notes, and why dependency, vendoring, adapted code, pattern-only reuse,
or rejection is the right choice.
