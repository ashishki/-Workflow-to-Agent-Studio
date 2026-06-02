# Frontier Opportunity Discovery Run

Status: public-source/demo frontier run; not buyer proof  
Date: 2026-06-02  
Model: `claude-opus-4-6`  
Prompt version: `frontier-opportunity-discovery-v1`  
Runtime output: `.data/frontier/frontier_opportunity_candidates.json` (ignored)

## Inputs

- Workflow context:
  `docs/demo/ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md`
- Public n8n metadata:
  `docs/experiments/n8n_template_mining_summary.md`
- Deterministic privacy class used by verifier: `sensitive`

## Result

Opus 4.6 proposed three unapproved opportunity candidates.

| ID | Candidate | Solution Type | Privacy | Confidence | Verifier Status | Exportable |
|---|---|---|---|---|---|---|
| FOC-001 | Claim verification research assistant | `rag_knowledge_assistant` | `sensitive` | `medium` | `needs_human_review` | no |
| FOC-002 | Post-call structured feedback capture and routing | `human_in_the_loop_workflow` | `sensitive` | `medium` | `needs_human_review` | no |
| FOC-003 | Duplicate and repeat applicant detection | `classic_script` | `sensitive` | `low` | `needs_human_review` | no |

Rejected ideas from the model:

- autonomous application scoring and auto-reject agent;
- AI-driven founder honesty detector.

Verifier result after deterministic checks:

- blocking findings: `0`;
- warning findings: `0`;
- every candidate remains `exportable_as_recommendation=false`;
- every candidate requires human review before roadmap inclusion.

## What Changed In The Customer Report

The customer-facing roadmap can now show a richer provenance trail:

```text
known pattern library recommendation
  + public n8n automation signals
  + frontier-suggested missed opportunities
  + deterministic verifier status
  + human review requirement
```

This makes the report more useful for a cofounder/sales conversation:

- base roadmap explains what to build first;
- n8n mining explains which automation patterns are common in public templates;
- frontier model suggests expansion candidates that the baseline library may
  miss;
- verifier proves the model cannot approve its own recommendations.

## Contract Lessons

The first live calls exposed useful failure modes:

- model returned invalid/truncated JSON when too many candidates were requested;
- model omitted required `privacy_class`;
- model invented a solution type outside the allowed enum;
- verifier initially over-blocked a candidate because it scanned
  do-not-automate text as if it were proposed behavior.

Fixes added:

- tighter prompt constraints;
- exactly three candidates per run;
- explicit allowed `candidate_solution_type` values;
- explicit `privacy_class` requirement;
- schema-validation failure handling with ignored `.data` debug outputs;
- verifier fix so do-not-automate boundaries do not trigger false high-impact
  decision blocks.

## Boundary

This run proves that the frontier layer can produce useful candidate ideas and
that the deterministic verifier keeps them unapproved. It does not prove buyer
demand, ROI, implementation safety, or production readiness.
