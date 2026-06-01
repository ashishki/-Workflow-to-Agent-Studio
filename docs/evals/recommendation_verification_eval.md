# Recommendation Verification Eval

Purpose: verify that recommendations are supported, traceable, and reviewable.

## Required Checks

- recommendation has ID;
- recommendation targets a workflow step;
- recommendation has solution type;
- recommendation has required data;
- recommendation has privacy class;
- recommendation has cost and time ranges;
- recommendation has risks;
- recommendation has validation method;
- recommendation has success metrics;
- recommendation has evidence or explicit assumptions;
- recommendation has fallback;
- high-risk recommendation has human gate;
- recommendation trace records pattern, cost, scoring, and privacy model
  versions.

## Forbidden Claims

Block:

- guaranteed ROI;
- fully compliant;
- no human needed;
- replaces human experts;
- automatically builds the agent;
- safe to send all customer data;
- legal advice automation;
- medical diagnosis automation;
- autonomous hiring rejection;
- autonomous refund/financial approval in MVP.

## Review Output

For each recommendation:

```yaml
recommendation_id: REC-001
accepted: yes/no/edited
reason: ""
missing_evidence: []
cost_realism: low/medium/high
privacy_concern: ""
would_show_to_client: yes/no
required_changes: []
```

## Pass Threshold

Report passes when:

- zero blocking verification findings;
- zero forbidden claims;
- all unresolved assumptions are listed;
- high-risk recommendations are either blocked or human-gated.

## Eval History

| Date | Task | Eval Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|--------------|--------|-------|----------|-------|-------------|-------------|
| 2026-06-01 | T81 | roadmap-eval-suite-v1 | Recommendation verification pass rate | 100%; evidence or assumptions present; trace model versions present | 100%; evidence or assumptions present; trace model versions present | 0% | No | pytest tests/eval/test_recommendation_verification_eval.py -q |
