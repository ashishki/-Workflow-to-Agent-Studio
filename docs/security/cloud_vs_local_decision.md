# Cloud Vs Local Decision

Purpose: select the safest practical processing mode for each roadmap
recommendation.

## Decision Matrix

| Condition | Recommended Mode |
|-----------|------------------|
| public/internal data only | lightweight cloud |
| sensitive personal data but redaction preserves context | lightweight cloud after redaction or private analysis |
| confidential business data | private analysis |
| passports, legal status, medical records, tax records, card data | local/on-prem or strict private analysis |
| customer cannot approve external model calls | local/on-prem |
| quality requires raw restricted documents | local/on-prem with human review |
| process can be described with metadata only | cloud or private using synthetic/redacted input |

## Required Report Fields

For every initiative:

- cloud_safe: yes/no/conditional;
- private_mode_recommended: yes/no;
- local_required: yes/no;
- redaction_required: yes/no;
- data classes involved;
- rationale;
- residual risk;
- human review gate;
- cost/quality tradeoff.

## Unsafe Recommendations

Block:

- "send all customer data to cloud";
- "cloud is safe because the model is good";
- "disclaimer is enough for legal advice";
- "local model means compliant";
- "private mode removes need for human review".

## Implementation Notes

The MVP should support policy decisions before it supports complex deployment.
For local/on-prem mode, the roadmap can recommend the mode and explain cost and
quality tradeoffs before the product has a packaged installer.
