# Retrieval Evaluation - Workflow-to-Agent Studio

Status: active
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

T07 established the initial source ingestion corpus fixture baseline before chunking,
embedding, or query-time retrieval exists.

T09 established the v1 chunking corpus fixture baseline for one source fixture and two
pattern-library templates.

T10 established the first local vector index metadata baseline with deterministic fake
embeddings and schema-versioned namespaces.

T11 established the first query-time retrieval metrics baseline with hit@3,
no-answer accuracy, citation precision, and `insufficient_evidence` behavior.

T18 established the end-to-end sample SOP fixture retrieval baseline through the CLI
workflow.

T21 established the transcript ingestion fixture baseline with speaker-label
normalization and whitespace-stable source fingerprints.

T22 established the notes, forms, and integration ingestion fixture baseline
with source-kind metadata and unsupported file rejection.

T24 established the real-world-style corpus fixture baseline with transcript,
notes, form, and integration source fixtures.

T25 established the evidence pack citation precision baseline for blueprint
sections and automation candidates.

- Date: 2026-05-19
- Task: T07
- Corpus Version: source-fixture-v1
- Index Schema: n/a
- Eval Source: pytest tests/integration/test_ingestion.py tests/eval/test_retrieval_eval.py -q
- Metric: Source ingestion fixture pass rate
- Score: 100%
- Regression: No

Chunking baseline:

- Date: 2026-05-19
- Task: T09
- Corpus Version: chunking-fixture-v1
- Index Schema: n/a
- Eval Source: pytest tests/unit/test_chunking.py tests/unit/test_pattern_library.py tests/eval/test_retrieval_eval.py -q
- Metric: Chunking corpus fixture count
- Score: 3 documents / 4 chunks
- Regression: No

Index baseline:

- Date: 2026-05-19
- Task: T10
- Corpus Version: index-fixture-v1
- Index Schema: v1
- Eval Source: pytest tests/unit/test_embeddings.py tests/integration/test_retrieval_index.py tests/eval/test_retrieval_eval.py -q
- Metric: Index metadata and namespace versioning
- Score: 100%
- Retrieval latency placeholder: n/a until query-time retrieval
- Regression: No

Query baseline:

- Date: 2026-05-19
- Task: T11
- Corpus Version: query-fixture-v1
- Index Schema: v1
- Eval Source: pytest tests/integration/test_retrieval_query.py tests/eval/test_retrieval_eval.py -q
- hit@3: 1.00
- hit@5: 1.00
- MRR: 1.00
- Citation precision: 1.00
- No-answer accuracy: 1.00
- p50 ms: 0.00
- p95 ms: 0.00
- Regression: No

Transcript ingestion baseline:

- Date: 2026-05-20
- Task: T21
- Corpus Version: transcript-fixture-v1
- Index Schema: n/a
- Eval Source: pytest tests/integration/test_ingestion.py tests/eval/test_retrieval_eval.py -q
- Metric: Transcript ingestion fixture pass rate
- Score: 100%
- Regression: No

Discovery artifact ingestion baseline:

- Date: 2026-05-20
- Task: T22
- Corpus Version: discovery-artifacts-fixture-v1
- Index Schema: n/a
- Eval Source: pytest tests/integration/test_ingestion.py tests/unit/test_docs.py tests/eval/test_retrieval_eval.py -q
- Metric: Notes, forms, and integration source-kind fixture pass rate
- Score: 100%
- Regression: No

Real-world-style corpus baseline:

- Date: 2026-05-20
- Task: T24
- Corpus Version: real-world-corpus-v1
- Index Schema: n/a
- Eval Source: pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_retrieval_eval.py -q
- Corpus count: 4
- Chunk count: 10
- Citation support: 1.00
- Regression: No

Evidence pack baseline:

- Date: 2026-05-20
- Task: T25
- Corpus Version: evidence-pack-fixture-v1
- Index Schema: v1
- Eval Source: pytest tests/integration/test_evidence_packs.py tests/eval/test_retrieval_eval.py -q
- Section packs: 2
- Automation candidate packs: 1
- Unsupported sections returning insufficient_evidence: 1
- Citation precision: 1.00
- Regression: No

---

## Evaluation History

| Date | Task | Corpus Version | Index Schema | Eval Source | hit@3 | hit@5 | MRR | Citation precision | No-answer acc. | p50 ms | p95 ms | Regression? |
|------|------|----------------|--------------|-------------|-------|-------|-----|--------------------|----------------|--------|--------|-------------|
| 2026-05-19 | T07 | source-fixture-v1 | n/a | pytest tests/integration/test_ingestion.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | n/a | n/a | n/a | n/a | No |
| 2026-05-19 | T09 | chunking-fixture-v1 | n/a | pytest tests/unit/test_chunking.py tests/unit/test_pattern_library.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | n/a | n/a | n/a | n/a | No |
| 2026-05-19 | T10 | index-fixture-v1 | v1 | pytest tests/unit/test_embeddings.py tests/integration/test_retrieval_index.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | n/a | n/a | n/a | n/a | No |
| 2026-05-19 | T11 | query-fixture-v1 | v1 | pytest tests/integration/test_retrieval_query.py tests/eval/test_retrieval_eval.py -q | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | No |
| 2026-05-19 | T18 | e2e-sample-sop-v1 | v1 | pytest tests/integration/test_cli_workflow.py tests/eval/test_end_to_end_eval.py -q | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | No |
| 2026-05-20 | T21 | transcript-fixture-v1 | n/a | pytest tests/integration/test_ingestion.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | n/a | n/a | n/a | n/a | No |
| 2026-05-20 | T22 | discovery-artifacts-fixture-v1 | n/a | pytest tests/integration/test_ingestion.py tests/unit/test_docs.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | n/a | n/a | n/a | n/a | No |
| 2026-05-20 | T24 | real-world-corpus-v1 | n/a | pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_retrieval_eval.py -q | n/a | n/a | n/a | 1.00 | n/a | n/a | n/a | No |
| 2026-05-20 | T25 | evidence-pack-fixture-v1 | v1 | pytest tests/integration/test_evidence_packs.py tests/eval/test_retrieval_eval.py -q | 1.00 | 1.00 | n/a | 1.00 | 1.00 | n/a | n/a | No |

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
