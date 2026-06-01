# Cost Estimation Eval

Purpose: keep cost ranges honest and avoid false precision.

## Required Estimate Fields

- one-time low/medium/high;
- monthly low/medium/high;
- currency;
- assumptions;
- confidence;
- model/price card version when LLM usage is included;
- maintenance cost;
- human review cost;
- integration/subscription cost.

## Automated Checks

- no single-point cost estimate;
- no estimate without assumptions;
- low <= medium <= high;
- local/private recommendations include infra and maintenance cost;
- cloud LLM recommendations include token/usage assumptions or explicit
  `unknown volume` assumption;
- high-risk workflow cost confidence cannot be high without sample data;
- no ROI guarantee appears.

## Eval History

| Date | Task | Cost Model Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|--------------------|--------|-------|----------|-------|-------------|-------------|
| 2026-06-01 | T76 | cost-engine-baseline-v1 | Deterministic cost engine expected-outcome pass rate | 100%; reminder, support assistant, private document assistant, missing assumptions blocked | 100%; reminder, support assistant, private document assistant, missing assumptions blocked | 0% | No | pytest tests/unit/test_cost_engine.py -q |

## Sanity Bands

The following are planning heuristics, not quotes:

- deterministic reminder: 500-3000 USD;
- small API lookup: 2000-10000 USD;
- support triage assistant: 3000-20000 USD;
- RAG knowledge assistant: 4000-25000 USD;
- private/local document assistant: 15000-80000 USD.

Any generated estimate outside these ranges must include a rationale.

## Human Review

Reviewer questions:

- Are integration assumptions realistic?
- Is maintenance included?
- Is privacy/security overhead included?
- Is confidence overstated?
- Would an implementer object to the range?
