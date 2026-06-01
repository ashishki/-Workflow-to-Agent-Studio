# Cost Estimation

Purpose: produce honest implementation and run-cost ranges with assumptions.

Cost estimates are not quotes. They are planning ranges that must be reviewed by
a human before being shown as implementation commitments.

## Components

Total estimate =

- implementation labor;
- LLM API usage;
- embedding/retrieval cost;
- vector database or storage;
- hosting;
- monitoring;
- human review;
- integration subscriptions;
- maintenance;
- security/privacy overhead;
- contingency.

## LLM Usage Formula

```text
monthly_llm_cost =
  requests_per_month
  * (
      avg_input_tokens * input_price_per_token
    + avg_cached_tokens * cached_price_per_token
    + avg_output_tokens * output_price_per_token
    )
  * retry_multiplier
  * safety_margin
```

Model prices change. Price cards must be versioned and include:

- provider;
- model;
- input price;
- output price;
- cached input price if used;
- captured_at date;
- source URL or manual source note;
- currency.

Do not hardcode current public model prices in product prose. Keep them in
versioned config and update them from official provider pages.

## Cost Confidence

High confidence:

- known volume;
- known systems;
- known data classes;
- existing SOP/policy;
- implementation pattern is mature.

Medium confidence:

- workflow known;
- volume estimated;
- integrations plausible;
- data quality partially known.

Low confidence:

- volume unknown;
- unclear integrations;
- sensitive data unresolved;
- no sample data;
- local/private deployment not tested.

## Example Ranges

### Cloud LLM Support Assistant

Assumptions:

- 2000 support messages/month;
- FAQ/policy exists;
- cloud LLM allowed after redaction;
- human review during pilot.

Planning range:

- implementation: 3000-20000 USD;
- monthly LLM/API/hosting: 50-1000 USD for small SMB usage;
- maintenance: 300-2000 USD/month;
- confidence: medium when support volume is known.

### Internal Knowledge Assistant

Assumptions:

- 50-500 documents;
- 10-100 employees;
- RAG over controlled internal docs;
- no high-sensitive data in MVP.

Planning range:

- implementation: 4000-25000 USD;
- monthly LLM/vector/hosting: 100-1500 USD;
- maintenance: document refresh, eval updates, access review;
- main cost driver: document quality and access control.

### Local/Private Document Analysis

Assumptions:

- sensitive legal, medical, financial, or identity documents;
- local/private model path;
- document extraction plus human review;
- security review required.

Planning range:

- implementation: 15000-80000 USD;
- infra: 500-5000 USD/month or GPU hardware cost;
- maintenance: high;
- confidence: low-medium until model quality and deployment constraints are
  tested.

## Blocking Rules

- No estimate without assumptions.
- No single-point estimate without a range.
- No ROI claim without pilot evidence.
- No local/private deployment estimate without infra and maintenance cost.
