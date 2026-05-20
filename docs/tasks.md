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
