"""AI Workflow Playbook-compatible local export."""

from __future__ import annotations

from pathlib import Path

from workflow_agent_studio.blueprint import DesignCandidateDraft
from workflow_agent_studio.domain.design_candidate import AgentDesignCandidate
from workflow_agent_studio.domain.workflow import EvidenceReference
from workflow_agent_studio.export.markdown import ApprovedExportBlockedError
from workflow_agent_studio.export.paths import resolve_export_path
from workflow_agent_studio.validators import BlueprintValidationFinding


def export_playbook_artifacts(
    *,
    design: DesignCandidateDraft,
    export_dir: Path,
    output_path: Path,
    approved_by: str,
    approved_at: str,
) -> Path:
    blockers = _approval_blockers(design)
    if blockers:
        raise ApprovedExportBlockedError(blockers)

    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _render_playbook_artifacts(
            candidate=design.candidate,
            approved_by=approved_by,
            approved_at=approved_at,
        ),
        encoding="utf-8",
    )
    return target


def _approval_blockers(design: DesignCandidateDraft) -> list[BlueprintValidationFinding]:
    if design.status == "ready":
        return []
    return [
        BlueprintValidationFinding(
            rule_id="PLAYBOOK-DESIGN-APPROVAL-REQUIRED",
            severity="blocking",
            section="design_candidate",
            message="Playbook export requires a ready, human-approved design candidate.",
            repair_hint="Resolve evidence gaps and approval findings before exporting.",
        )
    ]


def _render_playbook_artifacts(
    *,
    candidate: AgentDesignCandidate,
    approved_by: str,
    approved_at: str,
) -> str:
    evidence = _evidence_context_refs(candidate.evidence_references)
    lines = [
        "# AI Workflow Playbook Artifact Export",
        "",
        "Status: Approved Local Draft",
        "Authority: Convenience artifact only. Canonical authority remains the reviewed "
        "workflow evidence, implementation contract, ADRs, and approved blueprint.",
        f"Approved By: {approved_by}",
        f"Approved At: {approved_at}",
        "",
        "## Runtime Tier",
        f"- {candidate.runtime_tier}: selected for `{candidate.variant}` with "
        f"{candidate.autonomy_level} autonomy.",
        "",
        "## Tool Permission Boundaries",
        *_tool_boundaries(candidate),
        "",
        "## Human Approval Points",
        *_approval_points(candidate),
        "",
        "## Implementation Contract Deltas",
        "- Preserve deterministic validation for approval, evidence, eval, and export gates.",
        "- Keep exports local Markdown artifacts unless an ADR approves external side effects.",
        "- Treat generated Playbook tasks as convenience, not source of truth.",
        "",
        "## Eval Artifact Skeletons",
        *_eval_skeletons(candidate, evidence),
        "",
        "## Task Blocks",
        *_task_blocks(candidate, evidence),
        "",
    ]
    return "\n".join(lines)


def _tool_boundaries(candidate: AgentDesignCandidate) -> list[str]:
    return [
        f"- `{tool.name}`: {tool.permission_boundary}; Context-Refs: "
        f"{_format_context_refs(tool.evidence_references or candidate.evidence_references)}"
        for tool in candidate.required_tools
    ] or ["- none"]


def _approval_points(candidate: AgentDesignCandidate) -> list[str]:
    return [
        f"- {approval.decision}: approver={approval.approver}; reason={approval.reason}"
        for approval in candidate.human_approvals
    ]


def _eval_skeletons(candidate: AgentDesignCandidate, fallback_refs: list[str]) -> list[str]:
    skeletons: list[str] = []
    for index, eval_need in enumerate(candidate.eval_needs, start=1):
        refs = _format_context_refs(eval_need.evidence_references) or ", ".join(fallback_refs)
        skeletons.extend(
            [
                f"### EVAL-{index}",
                f"- Name: {eval_need.name}",
                f"- Expected Behavior: {eval_need.expected_behavior}",
                f"- Verification: {eval_need.verification_method}",
                f"- Context-Refs: {refs}",
                "",
            ]
        )
    return skeletons or ["- none"]


def _task_blocks(candidate: AgentDesignCandidate, fallback_refs: list[str]) -> list[str]:
    refs = ", ".join(fallback_refs)
    return [
        "### TASK-1: Implement Design Boundary",
        f"- Variant: {candidate.variant}",
        f"- Runtime Tier: {candidate.runtime_tier}",
        "- Acceptance Criteria: tool permissions and human approvals are enforced.",
        "- Tests/Evals: unit validator test and integration export test.",
        f"- Context-Refs: {refs}",
        "",
        "### TASK-2: Add Eval Gate",
        "- Acceptance Criteria: candidate eval skeletons run before approval.",
        "- Tests/Evals: eval artifact fixture covers expected behavior and verification.",
        f"- Context-Refs: {refs}",
    ]


def _evidence_context_refs(evidence: list[EvidenceReference]) -> list[str]:
    return [_format_context_ref(item) for item in evidence]


def _format_context_refs(evidence: list[EvidenceReference]) -> str:
    return ", ".join(_evidence_context_refs(evidence))


def _format_context_ref(evidence: EvidenceReference) -> str:
    return f"{evidence.source_id}#{evidence.chunk_id}"
