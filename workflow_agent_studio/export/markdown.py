"""Markdown export for automation blueprints."""

from __future__ import annotations

import json
from pathlib import Path

from workflow_agent_studio.domain.blueprint import (
    AutomationBlueprint,
    AutomationCandidate,
    Claim,
    DataField,
    EvalCase,
    Integration,
    RiskOrAssumption,
)
from workflow_agent_studio.domain.workflow import EvidenceReference, WorkflowStep
from workflow_agent_studio.export.paths import resolve_export_path
from workflow_agent_studio.storage import BlueprintApprovalRecord, BlueprintVersionRecord
from workflow_agent_studio.validators import (
    BlueprintValidationFinding,
    validate_blueprint_for_approval,
)


class ApprovedExportBlockedError(Exception):
    def __init__(self, findings: list[BlueprintValidationFinding]) -> None:
        super().__init__("approved export blocked by validation findings")
        self.findings = findings


def export_draft_blueprint(
    *,
    blueprint: AutomationBlueprint,
    findings: list[BlueprintValidationFinding],
    export_dir: Path,
    output_path: Path,
    version: BlueprintVersionRecord | None = None,
) -> Path:
    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _render_blueprint(
            blueprint=blueprint,
            status="Draft",
            version=version,
            findings=findings,
            approval=None,
        ),
        encoding="utf-8",
    )
    return target


def export_approved_blueprint(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
    approval: BlueprintApprovalRecord,
    export_dir: Path,
    output_path: Path,
) -> Path:
    validation = validate_blueprint_for_approval(blueprint)
    if not validation.can_approve:
        raise ApprovedExportBlockedError(validation.findings)
    if approval.blueprint_version_id != version.blueprint_version_id:
        raise ApprovedExportBlockedError(
            [
                BlueprintValidationFinding(
                    rule_id="EXPORT-APPROVAL-VERSION-MISMATCH",
                    severity="blocking",
                    section="approval",
                    message="Approval record does not match the exported blueprint version.",
                    repair_hint="Export the approved version attached to the approval record.",
                )
            ]
        )
    mismatch = _version_mismatch_finding(blueprint=blueprint, version=version)
    if mismatch is not None:
        raise ApprovedExportBlockedError([mismatch])

    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _render_blueprint(
            blueprint=blueprint,
            status="Approved",
            version=version,
            findings=[],
            approval=approval,
        ),
        encoding="utf-8",
    )
    return target


def _version_mismatch_finding(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
) -> BlueprintValidationFinding | None:
    blueprint_json = json.dumps(blueprint.model_dump(mode="json"), sort_keys=True)
    if blueprint_json == version.blueprint_json:
        return None
    return BlueprintValidationFinding(
        rule_id="EXPORT-VERSION-MISMATCH",
        severity="blocking",
        section="blueprint_version",
        message="Export blueprint does not match the immutable approved version.",
        repair_hint="Export the exact approved version payload.",
    )


def _render_blueprint(
    *,
    blueprint: AutomationBlueprint,
    status: str,
    version: BlueprintVersionRecord | None,
    findings: list[BlueprintValidationFinding],
    approval: BlueprintApprovalRecord | None,
) -> str:
    lines = [
        "# Automation Blueprint",
        "",
        f"Status: {status}",
    ]
    if version is not None:
        lines.append(f"Blueprint Version ID: {version.blueprint_version_id}")
    if approval is not None:
        lines.extend(
            [
                f"Reviewer: {approval.reviewer_label}",
                f"Approved At: {approval.approved_at}",
            ]
        )
    lines.extend(
        [
            "",
            "## Workflow Summary",
            blueprint.workflow_summary.text,
            "",
            "## Actors",
            *_bullet(f"{actor.name}: {actor.role}" for actor in blueprint.actors),
            "",
            "## Systems",
            *_bullet(f"{system.name}: {system.purpose}" for system in blueprint.systems),
            "",
            "## Triggers",
            *_bullet_claims(blueprint.triggers),
            "",
            "## Current Workflow",
            *_bullet_steps(blueprint.current_workflow_steps),
            "",
            "## Decisions",
            *_bullet_claims(blueprint.decisions),
            "",
            "## Exceptions",
            *_bullet_claims(blueprint.exceptions),
            "",
            "## Data Fields",
            *_bullet_data_fields(blueprint.data_fields),
            "",
            "## Integration Map",
            *_bullet_integrations(blueprint.integration_map),
            "",
            "## Pain Points",
            *_bullet_claims(blueprint.pain_points),
            "",
            "## Automation Candidates",
            *_bullet_candidates(blueprint.automation_candidates),
            "",
            "## Human Approval Boundaries",
            *_bullet(
                f"{boundary.decision}: {boundary.approver} - {boundary.reason}"
                for boundary in blueprint.human_approval_boundaries
            ),
            "",
            "## Risks And Assumptions",
            *_bullet_risks(blueprint.risks_and_assumptions),
            "",
            "## Eval Cases",
            *_bullet_eval_cases(blueprint.eval_cases),
            "",
            "## Observability Needs",
            *_bullet_claims(blueprint.observability_needs),
            "",
            "## Rough Effort Band",
            blueprint.rough_effort_band,
            "",
            "## Next Implementation Tasks",
            *_bullet(
                f"{task.task_id}: {task.owner}; AC: {', '.join(task.acceptance_criteria)}; "
                f"Tests: {', '.join(task.tests_or_evals)}"
                for task in blueprint.next_implementation_tasks
            ),
            "",
        ]
    )
    if status == "Draft":
        lines.extend(["## Unresolved Findings", *_bullet_findings(findings), ""])
    lines.extend(["## Evidence Appendix", *_bullet_evidence(_collect_evidence(blueprint)), ""])
    return "\n".join(lines)


