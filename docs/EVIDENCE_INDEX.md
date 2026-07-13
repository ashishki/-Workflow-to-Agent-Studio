# Evidence Index - Workflow-to-Agent Studio

Status: active
Date: 2026-05-19
Last verified: 2026-07-13

This file indexes proof artifacts. It does not replace the artifacts themselves.

| ID | Date | Artifact | Scope | Evidence Type | Status |
|----|------|----------|-------|---------------|--------|
| E-001 | 2026-05-19 | `docs/ARCHITECTURE.md#problem-fit-and-adoption-reality` | Project fit | Problem-first and adoption reality gate | Draft |
| E-002 | 2026-05-19 | `docs/retrieval_eval.md` | RAG profile | Retrieval baseline and regression tracking | Planned |
| E-003 | 2026-05-19 | `docs/plan_eval.md` | Planning profile | Blueprint schema and validation baseline | Planned |
| E-004 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t09-pattern-library-and-chunking` | Retrieval ingestion | Heavy-task evidence target | Current |
| E-005 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t10-embedding-and-index-schema` | Index schema | Heavy-task evidence target | Current |
| E-006 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t11-query-time-retrieval-and-insufficient-evidence` | Retrieval query | Heavy-task evidence target | Current |
| E-007 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t15-blueprint-validation-gate` | Planning validation | Heavy-task evidence target | Current |
| E-008 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t18-end-to-end-cli-workflow` | End-to-end workflow | Heavy-task evidence target | Current |
| E-009 | 2026-05-19 | `docs/archive/TASK_GRAPH_V1_T01_T20.md#t20-pilot-proof-metric-measurement` | Adoption proof metric | Pilot measurement target | Current |
| E-010 | 2026-05-19 | `docs/IMPLEMENTATION_REFERENCE_MAP.md` | RAG implementation reference | Reference map for retrieval/eval patterns | Current |
| E-011 | 2026-05-19 | `docs/tasks.md#t21-transcript-ingestion` | Transcript ingestion | Next evidence target | Planned |
| E-012 | 2026-07-13 | `docs/evidence/WORKFLOW_P0_RENAME_PREP_2026-07-13.md` | CI truth repair and rename inventory | Reproducible local verification with explicit remote blockers | Current |

## Evidence Rules

- Evidence rows must point to the canonical active artifact or archived historical artifact and the exact scope.
- A heavy task is not complete until its planned evidence row is updated to current and the referenced tests/evals pass.
- Retrieval and planning regressions are not closed by green unit tests alone; update the relevant eval artifact.
