# Planning Evaluation - Workflow-to-Agent Studio

Status: planned
Profile: Planning ON
Plan schema version: v1 planned
Date: 2026-05-19

---

## Evaluation Method

The v1 planning evaluation measures whether automation blueprints are complete, schema-valid, evidence-linked, and blocked when unsafe or underspecified.

Metrics:

- schema validation pass rate on blueprint fixtures
- required-section coverage
- evidence-link coverage
- blocking finding count by validator
- eval-case completeness
- approved-export eligibility rate

Regression criteria:

- Any valid fixture failing schema validation after a schema-compatible change is a P1.
- Any approved blueprint with blocking findings is a P1.
- Any reduction in required-section coverage from baseline is a P1 unless documented and accepted.
- Any task tagged `plan:schema` or `plan:validation` without a current eval row is incomplete.

Dataset boundary:

- demo fixtures validate product mechanics only
- synthetic benchmarks validate regression behavior only
- sanitized artifacts are not proof unless tied to a reviewed real pilot
- real pilot proof is recorded only in `docs/pilot_measurement.md`

---

## Fixture Set

Initial fixture set to implement in Phase 1 and Phase 4:

| Fixture ID | Purpose | Expected Result |
|------------|---------|-----------------|
| P01 | Minimal valid blueprint | Schema-valid |
| P02 | Claim without evidence or assumption | Blocking evidence finding |
| P03 | Missing approval boundaries | Blocking approval-boundary finding |
| P04 | Missing eval cases | Blocking eval-case finding |
| P05 | Forbidden autonomy claim | Blocking forbidden-claim finding |
| P06 | Complete sample SOP blueprint | Valid draft with measurable eval cases |

---

## Baseline

T05 established the initial schema-validation baseline with the minimal valid blueprint
fixture set.

T14 established the blueprint synthesis section-coverage baseline with the complete
workflow fixture.

T15 established the validation gate baseline with one valid blueprint fixture and
three invalid fixture variants covering approval boundaries, evidence coverage, and
eval cases.

T16 established the review-state approval baseline with immutable edit versioning,
approval blocking for invalid blueprints, and audit-backed approval recording.

T18 established the end-to-end CLI workflow baseline with one generated draft, one
blocking insufficient-evidence run, and one Markdown export.

T20 established the pilot proof metric template coverage baseline without claiming
pilot success before a real human-reviewed row is filled.

T23 established the evidence gap report baseline with source anchors, one
missing extraction question, and six required-section evidence gaps.

T24 established the real-world-style corpus planning baseline with required-section
coverage and evidence-gap metrics.

T27 established the provider-backed extraction schema baseline with fake-provider
parity and schema-error observability.

T28 established the prompt registry version baseline with two task-focused prompt
assets and generation-attempt version records.

T29 established the automation readiness baseline with deterministic risk,
next-question, and blocking-validation outcomes.

T30 established the governance report export baseline with readiness reporting,
approved-export blocking, and local path constraints.

T33 established the vertical pack schema baseline with deterministic pack loading
and generation-attempt metadata coverage.

T35 established the real pilot measurement baseline as template-only because no
human-reviewed pilot evidence exists yet. The measurement gate requires timing,
required-section acceptance, reviewer edits, and critical missing questions
before any pass claim can be made.

T38 established the approved handoff export baseline with approval/version gates,
blocking-validation rejection, local path constraints, and local-only side-effect
boundaries.

T39 established the reviewer feedback taxonomy baseline with six reusable
categories and audit storage that excludes raw confidential reviewer text.

T41 established the synthetic benchmark planning baseline with deterministic
required-section and feedback-category coverage. Synthetic results cannot
satisfy T34 or commercial pilot proof.

T42 established the deterministic sanitization baseline for benchmark and future
pilot artifacts, preserving eval structure while redacting common PII and
credential-like values.

T43 established the pilot intake checklist baseline with source-material,
reviewer-action, threshold, and missing-question gates that distinguish real
pilot evidence from demo or synthetic fixtures.

T44 established the vertical-pack dry-run planning baseline by comparing generic
and support-intake pack required-section expectations on synthetic fixtures. T34
remains blocked until real pilot evidence exists.

