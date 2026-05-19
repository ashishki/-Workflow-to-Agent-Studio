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

Not yet measured. First baseline is established by T05.

---

## Evaluation History

| Date | Task | Plan Schema Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|---------------------|--------|-------|----------|-------|-------------|-------------|

---

## Open Planning Findings

none

---

## Regression Notes

none
