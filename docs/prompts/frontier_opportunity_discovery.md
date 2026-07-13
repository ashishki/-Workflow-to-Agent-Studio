# Frontier Opportunity Discovery Prompt Contract

Status: prompt contract; not wired into runtime yet
Purpose: let a frontier model propose additional roadmap opportunity candidates
after deterministic workflow extraction and pattern matching.

## Inputs

- workflow map;
- pain points;
- systems and integrations;
- detected SMB pattern matches;
- n8n metadata signals, when available;
- privacy class;
- known assumptions;
- do-not-automate boundaries already detected;
- cost model constraints;
- target customer type and workflow volume, if known.

## Output Shape

The model must return unapproved candidates only:

```yaml
opportunity_id: FOC-001
title: Human-reviewed application triage assistant
workflow_step: Application intake and first-pass review
candidate_solution_type: human_in_the_loop_workflow
why_it_may_help:
  - repeated review work
  - high context switching
why_it_may_not_help:
  - low application volume
  - unclear review criteria
required_data:
  - application form fields
  - reviewer feedback
human_gate:
  required: true
  reviewer: senior reviewer
  approval_event: reviewer accepts or rejects recommendation
  rationale: admission decisions remain human-owned
do_not_automate:
  - final accept/reject decision
  - unsupported claims about founder honesty
critical_assumptions:
  - historical applications are available for shadow review
privacy_class: sensitive
privacy_notes:
  - founder personal data requires approved handling
cost_drivers:
  - CRM/application database integration
  - research depth per applicant
eval_cases:
  - strong founder with weak market
  - suspicious traction claim
confidence: medium
reject_if:
  - no reviewer can validate outputs
  - data access is not approved
```

## Required Instructions

Use this instruction block when calling a frontier model:

```text
You are generating unapproved AI roadmap opportunity candidates.

Do not approve recommendations.
Do not claim ROI.
Do not weaken the provided privacy class.
Do not propose autonomous legal, medical, financial, HR, admission, hiring,
firing, refund, or high-impact decisions.
Prefer deterministic automation or human-in-the-loop workflow before high
autonomy agents.

For every candidate, include:
- evidence from the provided workflow map or n8n metadata;
- explicit assumptions when evidence is missing;
- human gate;
- do-not-automate list;
- cost drivers, not a single price;
- confidence;
- reject conditions.

Return at most four candidates. Keep each list to at most three items.
Use only `low`, `medium`, or `high` for confidence.
Use only these `candidate_solution_type` values:
`do_not_automate_yet`, `classic_script`, `api_integration`, `rpa`,
`llm_assistant`, `rag_knowledge_assistant`, `human_in_the_loop_workflow`,
`bounded_ai_agent`, `high_autonomy_agent_future_only`.
Do not invent new solution type labels.

Also include at least two tempting but unsafe rejected ideas in
`rejected_candidate_titles`.
```

## Verifier Rules

A frontier candidate cannot enter a roadmap unless deterministic verification
confirms:

- evidence or explicit assumptions exist;
- human gate is present for any material business action;
- privacy class is compatible with the proposed implementation mode;
- cost estimate can be produced as a range;
- do-not-automate boundaries are present;
- forbidden claims are absent;
- reviewer accepts the candidate.

## Boundary

Frontier output can expand the search space. It is not the source of truth for:

- privacy class;
- cost;
- final recommendation approval;
- customer facts;
- legal/compliance status;
- production action permission.
