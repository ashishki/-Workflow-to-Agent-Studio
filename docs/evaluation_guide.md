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
