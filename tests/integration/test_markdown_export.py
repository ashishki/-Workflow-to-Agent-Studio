import json
from pathlib import Path

import pytest

from workflow_agent_studio.blueprint.review import approve_blueprint
from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.export import (
    ApprovedExportBlockedError,
    export_approved_blueprint,
    export_draft_blueprint,
)
from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintApprovalRepository,
    BlueprintVersionRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)
from workflow_agent_studio.validators import BlueprintValidationFinding


def _valid_blueprint() -> AutomationBlueprint:
    data = json.loads(
        Path("tests/fixtures/blueprints/minimal_valid.json").read_text(encoding="utf-8")
    )
    return AutomationBlueprint.model_validate(data)


def test_draft_export_includes_status_and_findings(tmp_path) -> None:
    blueprint = _valid_blueprint()
    finding = BlueprintValidationFinding(
        rule_id="PLAN-REQUIRED-SECTION",
        severity="blocking",
        section="eval_cases",
        message="Eval cases are required.",
        repair_hint="Add at least one eval case.",
    )

    output = export_draft_blueprint(
        blueprint=blueprint,
        findings=[finding],
        export_dir=tmp_path,
        output_path=Path("draft.md"),
    )

    markdown = output.read_text(encoding="utf-8")
    assert "Status: Draft" in markdown
    assert "## Unresolved Findings" in markdown
    assert "PLAN-REQUIRED-SECTION" in markdown


def test_approved_export_includes_version_and_evidence_appendix(tmp_path) -> None:
    database = connect_database(tmp_path / "workflow_studio.sqlite3")
    initialize_database(database)
    try:
        WorkflowRunRepository(database).create_run("run-1")
        blueprint = _valid_blueprint()
        version = BlueprintVersionRepository(database).add_version(
            run_id="run-1",
            blueprint=blueprint.model_dump(mode="json"),
        )
        approved = approve_blueprint(
            blueprint=blueprint,
            version=version,
            reviewer_label="operator",
            approvals=BlueprintApprovalRepository(database),
            audit_events=AuditEventRepository(database),
            approved_at="2026-05-19T00:00:00+00:00",
        )

        output = export_approved_blueprint(
            blueprint=blueprint,
            version=version,
            approval=approved.approval,
            export_dir=tmp_path / "exports",
            output_path=Path("approved.md"),
        )
    finally:
        database.close()

    markdown = output.read_text(encoding="utf-8")
    assert "Status: Approved" in markdown
    assert f"Blueprint Version ID: {version.blueprint_version_id}" in markdown
    assert "## Evidence Appendix" in markdown
    assert "src-1 / chk-1" in markdown


def test_approved_export_rejects_version_payload_mismatch(tmp_path) -> None:
    database = connect_database(tmp_path / "workflow_studio.sqlite3")
    initialize_database(database)
    try:
        WorkflowRunRepository(database).create_run("run-1")
        blueprint = _valid_blueprint()
        version = BlueprintVersionRepository(database).add_version(
            run_id="run-1",
            blueprint=blueprint.model_dump(mode="json"),
        )
        approved = approve_blueprint(
            blueprint=blueprint,
            version=version,
            reviewer_label="operator",
            approvals=BlueprintApprovalRepository(database),
            audit_events=AuditEventRepository(database),
            approved_at="2026-05-19T00:00:00+00:00",
        )
        edited_blueprint = blueprint.model_copy(update={"rough_effort_band": "medium"})

        with pytest.raises(ApprovedExportBlockedError) as error:
            export_approved_blueprint(
                blueprint=edited_blueprint,
                version=version,
                approval=approved.approval,
                export_dir=tmp_path / "exports",
                output_path=Path("approved.md"),
            )
    finally:
        database.close()

    assert any(finding.rule_id == "EXPORT-VERSION-MISMATCH" for finding in error.value.findings)
    assert not (tmp_path / "exports" / "approved.md").exists()
