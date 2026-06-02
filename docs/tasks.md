# Task Graph - Workflow-to-Agent Studio

Version: 2.0
Date: 2026-05-19

This is the active implementation task graph. The completed V1 graph is archived at `docs/archive/TASK_GRAPH_V1_T01_T20.md`.

Task format is intentionally compact so Codex can receive a narrow task digest without bloating prompts. Each task must still follow the implementation contract: read scoped context, implement within file scope, add tests for acceptance criteria, run pytest and ruff, and update evaluation artifacts when tagged.

---

## Phase 0: Local Evidence-Linked MVP ✅

Business goal: prove a local CLI can generate a reviewable evidence-linked automation blueprint from local workflow source material.

Status: complete. Implemented by T01-T20 plus FIX-1 and FIX-2. See:

- `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- `docs/archive/CODEX_PROMPT_V1_T01_T20_COMPLETE.md`
- `docs/archive/PHASE5_REVIEW.md`
- `docs/archive/CYCLE13_CODE2_FIX.md`

---

## Phase 1: Evidence Capture And Corpus Expansion

Business goal: make the product useful on messy real discovery inputs, not only clean SOP fixtures.

Exit criteria:

- transcripts, pasted notes, form descriptions, and integration snippets can be ingested locally
- every source has metadata, fingerprinting, and evidence anchors
- the system reports evidence gaps before synthesis
- retrieval and planning eval artifacts include real-world-style corpus fixtures

## T21: Transcript Ingestion

Owner: codex
Phase: 1
Type: rag:ingestion
Depends-On: T07, T18

Objective: add local transcript ingestion for discovery call exports while preserving source confidentiality.

Acceptance-Criteria:

- transcript fixtures with speaker labels ingest into normalized source records
- source fingerprints remain deterministic across whitespace-only transcript changes
- raw transcript text does not appear in logs, spans, or audit labels
- `docs/retrieval_eval.md` records the transcript ingestion fixture result

Files:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/domain/sources.py`
- `tests/integration/test_ingestion.py`
- `tests/eval/test_retrieval_eval.py`
- `docs/retrieval_eval.md`

Context-Refs:

- `docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag`
- `docs/product_strategy.md#development-phases`

## T22: Notes, Forms, And Integration Snippet Ingestion

Owner: codex
Phase: 1
Type: rag:ingestion
Depends-On: T21

Objective: support common discovery artifacts beyond transcripts: pasted notes, form descriptions, and API or integration excerpts.

Acceptance-Criteria:

- each supported source kind is represented in source metadata
- unsupported file types fail with a clear nonzero CLI error and no partial persisted source
- fixtures cover notes, form descriptions, and integration snippets
- ingestion docs explain supported source kinds and local-only boundaries

Files:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/cli.py`
- `docs/operator_guide.md`
- `tests/integration/test_ingestion.py`
- `tests/unit/test_docs.py`

Context-Refs:

- `docs/spec.md#feature-area-source-ingestion`
- `docs/IMPLEMENTATION_CONTRACT.md#source-confidentiality`

## T23: Evidence Anchor Map And Gap Report

Owner: codex
Phase: 1
Type: rag:query plan:validation
Depends-On: T21, T22

Objective: create a source-level evidence map and missing-evidence report before blueprint synthesis.

Acceptance-Criteria:

- evidence anchors connect source IDs, chunk IDs, headings or speaker labels, and normalized snippets
- missing evidence is reported for actors, systems, decisions, exceptions, data fields, and approval boundaries
- synthesis receives structured evidence gaps instead of silently filling missing fields
- planning eval records missing-question and evidence-gap counts

Files:

- `workflow_agent_studio/retrieval/`
- `workflow_agent_studio/blueprint/service.py`
- `workflow_agent_studio/validators/blueprint.py`
- `tests/integration/test_evidence_gap_report.py`
- `docs/plan_eval.md`

Context-Refs:

- `docs/ARCHITECTURE.md#profile-rag`
- `docs/ARCHITECTURE.md#profile-planning`

## T24: Real-World Corpus Fixture Baseline

Owner: codex
Phase: 1
Type: rag:ingestion plan:validation
Depends-On: T21, T22, T23

Objective: add a small realistic corpus pack and baseline metrics for source coverage, evidence gaps, and generated blueprint usefulness.

Acceptance-Criteria:

- corpus fixtures include at least one transcript, one notes file, one form description, and one integration excerpt
- retrieval eval records corpus count, chunk count, and citation support metrics
- plan eval records required-section coverage and evidence-gap metrics
- README points next contributors to the corpus and eval commands

Files:

- `tests/fixtures/sources/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`
- `README.md`
- `tests/eval/`

Context-Refs:

- `docs/product_strategy.md#market-lens`
- `docs/evaluation_guide.md`

---

## Phase 2: Retrieval And Evidence Engine

Business goal: make grounding reliable enough that operators can trust why each claim exists.

## T25: Evidence Pack Builder

Owner: codex
Phase: 2
Type: rag:query
Depends-On: T23, T24

Objective: build reusable evidence packs for workflow sections and automation candidates.

Acceptance-Criteria:

- evidence packs group source snippets by blueprint section and candidate automation
- unsupported sections produce `insufficient_evidence`
- citation precision is measured in `docs/retrieval_eval.md`

Files:

- `workflow_agent_studio/retrieval/`
- `workflow_agent_studio/blueprint/`
- `tests/integration/test_evidence_packs.py`
- `docs/retrieval_eval.md`

## T26: Retrieval Quality Controls

Owner: codex
Phase: 2
Type: rag:query
Depends-On: T25

Objective: add thresholds, reranking hooks, and no-answer behavior that improve evidence quality without fabricating support.

Acceptance-Criteria:

- threshold changes are configurable and tested
- reranking is provider-neutral and can be faked deterministically
- no-answer and low-confidence paths have explicit tests and eval rows

Files:

- `workflow_agent_studio/retrieval/`
- `workflow_agent_studio/config.py`
- `tests/unit/test_retrieval_query.py`
- `tests/eval/test_retrieval_eval.py`

---

## Phase 3: Structured LLM Extraction And Synthesis

Business goal: move from deterministic drafts to real structured LLM extraction while preserving schemas, validation, observability, and cost controls.