T45 established the review feedback analytics baseline with category, section,
and blueprint-version counts that exclude raw confidential reviewer text.

T46 established the demo/synthetic/real-pilot dataset boundary baseline for
planning eval artifacts and pilot measurement docs.

T51 established the public workflow research protocol planning baseline for
source-register completeness, public-vs-pilot boundary language, and operator
handoff instructions.

T52 established the lead-intake public corpus planning baseline with extracted
actors, systems, customer inputs, qualification fields, escalation points, and
unsafe-answer boundaries.

T53 established the three-pack public blueprint showcase baseline with lead
intake, issue triage, and incident response packs.

T54 established the public blueprint quality review rubric baseline with
showcase-ready results for all three public demo packs.

PUBLIC-TEST-1 established three internet workflow examples as public-source test
fixtures with actors, systems, decisions, data fields, and unsafe-answer
boundaries.

PUBLIC-PROOF-1 established public-data working product proof: 8 public workflow
fixtures, 3 internet workflow E2E fixtures, domain-specific blueprint markers,
and customer-proof boundary language.

T59 established the design candidate schema baseline with six
workflow-to-agent variants, required tradeoff fields, and deterministic blockers
for missing approval boundaries or eval plans.

T60 established the diverse design generation baseline with six generated
candidates, explicit tradeoff comparison, consolidated blueprint output, and
`needs_review` status when evidence gaps indicate insufficient evidence.

- Date: 2026-05-19
- Task: T05
- Eval Source: pytest tests/unit/test_blueprint_schema.py tests/eval/test_plan_eval.py -q
- Metric: Schema validation pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Regression: No

Blueprint synthesis baseline:

- Date: 2026-05-19
- Task: T14
- Eval Source: pytest tests/integration/test_blueprint_synthesis.py tests/eval/test_plan_eval.py -q
- Metric: Blueprint synthesis section coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Regression: No

Validation gate baseline:

- Date: 2026-05-19
- Task: T15
- Eval Source: pytest tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py -q
- Metric: Validation fixture expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Blocking findings: 3
- Regression: No

Review-state approval baseline:

- Date: 2026-05-19
- Task: T16
- Eval Source: pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q
- Metric: Review approval gate expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Approval blocked fixtures: 2
- Approval recorded fixtures: 1
- Regression: No

End-to-end CLI baseline:

- Date: 2026-05-19
- Task: T18
- Eval Source: pytest tests/integration/test_cli_workflow.py tests/eval/test_end_to_end_eval.py -q
- Metric: End-to-end draft blueprint expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Draft generated fixtures: 1
- Blocking run rejected fixtures: 1
- Export written fixtures: 1
- Regression: No

Pilot proof metric template baseline:

- Date: 2026-05-19
- Task: T20
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Pilot proof metric template coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Regression: No

Evidence gap report baseline:

- Date: 2026-05-20
- Task: T23
- Eval Source: pytest tests/integration/test_evidence_gap_report.py tests/eval/test_plan_eval.py -q
- Metric: Evidence gap report expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Missing questions: 1
- Evidence gaps: 6
- Regression: No

Real-world-style corpus planning baseline:

- Date: 2026-05-20
- Task: T24
- Eval Source: pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_plan_eval.py -q
- Metric: Corpus required-section evidence coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Required-section coverage: 0.67
- Evidence gaps: 2
- Regression: No

Provider-backed extraction baseline:

- Date: 2026-05-20
- Task: T27
- Eval Source: pytest tests/integration/test_extraction.py tests/unit/test_llm_gateway.py tests/eval/test_plan_eval.py -q
- Metric: Provider-backed extraction schema pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Fake/provider fixture parity: 100%
- Provider credential path: optional
- Regression: No

Prompt registry baseline:

- Date: 2026-05-20
- Task: T28
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Prompt registry version coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Prompt registry size: 2
- Prompt versions recorded per generation attempt: 2
- Regression: No

Automation readiness baseline:

