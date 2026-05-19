"""Blueprint review and approval workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintApprovalRecord,
    BlueprintApprovalRepository,
    BlueprintVersionRecord,
    BlueprintVersionRepository,
)
from workflow_agent_studio.validators import (
    BlueprintValidationFinding,
    validate_blueprint_for_approval,
)


class ApprovalBlockedError(Exception):
    def __init__(self, findings: list[BlueprintValidationFinding]) -> None:
        super().__init__("approval blocked by validation findings")
        self.findings = findings


@dataclass(frozen=True)
class ApprovedBlueprint:
    approval: BlueprintApprovalRecord
    version: BlueprintVersionRecord


def edit_blueprint(
    *,
    run_id: str,
    blueprint: AutomationBlueprint,
    editor_label: str,
    versions: BlueprintVersionRepository,
    audit_events: AuditEventRepository,
    edited_at: str | None = None,
) -> BlueprintVersionRecord:
    version = versions.add_version(
        run_id=run_id,
        blueprint=blueprint.model_dump(mode="json"),
        created_at=edited_at,
    )
    audit_events.add_event(
        event_id=f"{run_id}:blueprint_edited:{version.blueprint_version_id}",
        run_id=run_id,
        event_type="blueprint_edited",
        payload={
            "blueprint_version_id": version.blueprint_version_id,
            "version_number": version.version_number,
            "editor_label": editor_label,
        },
        created_at=edited_at,
    )
    return version


def approve_blueprint(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
    reviewer_label: str,
    approvals: BlueprintApprovalRepository,
    audit_events: AuditEventRepository,
    approved_at: str | None = None,
) -> ApprovedBlueprint:
    mismatch = _version_mismatch_finding(blueprint=blueprint, version=version)
    if mismatch is not None:
        raise ApprovalBlockedError([mismatch])

    validation = validate_blueprint_for_approval(blueprint)
    if not validation.can_approve:
        raise ApprovalBlockedError(validation.findings)

    approval = approvals.approve(
        blueprint_version_id=version.blueprint_version_id,
        run_id=version.run_id,
        reviewer_label=reviewer_label,
        approved_at=approved_at,
    )
    audit_events.add_event(
        event_id=f"{version.run_id}:blueprint_approved:{version.blueprint_version_id}",
        run_id=version.run_id,
        event_type="blueprint_approved",
        payload={
            "blueprint_version_id": version.blueprint_version_id,
            "version_number": version.version_number,
            "reviewer_label": reviewer_label,
            "approved_at": approval.approved_at,
            "status": approval.status,
        },
        created_at=approval.approved_at,
    )
    return ApprovedBlueprint(approval=approval, version=version)


def _version_mismatch_finding(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
) -> BlueprintValidationFinding | None:
    blueprint_json = json.dumps(blueprint.model_dump(mode="json"), sort_keys=True)
    if blueprint_json == version.blueprint_json:
        return None
    return BlueprintValidationFinding(
        rule_id="PLAN-VERSION-MISMATCH",
        severity="blocking",
        section="blueprint_version",
        message="Approval blueprint does not match the immutable stored version.",
        repair_hint="Load the exact stored version payload before approval.",
    )