## T27: Provider-Backed Structured Extraction

Owner: codex
Phase: 3
Type: plan:schema
Depends-On: T12, T13, T24

Objective: enable a real provider path for workflow extraction behind the existing structured-output gateway.

Acceptance-Criteria:

- provider selection remains environment-backed and defaults to fake provider in tests
- model outputs are parsed into versioned schemas before storage
- schema errors are observable without logging raw source text
- extraction eval compares fake and provider-backed fixture behavior where provider credentials are available

Files:

- `workflow_agent_studio/llm/`
- `workflow_agent_studio/extraction/`
- `docs/plan_eval.md`
- `tests/unit/`
- `tests/integration/`

## T28: Prompt Registry And Versioned Prompt Evals

Owner: codex
Phase: 3
Type: plan:schema
Depends-On: T27

Objective: make extraction and synthesis prompts versioned assets with regression checks.

Acceptance-Criteria:

- prompt versions are recorded with blueprint generation attempts
- prompt changes require fixture eval updates
- prompts stay task-focused and do not embed full roadmap or architecture documents

Files:

- `workflow_agent_studio/llm/`
- `workflow_agent_studio/blueprint/prompts.py`
- `docs/plan_eval.md`
- `tests/unit/test_docs.py`

---

## Phase 4: Automation Readiness And Governance

Business goal: turn blueprints into defensible readiness decisions.

## T29: Automation Readiness Score

Owner: codex
Phase: 4
Type: plan:validation
Depends-On: T23, T25

Objective: compute deterministic readiness signals from evidence coverage, risk, integration clarity, eval quality, and approval boundaries.

Acceptance-Criteria:

- readiness output explains blockers, risks, and next questions
- scores cannot override blocking validation findings
- plan eval records readiness fixture outcomes

Files:

- `workflow_agent_studio/validators/`
- `workflow_agent_studio/domain/blueprint.py`
- `tests/unit/test_blueprint_validators.py`
- `docs/plan_eval.md`

## T30: Governance Report Export

Owner: codex
Phase: 4
Type: plan:validation
Depends-On: T29

Objective: export a governance-focused report for reviewer approval and implementation handoff.

Acceptance-Criteria:

- report includes evidence coverage, assumptions, approval boundaries, readiness result, and unresolved findings
- approved governance export is blocked when validation has blocking findings
- local export path constraints remain enforced

Files:

- `workflow_agent_studio/export/`
- `tests/integration/test_markdown_export.py`
- `docs/operator_guide.md`

---

## Phase 5: Review Workspace And Human Editing

Business goal: make human review fast, traceable, and useful enough for repeated pilot use.

## T31: Review Diff And Comment Model

Owner: codex
Phase: 5
Type: plan:validation
Depends-On: T16, T29

Objective: add structured reviewer comments and version-to-version diffs for blueprint sections.

Acceptance-Criteria:

- comments attach to blueprint sections and evidence anchors
- diffs show changed claims, assumptions, findings, and approval boundaries
- audit events record comment and diff actions without raw confidential source text

Files:

- `workflow_agent_studio/blueprint/review.py`
- `workflow_agent_studio/storage/repositories.py`
- `tests/integration/test_review_state.py`

## T32: Review Workspace Interface

Owner: codex
Phase: 5
Type: none
Depends-On: T31

Objective: provide the smallest useful local review interface, CLI or UI, for editing and approving blueprint sections.

Acceptance-Criteria:

- reviewer can inspect findings, evidence, comments, and version history
- reviewer can create an edited draft and export it locally
- interface documentation stays operator-focused and does not claim autonomous deployment

Files:

- `workflow_agent_studio/cli.py`
- `docs/operator_guide.md`
- `tests/integration/`

---

## Phase 6: Vertical Blueprint Packs

Business goal: create repeatable market wedges with domain-specific patterns, evals, and output expectations.

## T33: Vertical Pack Contract

Owner: codex
Phase: 6
Type: rag:ingestion plan:schema
Depends-On: T24, T28

Objective: define a versioned contract for vertical workflow packs.

Acceptance-Criteria:

- packs declare domain, source examples, extraction hints, required blueprint sections, risks, and eval fixtures
- pack loading is deterministic and locally testable
- pack metadata appears in generation attempts and eval artifacts

Files:

- `patterns/`
- `workflow_agent_studio/patterns/`
- `tests/unit/test_pattern_library.py`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

## T34: First Vertical Pack From Pilot Evidence

Owner: codex
Phase: 6
Type: rag:ingestion plan:validation
Depends-On: T33, T40

Objective: implement the first vertical pack only after pilot data identifies the strongest wedge.

Acceptance-Criteria:

- selected vertical is justified by pilot evidence, not guesswork
- pack includes realistic fixtures and expected blueprint characteristics
- evals compare generic output against vertical-pack output

Files:

- `patterns/`
- `tests/fixtures/`
- `docs/plan_eval.md`
- `docs/pilot_measurement.md`

---

## Phase 7: Pilot Proof And Commercial Packaging

Business goal: prove the product creates useful artifacts for real users and package the repeatable offer.

## T35: Real Pilot Measurement Row

Owner: codex
Phase: 7
Type: plan:validation
Depends-On: T24, T32

Objective: record the first real pilot measurement without overstating product maturity.

Acceptance-Criteria:

- `docs/pilot_measurement.md` contains one reviewed real pilot row or explicitly remains template-only
- pass/fail result is based on time-to-blueprint and required-section acceptance thresholds
- reviewer edits and critical missing questions are recorded

Files:

- `docs/pilot_measurement.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`

## T36: Commercial Pilot Package

Owner: codex
Phase: 7
Type: none
Depends-On: T35

Objective: document the minimum sellable pilot package, buyer promise, boundaries, and proof metrics.

Acceptance-Criteria:

- package states buyer, use case, deliverables, non-goals, and success criteria
- claims are tied to pilot evidence or marked as assumptions
- README links the package without replacing operator docs

Files:

- `docs/product_strategy.md`
- `README.md`
- `tests/unit/test_docs.py`

---

## Phase 8: Integrations And Controlled Handoff

Business goal: import from real systems and export implementation handoffs without losing approval control.

## T37: Controlled Import Connectors

