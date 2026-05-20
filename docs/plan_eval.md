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

---

## Open Planning Findings

none

---

## Regression Notes

No regressions. FIX-1 tightened schema validation for workflow steps without reducing the valid blueprint fixture pass rate.
