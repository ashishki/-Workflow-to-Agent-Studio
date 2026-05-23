import json
import subprocess
import sys
from pathlib import Path

import pytest

PUBLIC_WORKFLOW_CASES = (
    pytest.param(
        "kubernetes-issue-triage",
        "tests/fixtures/public_sources/kubernetes_issue_triage.notes.md",
        (
            "Kubernetes",
            "GitHub Issues",
            "SIG",
            "triage/needs-information",
            "lifecycle/stale",
            "priority",
        ),
        id="kubernetes",
    ),
    pytest.param(
        "openstack-bug-triage",
        "tests/fixtures/public_sources/openstack_bug_triage.notes.md",
        (
            "OpenStack",
            "Launchpad",
            "Bug supervisor",
            "Incomplete",
            "Confirmed",
            "Critical",
        ),
        id="openstack",
    ),
    pytest.param(
        "gitlab-incident-workflow",
        "tests/fixtures/public_sources/gitlab_incident_workflow.notes.md",
        (
            "GitLab",
            "Incident.io",
            "PagerDuty",
            "Slack",
            "Engineer on call",
            "Google Docs",
        ),
        id="gitlab",
    ),
    pytest.param(
        "hvac-lead-intake",
        "tests/fixtures/public_sources/hvac_lead_intake.notes.md",
        (
            "HVAC",
            "Service-area checker",
            "Scheduling coordinator",
            "emergency",
            "service address",
            "appointment",
        ),
        id="hvac-lead-intake",
    ),
)