Owner: codex
Phase: 8
Type: rag:ingestion
Depends-On: T24, T30

Objective: add connector architecture for read-only imports while preserving local confidentiality and auditability.

Acceptance-Criteria:

- connector credentials are environment-backed and never persisted
- imports are read-only and produce source records with connector metadata
- connector failures do not corrupt existing runs

Files:

- `workflow_agent_studio/ingestion/`
- `workflow_agent_studio/config.py`
- `docs/ARCHITECTURE.md`
- `tests/integration/`

## T38: Approved Handoff Export

Owner: codex
Phase: 8
Type: plan:validation
Depends-On: T30, T35

Objective: export implementation handoff artifacts only after human approval.

Acceptance-Criteria:

- handoff includes tasks, eval cases, boundaries, assumptions, and evidence appendix
- unapproved or blocked blueprints cannot produce approved handoff exports
- external side effects remain disabled unless an ADR explicitly changes the boundary

Files:

- `workflow_agent_studio/export/`
- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/operator_guide.md`
- `tests/integration/`

---

## Phase 9: Learning System And Moat

Business goal: improve output quality from reviewed outcomes without leaking client data or weakening evidence requirements.

## T39: Reviewer Feedback Taxonomy

Owner: codex
Phase: 9
Type: plan:validation
Depends-On: T31, T35

Objective: classify reviewer edits into reusable feedback categories.

Acceptance-Criteria:

- taxonomy captures missing evidence, wrong boundary, weak eval, wrong integration, unclear risk, and unsupported claim
- feedback is stored without raw confidential source text
- plan eval records feedback category coverage

Files:

- `workflow_agent_studio/blueprint/review.py`
- `workflow_agent_studio/domain/review.py`
- `docs/plan_eval.md`
- `tests/integration/test_review_state.py`

## T40: Pattern Learning And Benchmark Corpus

Owner: codex
Phase: 9
Type: rag:ingestion plan:validation
Depends-On: T34, T39

Objective: turn approved, sanitized outcomes into better pattern packs and benchmark fixtures.

Acceptance-Criteria:

- sanitized benchmark fixtures exclude raw confidential client text
- pattern updates require eval comparison before becoming default
- benchmark results become release-gating documentation

Files:

- `patterns/`
- `tests/fixtures/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`
- `docs/product_strategy.md`

---

## Phase 10: Pre-Pilot Hardening

Business goal: keep improving engineering quality while real pilot evidence is unavailable, without treating synthetic fixtures as commercial proof.

## T41: Synthetic Benchmark Harness

Owner: codex
Phase: 10
Type: rag:ingestion plan:validation
Depends-On: T39

Objective: create a synthetic-only benchmark harness for regression testing without satisfying real-pilot evidence gates.

Acceptance-Criteria:

- synthetic benchmark fixtures are explicitly labeled as not pilot evidence
- harness reports retrieval and planning fixture coverage deterministically
- eval docs state synthetic results cannot satisfy T34 or commercial pilot proof

Files:

- `tests/fixtures/benchmarks/`
- `workflow_agent_studio/eval/`
- `tests/eval/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

## T42: Redaction And Sanitization Pipeline

Owner: codex
Phase: 10
Type: rag:ingestion plan:validation
Depends-On: T39

Objective: add deterministic sanitization helpers for future benchmark fixtures and pilot artifacts.

Acceptance-Criteria:

- common PII and credential-like tokens are redacted before benchmark export
- sanitization preserves enough structure for eval usefulness
- tests prove raw confidential strings are absent from sanitized output

Files:

- `workflow_agent_studio/safety/`
- `tests/unit/`
- `docs/operator_guide.md`
- `docs/plan_eval.md`

## T43: Pilot Intake Checklist

Owner: codex
Phase: 10
Type: plan:validation
Depends-On: T35, T39

Objective: document and validate the exact evidence needed to convert a future real pilot into a measurement row.

Acceptance-Criteria:

- checklist enumerates required source material, reviewer actions, thresholds, and missing-question rules
- checklist distinguishes real pilot evidence from demo or synthetic fixtures
- docs tests prevent pilot proof claims while checklist inputs are incomplete

Files:

- `docs/pilot_measurement.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`

## T44: Vertical Pack Dry-Run Evaluation

Owner: codex
Phase: 10
Type: rag:ingestion plan:validation
Depends-On: T33, T41

Objective: evaluate vertical-pack mechanics on synthetic fixtures without claiming a real wedge.

Acceptance-Criteria:

- dry-run compares generic and vertical-pack expectations on synthetic fixtures
- results are labeled not pilot evidence
- T34 remains blocked until real pilot evidence exists

Files:

- `patterns/`
- `tests/fixtures/benchmarks/`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

## T45: Review Feedback Analytics

Owner: codex
Phase: 10
Type: plan:validation
Depends-On: T39

Objective: aggregate reviewer feedback categories without storing raw confidential review text.

Acceptance-Criteria:

- analytics report counts feedback categories by section and version
- raw feedback text is not persisted in analytics output
- plan eval records feedback analytics coverage

Files:

- `workflow_agent_studio/blueprint/review.py`
- `workflow_agent_studio/domain/review.py`
- `tests/integration/test_review_state.py`
- `docs/plan_eval.md`

## T46: Demo Dataset Boundary

Owner: codex
Phase: 10
Type: rag:ingestion plan:validation
Depends-On: T41

Objective: make demo, synthetic, and real-pilot dataset boundaries explicit in docs and tests.

Acceptance-Criteria:

- docs define which datasets can and cannot support commercial claims
- eval artifacts identify synthetic and demo baselines separately from real pilots
- tests prevent synthetic fixtures from being counted as real pilot rows

Files:

