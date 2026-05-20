from pathlib import Path


def test_plan_eval_records_schema_baseline() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert (
        "| 2026-05-19 | T05 | v1 | Schema validation pass rate | "
        "100% | 100% | 0% | No |" in plan_eval
    )
    assert (
        "Eval Source: pytest tests/unit/test_blueprint_schema.py "
        "tests/eval/test_plan_eval.py -q" in plan_eval
    )


def test_plan_eval_records_synthesis_coverage() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T14 established the blueprint synthesis section-coverage baseline" in plan_eval
    assert (
        "| 2026-05-19 | T14 | v1 | Blueprint synthesis section coverage | "
        "100% | 100% | 0% | No |" in plan_eval
    )


def test_plan_eval_records_validation_gate_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T15 established the validation gate baseline" in plan_eval
    assert "Blocking findings: 3" in plan_eval
    assert (
        "| 2026-05-19 | T15 | v1 | Validation fixture expected-outcome pass rate; "
        "blocking findings | 100%; 3 blocking findings | "
        "100%; 3 blocking findings | 0% | No |" in plan_eval
    )


def test_plan_eval_records_review_state_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T16 established the review-state approval baseline" in plan_eval
    assert (
        "| 2026-05-19 | T16 | v1 | Review approval gate expected-outcome pass rate | "
        "100%; 2 approvals blocked; 1 approval recorded | "
        "100%; 2 approvals blocked; 1 approval recorded | 0% | No |" in plan_eval
    )


def test_plan_eval_records_pilot_measurement_template() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T20 established the pilot proof metric template coverage baseline" in plan_eval
    assert (
        "| 2026-05-19 | T20 | v1 | Pilot proof metric template coverage | "
        "100% | 100% | 0% | No |" in plan_eval
    )


def test_plan_eval_records_evidence_gap_report_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T23 established the evidence gap report baseline" in plan_eval
    assert "Missing questions: 1" in plan_eval
    assert "Evidence gaps: 6" in plan_eval
    assert (
        "| 2026-05-20 | T23 | v1 | Evidence gap report expected-outcome pass rate | "
        "100%; 1 missing question; 6 evidence gaps | "
        "100%; 1 missing question; 6 evidence gaps | 0% | No |" in plan_eval
    )
