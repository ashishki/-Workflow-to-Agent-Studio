from pathlib import Path

from workflow_agent_studio.eval import (
    load_synthetic_benchmark_fixtures,
    synthetic_benchmark_coverage,
)


def test_synthetic_benchmarks_are_labeled_not_pilot_evidence() -> None:
    fixtures = load_synthetic_benchmark_fixtures("tests/fixtures/benchmarks")

    assert [fixture.benchmark_id for fixture in fixtures] == [
        "synthetic_invoice_approval",
        "synthetic_support_intake",
    ]
    assert {fixture.dataset_kind for fixture in fixtures} == {"synthetic"}
    assert all(fixture.not_pilot_evidence for fixture in fixtures)


def test_synthetic_benchmark_coverage_reports_retrieval_and_planning() -> None:
    fixtures = load_synthetic_benchmark_fixtures("tests/fixtures/benchmarks")
    report = synthetic_benchmark_coverage(fixtures)

    assert report.fixture_count == 2
    assert report.retrieval_query_count == 6
    assert report.required_section_count == 7
    assert report.feedback_category_count == 6
    assert report.dataset_kind == "synthetic"
    assert report.not_pilot_evidence is True


def test_synthetic_benchmark_eval_artifacts_disclaim_pilot_proof() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T41 established the synthetic benchmark harness baseline" in retrieval_eval
    assert "Synthetic results cannot" in retrieval_eval
    assert "satisfy T34 or commercial pilot proof." in retrieval_eval
    assert "T41 established the synthetic benchmark planning baseline" in plan_eval
    assert "Synthetic results cannot" in plan_eval
    assert "satisfy T34 or commercial pilot proof." in plan_eval