- `docs/product_strategy.md`
- `docs/pilot_measurement.md`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`
- `tests/unit/test_docs.py`

---

## Phase 11: Public-Source Demo Quality

Business goal: use public workflow sources to improve draft quality until the
system produces stable, source-grounded demo outputs, then request real workflow
data from potential customers for pilot proof.

Boundary:

- public-source experiments can improve mechanics and demo quality
- public-source experiments do not satisfy T34/T40 or commercial pilot proof
- the transition to prospect/customer data happens only after stable public demo
  results are documented

Exit criteria:

- at least one public-source workflow fixture produces a domain-specific
  blueprint instead of a generic support-intake draft
- public-source evals cover source fact preservation, review exports, and pilot
  boundary enforcement
- demo artifacts can be shown as public-source demos without claiming buyer
  acceptance

## T47: Public-Source Workflow Fact Eval

Owner: codex
Phase: 11
Type: rag:ingestion plan:validation
Depends-On: T46

Objective: create a regression eval that proves public-source workflow facts
survive ingestion, retrieval, synthesis, and export.

Acceptance-Criteria:

- NetBox issue triage fixture checks domain-specific facts in generated output
- eval fails if the draft collapses back to generic support-intake language only
- report keeps the public-source vs real-pilot boundary explicit

Files:

- `tests/fixtures/public_sources/`
- `tests/eval/test_public_source_experiment.py`
- `docs/experiments/public_source_netbox_issue_triage.md`

## T48: Source-Grounded Extraction Upgrade

Owner: codex
Phase: 11
Type: plan:schema
Depends-On: T47

Objective: improve deterministic extraction and synthesis so public workflow
fixtures preserve source-specific actors, systems, decisions, exceptions, and
approval boundaries.

Acceptance-Criteria:

- NetBox fixture produces GitHub Issues, issue templates, maintainers, reporters,
  stale handling, duplicate handling, and reproducibility checks in the blueprint
- existing support-intake fixtures continue to pass
- generated eval cases and automation candidates remain evidence-linked

Files:

- `workflow_agent_studio/extraction/`
- `workflow_agent_studio/blueprint/`
- `tests/integration/`
- `tests/eval/test_public_source_experiment.py`

## T49: Public Demo Pack

Owner: codex
Phase: 11
Type: rag:ingestion plan:validation
Depends-On: T48

Objective: create a reproducible public demo pack that can be shared before real
prospect data is available.

Acceptance-Criteria:

- demo pack includes source fixture, command transcript, generated blueprint,
  review workspace, and gap summary
- generated artifacts are reproducible from committed fixtures
- docs label the pack as public-source demo material, not customer proof

Files:

- `docs/experiments/`
- `tests/fixtures/public_sources/`
- `docs/operator_guide.md`
- `tests/eval/`

## T50: Prospect Data Request Gate

Owner: codex
Phase: 11
Type: plan:validation
Depends-On: T49

Objective: define when public-source quality is stable enough to ask potential
customers for real workflow data.

Acceptance-Criteria:

- gate requires stable public-source evals before prospect data requests
- request checklist states minimum safe source types and confidentiality boundary
- T34/T40 remain blocked until prospect/customer data is reviewed as a real pilot

Files:

- `docs/pilot_measurement.md`
- `docs/product_strategy.md`
- `docs/evaluation_guide.md`
- `tests/unit/test_docs.py`

---

## Phase 12: Solo Public Workflow Showcase

Business goal: create a polished public-source automation-discovery showcase
that a solo operator can show before having business relationships or customer
workflow data. This phase should make the product useful for portfolio demos and
for preparing focused data requests to future prospects.

Boundary:

- public-source research and public demo packs are allowed;
- public-source packs remain demo-quality only and do not satisfy real pilot
  proof, T34, or T40;
- if a task lacks enough workflow evidence, the agent must follow
  `docs/open_source_research_protocol.md` and collect public sources instead of
  stopping.

Exit criteria:

- at least three public workflow demo packs exist;
- one pack is a lead-intake workflow that can hand off to Lead Response SLA
  Agent;
- every demo pack includes source register, generated blueprint, review
  workspace, gap summary, and public-vs-pilot boundary label;
- a concise prospect data request pack is ready for manual outreach.

## T51: Public Workflow Research Protocol

Owner: codex
Phase: 12
Type: rag:ingestion plan:validation research
Depends-On: T50

Objective: document the public-source research protocol and link it from the
operator workflow so future agents know how to gather missing public workflow
data.

Acceptance-Criteria:

- `docs/open_source_research_protocol.md` defines allowed sources, forbidden
  sources, required source register fields, and public-demo claim boundaries.
- `docs/operator_guide.md` references the protocol for public demo-pack work.
- `docs/pilot_measurement.md` still states that public demos cannot satisfy real
  pilot proof.

Files:

- `docs/open_source_research_protocol.md`
- `docs/operator_guide.md`
- `docs/pilot_measurement.md`

## T52: Lead Intake Public Workflow Corpus

Owner: codex
Phase: 12
Type: rag:ingestion plan:validation research
Depends-On: T51

Objective: collect a small public workflow corpus for local-service lead intake
using public business pages, FAQs, booking forms, service-area pages, and
support/contact instructions.

Acceptance-Criteria:

- source register contains at least 20 public sources across one selected local
  service vertical;
- source notes extract actors, systems, customer inputs, qualification fields,
  escalation points, and unsafe-answer boundaries;
- committed fixtures are sanitized and public-demo labeled;
- no pricing, conversion, or buyer-readiness claim is made without explicit
  evidence.

Files:

- `docs/experiments/public_sources/lead_intake/`
- `tests/fixtures/public_sources/`
- `docs/open_source_research_protocol.md`

## T53: Three Public Blueprint Showcase Packs

Owner: codex
Phase: 12
Type: plan:validation report
Depends-On: T52

Objective: produce three reproducible public-source demo packs that show the
product can turn public workflow evidence into useful automation blueprints.

Acceptance-Criteria:

- one pack covers lead intake;
- one pack covers public issue/support triage;
- one pack covers an operations workflow such as onboarding, invoice approval,
  or incident response;
- each pack includes source fixture/register, command transcript, generated
  blueprint, review workspace, gap summary, and boundary label.

Files:

- `docs/experiments/public_demo_pack/`
- `tests/fixtures/public_sources/`
- `docs/evaluation_guide.md`

## T54: Public Blueprint Quality Review Rubric

Owner: codex
Phase: 12
Type: plan:validation eval
Depends-On: T53

Objective: add a repeatable rubric for judging whether a public-source
blueprint is demo-worthy before it is shown to a prospect.

Acceptance-Criteria:

- rubric scores evidence coverage, workflow specificity, missing questions,
  approval boundaries, integration realism, eval-case quality, and forbidden
  claims;
- each public demo pack records a review result;
- unresolved critical missing questions block "showcase_ready" status.

Files:

- `docs/evaluation_guide.md`
- `docs/experiments/public_demo_pack/`
- `tests/eval/`

## T55: Lead Agent Handoff Blueprint

Owner: codex
Phase: 12
Type: portfolio handoff
Depends-On: T53, T54

Objective: convert the lead-intake public blueprint into a focused handoff pack
for Lead Response SLA Agent.

Acceptance-Criteria:

- handoff pack includes workflow map, qualification fields, safe reply
  boundaries, handoff reasons, knowledge-pack requirements, eval cases, and
  missing data requests;
- handoff pack cites only public source evidence or marks assumptions;
- Lead Response SLA Agent can start its demo corpus work from this handoff
  without reading every source.

Files:

- `docs/handoffs/lead_response_sla_agent.md`
- `docs/experiments/public_demo_pack/`

## T56: Solo Prospect Data Request Pack

Owner: human + codex
Phase: 12
Type: gtm research
Depends-On: T53, T54

Objective: create a lightweight request pack a solo operator can send manually
to prospects, asking for one narrow workflow packet without broad system access.

Acceptance-Criteria:

- request asks for one SOP, transcript, notes file, form description,
  integration excerpt, or mixed packet;
- request explains local processing, confidentiality boundaries, human review,
  and optional sanitized benchmark reuse;
- request includes the public demo pack as demo material, not proof.

Files:

- `docs/prospect_data_request_pack.md`
- `docs/pilot_measurement.md`

## T57: Solo Showcase Readiness Review

Owner: human + codex
Phase: 12
Type: audit decision
Depends-On: T53, T55, T56

Objective: decide whether the public-source showcase is ready to show manually
to prospects and whether the next work is prospect data collection or another
public-source quality pass.

Acceptance-Criteria:

- review cites all three public demo packs and their rubric results;
- review confirms public-source artifacts are not represented as buyer proof;
- review records next action: request prospect data, improve demo quality, or
  pause.

Files:

- `docs/audit/SOLO_SHOWCASE_READINESS_REVIEW.md`
- `docs/CODEX_PROMPT.md`

---

## Phase 13: Workflow-To-Agent Framework Upgrade

Business goal: reposition the project from a local demo generator into a serious
framework for converting human workflows into bounded, reviewable agent system
designs.

Exit criteria:

- the product can generate multiple design candidates for the same workflow;
- each candidate has explicit autonomy, risk, cost, eval, and approval tradeoffs;
- one consolidated blueprint can be exported into AI Workflow Playbook artifacts;
- public README and product docs explain the framework direction without
  claiming automated agent deployment.

## T58: Framework Positioning Refresh

Owner: human + codex
Phase: 13
Type: docs strategy
Depends-On: T57

Objective: update the public and internal product positioning around
workflow-to-agent design, not generic agent generation.

Acceptance-Criteria:

- README explains the product as a workflow evidence to agent blueprint
  framework;
- docs/product_strategy.md lists the new framework role, non-goals, and
  design-output artifacts;
- docs/PROJECT_PLAN.md and docs/CODEX_PROMPT.md agree on the next active work.

Files:

- `README.md`
- `docs/product_strategy.md`
- `docs/PROJECT_PLAN.md`
- `docs/CODEX_PROMPT.md`

## T59: Design Diversity Candidate Set

Owner: codex
Phase: 13
Type: plan:schema
Depends-On: T58

Objective: add a candidate design model that can represent several bounded
agent/workflow architectures for the same source evidence.

Acceptance-Criteria:

- candidate schema supports deterministic-first, human-in-the-loop,
  bounded-agent, high-autonomy, compliance-heavy, and low-cost MVP variants;
- each candidate records autonomy level, required tools, human approvals,
  runtime tier, eval needs, risks, cost posture, and evidence gaps;
- validators reject candidates that lack approval boundaries or eval plan;
- tests cover schema validation and missing-field rejection.

Files:

- `workflow_agent_studio/domain/`
- `workflow_agent_studio/validators/`
- `tests/unit/`
- `docs/plan_eval.md`

Context-Refs:

- `docs/PROJECT_PLAN.md#near-term-roadmap`
- `docs/ARCHITECTURE.md#solution-shape-selection`

