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


def test_plan_eval_records_provider_backed_extraction_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T27 established the provider-backed extraction schema baseline" in plan_eval
    assert "Fake/provider fixture parity: 100%" in plan_eval
    assert "Provider credential path: optional" in plan_eval
    assert (
        "| 2026-05-20 | T27 | v1 | Provider-backed extraction schema pass rate | "
        "100%; fake/provider parity 100%; provider credential path optional | "
        "100%; fake/provider parity 100%; provider credential path optional | "
        "0% | No |" in plan_eval
    )


def test_plan_eval_records_prompt_registry_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T28 established the prompt registry version baseline" in plan_eval
    assert "Prompt registry size: 2" in plan_eval
    assert (
        "| 2026-05-20 | T28 | v1 | Prompt registry version coverage | "
        "100%; 2 prompt versions recorded | 100%; 2 prompt versions recorded | "
        "0% | No |" in plan_eval
    )


def test_plan_eval_records_readiness_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T29 established the automation readiness baseline" in plan_eval
    assert "Ready fixture score: 80" in plan_eval
    assert "Blocked fixture score: 0" in plan_eval
    assert (
        "| 2026-05-20 | T29 | v1 | Automation readiness expected-outcome pass rate | "
        "100%; ready score 80; blocked score 0 | "
        "100%; ready score 80; blocked score 0 | 0% | No |" in plan_eval
    )


def test_plan_eval_records_governance_export_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T30 established the governance report export baseline" in plan_eval
    assert "Approved governance blocks: 1" in plan_eval
    assert (
        "| 2026-05-20 | T30 | v1 | Governance report export expected-outcome pass rate | "
        "100%; 1 approved governance block; path constraints pass | "
        "100%; 1 approved governance block; path constraints pass | "
        "0% | No |" in plan_eval
    )


def test_plan_eval_records_vertical_pack_schema_metrics() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T33 established the vertical pack schema baseline" in plan_eval
    assert "Pack metadata generation coverage: 100%" in plan_eval
    assert (
        "| 2026-05-20 | T33 | v1 | Vertical pack schema pass rate | "
        "100%; 1 pack loaded; metadata coverage 100% | "
        "100%; 1 pack loaded; metadata coverage 100% | 0% | No |" in plan_eval
    )


def test_plan_eval_records_pilot_measurement_evidence_gate() -> None:
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T35 established the real pilot measurement baseline as template-only" in plan_eval
    assert "Pilot status: template-only" in plan_eval
    assert "Reviewed pilot rows: 0" in plan_eval
    assert (
        "| 2026-05-20 | T35 | v1 | Pilot measurement evidence gate coverage | "
        "100%; template-only; 0 reviewed pilot rows | "
        "100%; template-only; 0 reviewed pilot rows | 0% | No |" in plan_eval
    )
