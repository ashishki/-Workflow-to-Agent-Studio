# Readiness And Deployment Fit

Purpose: turn roadmap recommendations into reviewable implementation decisions.
The score is a planning aid, not proof of ROI or production safety.

## Candidate Score

Each workflow candidate records:

- feasibility: can the workflow be implemented with known systems and owners;
- data readiness: are authoritative sources, freshness, metadata, and privacy
  boundaries known;
- eval readiness: can golden cases, acceptance criteria, regression tests, and
  stop conditions be defined before build;
- risk level: low, medium, high, or regulated;
- TCO complexity: setup, integration, privacy mode, review, and maintenance
  complexity;
- ROI proxy: service delta and effort assumptions with evidence basis;
- autonomy fit: deterministic, workflow, bounded-agent, or autonomous-routine
  suitability;
- deployment fit: local, GitHub Action, hosted sandbox, self-hosted worker,
  cloud function, or not recommended.

## Blocking Principles

- Do not show a specific ROI or time-saved claim without an evidence basis.
- Treat demo and public-source fixtures as mechanics proof only.
- Prefer deterministic or human-in-the-loop workflow when risk or eval clarity is
  weak.
- Mark autonomous deployment as not recommended until trigger, idempotency,
  secrets, fallback, monitoring, and budget boundaries are explicit.

## Required Next Questions

Every roadmap should ask missing questions for:

- data: authoritative source, freshness, redaction, retention, and access;
- eval: golden cases, human-review sample, cost/latency budget, and stop gates;
- cost/TCO: inference, integration, human review, maintenance, and support;
- runtime: trigger, idempotency key, permissions, fallback, monitoring, and
  rollback.