## T60: Diverse Blueprint Generation Flow

Owner: codex
Phase: 13
Type: plan:validation
Depends-On: T59

Objective: generate and validate several design candidates from one workflow
source package before selecting a consolidated blueprint.

Acceptance-Criteria:

- generation flow produces at least three candidate designs from one fixture;
- candidates cite source evidence and record assumptions separately;
- consolidation output compares tradeoffs instead of silently choosing one;
- tests verify insufficient evidence keeps a candidate in `needs_review` status.

Files:

- `workflow_agent_studio/blueprint/`
- `workflow_agent_studio/extraction/`
- `workflow_agent_studio/export/`
- `tests/integration/`
- `docs/evaluation_guide.md`

## T61: Playbook Artifact Export

Owner: codex
Phase: 13
Type: portfolio handoff
Depends-On: T60

Objective: export an approved workflow-to-agent design into AI Workflow
Playbook-compatible artifacts.

Acceptance-Criteria:

- export includes task blocks, implementation contract deltas, eval artifact
  skeletons, runtime tier, tool permission boundaries, and human approval points;
- exported tasks include Context-Refs back to source evidence;
- export marks generated artifacts as convenience, not authority;
- tests cover Markdown export structure.

Files:

- `workflow_agent_studio/export/`
- `docs/examples/playbook_export/`
- `tests/integration/test_playbook_export.py`

## T62: Permission And Runtime Boundary Pack

Owner: codex
Phase: 13
Type: tool:schema
Depends-On: T60

Objective: create a reusable permission/runtime boundary section for every
agent candidate.

Acceptance-Criteria:

- every candidate lists read/write/destructive tool surfaces;
- risky actions include confirmation or sandbox recommendation;
- runtime tier is justified by mutability, privilege, and blast radius;
- output can feed AI Rollout Training OS scenarios.

Files:

- `workflow_agent_studio/domain/`
- `workflow_agent_studio/blueprint/`
- `tests/unit/`
- `docs/handoffs/ai_rollout_training_os.md`

