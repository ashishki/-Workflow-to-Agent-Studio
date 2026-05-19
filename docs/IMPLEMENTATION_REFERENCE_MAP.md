# Implementation Reference Map - Workflow-to-Agent Studio

Status: reference-only
Date: 2026-05-19

Reference repository:

- `https://github.com/ashishki/Dream_Motif_Interpreter`

Use this file when implementing RAG and retrieval evaluation so Codex ports proven patterns instead of inventing the whole retrieval stack from scratch.

---

## Rule of Use

Use `Dream_Motif_Interpreter` as the implementation reference for:

- text-only RAG pipeline separation
- normalized source document types and connector boundary shape
- chunking and embedding index contracts
- typed evidence blocks and `insufficient_evidence`
- retrieval evaluation document structure
- evaluation script shape and metric calculation
- regression slices for user-reported retrieval failures

Do not treat it as the source of truth for:

- Workflow-to-Agent Studio domain schema
- dream-specific query expansion, motif semantics, or Russian religious/object recall rules
- PostgreSQL-only implementation decisions
- Telegram assistant behavior
- external provider choices or model names
- any runtime tier escalation beyond T0

The reference informs shape and tests. Canonical decisions remain in `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_CONTRACT.md`, and ADRs.

---

## File-to-Target Map

| Reference repo file | Why it matters | Workflow-to-Agent Studio target |
|---------------------|----------------|---------------------------------|
| `app/retrieval/types.py` | Defines source connector protocols, normalized documents, embedding client protocol, and typed embedding errors. | `workflow_agent_studio/domain/sources.py`, `workflow_agent_studio/retrieval/embeddings.py`, `workflow_agent_studio/ingestion/normalizer.py` |
| `app/retrieval/ingestion.py` | Shows ingestion/query separation, index schema versioning, tokenizer-based chunking, embedding dimensions, idempotent chunk upsert, and tracing spans. | `workflow_agent_studio/retrieval/chunking.py`, `workflow_agent_studio/retrieval/index.py`, `workflow_agent_studio/retrieval/embeddings.py` |
| `app/retrieval/query.py` | Shows typed `EvidenceBlock`, `InsufficientEvidence`, threshold filtering, hybrid exact/semantic retrieval, deterministic query profiles, and evidence fragment coercion. | `workflow_agent_studio/retrieval/query.py`, `workflow_agent_studio/retrieval/evidence.py` |
| `docs/retrieval_eval.md` | Mature eval artifact with validity rule, query types, baseline/current metrics, answer-quality separation, Eval Source requirement, and regression slices. | `docs/retrieval_eval.md` |
| `scripts/eval.py` | Loads eval dataset from Markdown, runs a seeded corpus, calculates hit@3/hit@5/MRR/citation precision/no-answer accuracy/latency, and writes eval history. | `scripts/eval_retrieval.py` or equivalent future eval script |
| `tests/unit/test_retrieval_eval.py` | Validates eval dataset coverage and evaluation history entries. | `tests/eval/test_retrieval_eval.py` |
| `tests/unit/test_rag_ingestion.py` | Tests ingestion/query separation, tokenizer boundary, embedding errors, and schema constants. | `tests/unit/test_chunking.py`, `tests/unit/test_embeddings.py` |
| `tests/unit/test_rag_query.py` | Tests query path separation, embedding errors, empty query insufficient evidence, and query probes. | `tests/integration/test_retrieval_query.py`, `tests/unit/test_retrieval_query.py` |
| `alembic/versions/006_add_hnsw_index.py` | Example of explicit vector index migration. | Reference only; v1 uses local vector index unless ADR changes storage. |
| `docs/archive/PHASE3_REVIEW.md` and `docs/archive/PHASE3_BOUNDARY_REVIEW.md` | Shows RAG review failure modes: wrong embedding model, word-count tokenization, missing HNSW, dead HTTP error handling, missing eval rows. | RAG verifier focus and future review checklist calibration. |

---

## Patterns to Port

1. Keep ingestion and query-time retrieval in separate modules. Tests should assert they do not import each other directly when that would mix responsibilities.
2. Store index schema version, embedding model name, corpus version, chunk count, and created timestamp with every index build.
3. Use tokenizer-aware chunking when a token boundary is declared; do not use word count as a token proxy.
4. Make embedding provider errors typed and test 429/500-style failures without leaking source text or credentials.
5. Return typed evidence objects, not raw dicts, from query-time retrieval.
6. Implement `insufficient_evidence` as a first-class result for empty, unsupported, or below-threshold queries.
7. Evaluate retrieval quality separately from answer quality.
8. Require every eval history row to include Date, Corpus Version, and Eval Source.
9. Include no-answer queries in every baseline.
10. Add focused regression slices when a real user or operator reports a missed recall or false-positive case.

---

## Patterns to Adapt

- `Dream_Motif_Interpreter` uses PostgreSQL FTS plus pgvector and reciprocal-rank fusion. Workflow-to-Agent Studio v1 remains local-first; use the hybrid retrieval idea only if it fits local vector/search storage.
- `Dream_Motif_Interpreter` includes domain-specific deterministic query expansion for dream search. Workflow-to-Agent Studio may later add deterministic query profiles for workflow domains, integration names, approval language, and eval-case wording, but should not copy dream-domain terms.
- Reference eval fixtures are dream-entry focused. Workflow-to-Agent Studio eval fixtures must cover SOP steps, actors/systems, fields, integrations, approval boundaries, eval cases, risks, and unsupported production-execution claims.

---

## Recommended Use by Task

| Task | Reference sections |
|------|--------------------|
| T09 Pattern Library and Chunking | `app/retrieval/ingestion.py` constants and chunking tests; `docs/retrieval_eval.md` corpus/dataset shape |
| T10 Embedding and Index Schema | `app/retrieval/types.py` embedding protocol/errors; `app/retrieval/ingestion.py` schema version and embedding validation |
| T11 Query-Time Retrieval and Insufficient Evidence | `app/retrieval/query.py` typed evidence and threshold behavior; `tests/unit/test_rag_query.py` insufficient-evidence tests |
| T18 End-to-End CLI Workflow | `scripts/eval.py` metric calculation and eval-history writing pattern |

## Reference Snapshot

The reference was inspected from a shallow clone on 2026-05-19. If the upstream repo changes materially, refresh this map before porting new patterns.
