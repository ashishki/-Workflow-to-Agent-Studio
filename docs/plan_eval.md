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

---

## Open Planning Findings

none

---

## Regression Notes

No regressions. FIX-1 tightened schema validation for workflow steps without reducing the valid blueprint fixture pass rate.