## T63: Framework Readiness Review

Owner: human + codex
Phase: 13
Type: audit decision
Depends-On: T58, T60, T61, T62

Objective: decide whether the project is ready to be shown as a serious
workflow-to-agent framework or needs another quality pass.

Acceptance-Criteria:

- review cites candidate diversity, Playbook export, permission boundary pack,
  eval evidence, and public positioning;
- review records what claims are still forbidden before real workflow data;
- CODEX_PROMPT.md records the next task or pause decision.

Files:

- `docs/audit/FRAMEWORK_READINESS_REVIEW.md`
- `docs/CODEX_PROMPT.md`

---

## Phase 14: SMB AI Roadmap Product Layer

Business goal: turn the current evidence-linked workflow-to-agent framework into
an SMB AI implementation roadmap product layer. The product should produce
verified implementation roadmaps that state what to automate, what not to
automate yet, which solution type fits, which privacy mode is safe, what the
cost/time/team assumptions are, and how each recommendation should be reviewed
and evaluated.

Exit criteria:

- RoadmapReport v1, RecommendationCard, privacy, costing, scoring, and
  verification schemas are typed and tested;
- privacy classification and cloud/private/local policy gates block unsafe
  recommendations;
- SMB implementation patterns are versioned and validated;
- deterministic cost and priority engines produce ranges and bands with
  assumptions;
- three synthetic demo workflows generate roadmap reports with verification
  appendices;
- roadmap evals block generic reports, unsupported claims, unsafe privacy
  recommendations, and false-precision estimates.

## T64: Privacy Domain Model

Owner: codex
Phase: 14
Type: plan:schema compliance:control
Depends-On: T63

Objective: add typed privacy classes and classification result schemas used by
roadmap recommendations and policy gates.

Acceptance-Criteria:

- privacy classes include public, internal, confidential, sensitive, and
  restricted;
- unknown privacy classes fail Pydantic validation;
- schema can represent detected flags, redaction status, source privacy class,
  and recommendation privacy class;
- unit tests cover valid classes and invalid class rejection.

Files:

- `workflow_agent_studio/domain/privacy.py`
- `tests/unit/test_privacy_schema.py`

Context-Refs:

- `docs/security/data_classification.md`
- `docs/security/privacy_modes.md`
- `docs/product/report_contract.md`

## T65: Recommendation Card Schema

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T64

Objective: implement the `RecommendationCard` schema for roadmap initiatives.

Acceptance-Criteria:

- recommendation without target workflow step fails validation;
- recommendation without evidence and without assumptions fails validation;
- recommendation without fallback fails validation;
- recommendation requires privacy, cost, time, risks, validation method, success
  metrics, required data, dependencies, and human gate fields;
- unit tests cover happy path and each blocking invalid case.

Files:

- `workflow_agent_studio/domain/recommendation.py`
- `tests/unit/test_recommendation_schema.py`

Context-Refs:

- `docs/product/report_contract.md#6-recommendation-cards`
- `docs/methodology/ai_suitability_classification.md`

## T66: Costing Domain Model

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T65

Objective: implement cost estimate schemas with one-time/monthly ranges,
assumptions, confidence, and price-card references.

Acceptance-Criteria:

- low, medium, and high cost ordering is validated;
- estimate without assumptions fails validation;
- estimate confidence supports low, medium, and high;
- monthly and one-time costs can be represented separately;
- unit tests cover invalid ordering and missing assumptions.

Files:

- `workflow_agent_studio/domain/costing.py`
- `tests/unit/test_costing_schema.py`

Context-Refs:

- `docs/methodology/cost_estimation.md`
- `docs/evals/cost_estimation_eval.md`

## T67: Scoring Domain Model

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T65

Objective: implement priority score schemas for business value, delivery
readiness, risk penalty, priority band, confidence, rationale, and uncertainty.

Acceptance-Criteria:

- priority band supports quick_win, strategic_pilot, prepare_first,
  do_not_automate_yet, classic_automation, and human_only;
- score output requires rationale and uncertainty notes;
- invalid score bands fail validation;
- unit tests cover valid and invalid score outputs.

Files:

- `workflow_agent_studio/domain/scoring.py`
- `tests/unit/test_priority_scoring_schema.py`

Context-Refs:

- `docs/methodology/scoring_model.md`

## T68: Verification Domain Model

Owner: codex
Phase: 14
Type: compliance:evidence plan:schema
Depends-On: T65

Objective: implement claims, assumptions, evidence items, recommendation traces,
and verification receipt schemas for roadmap reports.

Acceptance-Criteria:

- claim requires claim type, evidence level, confidence, and status;
- assumption requires impact, verification method, owner, and status;
- recommendation trace records pattern, cost model, scoring model, and privacy
  model versions;
- receipt records source hashes, report schema version, model metadata, and
  blocking finding count;
- unit tests cover minimal valid receipt and invalid missing fields.

Files:

- `workflow_agent_studio/domain/verification.py`
- `tests/unit/test_verification_receipt.py`

Context-Refs:

- `docs/methodology/verification_model.md`
- `docs/architecture/reproducibility.md`

## T69: Roadmap Report Schema

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T64, T65, T66, T67, T68

Objective: implement the `RoadmapReport` aggregate schema.

Acceptance-Criteria:

- report requires executive summary, evidence packet, workflow map, process
  inventory, recommendations, rollout plan, evaluation plan, governance plan,
  and verification appendix;
- report fails validation when recommendations list is empty and no
  do-not-automate rationale is provided;
- JSON fixture round-trips through Pydantic serialization;
- tests cover minimal valid and invalid reports.

Files:

- `workflow_agent_studio/domain/roadmap.py`
- `tests/unit/test_roadmap_report_schema.py`
- `tests/fixtures/roadmaps/minimal_valid_roadmap.json`

Context-Refs:

- `docs/product/report_contract.md`
- `docs/architecture/roadmap_data_model.md`

## T70: Deterministic Privacy Classifier

Owner: codex
Phase: 14
Type: compliance:control
Depends-On: T64

Objective: classify workflow fields and source snippets for PII, secrets, legal,
health, payment, tax, HR, and identity hints.

Acceptance-Criteria:

- classifier marks email, phone, address, passport/ID-like, payment-like, and
  API-key-like examples;
