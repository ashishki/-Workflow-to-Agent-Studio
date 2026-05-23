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

Passing this gate authorizes a controlled source request only. It does not create
a pilot measurement row, does not satisfy T34/T40, and does not support
commercial claims until the prospect source is reviewed by a human reviewer and
recorded in `docs/pilot_measurement.md`.

The active AI product development roadmap is documented in [`docs/tasks.md`](tasks.md), with strategy summarized in [`docs/product_strategy.md`](product_strategy.md).