- Date: 2026-05-20
- Task: T29
- Eval Source: pytest tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py -q
- Metric: Automation readiness expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Ready fixture score: 80
- Blocked fixture score: 0
- Regression: No

Governance report export baseline:

- Date: 2026-05-20
- Task: T30
- Eval Source: pytest tests/integration/test_markdown_export.py tests/eval/test_plan_eval.py -q
- Metric: Governance report export expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Approved governance blocks: 1
- Local path constraints: pass
- Regression: No

Vertical pack schema baseline:

- Date: 2026-05-20
- Task: T33
- Eval Source: pytest tests/unit/test_pattern_library.py tests/eval/test_plan_eval.py -q
- Metric: Vertical pack schema pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Pack metadata generation coverage: 100%
- Regression: No

Real pilot measurement baseline:

- Date: 2026-05-20
- Task: T35
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Pilot measurement evidence gate coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Pilot status: template-only
- Reviewed pilot rows: 0
- Regression: No

Approved handoff export baseline:

- Date: 2026-05-20
- Task: T38
- Eval Source: pytest tests/integration/test_markdown_export.py tests/eval/test_plan_eval.py -q
- Metric: Approved handoff export expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Approval gates: pass
- Local side effects only: pass
- Regression: No

Reviewer feedback taxonomy baseline:

- Date: 2026-05-20
- Task: T39
- Eval Source: pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q
- Metric: Feedback category coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Categories: 6
- Raw feedback text persisted in audit: no
- Regression: No

Synthetic benchmark planning baseline:

- Date: 2026-05-20
- Task: T41
- Eval Source: pytest tests/eval/test_synthetic_benchmark_eval.py tests/eval/test_plan_eval.py -q
- Metric: Synthetic benchmark planning coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Fixtures: 2
- Required sections covered: 7
- Feedback categories covered: 6
- Pilot evidence: no
- Regression: No

Sanitization baseline:

- Date: 2026-05-20
- Task: T42
- Eval Source: pytest tests/unit/test_sanitization.py tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Sanitization expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Redaction classes: 6
- Structure preservation: pass
- Regression: No

Pilot intake checklist baseline:

- Date: 2026-05-20
- Task: T43
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Pilot intake checklist coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Real-pilot gate: explicit
- Demo/synthetic exclusion: pass
- Regression: No

Vertical-pack dry-run planning baseline:

- Date: 2026-05-20
- Task: T44
- Eval Source: pytest tests/eval/test_vertical_pack_dry_run_eval.py tests/eval/test_plan_eval.py -q
- Metric: Vertical-pack dry-run expected-section coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Generic expected sections: 3
- Vertical expected sections: 7
- Pilot evidence: no
- Regression: No

Review feedback analytics baseline:

- Date: 2026-05-20
- Task: T45
- Eval Source: pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q
- Metric: Feedback analytics expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Analytics dimensions: category, section, blueprint_version_id
- Raw feedback text persisted: no
- Regression: No

Dataset boundary baseline:

- Date: 2026-05-20
- Task: T46
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Dataset boundary documentation coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Demo/synthetic proof status: excluded
- Real pilot proof source: docs/pilot_measurement.md
- Regression: No

Public workflow research protocol baseline:

- Date: 2026-05-23
- Task: T51
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Public workflow research protocol coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Source register coverage: pass
- Public-vs-pilot boundary: pass
- Regression: No

Lead-intake public corpus baseline:

- Date: 2026-05-23
- Task: T52
- Eval Source: pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q
- Metric: Lead-intake public corpus coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Source rows: 21
- Required workflow fact groups: 6
- Public-vs-pilot boundary: pass
- Regression: No

Three-pack public showcase baseline:

- Date: 2026-05-23
- Task: T53
- Eval Source: pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q
- Metric: Public showcase pack completeness
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Packs: 3
- Required artifacts per pack: 6
- Public-vs-pilot boundary: pass
- Regression: No

Public blueprint quality rubric baseline:

- Date: 2026-05-23
- Task: T54
- Eval Source: pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q
- Metric: Public blueprint quality rubric coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Rubric dimensions: 7
- Showcase-ready pack results: 3
- Critical missing question blocker: pass
- Regression: No