- legal consultancy fixture is classified restricted;
- salon fixture is classified sensitive, not restricted;
- false-positive fixture remains internal or confidential as expected;
- tests cover all required privacy eval categories.

Files:

- `workflow_agent_studio/privacy/classifier.py`
- `tests/unit/test_privacy_classifier.py`
- `tests/fixtures/smb/`

Context-Refs:

- `docs/security/data_classification.md`
- `docs/evals/privacy_classification_eval.md`

## T71: Redaction Preview

Owner: codex
Phase: 14
Type: compliance:control
Depends-On: T70

Objective: implement deterministic redaction preview that masks detected secrets
and personal values while preserving field names and workflow meaning.

Acceptance-Criteria:

- preview replaces emails, phones, addresses, IDs, card-like values, and API
  keys with stable placeholders;
- preview reports redaction counts by type;
- original raw values do not appear in preview output;
- tests cover mixed synthetic/real examples.

Files:

- `workflow_agent_studio/privacy/redaction.py`
- `tests/unit/test_redaction_preview.py`

Context-Refs:

- `docs/security/redaction_policy.md`

## T72: Cloud Private Local Policy Gate

Owner: codex
Phase: 14
Type: compliance:control plan:validation
Depends-On: T70, T71

Objective: block unsafe model-mode recommendations based on privacy class and
redaction status.

Acceptance-Criteria:

- restricted data blocks lightweight cloud recommendation unless source is
  synthetic/redacted and report states the condition;
- sensitive data requires redaction note for cloud mode;
- high-risk legal, medical, financial, and HR domains require a human review
  gate;
- tests cover legal consultancy, e-commerce, and hair salon fixtures.

Files:

- `workflow_agent_studio/validators/privacy.py`
- `tests/unit/test_privacy_policy_gate.py`

Context-Refs:

- `docs/security/cloud_vs_local_decision.md`
- `docs/security/privacy_modes.md`

## T73: SMB Implementation Pattern Schema

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T65

Objective: implement schema and loader for versioned SMB implementation
patterns.

Acceptance-Criteria:

- pattern schema validates pattern ID, version, signals, required data, privacy
  default, architecture, risks, eval metrics, and when-not-to-use;
- invalid JSON pattern fails with a clear validation error;
- loader returns pattern version metadata;
- unit tests validate every pattern file.

Files:

- `workflow_agent_studio/patterns/smb.py`
- `workflow_agent_studio/patterns/smb/`
- `tests/unit/test_smb_pattern_library.py`

Context-Refs:

- `docs/methodology/implementation_patterns.md`

## T74: MVP SMB Pattern Pack

Owner: codex
Phase: 14
Type: plan:schema
Depends-On: T73

Objective: add the first versioned SMB pattern JSON pack.

Acceptance-Criteria:

- pattern pack includes support triage, knowledge assistant, sales email, lead
  qualification, document extraction, invoice processing, appointment booking,
  legal checklist, e-commerce returns, reporting automation, and messaging
  support bot;
- every pattern includes when-not-to-use;
- pattern library tests validate all JSON files.

Files:

- `workflow_agent_studio/patterns/smb/*.json`
- `tests/unit/test_smb_pattern_library.py`

Context-Refs:

- `docs/methodology/implementation_patterns.md#mvp-pattern-set`

## T75: Pattern Matching Baseline

Owner: codex
Phase: 14
Type: plan:validation
Depends-On: T72, T73, T74

Objective: match opportunities to SMB patterns with anti-matches and privacy
checks.

Acceptance-Criteria:

- hair salon reminder maps to deterministic reminder/appointment pattern, not a
  high-autonomy agent;
- e-commerce returns maps to human-in-the-loop returns assistant, not automatic
  refund;
- legal checklist maps to private checklist assistant, not legal advice
  automation;
- pattern matching eval records expected matches.

Files:

- `workflow_agent_studio/roadmap/pattern_matching.py`
- `tests/eval/test_pattern_matching_eval.py`
- `docs/evals/pattern_matching_eval.md`

Context-Refs:

- `docs/evals/pattern_matching_eval.md`

## T76: Cost Engine

Owner: codex
Phase: 14
Type: plan:validation
Depends-On: T66, T73

Objective: generate deterministic cost ranges from pattern, scope, privacy mode,
volume, and assumptions.

Acceptance-Criteria:

- engine returns one-time and monthly low/medium/high ranges;
- engine requires assumptions and confidence;
- local/private mode includes infra and maintenance overhead;
- tests cover reminder, support assistant, and private document assistant.

Files:

- `workflow_agent_studio/costing/engine.py`
- `workflow_agent_studio/costing/price_cards.py`
- `tests/unit/test_cost_engine.py`

Context-Refs:

- `docs/methodology/cost_estimation.md`
- `docs/evals/cost_estimation_eval.md`

## T77: Priority Scoring Engine

Owner: codex
Phase: 14
Type: plan:validation
Depends-On: T67, T72, T75

Objective: compute priority bands from business value, delivery readiness, risk
penalty, and confidence.

Acceptance-Criteria:

- high value/high readiness/low risk maps to quick_win;
- high privacy risk and low evaluation clarity maps to prepare_first or
  do_not_automate_yet;
- deterministic reminder can map to classic_automation;
- output includes uncertainty notes.

Files:

- `workflow_agent_studio/scoring/priority.py`
- `tests/unit/test_priority_scoring.py`

Context-Refs:

- `docs/methodology/scoring_model.md`

## T78: Roadmap Assembly Service

Owner: codex
Phase: 14
Type: plan:schema plan:validation
Depends-On: T69, T72, T75, T76, T77

Objective: assemble workflow map, opportunities, privacy results, pattern
matches, costs, scores, and verification data into `RoadmapReport`.

Acceptance-Criteria:

- service creates a valid RoadmapReport from each of the three demo inputs;
- report includes do-not-automate items;
- report includes privacy mode recommendation;
- report includes verification appendix.

Files:

- `workflow_agent_studio/roadmap/service.py`
- `tests/integration/test_roadmap_generation.py`

Context-Refs:

- `docs/product/report_contract.md`
- `docs/examples/domains/`

## T79: Roadmap Markdown Export

