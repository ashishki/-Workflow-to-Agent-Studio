# Evaluation Guide

Run all tests:

```bash
python -m pytest tests/ -q
```

## Retrieval Evaluation

Command:

```bash
python -m pytest tests/integration/test_retrieval_query.py tests/eval/test_retrieval_eval.py -q
```

Metrics updated in `docs/retrieval_eval.md`:

- hit@3
- hit@5
- MRR
- citation precision
- no-answer accuracy
- p50 retrieval latency
- p95 retrieval latency
- corpus version
- eval source

End-to-end retrieval fixture command:

```bash
python -m pytest tests/integration/test_cli_workflow.py tests/eval/test_end_to_end_eval.py -q
```

## Planning Evaluation

Command:

```bash
python -m pytest tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py -q
```

Metrics updated in `docs/plan_eval.md`:

- schema validation pass rate
- blueprint synthesis section coverage
- validation fixture expected-outcome pass rate
- blocking finding count
- review approval gate expected-outcome pass rate
- end-to-end draft blueprint expected-outcome pass rate

The first pilot proof metric is recorded in [`docs/pilot_measurement.md`](pilot_measurement.md).
It remains template-only until a human-reviewed pilot records both required
threshold results, reviewer edits, and critical missing questions. Overall pass
requires time-to-reviewable blueprint under 30 minutes, at least 80 percent
required-section acceptance after human review, and no unresolved critical
missing questions. The pilot intake checklist in that file must be complete
before any demo, synthetic, or sanitized artifact can be excluded from the
real-pilot evidence gate.

## Prospect Data Request Gate

Before asking a potential customer for real workflow data, run the full test
suite and confirm that public-source evals cover pipeline mechanics,
domain-specific fact preservation, public-vs-pilot boundary labeling, and
demo-pack reproducibility. The current public demo pack is
`docs/experiments/public_demo_pack/netbox_issue_triage/`.

Phase 12 showcase packs live under `docs/experiments/public_demo_pack/`:

- `hvac_lead_intake/`
- `netbox_issue_triage/`
- `gitlab_incident_response/`

Each pack must include a source register or fixture pointer, command transcript,
generated blueprint, review workspace, gap summary, and boundary label.

The public-data working product proof is recorded in
`docs/audit/PUBLIC_DATA_PRODUCT_PROOF.md`. It supports technical demo claims
only and keeps customer proof blocked until real prospect data is reviewed.

## Public Blueprint Quality Review Rubric

Use this rubric before showing a public-source blueprint pack to a prospect.
Scores are `pass`, `warning`, or `fail`.

| Dimension | Pass Standard | Fail / Blocker |
|---|---|---|
| evidence coverage | Important claims cite the public source fixture/register or mark assumptions. | Unsupported claims are presented as facts. |
| workflow specificity | Blueprint preserves domain actors, systems, decisions, data fields, and exceptions. | Blueprint collapses into a generic support-intake draft. |
| missing questions | Missing questions are recorded and classified as demo-only, pilot-blocking, or critical. | Any unresolved critical missing question remains. |
| approval boundaries | Human approval is explicit before external commitments or unsafe actions. | Blueprint allows autonomous commitments, dispatch, closure, paging, or publication. |
| integration realism | Integrations are named as public-source evidence or explicit assumptions. | Blueprint invents internal tools or hidden integrations as facts. |
| eval-case quality | Eval cases are measurable and tied to the workflow boundary. | Eval cases are vague or unrelated to the source workflow. |
| forbidden claims | Pack labels reject buyer proof, pilot proof, pricing, conversion, and demand claims. | Pack implies customer acceptance, commercial proof, T34, or T40 completion. |

`showcase_ready` is allowed only when every dimension is `pass` or documented
`warning` and no unresolved critical missing question remains. Real-pilot gaps
may be non-blocking for public showcase readiness, but they still block
commercial proof and pilot measurement.

Passing this gate authorizes a controlled source request only. It does not create
a pilot measurement row, does not satisfy T34/T40, and does not support
commercial claims until the prospect source is reviewed by a human reviewer and
recorded in `docs/pilot_measurement.md`.

The active AI product development roadmap is documented in [`docs/tasks.md`](tasks.md), with strategy summarized in [`docs/product_strategy.md`](product_strategy.md).
