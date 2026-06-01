# Scoring Model

Purpose: prioritize AI implementation opportunities without fake precision.

The output is a band, not a decimal score.

## Business Value

Business Value =

- 0.30 impact;
- 0.20 frequency/volume;
- 0.15 pain severity;
- 0.15 strategic fit;
- 0.10 time-to-value;
- 0.10 reusability.

## Delivery Readiness

Delivery Readiness =

- 0.25 data readiness;
- 0.20 process stability;
- 0.20 integration feasibility;
- 0.15 evaluation clarity;
- 0.10 stakeholder ownership;
- 0.10 pattern fit.

## Risk Penalty

Risk Penalty =

- 0.30 privacy risk;
- 0.25 security risk;
- 0.20 business criticality;
- 0.15 compliance risk;
- 0.10 change management risk.

## Priority Bands

| Band | Meaning |
|------|---------|
| Quick win | high value, high readiness, low or moderate risk |
| Strategic pilot | high value, medium readiness, controlled risk |
| Prepare first | value exists but process, data, or ownership is not ready |
| Do not automate yet | high risk, low clarity, no owner, or no eval path |
| Classic automation | deterministic script/integration is enough |
| Human-only | high-stakes judgment should remain manual |

## Display Format

Do not show `87.43`.

Show:

```text
Priority: High
Confidence: Medium
Why:
- high message volume
- clear FAQ
- low integration complexity
- moderate privacy risk
Uncertainty:
- exact monthly volume not verified
- refund policy needs review
```

## Confidence Bands

High confidence:

- volume known;
- workflow stable;
- system ownership clear;
- data sources known;
- evaluation set can be built.

Medium confidence:

- workflow known;
- volume estimated;
- integrations plausible;
- privacy classification mostly clear.

Low confidence:

- volume unknown;
- source data missing;
- owner unclear;
- high-risk domain unresolved;
- no eval examples.
