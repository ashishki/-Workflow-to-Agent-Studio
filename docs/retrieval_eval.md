# Retrieval Evaluation - Workflow-to-Agent Studio

Status: planned
Profile: RAG ON
Retrieval mode: text-only
Date: 2026-05-19

---

## Evaluation Method

The v1 retrieval evaluation measures whether the system can retrieve source and pattern evidence needed to build automation blueprints.

Metrics:

- hit@3 for representative workflow and pattern queries
- hit@5 and MRR for ranking quality
- no-answer accuracy for unsupported questions
- citation precision for evidence snippets used in generated sections
- median and p95 retrieval latency in milliseconds
- corpus version recorded for every run
- Eval Source recorded for every run

Regression criteria:

- Any hit@3 drop greater than 0.05 from the current baseline is a P1 unless justified and accepted.
- Any no-answer accuracy drop below 1.00 on the unsupported fixture set is a P1.
- Any evaluation row without Date, Corpus Version, or Eval Source is incomplete.
- Any query-time retrieval change without an `insufficient_evidence` test is incomplete.

Reference pattern: `Dream_Motif_Interpreter/docs/retrieval_eval.md` separates retrieval quality from answer quality and requires exact Eval Source values. Use `docs/IMPLEMENTATION_REFERENCE_MAP.md` when implementing the eval script and tests.

---

## Evaluation Dataset

Initial fixture set to implement in Phase 3:

| Query ID | Query Purpose | Query Type | Expected Evidence |
|----------|---------------|------------|-------------------|
| Q01 | Retrieve current workflow steps from sample SOP | simple | Source chunk containing ordered SOP steps |
| Q02 | Retrieve actors and systems | simple | Source chunk naming actors and tools |
| Q03 | Retrieve exception handling | simple | Source chunk describing exceptions or missing detail |
| Q04 | Retrieve approval boundary pattern | pattern | Pattern-library chunk for human approval boundaries |
| Q05 | Retrieve eval-case pattern | pattern | Pattern-library chunk for measurable eval cases |
| Q06 | Retrieve integration checklist | pattern | Pattern-library chunk for external integration mapping |
| Q07 | Unsupported production deployment question | no-answer | `insufficient_evidence` |
| Q08 | Unsupported credential extraction question | no-answer | `insufficient_evidence` |
| Q09 | Retrieve source data fields | field-exact | Source chunk containing form/API fields |
| Q10 | Retrieve risk or assumption evidence | multi-hop | Source or pattern chunk supporting risk/assumption section |

## Regression Slices

Focused regression slices are added after real operator failures. Follow the `Dream_Motif_Interpreter` pattern:

- name the failure and date
- list exact queries
- define the expected evidence class
- define false-positive or false-negative policy
- record Eval Source and current result

Initial planned slices:

- exact field recall: field names from forms/API samples must surface exact source evidence
- approval boundary recall: approval, escalation, sign-off, and security-review language must retrieve approval-boundary evidence
- unsupported execution claims: production deployment, credential extraction, or autonomous execution queries must return `insufficient_evidence`

---

## Baseline

Not yet measured. First baseline is established by T09-T11.

---

## Evaluation History

| Date | Task | Corpus Version | Index Schema | Eval Source | hit@3 | hit@5 | MRR | Citation precision | No-answer acc. | p50 ms | p95 ms | Regression? |
|------|------|----------------|--------------|-------------|-------|-------|-----|--------------------|----------------|--------|--------|-------------|

---

## Answer Quality Metrics

Not yet measured. Once blueprint synthesis uses retrieved context, record answer quality separately from retrieval quality:

| Date | Task | Corpus Version | Eval Source | Faithfulness | Completeness | Relevance | Regression? |
|------|------|----------------|-------------|--------------|--------------|-----------|-------------|

---

## Open Retrieval Findings

none

---

## Regression Notes

none
