# Roadmap Report Contract

Contract name: `RoadmapReport v1`

Purpose: define the target output artifact for SMB AI implementation planning.

The report is a contract-bound artifact, not a prose-only PDF. Markdown export
is one view of the same structured data.

## Required Sections

### 1. Executive Summary

Required fields:

- company context;
- top recommended initiatives;
- top do-not-automate-yet items;
- 30/60/90 day roadmap;
- overall privacy mode recommendation;
- overall confidence level;
- critical assumptions.

### 2. What The Agent Will Not Replace

Required fields:

- realistic autonomy level;
- autonomy rationale;
- human-owned responsibilities;
- workflow-specific agent myths;
- required human capabilities;
- proof gates before rollout.

Purpose: make the report useful in presales by showing where AI is only a lever,
where a human remains accountable, and what must be proven with logs, tests,
shadow mode, and review before production.

### 3. Evidence Packet

Required fields:

- source documents;
- source type;
- source fingerprint/hash;
- extracted evidence snippets;
- missing evidence;
- redaction status;
- source privacy class.

### 4. Workflow Map

For each workflow:

- workflow ID;
- workflow name;
- business owner;
- trigger;
- actors;
- systems;
- steps;
- decisions;
- exceptions;
- inputs and outputs;
- frequency/volume;
- pain points;
- current tools;
- current manual effort;
- evidence references.

### 5. Process Inventory

For each process:

- automation feasibility score;
- business impact score;
- privacy sensitivity score;
- security risk score;
- data readiness score;
- implementation complexity score;
- evaluation clarity score;
- recommended solution type.

### 5.5 Readiness And Deployment Fit

For each candidate:

- feasibility, data readiness, and eval readiness scored from 1 to 5;
- risk level: low, medium, high, or regulated;
- TCO complexity: low, medium, or high;
- ROI proxy with evidence basis and caveats, never guaranteed ROI;
- autonomy fit across deterministic, workflow, bounded-agent, and autonomous
  routine modes;
- deployment fit: local, GitHub Action, hosted sandbox, self-hosted worker,
  cloud function, or not recommended;
- data readiness report with source blockers and next questions;
- eval readiness report with golden cases, acceptance criteria, and missing
  proof questions;
- autonomous deployment recommendation with trigger, idempotency key, secret
  boundary, fallback policy, and blockers.

Purpose: make the roadmap reject premature automation when data, eval, cost,
or runtime controls are not ready.

Allowed solution types:

- do not automate yet;
- classic script;
- API integration;
- RPA;
- LLM assistant;
- RAG knowledge assistant;
- human-in-the-loop workflow;
- bounded AI agent;
- high-autonomy agent - future only.

### 6. AI Opportunity Map

Each opportunity must include:

- workflow step;
- pain point;
- automation pattern;
- why AI is useful or why AI is not needed;
- expected value;
- required data;
- privacy class;
- confidence;
- fallback option.

### 7. Recommendation Cards

Each recommendation card must include:

```yaml
recommendation_id: REC-001
recommendation: Customer support triage assistant
target_workflow_step: Inbound message classification
expected_value:
  qualitative: Faster response and fewer missed requests
  quantitative_assumption: Reduce manual triage time by 30-50 percent
required_data:
  - support messages
  - order status
  - FAQ/SOP
privacy_class: moderate
implementation_option: LLM assistant plus deterministic routing
architecture:
  model: Cloud LLM API or private mode depending on customer data
  deterministic_components:
    - routing rules
    - refund approval gate
    - PII redaction
  llm_components:
    - message summarization
    - intent classification draft
estimated_cost:
  one_time_low: 2000
  one_time_medium: 7000
  one_time_high: 20000
  currency: USD
estimated_time:
  low: 2 weeks
  medium: 4 weeks
  high: 8 weeks
required_people:
  - AI automation engineer
  - business process owner
  - reviewer/support lead
dependencies:
  - clean FAQ
  - support inbox access
  - refund policy
risks:
  - hallucinated policy answer
  - exposure of customer data
  - wrong escalation
validation_method:
  - golden support tickets
  - human review of first 100 classifications
success_metrics:
  - first response time
  - escalation accuracy
  - manual handling time
confidence_level: medium
assumptions:
  - Support requests are repetitive enough
  - FAQ reflects current policy
evidence:
  - source_id: SRC-001
    chunk_id: CH-004
fallback_option: Deterministic canned replies and manual routing
```

Each generated roadmap must also include a harness candidate card for agentic or
LLM-owned recommendations:

- model/prompt/harness boundary;
- tools;
- memory policy;
- retry and recovery policy;
- permission policy;
- human handoff;
- trace requirements;
- eval required before deployment.

### 8. Cloud Vs Local/Private Recommendation

For each initiative:

- cloud safe;
- cloud only after redaction;
- private mode recommended;
- local/on-prem required;
- rationale;
- data classes involved;
- quality/cost tradeoff.

### 9. Build Vs Buy

Allowed outputs:

- buy SaaS;
- configure existing SaaS;
- build small integration;
- build custom AI workflow;
- do not build yet.

### 10. Cost, Time, And Team Plan

Required fields:

- one-time implementation cost range;
- monthly run cost range;
- human review cost;
- integration/subscription cost;
- maintenance cost;
- roles and estimated involvement;
- assumptions and confidence.

### 11. Rollout Plan

Required stages:

- Phase 0: process and data cleanup;
- Phase 1: low-risk assistant or deterministic automation;
- Phase 2: human-in-the-loop automation;
- Phase 3: integration or bounded-agent pilot;
- Phase 4: scale, revise, or stop.

### 12. Evaluation Plan

Required fields:

- golden test cases;
- shadow mode;
- human review sample;
- acceptance criteria;
- regression tests;
- stop conditions.

### 13. Governance And Maintenance

Required fields:

- owner;
- review cadence;
- approval rules;
- incident handling;
- prompt/model/version change policy;
- data retention;
- audit logs.

### 14. Verification Appendix

Required files or sections:

- claims registry;
- assumptions registry;
- evidence table;
- recommendation trace;
- decision log;
- reviewer notes;
- confidence and uncertainty flags.

## Blocking Conditions

The report must fail validation when:

- a recommendation lacks a workflow step;
- a recommendation lacks evidence and lacks assumptions;
- cost ranges lack assumptions;
- a restricted privacy workflow recommends unrestricted cloud analysis;
- high-risk recommendations lack a human approval gate;
- "guaranteed ROI" or similar unsupported claims appear;
- autonomous legal, medical, financial, or HR decisions are recommended;
- a high-autonomy agent is recommended for a high-risk workflow.
- a report lacks explicit autonomy limits and proof gates.