Internet workflow test examples baseline:

- Date: 2026-05-23
- Task: PUBLIC-TEST-1
- Eval Source: pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q
- Metric: Internet workflow example fixture coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Fixture count: 3
- Required fact groups: 5
- Public-test-only boundary: pass
- Regression: No

Public-data working product proof baseline:

- Date: 2026-05-23
- Task: PUBLIC-PROOF-1
- Eval Source: pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q
- Metric: Public-data working product proof coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Public workflow fixtures: 8
- Internet E2E fixtures: 3
- Showcase-ready packs: 3
- Domain-specific blueprint markers: pass
- Customer proof: no
- Regression: No

Design diversity candidate schema baseline:

- Date: 2026-05-29
- Task: T59
- Eval Source: pytest tests/unit/test_design_candidate_schema.py tests/eval/test_plan_eval.py -q
- Metric: Design candidate schema and validator expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Candidate variants: 6
- Blocking validator paths: 2
- Regression: No

Diverse blueprint generation flow baseline:

- Date: 2026-05-29
- Task: T60
- Eval Source: pytest tests/integration/test_design_candidate_flow.py tests/eval/test_plan_eval.py -q
- Metric: Diverse design generation expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Candidate variants generated: 6
- Tradeoff comparison coverage: 100%
- Insufficient-evidence status: needs_review
- Regression: No

Privacy classification schema baseline:

- Date: 2026-06-01
- Task: T64
- Eval Source: pytest tests/unit/test_privacy_schema.py -q
- Metric: Privacy classification schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Privacy classes: 5
- Invalid class rejection paths: 2
- Classification fields: detected flags, redaction status, source class, recommendation class
- Regression: No

Recommendation card schema baseline:

- Date: 2026-06-01
- Task: T65
- Eval Source: pytest tests/unit/test_recommendation_schema.py -q
- Metric: Recommendation card schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Blocking invalid cases: missing workflow step, evidence or assumptions, fallback, planning fields
- Required planning fields: privacy, cost, time, risks, validation, metrics, data, dependencies, human gate
- Regression: No

Cost estimate schema baseline:

- Date: 2026-06-01
- Task: T66
- Eval Source: pytest tests/unit/test_costing_schema.py -q
- Metric: Cost estimate schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Cost ranges: one-time and monthly represented separately
- Blocking invalid cases: unordered one-time range, unordered monthly range, missing assumptions
- Confidence levels: low, medium, high
- Regression: No

Priority scoring schema baseline:

- Date: 2026-06-01
- Task: T67
- Eval Source: pytest tests/unit/test_priority_scoring_schema.py -q
- Metric: Priority scoring schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Priority bands: 6
- Required fields: business value, delivery readiness, risk penalty, band, confidence, rationale, uncertainty
- Invalid band rejection: pass
- Regression: No

Roadmap verification schema baseline:

- Date: 2026-06-01
- Task: T68
- Eval Source: pytest tests/unit/test_verification_receipt.py -q
- Metric: Verification receipt schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Valid receipt coverage: claims, assumptions, evidence items, recommendation traces, receipt
- Blocking invalid cases: missing claim, assumption, trace, and receipt required fields
- Regression: No

Roadmap report aggregate schema baseline:

- Date: 2026-06-01
- Task: T69
- Eval Source: pytest tests/unit/test_roadmap_report_schema.py -q
- Metric: Roadmap report aggregate schema expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Fixture round-trip: pass
- Blocking invalid cases: missing required sections, empty recommendations without do-not-automate rationale
- Regression: No

Privacy policy gate baseline:

- Date: 2026-06-01
- Task: T72
- Eval Source: pytest tests/unit/test_privacy_policy_gate.py -q
- Metric: Cloud/private/local privacy policy gate expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Blocking paths: restricted cloud, sensitive cloud without redaction note, high-risk domain without human gate
- Allowed paths: restricted redacted/synthetic condition, salon cloud after redaction note
- Regression: No

SMB implementation pattern schema baseline:

- Date: 2026-06-01
- Task: T73
- Eval Source: pytest tests/unit/test_smb_pattern_library.py -q
- Metric: SMB pattern schema and loader expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Pattern files validated: 1
- Blocking invalid cases: malformed JSON, missing required schema field
- Regression: No

MVP SMB pattern pack baseline:

- Date: 2026-06-01
- Task: T74
- Eval Source: pytest tests/unit/test_smb_pattern_library.py -q
- Metric: MVP SMB pattern pack coverage
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Pattern files validated: 11
- Required pattern coverage: support triage, knowledge assistant, sales email, lead qualification, document extraction, invoice processing, appointment booking, legal checklist, e-commerce returns, reporting automation, messaging support bot
- Regression: No

Pattern matching baseline:

- Date: 2026-06-01
- Task: T75
- Eval Source: pytest tests/eval/test_pattern_matching_eval.py -q
- Metric: Expected SMB pattern matches
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Expected matches: salon appointment, e-commerce returns, legal checklist, reporting automation
- Anti-matches: high-autonomy agent, automatic refund, legal advice agent, unrestricted cloud bot, weak privacy default
- Regression: No

Cost engine baseline:

- Date: 2026-06-01
- Task: T76
- Eval Source: pytest tests/unit/test_cost_engine.py -q
- Metric: Deterministic cost engine expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Covered estimates: deterministic reminder, support assistant, private document assistant
- Blocking invalid cases: missing assumptions
- Regression: No

Priority scoring engine baseline:

- Date: 2026-06-01
- Task: T77
- Eval Source: pytest tests/unit/test_priority_scoring.py -q
- Metric: Deterministic priority scoring expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Expected bands: quick_win, do_not_automate_yet, classic_automation
- Required output: rationale and uncertainty notes
- Regression: No

Roadmap assembly baseline:

- Date: 2026-06-01
- Task: T78
- Eval Source: pytest tests/integration/test_roadmap_generation.py -q
- Metric: Demo roadmap assembly expected-outcome pass rate
- Score: 100%
- Baseline: 100%
- Delta: 0%
- Demo inputs: hair salon, e-commerce, legal consultancy
- Required report coverage: recommendations, do-not-automate items, privacy mode, verification appendix
- Regression: No

Roadmap eval suite baseline:

- Date: 2026-06-01
- Task: T81
- Eval Source: pytest tests/eval/test_roadmap_quality_eval.py tests/eval/test_privacy_classification_eval.py tests/eval/test_cost_estimation_eval.py tests/eval/test_pattern_matching_eval.py tests/eval/test_recommendation_verification_eval.py -q
- Metric: Roadmap quality/privacy/cost/pattern/verification expected-outcome pass rate
- Score: 100%; 14 checks
- Baseline: 100%; 14 checks
- Delta: 0%
- Covered gates: forbidden claims, evidence or assumptions, legal cloud blocker, single-point costs, pattern trace
- Regression: No

Roadmap review and handoff baseline:

- Date: 2026-06-01
- Task: T82
- Eval Source: pytest tests/integration/test_roadmap_review.py tests/integration/test_roadmap_handoff_export.py -q
- Metric: Roadmap review and approved handoff expected-outcome pass rate
- Score: 100%; 5 checks
- Baseline: 100%; 5 checks
- Delta: 0%
- Covered gates: reviewer checklist fields, blocking findings, approved handoff content, unapproved handoff blocker
- Regression: No

---

## Evaluation History