def test_netbox_public_source_fixture_runs_draft_pipeline(tmp_path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "run",
            "--database",
            str(tmp_path / "workflow.sqlite3"),
            "--run-id",
            "public-netbox-issue-triage",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/public_sources/netbox_issue_triage.notes.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    payload = json.loads(result.stdout)
    assert result.returncode == 0
    assert payload["source_count"] == 1
    assert payload["chunk_count"] >= 10
    assert payload["blueprint_version_id"] == 1
    assert payload["finding_ids"] == []
    assert payload["index_namespace"] == "v1-public-netbox-issue-triage-e2e"


def test_netbox_public_source_blueprint_preserves_domain_facts(tmp_path) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "run",
            "--database",
            str(database),
            "--run-id",
            "public-netbox-issue-triage",
            "--index-dir",
            str(tmp_path / "index"),
            "tests/fixtures/public_sources/netbox_issue_triage.notes.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    version_id = json.loads(run_result.stdout)["blueprint_version_id"]

    export_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "export",
            "--database",
            str(database),
            "--blueprint-version-id",
            str(version_id),
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            "netbox_blueprint.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    export_payload = json.loads(export_result.stdout)
    markdown = Path(export_payload["path"]).read_text(encoding="utf-8")
    assert export_result.returncode == 0
    assert "GitHub Issues" in markdown
    assert "Issue templates" in markdown
    assert "Reporter" in markdown
    assert "Maintainer or triager" in markdown
    assert "duplicate" in markdown
    assert "stale" in markdown
    assert "reproduc" in markdown
    assert "Support intake workflow routes customer requests" not in markdown


def test_netbox_public_source_experiment_keeps_pilot_boundary_explicit() -> None:
    report = Path("docs/experiments/public_source_netbox_issue_triage.md").read_text(
        encoding="utf-8"
    )
    normalized_report = " ".join(report.split())
    fixture = Path("tests/fixtures/public_sources/netbox_issue_triage.notes.md").read_text(
        encoding="utf-8"
    )

    assert "public-source experiment; not real pilot evidence" in report
    assert "not counted in `docs/pilot_measurement.md`" in report
    assert "does not satisfy T34/T40" in report
    assert "template-shaped" in report
    assert "current result preserves NetBox-specific actors" in report
    assert "pass for pipeline mechanics" in normalized_report
    assert "pass for domain-specific draft quality" in normalized_report
    assert "still blocked for real-pilot proof" in normalized_report
    assert "Dataset kind: public-source experiment only; not operator pilot evidence." in fixture
    assert "https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow" in fixture


def test_netbox_public_demo_pack_contains_reproducible_artifacts() -> None:
    pack_dir = Path("docs/experiments/public_demo_pack/netbox_issue_triage")
    readme = (pack_dir / "README.md").read_text(encoding="utf-8")
    transcript = (pack_dir / "command_transcript.md").read_text(encoding="utf-8")
    blueprint = (pack_dir / "generated_blueprint.md").read_text(encoding="utf-8")
    review = (pack_dir / "review_workspace.md").read_text(encoding="utf-8")
    gap_summary = (pack_dir / "gap_summary.md").read_text(encoding="utf-8")
    boundary_label = (pack_dir / "boundary_label.md").read_text(encoding="utf-8")
    source_register = (pack_dir / "source_register.md").read_text(encoding="utf-8")
    review_result = (pack_dir / "review_result.md").read_text(encoding="utf-8")

    assert "tests/fixtures/public_sources/netbox_issue_triage.notes.md" in readme
    assert "public-source demo material; not customer proof" in readme
    assert "source_register.md" in readme
    assert "boundary_label.md" in readme
    assert "workflow-agent-studio run" in transcript
    assert "workflow-agent-studio export" in transcript
    assert "workflow-agent-studio review" in transcript
    assert '"run_id": "public-demo-netbox-issue-triage"' in transcript
    assert "GitHub Issues triage workflow" in blueprint
    assert "Maintainer approves before issue status" in blueprint
    assert "## Findings\n- none" in review
    assert "Approval authority remains unresolved" in gap_summary
    assert "must not be counted in" in gap_summary
    assert "public_demo_only" in source_register
    assert "true" in source_register
    assert "not customer proof" in boundary_label
    assert "Status: showcase_ready" in review_result


def test_phase_12_public_showcase_packs_are_complete() -> None:
    packs = {
        "hvac_lead_intake": (
            "HVAC lead intake workflow",
            "tests/fixtures/public_sources/hvac_lead_intake.notes.md",
            "service-area checks",
        ),
        "netbox_issue_triage": (
            "GitHub Issues triage workflow",
            "tests/fixtures/public_sources/netbox_issue_triage.notes.md",
            "template checks",
        ),
        "gitlab_incident_response": (
            "GitLab incident workflow",
            "tests/fixtures/public_sources/gitlab_incident_workflow.notes.md",
            "PagerDuty notification",
        ),
    }

    for pack_name, (blueprint_marker, fixture_marker, workflow_marker) in packs.items():
        pack_dir = Path("docs/experiments/public_demo_pack") / pack_name
        readme = (pack_dir / "README.md").read_text(encoding="utf-8")
        source_register = (pack_dir / "source_register.md").read_text(encoding="utf-8")
        transcript = (pack_dir / "command_transcript.md").read_text(encoding="utf-8")
        blueprint = (pack_dir / "generated_blueprint.md").read_text(encoding="utf-8")
        review = (pack_dir / "review_workspace.md").read_text(encoding="utf-8")
        gap_summary = (pack_dir / "gap_summary.md").read_text(encoding="utf-8")
        boundary = (pack_dir / "boundary_label.md").read_text(encoding="utf-8")
        review_result = (pack_dir / "review_result.md").read_text(encoding="utf-8")
        normalized_blueprint = " ".join(blueprint.split())

        assert fixture_marker in readme or fixture_marker in source_register
        assert "public-source demo material" in readme
        assert "public_demo_only" in source_register
        assert "| true |" in source_register
        assert "workflow-agent-studio run" in transcript
        assert "workflow-agent-studio export" in transcript
        assert "workflow-agent-studio review" in transcript
        assert blueprint_marker in normalized_blueprint
        assert workflow_marker in normalized_blueprint
        assert "## Findings\n- none" in review
        assert "not real pilot review" in gap_summary
        assert "not customer proof" in boundary
        assert "Status: showcase_ready" in review_result
        assert "Critical missing questions: none" in review_result
        assert "Pilot-blocking gaps:" in review_result


def test_evaluation_guide_lists_phase_12_showcase_packs() -> None:
    guide = Path("docs/evaluation_guide.md").read_text(encoding="utf-8")

    assert "Phase 12 showcase packs" in guide
    assert "hvac_lead_intake/" in guide
    assert "netbox_issue_triage/" in guide
    assert "gitlab_incident_response/" in guide
    assert "source register or fixture pointer" in guide
    assert "boundary label" in guide


def test_public_blueprint_quality_rubric_blocks_critical_missing_questions() -> None:
    guide = Path("docs/evaluation_guide.md").read_text(encoding="utf-8")
    normalized = " ".join(guide.split())

    assert "## Public Blueprint Quality Review Rubric" in guide
    assert "evidence coverage" in guide
    assert "workflow specificity" in guide
    assert "missing questions" in guide
    assert "approval boundaries" in guide
    assert "integration realism" in guide
    assert "eval-case quality" in guide
    assert "forbidden claims" in guide
    assert "`showcase_ready` is allowed only" in guide
    assert "no unresolved critical missing question remains" in normalized


def test_lead_response_sla_agent_handoff_is_source_bounded() -> None:
    handoff = Path("docs/handoffs/lead_response_sla_agent.md").read_text(encoding="utf-8")
    normalized = " ".join(handoff.split())

    assert "Status: public-source demo handoff; not customer proof" in handoff
    assert "docs/experiments/public_demo_pack/hvac_lead_intake/" in handoff
    assert "tests/fixtures/public_sources/hvac_lead_intake.notes.md" in handoff
    assert "## Workflow Map" in handoff
    assert "## Qualification Fields" in handoff
    assert "## Safe Reply Boundaries" in handoff
    assert "## Handoff Reasons" in handoff
    assert "## Knowledge-Pack Requirements" in handoff
    assert "## Eval Cases" in handoff
    assert "## Missing Data Requests" in handoff
    assert "do not confirm arrival" in handoff
    assert "do not promise coverage" in handoff
    assert "public_demo_only=true" in handoff
    assert "Does not satisfy T34, T40" in normalized


@pytest.mark.parametrize(
    ("run_slug", "fixture_path", "expected_markers"),
    PUBLIC_WORKFLOW_CASES,
)
def test_public_source_workflow_candidates_preserve_domain_facts(
    tmp_path,
    run_slug: str,
    fixture_path: str,
    expected_markers: tuple[str, ...],
) -> None:
    database = tmp_path / "workflow.sqlite3"
    run_id = f"public-{run_slug}"
    run_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "run",
            "--database",
            str(database),
            "--run-id",
            run_id,
            "--index-dir",
            str(tmp_path / "index"),
            fixture_path,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    run_payload = json.loads(run_result.stdout)
    assert run_result.returncode == 0
    assert run_payload["source_count"] == 1
    assert run_payload["chunk_count"] >= 10
    assert run_payload["finding_ids"] == []

    export_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "workflow_agent_studio.cli",
            "export",
            "--database",
            str(database),
            "--blueprint-version-id",
            str(run_payload["blueprint_version_id"]),
            "--export-dir",
            str(tmp_path / "exports"),
            "--output",
            f"{run_slug}.md",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    export_payload = json.loads(export_result.stdout)
    markdown = Path(export_payload["path"]).read_text(encoding="utf-8")

    assert export_result.returncode == 0
    assert "Support intake workflow routes customer requests" not in markdown
    for marker in expected_markers:
        assert marker in markdown


def test_public_source_workflow_candidate_catalog_keeps_boundaries() -> None:
    catalog = Path("docs/experiments/public_source_workflow_candidates.md").read_text(
        encoding="utf-8"
    )

    assert "public-source candidate catalog; not customer proof" in catalog
    assert "kubernetes_issue_triage.notes.md" in catalog
    assert "openstack_bug_triage.notes.md" in catalog
    assert "gitlab_incident_workflow.notes.md" in catalog
    assert "must not be counted in `docs/pilot_measurement.md`" in catalog
