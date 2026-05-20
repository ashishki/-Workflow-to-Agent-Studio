"""Blueprint review and approval workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass

from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.domain.review import ReviewFeedback, ReviewFeedbackCategory
from workflow_agent_studio.domain.workflow import EvidenceReference
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


@dataclass(frozen=True)
class ReviewComment:
    comment_id: str
    blueprint_version_id: int
    section: str
    reviewer_label: str
    comment_text: str
    evidence_reference: EvidenceReference | None = None


@dataclass(frozen=True)
class BlueprintDiffEntry:
    section: str
    previous: str
    current: str


@dataclass(frozen=True)
class BlueprintDiff:
    previous_version_id: int
    current_version_id: int
    entries: list[BlueprintDiffEntry]


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


def add_review_comment(
    *,
    run_id: str,
    blueprint_version_id: int,
    section: str,
    reviewer_label: str,
    comment_text: str,
    audit_events: AuditEventRepository,
    evidence_reference: EvidenceReference | None = None,
    commented_at: str | None = None,
) -> ReviewComment:
    comment = ReviewComment(
        comment_id=f"{run_id}:comment:{blueprint_version_id}:{section}",
        blueprint_version_id=blueprint_version_id,
        section=section,
        reviewer_label=reviewer_label,
        comment_text=comment_text,
        evidence_reference=evidence_reference,
    )
    payload = {
        "blueprint_version_id": blueprint_version_id,
        "section": section,
        "reviewer_label": reviewer_label,
    }
    if evidence_reference is not None:
        payload["evidence_reference"] = {
            "source_id": evidence_reference.source_id,
            "chunk_id": evidence_reference.chunk_id,
        }
    audit_events.add_event(
        event_id=comment.comment_id,
        run_id=run_id,
        event_type="review_comment_added",
        payload=payload,
        created_at=commented_at,
    )
    return comment


def record_review_feedback(
    *,
    run_id: str,
    blueprint_version_id: int,
    category: ReviewFeedbackCategory,
    section: str,
    reviewer_label: str,
    summary: str,
    audit_events: AuditEventRepository,
    evidence_reference: EvidenceReference | None = None,
    recorded_at: str | None = None,
) -> ReviewFeedback:
    feedback = ReviewFeedback(
        feedback_id=f"{run_id}:feedback:{blueprint_version_id}:{section}:{category}",
        blueprint_version_id=blueprint_version_id,
        category=category,
        section=section,
        reviewer_label=reviewer_label,
        summary=summary,
    )
    payload = {
        "blueprint_version_id": blueprint_version_id,
        "category": category,
        "section": section,
        "reviewer_label": reviewer_label,
    }
    if evidence_reference is not None:
        payload["evidence_reference"] = {
            "source_id": evidence_reference.source_id,
            "chunk_id": evidence_reference.chunk_id,
        }
    audit_events.add_event(
        event_id=feedback.feedback_id,
        run_id=run_id,
        event_type="review_feedback_recorded",
        payload=payload,
        created_at=recorded_at,
    )
    return feedback


def diff_blueprints(
    *,
    previous: AutomationBlueprint,
    current: AutomationBlueprint,
    previous_version_id: int,
    current_version_id: int,
) -> BlueprintDiff:
    entries: list[BlueprintDiffEntry] = []
    _append_if_changed(
        entries,
        section="workflow_summary",
        previous=previous.workflow_summary.text,
        current=current.workflow_summary.text,
    )
    _append_if_changed(
        entries,
        section="assumptions",
        previous=_assumption_signature(previous),
        current=_assumption_signature(current),
    )
    _append_if_changed(
        entries,
        section="findings",
        previous=_finding_signature(previous),
        current=_finding_signature(current),
    )
    _append_if_changed(
        entries,
        section="approval_boundaries",
        previous=_approval_boundary_signature(previous),
        current=_approval_boundary_signature(current),
    )
    return BlueprintDiff(
        previous_version_id=previous_version_id,
        current_version_id=current_version_id,
        entries=entries,
    )


def record_blueprint_diff(
    *,
    run_id: str,
    diff: BlueprintDiff,
    audit_events: AuditEventRepository,
    recorded_at: str | None = None,
) -> None:
    audit_events.add_event(
        event_id=f"{run_id}:blueprint_diff:{diff.previous_version_id}:{diff.current_version_id}",
        run_id=run_id,
        event_type="blueprint_diff_recorded",
        payload={
            "previous_version_id": diff.previous_version_id,
            "current_version_id": diff.current_version_id,
            "changed_sections": [entry.section for entry in diff.entries],
            "change_count": len(diff.entries),
        },
        created_at=recorded_at,
    )


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


def _append_if_changed(
    entries: list[BlueprintDiffEntry],
    *,
    section: str,
    previous: str,
    current: str,
) -> None:
    if previous != current:
        entries.append(BlueprintDiffEntry(section=section, previous=previous, current=current))


def _assumption_signature(blueprint: AutomationBlueprint) -> str:
    return json.dumps(
        [
            item.model_dump(mode="json")
            for item in blueprint.risks_and_assumptions
            if item.kind == "assumption"
        ],
        sort_keys=True,
    )


def _finding_signature(blueprint: AutomationBlueprint) -> str:
    validation = validate_blueprint_for_approval(blueprint)
    return json.dumps(
        [
            {
                "rule_id": finding.rule_id,
                "section": finding.section,
                "severity": finding.severity,
            }
            for finding in validation.findings
        ],
        sort_keys=True,
    )


def _approval_boundary_signature(blueprint: AutomationBlueprint) -> str:
    return json.dumps(
        [boundary.model_dump(mode="json") for boundary in blueprint.human_approval_boundaries],
        sort_keys=True,
    )