| Date | Task | Plan Schema Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|---------------------|--------|-------|----------|-------|-------------|-------------|
| 2026-05-19 | T05 | v1 | Schema validation pass rate | 100% | 100% | 0% | No | pytest tests/unit/test_blueprint_schema.py tests/eval/test_plan_eval.py -q |
| 2026-05-19 | FIX-1 | v1 | Workflow-step evidence contract regression | 100% | 100% | 0% | No | pytest tests/unit/test_blueprint_schema.py::test_workflow_step_requires_evidence_or_assumption -q |
| 2026-05-19 | T14 | v1 | Blueprint synthesis section coverage | 100% | 100% | 0% | No | pytest tests/integration/test_blueprint_synthesis.py tests/eval/test_plan_eval.py -q |
| 2026-05-19 | T15 | v1 | Validation fixture expected-outcome pass rate; blocking findings | 100%; 3 blocking findings | 100%; 3 blocking findings | 0% | No | pytest tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py -q |
| 2026-05-19 | T16 | v1 | Review approval gate expected-outcome pass rate | 100%; 2 approvals blocked; 1 approval recorded | 100%; 2 approvals blocked; 1 approval recorded | 0% | No | pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q |
| 2026-05-19 | T18 | v1 | End-to-end draft blueprint expected-outcome pass rate | 100%; 1 draft generated; 1 blocking run rejected; 1 export written | 100%; 1 draft generated; 1 blocking run rejected; 1 export written | 0% | No | pytest tests/integration/test_cli_workflow.py tests/eval/test_end_to_end_eval.py -q |
| 2026-05-19 | T20 | v1 | Pilot proof metric template coverage | 100% | 100% | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T23 | v1 | Evidence gap report expected-outcome pass rate | 100%; 1 missing question; 6 evidence gaps | 100%; 1 missing question; 6 evidence gaps | 0% | No | pytest tests/integration/test_evidence_gap_report.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T24 | v1 | Corpus required-section evidence coverage | 100%; coverage 0.67; 2 evidence gaps | 100%; coverage 0.67; 2 evidence gaps | 0% | No | pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T27 | v1 | Provider-backed extraction schema pass rate | 100%; fake/provider parity 100%; provider credential path optional | 100%; fake/provider parity 100%; provider credential path optional | 0% | No | pytest tests/integration/test_extraction.py tests/unit/test_llm_gateway.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T28 | v1 | Prompt registry version coverage | 100%; 2 prompt versions recorded | 100%; 2 prompt versions recorded | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T29 | v1 | Automation readiness expected-outcome pass rate | 100%; ready score 80; blocked score 0 | 100%; ready score 80; blocked score 0 | 0% | No | pytest tests/unit/test_blueprint_validators.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T30 | v1 | Governance report export expected-outcome pass rate | 100%; 1 approved governance block; path constraints pass | 100%; 1 approved governance block; path constraints pass | 0% | No | pytest tests/integration/test_markdown_export.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T33 | v1 | Vertical pack schema pass rate | 100%; 1 pack loaded; metadata coverage 100% | 100%; 1 pack loaded; metadata coverage 100% | 0% | No | pytest tests/unit/test_pattern_library.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T35 | v1 | Pilot measurement evidence gate coverage | 100%; template-only; 0 reviewed pilot rows | 100%; template-only; 0 reviewed pilot rows | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T38 | v1 | Approved handoff export expected-outcome pass rate | 100%; approval gates pass; local side effects only | 100%; approval gates pass; local side effects only | 0% | No | pytest tests/integration/test_markdown_export.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T39 | v1 | Feedback category coverage | 100%; 6 categories; raw feedback audit persistence no | 100%; 6 categories; raw feedback audit persistence no | 0% | No | pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T41 | v1 | Synthetic benchmark planning coverage | 100%; 2 fixtures; 7 sections; 6 feedback categories; pilot evidence no | 100%; 2 fixtures; 7 sections; 6 feedback categories; pilot evidence no | 0% | No | pytest tests/eval/test_synthetic_benchmark_eval.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T42 | v1 | Sanitization expected-outcome pass rate | 100%; 6 redaction classes; structure preservation pass | 100%; 6 redaction classes; structure preservation pass | 0% | No | pytest tests/unit/test_sanitization.py tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T43 | v1 | Pilot intake checklist coverage | 100%; real-pilot gate explicit; demo/synthetic excluded | 100%; real-pilot gate explicit; demo/synthetic excluded | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T44 | v1 | Vertical-pack dry-run expected-section coverage | 100%; generic sections 3; vertical sections 7; pilot evidence no | 100%; generic sections 3; vertical sections 7; pilot evidence no | 0% | No | pytest tests/eval/test_vertical_pack_dry_run_eval.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T45 | v1 | Feedback analytics expected-outcome pass rate | 100%; category/section/version counts; raw feedback persistence no | 100%; category/section/version counts; raw feedback persistence no | 0% | No | pytest tests/integration/test_review_state.py tests/eval/test_plan_eval.py -q |
| 2026-05-20 | T46 | v1 | Dataset boundary documentation coverage | 100%; demo/synthetic proof excluded; real pilot source recorded | 100%; demo/synthetic proof excluded; real pilot source recorded | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | T51 | v1 | Public workflow research protocol coverage | 100%; source register pass; public-vs-pilot boundary pass | 100%; source register pass; public-vs-pilot boundary pass | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | T52 | v1 | Lead-intake public corpus coverage | 100%; source rows 21; workflow fact groups 6; public-vs-pilot boundary pass | 100%; source rows 21; workflow fact groups 6; public-vs-pilot boundary pass | 0% | No | pytest tests/unit/test_docs.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | T53 | v1 | Public showcase pack completeness | 100%; packs 3; required artifacts per pack 6; public-vs-pilot boundary pass | 100%; packs 3; required artifacts per pack 6; public-vs-pilot boundary pass | 0% | No | pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | T54 | v1 | Public blueprint quality rubric coverage | 100%; rubric dimensions 7; showcase-ready pack results 3; critical blocker pass | 100%; rubric dimensions 7; showcase-ready pack results 3; critical blocker pass | 0% | No | pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | PUBLIC-TEST-1 | v1 | Internet workflow example fixture coverage | 100%; fixtures 3; required fact groups 5; public-test-only boundary pass | 100%; fixtures 3; required fact groups 5; public-test-only boundary pass | 0% | No | pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q |
| 2026-05-23 | PUBLIC-PROOF-1 | v1 | Public-data working product proof coverage | 100%; public fixtures 8; internet E2E fixtures 3; showcase-ready packs 3; customer proof no | 100%; public fixtures 8; internet E2E fixtures 3; showcase-ready packs 3; customer proof no | 0% | No | pytest tests/eval/test_public_source_experiment.py tests/eval/test_plan_eval.py -q |
| 2026-05-29 | T59 | design-candidate-v1 | Design candidate schema and validator expected-outcome pass rate | 100%; 6 variants; 2 blocking validator paths | 100%; 6 variants; 2 blocking validator paths | 0% | No | pytest tests/unit/test_design_candidate_schema.py tests/eval/test_plan_eval.py -q |
| 2026-05-29 | T60 | design-candidate-v1 | Diverse design generation expected-outcome pass rate | 100%; 6 candidates; tradeoff coverage 100%; insufficient evidence needs_review | 100%; 6 candidates; tradeoff coverage 100%; insufficient evidence needs_review | 0% | No | pytest tests/integration/test_design_candidate_flow.py tests/eval/test_plan_eval.py -q |
| 2026-06-01 | T64 | privacy-classification-v1 | Privacy classification schema expected-outcome pass rate | 100%; 5 privacy classes; 2 invalid class rejection paths | 100%; 5 privacy classes; 2 invalid class rejection paths | 0% | No | pytest tests/unit/test_privacy_schema.py -q |
| 2026-06-01 | T65 | recommendation-card-v1 | Recommendation card schema expected-outcome pass rate | 100%; happy path; 12 blocking invalid cases | 100%; happy path; 12 blocking invalid cases | 0% | No | pytest tests/unit/test_recommendation_schema.py -q |
| 2026-06-01 | T66 | cost-estimate-v1 | Cost estimate schema expected-outcome pass rate | 100%; 2 ordered range paths; 3 confidence levels; missing assumptions blocked | 100%; 2 ordered range paths; 3 confidence levels; missing assumptions blocked | 0% | No | pytest tests/unit/test_costing_schema.py -q |
| 2026-06-01 | T67 | priority-score-v1 | Priority scoring schema expected-outcome pass rate | 100%; 6 bands; rationale and uncertainty required; invalid band blocked | 100%; 6 bands; rationale and uncertainty required; invalid band blocked | 0% | No | pytest tests/unit/test_priority_scoring_schema.py -q |
| 2026-06-01 | T68 | roadmap-verification-receipt-v1 | Verification receipt schema expected-outcome pass rate | 100%; valid receipt; required claim, assumption, trace, receipt fields blocked | 100%; valid receipt; required claim, assumption, trace, receipt fields blocked | 0% | No | pytest tests/unit/test_verification_receipt.py -q |
| 2026-06-01 | T69 | roadmap-report-v1 | Roadmap report aggregate schema expected-outcome pass rate | 100%; JSON round-trip; missing required sections blocked; empty recommendation rationale gate | 100%; JSON round-trip; missing required sections blocked; empty recommendation rationale gate | 0% | No | pytest tests/unit/test_roadmap_report_schema.py -q |
| 2026-06-01 | T72 | privacy-policy-gate-v1 | Cloud/private/local privacy policy gate expected-outcome pass rate | 100%; restricted/sensitive/high-risk blockers; allowed redacted paths | 100%; restricted/sensitive/high-risk blockers; allowed redacted paths | 0% | No | pytest tests/unit/test_privacy_policy_gate.py -q |
| 2026-06-01 | T73 | smb-pattern-v1 | SMB pattern schema and loader expected-outcome pass rate | 100%; 1 pattern file; malformed JSON and schema blockers | 100%; 1 pattern file; malformed JSON and schema blockers | 0% | No | pytest tests/unit/test_smb_pattern_library.py -q |
| 2026-06-01 | T74 | smb-pattern-v1 | MVP SMB pattern pack coverage | 100%; 11 required patterns; every file validates; when-not-to-use present | 100%; 11 required patterns; every file validates; when-not-to-use present | 0% | No | pytest tests/unit/test_smb_pattern_library.py -q |
| 2026-06-01 | T75 | pattern-matching-baseline-v1 | Expected SMB pattern matches | 100%; expected matches and anti-matches pass | 100%; expected matches and anti-matches pass | 0% | No | pytest tests/eval/test_pattern_matching_eval.py -q |
| 2026-06-01 | T76 | cost-engine-baseline-v1 | Deterministic cost engine expected-outcome pass rate | 100%; reminder, support assistant, private document assistant, assumptions gate | 100%; reminder, support assistant, private document assistant, assumptions gate | 0% | No | pytest tests/unit/test_cost_engine.py -q |
| 2026-06-01 | T77 | priority-scoring-engine-v1 | Deterministic priority scoring expected-outcome pass rate | 100%; quick_win, do_not_automate_yet, classic_automation, uncertainty gate | 100%; quick_win, do_not_automate_yet, classic_automation, uncertainty gate | 0% | No | pytest tests/unit/test_priority_scoring.py -q |
| 2026-06-01 | T78 | roadmap-report-v1 | Demo roadmap assembly expected-outcome pass rate | 100%; 3 demo reports; privacy and verification appendix present | 100%; 3 demo reports; privacy and verification appendix present | 0% | No | pytest tests/integration/test_roadmap_generation.py -q |
| 2026-06-01 | T81 | roadmap-eval-suite-v1 | Roadmap quality/privacy/cost/pattern/verification expected-outcome pass rate | 100%; 14 checks; forbidden claims and unsafe privacy blocked | 100%; 14 checks; forbidden claims and unsafe privacy blocked | 0% | No | pytest tests/eval/test_roadmap_quality_eval.py tests/eval/test_privacy_classification_eval.py tests/eval/test_cost_estimation_eval.py tests/eval/test_pattern_matching_eval.py tests/eval/test_recommendation_verification_eval.py -q |
| 2026-06-01 | T82 | roadmap-review-handoff-v1 | Roadmap review and approved handoff expected-outcome pass rate | 100%; 5 checks; approval and blocking gates pass | 100%; 5 checks; approval and blocking gates pass | 0% | No | pytest tests/integration/test_roadmap_review.py tests/integration/test_roadmap_handoff_export.py -q |

---

## Open Planning Findings

none

---

## Regression Notes

No regressions. FIX-1 tightened schema validation for workflow steps without reducing the valid blueprint fixture pass rate.
