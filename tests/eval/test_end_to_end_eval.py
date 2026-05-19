from pathlib import Path


def test_eval_artifacts_record_end_to_end_fixture() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert (
        "| 2026-05-19 | T18 | e2e-sample-sop-v1 | v1 | "
        "pytest tests/integration/test_cli_workflow.py tests/eval/test_end_to_end_eval.py -q | "
        "1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | No |" in retrieval_eval
    )
    assert (
        "| 2026-05-19 | T18 | v1 | End-to-end draft blueprint expected-outcome pass rate | "
        "100%; 1 draft generated; 1 blocking run rejected; 1 export written | "
        "100%; 1 draft generated; 1 blocking run rejected; 1 export written | 0% | No |"
        in plan_eval
    )
