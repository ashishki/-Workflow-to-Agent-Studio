# SMB Roadmap Architecture

Purpose: describe the target architecture for the commercial roadmap layer while
preserving the existing local-first blueprint kernel.

## MVP Flow

```text
CLI / thin demo UI
  -> Project Workspace
  -> Ingestion Layer
  -> Privacy / Redaction Layer
  -> Workflow Decomposer
  -> Data Inventory + Risk Classifier
  -> Pattern Matching Layer
  -> Cost + Priority Scoring
  -> Roadmap Generator
  -> Verification Layer
  -> Markdown / JSON Export
```

## New Core Modules

Planned modules:

- `workflow_agent_studio/domain/roadmap.py`;
- `workflow_agent_studio/domain/recommendation.py`;
- `workflow_agent_studio/domain/privacy.py`;
- `workflow_agent_studio/domain/costing.py`;
- `workflow_agent_studio/domain/scoring.py`;
- `workflow_agent_studio/domain/verification.py`;
- `workflow_agent_studio/privacy/`;
- `workflow_agent_studio/costing/`;
- `workflow_agent_studio/scoring/`;
- `workflow_agent_studio/roadmap/`;
- `workflow_agent_studio/reporting/`;
- `workflow_agent_studio/verification/`;
- `workflow_agent_studio/patterns/smb/`.

## Keep From Current System

- local SQLite storage;
- source document fingerprinting;
- evidence references;
- Pydantic schemas;
- deterministic validators;
- audit events;
- review workspace;
- immutable blueprint versions;
- Markdown export;
- design candidate portfolio.

## Use LLM For

- messy workflow step extraction;
- clarifying question suggestions;
- pain point inference;
- recommendation rationale draft;
- report prose;
- pattern match suggestions;
- uncertainty flags.

## Use Deterministic Logic For

- schema validation;
- source fingerprints;
- evidence coverage;
- privacy class hard gates;
- score formulas;
- cost formulas;
- forbidden claims;
- redaction;
- audit logs;
- approval gates;
- export path constraints;
- reproducibility metadata.

## Human Review Required For

- final client-facing roadmap;
- cost assumptions;
- cloud/private/local recommendation for sensitive data;
- high-risk domains;
- legal, medical, HR, financial, or identity workflows;
- implementation handoff.

## Later Production Stack

Only after pilots:

- frontend: Next.js;
- backend: FastAPI;
- database: Postgres;
- vector search: pgvector or Qdrant;
- queue: Redis/RQ or Celery;
- object storage: S3-compatible;
- auth: Clerk/Auth0/Supabase Auth, enterprise SSO later;
- audit: append-only database table and exportable audit bundle;
- observability: OpenTelemetry and Sentry;
- exports: Markdown, PDF, Notion-ready.

## Local/Private Deployment Stack

Later private mode:

- Docker Compose;
- SQLite or Postgres;
- Qdrant or LanceDB;
- Ollama, vLLM, or llama.cpp;
- local embeddings;
- encrypted local storage;
- no outbound LLM calls;
- local Markdown/PDF export.
