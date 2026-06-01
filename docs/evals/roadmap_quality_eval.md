# Roadmap Quality Eval

Purpose: prevent generic AI consulting reports.

## Golden Fixtures

Initial fixtures:

- `docs/examples/domains/hair_salon_input.md`;
- `docs/examples/domains/ecommerce_input.md`;
- `docs/examples/domains/legal_consultancy_input.md`.

Future fixtures:

- no-AI-needed simple task;
- high-privacy medical blocker;
- low-volume no-ROI workflow;
- unstable policy workflow;
- missing-owner workflow.

## Rubric

Score each dimension from 1 to 5.

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| Workflow fidelity | invented or missed core steps | mostly correct | precise and evidence-linked |
| Recommendation specificity | generic | somewhat actionable | clear data/cost/team/eval |
| Privacy awareness | unsafe | partial | mode and controls justified |
| Cost realism | magic number | rough range | assumptions and confidence |
| Verification | none | some assumptions | claims/evidence/trace complete |
| Anti-overengineering | agent everywhere | mixed | simplest sufficient solution |
| Business usefulness | vague | useful | client-ready |

## Automated Checks

- report validates against `RoadmapReport v1`;
- every recommendation has evidence or assumptions;
- every recommendation has a fallback;
- every high-risk recommendation has a human approval gate;
- every cost estimate has assumptions and confidence;
- no forbidden claims appear;
- do-not-automate section exists;
- cloud/local/private recommendation exists.

## Human Review Questions

For each recommendation:

- would this be useful to a business owner?
- would this be useful to an implementation engineer?
- is the recommendation specific to the workflow?
- is the privacy mode defensible?
- is the cost range honest?
- would you show this to a client after review?

## Pass Threshold

MVP demo report passes when:

- no blocking automated checks fail;
- average human rubric score is at least 4.0;
- privacy awareness score is at least 4;
- anti-overengineering score is at least 4;
- unsupported claim count is zero.

## Eval History

| Date | Task | Eval Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|--------------|--------|-------|----------|-------|-------------|-------------|
| 2026-06-01 | T81 | roadmap-eval-suite-v1 | Roadmap quality gate pass rate | 100%; 3 demo reports; forbidden claim surfaces clean; required quality sections present | 100%; 3 demo reports; forbidden claim surfaces clean; required quality sections present | 0% | No | pytest tests/eval/test_roadmap_quality_eval.py -q |
