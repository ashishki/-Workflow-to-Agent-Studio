import json
from pathlib import Path

from workflow_agent_studio.patterns import load_vertical_pack


def _dry_run_fixture() -> dict:
    return json.loads(
        Path("tests/fixtures/benchmarks/vertical_pack_dry_run.json").read_text(encoding="utf-8")
    )


def test_vertical_pack_dry_run_compares_generic_and_pack_expectations() -> None:
    dry_run = _dry_run_fixture()
    pack = load_vertical_pack("patterns/support_intake_pack.json")

    assert dry_run["vertical_pack_id"] == pack.pack_id
    assert dry_run["dataset_kind"] == "synthetic"
    assert dry_run["not_pilot_evidence"] is True
    assert dry_run["generic_expected_sections"] == [
        "workflow_summary",
        "current_workflow_steps",
        "eval_cases",
    ]
    assert dry_run["vertical_expected_sections"] == pack.required_blueprint_sections
    assert set(dry_run["vertical_expected_sections"]) > set(dry_run["generic_expected_sections"])


def test_vertical_pack_dry_run_artifacts_keep_t34_blocked() -> None:
    dry_run = _dry_run_fixture()
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert dry_run["result_label"] == "dry-run only - not pilot evidence"
    assert "T44 established the vertical-pack dry-run baseline" in retrieval_eval
    assert "T34 remains blocked" in retrieval_eval
    assert "until real pilot evidence exists." in retrieval_eval
    assert "T44 established the vertical-pack dry-run planning baseline" in plan_eval
    assert "remains blocked" in plan_eval
    assert "until real pilot evidence exists." in plan_eval
