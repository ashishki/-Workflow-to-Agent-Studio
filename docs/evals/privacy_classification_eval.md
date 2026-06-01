# Privacy Classification Eval

Purpose: verify that the privacy classifier catches sensitive and restricted data
before roadmap recommendations choose model mode.

## Required Test Categories

- email;
- phone;
- street address;
- person name in context;
- order ID;
- passport/ID-like value;
- payment card-like value;
- API key;
- legal/immigration keywords;
- health keywords;
- tax/accounting keywords;
- HR/candidate keywords;
- minor/student data hints;
- synthetic examples that should remain allowed.

## Expected Class Examples

| Example | Expected Class |
|---------|----------------|
| public FAQ text | public |
| internal SOP without personal data | internal |
| private pricing/margin process | confidential |
| customer email and shipping address | sensitive |
| passport copy and legal status | restricted |
| diagnosis notes | restricted |
| tax filings | restricted |
| API key | blocked secret |

## Automated Checks

- secret-like values are blocked from export;
- restricted source blocks lightweight cloud recommendation;
- redacted source preserves field names;
- false-positive fixture does not classify generic process terms as restricted;
- report includes source privacy class and recommendation privacy class.

## Eval History

| Date | Task | Classifier Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|--------------------|--------|-------|----------|-------|-------------|-------------|
| 2026-06-01 | T70 | privacy-classification-v1 | Required privacy category coverage | 100%; 13 categories; legal restricted; salon sensitive; false-positive not restricted | 100%; 13 categories; legal restricted; salon sensitive; false-positive not restricted | 0% | No | pytest tests/unit/test_privacy_classifier.py -q |

## Human Review

Reviewers should inspect:

- whether classification is too permissive;
- whether redaction removed business meaning;
- whether cloud/private/local recommendation follows data class;
- whether sensitive examples are marked synthetic or redacted.