Owner: codex
Phase: 14
Type: none
Depends-On: T78

Objective: export RoadmapReport to stable Markdown with recommendation cards and
verification appendix.

Acceptance-Criteria:

- export includes all required report sections in stable order;
- draft export is visibly labeled as draft;
- verification appendix includes claims and assumptions;
- local export path constraints remain enforced.

Files:

- `workflow_agent_studio/reporting/roadmap_markdown.py`
- `workflow_agent_studio/export/roadmap.py`
- `tests/integration/test_roadmap_markdown_export.py`

Context-Refs:

- `docs/product/report_contract.md`
- `workflow_agent_studio/export/paths.py`

## T80: Roadmap CLI Command

Owner: codex
Phase: 14
Type: none
Depends-On: T78, T79

Objective: add a local CLI command that generates a roadmap from a business
profile/input file.

Acceptance-Criteria:

- command accepts database, run ID, business profile, privacy mode, and output
  path;
- command can generate the hair salon demo report without external credentials;
- invalid privacy mode exits nonzero with clear error;
- integration test covers command success and invalid mode.

Files:

- `workflow_agent_studio/cli.py`
- `tests/integration/test_roadmap_cli.py`
- `docs/operator_guide.md`

Context-Refs:

- `docs/examples/domains/hair_salon_input.md`

## T81: Roadmap Eval Suite

Owner: codex
Phase: 14
Type: plan:validation eval
Depends-On: T79, T80

Objective: implement automated evals for roadmap quality, privacy
classification, cost estimation, pattern matching, and recommendation
verification.

Acceptance-Criteria:

- eval tests assert no forbidden claims in demo reports;
- eval tests assert every recommendation has evidence or assumptions;
- privacy eval blocks unrestricted cloud mode for legal consultancy;
- cost eval rejects single-point estimates.

Files:

- `tests/eval/test_roadmap_quality_eval.py`
- `tests/eval/test_privacy_classification_eval.py`
- `tests/eval/test_cost_estimation_eval.py`
- `tests/eval/test_pattern_matching_eval.py`
- `tests/eval/test_recommendation_verification_eval.py`

Context-Refs:

- `docs/evals/`

## T82: Roadmap Review And Handoff Export

Owner: codex
Phase: 14
Type: plan:validation compliance:evidence
Depends-On: T81

Objective: add reviewer checklist output and approved implementation handoff
export for roadmap recommendations.

Acceptance-Criteria:

- reviewer output includes accepted, reason, missing evidence, cost realism,
  privacy concern, would-show-to-client, and required changes;
- unresolved blocking findings prevent approved export;
- handoff includes tasks, acceptance criteria, eval cases, risks, owner, privacy
  mode, and human gates;
- unapproved or blocked roadmap cannot produce approved handoff.

Files:

- `workflow_agent_studio/roadmap/review.py`
- `workflow_agent_studio/export/roadmap_handoff.py`
- `tests/integration/test_roadmap_review.py`
- `tests/integration/test_roadmap_handoff_export.py`
- `docs/operator_guide.md`

Context-Refs:

- `docs/evals/recommendation_verification_eval.md`
- `docs/prompts/ORCHESTRATOR.md`
- `docs/CODEX_PROMPT.md`

---

# Phase 15 - Pattern Library Expansion And Frontier Discovery

Goal: expand the roadmap pattern library from public automation-template
corpora without copying third-party workflows into product logic, then add a
frontier-model discovery layer that proposes additional opportunity candidates
under deterministic verification and human review.

Guardrails:

- public n8n templates are research inputs, not customer proof;
- raw third-party workflow JSON should not be committed unless license review
  explicitly allows it;
- extracted patterns must be deduplicated and normalized before review;
- frontier-model output can create candidates only, not approved roadmap
  recommendations;
- privacy, cost, forbidden-claim, and approval gates remain deterministic.

## T83: Public n8n Pattern Mining Foundation

Owner: codex
Phase: 15
Type: rag:ingestion plan:schema
Depends-On: T82

Objective: add a reproducible foundation for mining public n8n workflow
templates into deduplicated pattern candidates.

Acceptance-Criteria:

- source register documents public n8n repositories, licenses, limitations, and
  demo-only claim boundaries;
- parser extracts node integrations, triggers, actions, AI nodes, risk signals,
  data sensitivity hints, and stable fingerprints from n8n workflow JSON;
- duplicate candidates are collapsed by fingerprint while preserving source
  locators;
- tests cover parser extraction, fingerprint stability, and dedupe behavior;
- docs explain that extracted candidates require human review before becoming
  SMB implementation patterns.

Files:

- `workflow_agent_studio/patterns/n8n.py`
- `tests/unit/test_n8n_pattern_mining.py`
- `docs/experiments/n8n_template_source_register.md`
- `docs/methodology/N8N_PATTERN_MINING_RU.md`
- `docs/tasks.md`
- `docs/CODEX_PROMPT.md`

Context-Refs:

- `docs/open_source_research_protocol.md`
- `docs/methodology/implementation_patterns.md`
- `workflow_agent_studio/patterns/smb.py`

## T84: Frontier Opportunity Discovery Layer

Owner: codex
Phase: 15
Type: plan:validation eval
Depends-On: T83

Objective: add a prompt contract and candidate schema for frontier models to
suggest additional roadmap opportunities without becoming the source of truth.

Acceptance-Criteria:

- prompt contract asks the model for missed opportunities, alternatives,
  do-not-automate candidates, assumptions, and confidence;
- model outputs are represented as unapproved opportunity candidates;
- deterministic verifier rejects candidates missing evidence/assumptions,
  human gates, privacy compatibility, or cost assumptions;
- tests prove frontier candidates cannot be exported as approved roadmap
  recommendations without review;
- docs clearly separate pattern-library matches from frontier-suggested
  candidates.

Files:

- `docs/prompts/frontier_opportunity_discovery.md`
- `workflow_agent_studio/roadmap/`
- `tests/eval/`
- `docs/methodology/ROADMAP_CALCULATION_RU.md`
- `docs/CODEX_PROMPT.md`

Context-Refs:

- `docs/prompts/roadmap_prompt_contracts.md`
- `docs/product/report_contract.md`
- `tests/eval/test_recommendation_verification_eval.py`