def _bullet(items) -> list[str]:
    values = list(items)
    return [f"- {item}" for item in values] if values else ["- none"]


def _bullet_claims(claims: list[Claim]) -> list[str]:
    return _bullet(f"{claim.text}{' (assumption)' if claim.assumption else ''}" for claim in claims)


def _bullet_steps(steps: list[WorkflowStep]) -> list[str]:
    return _bullet(f"{step.step_id}: {step.description} [{step.actor}]" for step in steps)


def _bullet_data_fields(fields: list[DataField]) -> list[str]:
    return _bullet(
        f"{field.name}: {field.description} (source: {field.source})" for field in fields
    )


def _bullet_integrations(integrations: list[Integration]) -> list[str]:
    return _bullet(
        f"{item.source_system} -> {item.target_system}: {', '.join(item.data_fields)}"
        for item in integrations
    )


def _bullet_candidates(candidates: list[AutomationCandidate]) -> list[str]:
    return _bullet(
        f"{candidate.name}: risk={candidate.risk_level}; "
        f"implementation boundary={candidate.implementation_boundary}; "
        f"approval boundary={candidate.human_approval_boundary}"
        for candidate in candidates
    )


def _bullet_risks(items: list[RiskOrAssumption]) -> list[str]:
    return _bullet(f"{item.kind}: {item.description}" for item in items)


def _bullet_eval_cases(eval_cases: list[EvalCase]) -> list[str]:
    return _bullet(
        f"{case.name}: when {case.input_condition}, expect {case.expected_behavior}; "
        f"verify by {case.verification_method}"
        for case in eval_cases
    )


def _bullet_findings(findings: list[BlueprintValidationFinding]) -> list[str]:
    return _bullet(
        f"{finding.severity} {finding.rule_id} [{finding.section}]: "
        f"{finding.message} Repair: {finding.repair_hint}"
        for finding in findings
    )


def _bullet_evidence(evidence: list[EvidenceReference]) -> list[str]:
    return _bullet(
        f"{item.source_id} / {item.chunk_id}{f': {item.quote}' if item.quote else ''}"
        for item in evidence
    )


def _collect_evidence(blueprint: AutomationBlueprint) -> list[EvidenceReference]:
    evidence: list[EvidenceReference] = []
    claims = [
        blueprint.workflow_summary,
        *blueprint.triggers,
        *blueprint.decisions,
        *blueprint.exceptions,
        *blueprint.pain_points,
        *blueprint.observability_needs,
    ]
    for claim in claims:
        evidence.extend(claim.evidence_references)
    for step in blueprint.current_workflow_steps:
        evidence.extend(step.evidence_references)
    for candidate in blueprint.automation_candidates:
        evidence.extend(candidate.evidence_references)
    for item in blueprint.risks_and_assumptions:
        evidence.extend(item.evidence_references)
    for case in blueprint.eval_cases:
        evidence.append(case.evidence_reference)
    deduped: dict[tuple[str, str], EvidenceReference] = {}
    for item in evidence:
        deduped[(item.source_id, item.chunk_id)] = item
    return list(deduped.values())
