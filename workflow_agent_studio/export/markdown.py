"""Markdown export for automation blueprints."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import ValidationError

from workflow_agent_studio.blueprint.design_candidates import DesignCandidatePortfolio
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
from workflow_agent_studio.proof import build_blueprint_proof_receipt
from workflow_agent_studio.storage import BlueprintApprovalRecord, BlueprintVersionRecord
from workflow_agent_studio.validators import (
    AutomationReadinessResult,
    BlueprintValidationFinding,
    compute_automation_readiness,
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
    receipt_path = _proof_receipt_path(target)
    payload = _render_blueprint(
        blueprint=blueprint,
        status="Approved",
        version=version,
        findings=[],
        approval=approval,
        proof_receipt_ref=str(receipt_path),
    )
    proof_findings = _proof_receipt_blockers(
        blueprint=blueprint,
        artifact=target,
        artifact_payload=payload,
        rule_prefix="EXPORT",
    )
    if proof_findings:
        raise ApprovedExportBlockedError(proof_findings)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload, encoding="utf-8")
    _write_proof_receipt(blueprint=blueprint, artifact=target, artifact_payload=payload)
    return target


def export_approved_handoff(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
    approval: BlueprintApprovalRecord | None,
    export_dir: Path,
    output_path: Path,
) -> Path:
    findings = _approved_handoff_blockers(
        blueprint=blueprint,
        version=version,
        approval=approval,
    )
    if findings:
        raise ApprovedExportBlockedError(findings)

    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    receipt_path = _proof_receipt_path(target)
    payload = _render_approved_handoff(
        blueprint=blueprint,
        version=version,
        approval=approval,
        proof_receipt_ref=str(receipt_path),
    )
    proof_findings = _proof_receipt_blockers(
        blueprint=blueprint,
        artifact=target,
        artifact_payload=payload,
        rule_prefix="HANDOFF",
    )
    if proof_findings:
        raise ApprovedExportBlockedError(proof_findings)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload, encoding="utf-8")
    _write_proof_receipt(blueprint=blueprint, artifact=target, artifact_payload=payload)
    return target


def export_governance_report(
    *,
    blueprint: AutomationBlueprint,
    export_dir: Path,
    output_path: Path,
    version: BlueprintVersionRecord | None = None,
    approval: BlueprintApprovalRecord | None = None,
) -> Path:
    validation = validate_blueprint_for_approval(blueprint)
    if approval is not None and not validation.can_approve:
        raise ApprovedExportBlockedError(validation.findings)
    if approval is not None and version is not None:
        if approval.blueprint_version_id != version.blueprint_version_id:
            raise ApprovedExportBlockedError(
                [
                    BlueprintValidationFinding(
                        rule_id="EXPORT-APPROVAL-VERSION-MISMATCH",
                        severity="blocking",
                        section="approval",
                        message="Approval record does not match the governance report version.",
                        repair_hint="Export the approved version attached to the approval record.",
                    )
                ]
            )
        mismatch = _version_mismatch_finding(blueprint=blueprint, version=version)
        if mismatch is not None:
            raise ApprovedExportBlockedError([mismatch])

    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    receipt_path = _proof_receipt_path(target) if approval is not None else None
    payload = _render_governance_report(
        blueprint=blueprint,
        readiness=compute_automation_readiness(blueprint, validation=validation),
        findings=validation.findings,
        version=version,
        approval=approval,
        proof_receipt_ref=str(receipt_path) if receipt_path is not None else None,
    )
    if approval is not None:
        proof_findings = _proof_receipt_blockers(
            blueprint=blueprint,
            artifact=target,
            artifact_payload=payload,
            rule_prefix="GOVERNANCE",
        )
        if proof_findings:
            raise ApprovedExportBlockedError(proof_findings)

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload, encoding="utf-8")
    if approval is not None:
        _write_proof_receipt(blueprint=blueprint, artifact=target, artifact_payload=payload)
    return target


def export_design_candidate_portfolio(
    *,
    portfolio: DesignCandidatePortfolio,
    export_dir: Path,
    output_path: Path,
) -> Path:
    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_render_design_candidate_portfolio(portfolio), encoding="utf-8")
    return target


def _approved_handoff_blockers(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
    approval: BlueprintApprovalRecord | None,
) -> list[BlueprintValidationFinding]:
    if approval is None or approval.status != "approved":
        return [
            BlueprintValidationFinding(
                rule_id="HANDOFF-APPROVAL-REQUIRED",
                severity="blocking",
                section="approval",
                message="Approved handoff export requires an approved blueprint record.",
                repair_hint="Approve the exact blueprint version before exporting a handoff.",
            )
        ]

    validation = validate_blueprint_for_approval(blueprint)
    if not validation.can_approve:
        return validation.findings
    if approval.blueprint_version_id != version.blueprint_version_id:
        return [
            BlueprintValidationFinding(
                rule_id="HANDOFF-APPROVAL-VERSION-MISMATCH",
                severity="blocking",
                section="approval",
                message="Approval record does not match the handoff blueprint version.",
                repair_hint="Export the approved version attached to the approval record.",
            )
        ]
    mismatch = _version_mismatch_finding(blueprint=blueprint, version=version)
    return [mismatch] if mismatch is not None else []


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


def _proof_receipt_path(artifact: Path) -> Path:
    return artifact.with_name(f"{artifact.name}.proof_receipt.json")


def _write_proof_receipt(
    *,
    blueprint: AutomationBlueprint,
    artifact: Path,
    artifact_payload: str,
) -> Path:
    receipt_path = _proof_receipt_path(artifact)
    receipt = build_blueprint_proof_receipt(
        blueprint=blueprint,
        artifact_ref=artifact,
        artifact_payload=artifact_payload,
    )
    receipt_path.write_text(
        f"{receipt.model_dump_json(exclude_none=True, indent=2)}\n",
        encoding="utf-8",
    )
    return receipt_path


def _proof_receipt_blockers(
    *,
    blueprint: AutomationBlueprint,
    artifact: Path,
    artifact_payload: str,
    rule_prefix: str,
) -> list[BlueprintValidationFinding]:
    try:
        receipt = build_blueprint_proof_receipt(
            blueprint=blueprint,
            artifact_ref=artifact,
            artifact_payload=artifact_payload,
        )
    except ValidationError as exc:
        return [
            BlueprintValidationFinding(
                rule_id=f"{rule_prefix}-PROOF-RECEIPT",
                severity="blocking",
                section="proof_receipt",
                message="Proof receipt could not be generated for the exported artifact.",
                repair_hint=str(exc),
            )
        ]
    if receipt.verifier_status == "passed":
        return []
    return [
        BlueprintValidationFinding(
            rule_id=f"{rule_prefix}-PROOF-RECEIPT",
            severity="blocking",
            section="proof_receipt",
            message="Proof receipt did not pass verification for the exported artifact.",
            repair_hint="Add evidence references and resolve verifier notes before export.",
        )
    ]


def _render_blueprint(
    *,
    blueprint: AutomationBlueprint,
    status: str,
    version: BlueprintVersionRecord | None,
    findings: list[BlueprintValidationFinding],
    approval: BlueprintApprovalRecord | None,
    proof_receipt_ref: str | None = None,
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
    if proof_receipt_ref is not None:
        lines.extend(["## Blueprint Proof Receipt", f"- Receipt Artifact: {proof_receipt_ref}", ""])
    if status == "Draft":
        lines.extend(["## Unresolved Findings", *_bullet_findings(findings), ""])
    lines.extend(["## Evidence Appendix", *_bullet_evidence(_collect_evidence(blueprint)), ""])
    return "\n".join(lines)


def _render_approved_handoff(
    *,
    blueprint: AutomationBlueprint,
    version: BlueprintVersionRecord,
    approval: BlueprintApprovalRecord | None,
    proof_receipt_ref: str | None = None,
) -> str:
    lines = [
        "# Implementation Handoff",
        "",
        "Status: Approved",
        f"Blueprint Version ID: {version.blueprint_version_id}",
        f"Reviewer: {approval.reviewer_label if approval else 'unknown'}",
        f"Approved At: {approval.approved_at if approval else 'unknown'}",
        "",
        "## Implementation Tasks",
        *_bullet(
            f"{task.task_id}: owner={task.owner}; "
            f"depends_on={', '.join(task.depends_on) or 'none'}; "
            f"AC: {', '.join(task.acceptance_criteria)}; Tests: {', '.join(task.tests_or_evals)}"
            for task in blueprint.next_implementation_tasks
        ),
        "",
        "## Eval Cases",
        *_bullet_eval_cases(blueprint.eval_cases),
        "",
        "## Automation Boundaries",
        *_bullet_candidates(blueprint.automation_candidates),
        "",
        "## Human Approval Boundaries",
        *_bullet(
            f"{boundary.decision}: {boundary.approver} - {boundary.reason}"
            for boundary in blueprint.human_approval_boundaries
        ),
        "",
        "## Assumptions",
        *_bullet(
            item.description
            for item in blueprint.risks_and_assumptions
            if item.kind == "assumption"
        ),
        "",
        "## Risks",
        *_bullet(
            item.description for item in blueprint.risks_and_assumptions if item.kind == "risk"
        ),
        "",
        "## External Side Effects",
        "- Disabled. This handoff is a local Markdown artifact only.",
        "",
        "## Blueprint Proof Receipt",
        f"- Receipt Artifact: {proof_receipt_ref or 'not generated'}",
        "",
        "## Evidence Appendix",
        *_bullet_evidence(_collect_evidence(blueprint)),
        "",
    ]
    return "\n".join(lines)


def _render_design_candidate_portfolio(portfolio: DesignCandidatePortfolio) -> str:
    lines = [
        "# Design Candidate Portfolio",
        "",
        "Status: Draft",
        "",
        "## Candidates",
    ]
    for draft in portfolio.candidates:
        candidate = draft.candidate
        lines.extend(
            [
                f"### {candidate.name}",
                f"Status: {draft.status}",
                f"Variant: {candidate.variant}",
                f"Autonomy: {candidate.autonomy_level}",
                f"Runtime Tier: {candidate.runtime_tier}",
                f"Cost Posture: {candidate.cost_posture}",
                "",
                "Approvals:",
                *_bullet(
                    f"{approval.decision}: {approval.approver} - {approval.reason}"
                    for approval in candidate.human_approvals
                ),
                "",
                "Eval Needs:",
                *_bullet(
                    f"{item.name}: expect {item.expected_behavior}; verify by "
                    f"{item.verification_method}"
                    for item in candidate.eval_needs
                ),
                "",
                "Assumptions:",
                *_bullet(item.description for item in draft.assumptions),
                "",
            ]
        )
    lines.extend(
        [
            "## Tradeoff Comparison",
            *_bullet(
                f"{item.variant}: autonomy={item.autonomy_level}; "
                f"runtime={item.runtime_tier}; cost={item.cost_posture}; "
                f"approvals={item.approval_count}; evals={item.eval_count}; "
                f"risks={item.risk_count}; evidence_gaps={item.evidence_gap_count}"
                for item in portfolio.tradeoff_comparison
            ),
            "",
            "## Consolidated Blueprint",
            portfolio.consolidated_blueprint.workflow_summary.text,
            "",
        ]
    )
    return "\n".join(lines)


def _render_governance_report(
    *,
    blueprint: AutomationBlueprint,
    readiness: AutomationReadinessResult,
    findings: list[BlueprintValidationFinding],
    version: BlueprintVersionRecord | None,
    approval: BlueprintApprovalRecord | None,
    proof_receipt_ref: str | None = None,
) -> str:
    evidence = _collect_evidence(blueprint)
    lines = [
        "# Governance Report",
        "",
        f"Status: {'Approved' if approval else 'Draft'}",
    ]
    if version is not None:
        lines.append(f"Blueprint Version ID: {version.blueprint_version_id}")
    if approval is not None:
        lines.extend(
            [f"Reviewer: {approval.reviewer_label}", f"Approved At: {approval.approved_at}"]
        )
    lines.extend(
        [
            "",
            "## Readiness Result",
            f"Status: {readiness.status}",
            f"Score: {readiness.score}",
            "",
            "## Evidence Coverage",
            f"Evidence references: {len(evidence)}",
            *_bullet_evidence(evidence),
            "",
            "## Assumptions And Next Questions",
            *_bullet(readiness.next_questions),
            "",
            "## Approval Boundaries",
            *_bullet(
                f"{boundary.decision}: {boundary.approver} - {boundary.reason}"
                for boundary in blueprint.human_approval_boundaries
            ),
            "",
            "## Risks",
            *_bullet(readiness.risks),
            "",
            "## Unresolved Findings",
            *_bullet_findings(findings),
            "",
        ]
    )
    if proof_receipt_ref is not None:
        lines.extend(["## Blueprint Proof Receipt", f"- Receipt Artifact: {proof_receipt_ref}", ""])
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
