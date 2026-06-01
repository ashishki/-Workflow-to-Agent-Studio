"""Approved roadmap implementation handoff export."""

from __future__ import annotations

from pathlib import Path

from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.export.markdown import ApprovedExportBlockedError
from workflow_agent_studio.export.paths import resolve_export_path
from workflow_agent_studio.roadmap.review import RoadmapReviewOutput
from workflow_agent_studio.validators import BlueprintValidationFinding


def export_approved_roadmap_handoff(
    *,
    report: RoadmapReport,
    review: RoadmapReviewOutput,
    export_dir: Path,
    output_path: Path,
) -> Path:
    blockers = _handoff_blockers(report=report, review=review)
    if blockers:
        raise ApprovedExportBlockedError(blockers)

    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_render_handoff(report=report, review=review), encoding="utf-8")
    return target


def _handoff_blockers(
    *,
    report: RoadmapReport,
    review: RoadmapReviewOutput,
) -> list[BlueprintValidationFinding]:
    findings: list[BlueprintValidationFinding] = []
    if review.report_id != report.report_id:
        findings.append(
            _finding(
                rule_id="ROADMAP-HANDOFF-REPORT-MISMATCH",
                section="review",
                message="Review output does not match the roadmap report.",
                repair_hint="Export the handoff with the review generated for this report.",
            )
        )
    if review.review_status != "approved":
        findings.append(
            _finding(
                rule_id="ROADMAP-HANDOFF-APPROVAL-REQUIRED",
                section="review",
                message="Approved roadmap handoff requires approved review output.",
                repair_hint="Approve the roadmap review checklist before handoff export.",
            )
        )
    for finding in review.blocking_findings:
        if finding.severity == "blocking":
            findings.append(
                _finding(
                    rule_id=finding.rule_id,
                    section=finding.section,
                    message=finding.message,
                    repair_hint=finding.repair_hint,
                )
            )
    for item in review.recommendation_reviews:
        if not item.accepted or not item.would_show_to_client:
            findings.append(
                _finding(
                    rule_id="ROADMAP-HANDOFF-RECOMMENDATION-NOT-ACCEPTED",
                    section=item.recommendation_id,
                    message="Recommendation review is not accepted for client handoff.",
                    repair_hint="Resolve required changes before exporting an approved handoff.",
                )
            )
    return findings


def _render_handoff(*, report: RoadmapReport, review: RoadmapReviewOutput) -> str:
    lines = [
        "# Roadmap Implementation Handoff",
        "",
        "Status: Approved",
        f"Report ID: {report.report_id}",
        f"Reviewer: {review.reviewer_label}",
        "",
        "## Implementation Tasks",
        *_implementation_tasks(report),
        "",
        "## Acceptance Criteria",
        *_bullet(report.evaluation_plan.acceptance_criteria),
        "",
        "## Eval Cases",
        *_bullet(report.evaluation_plan.golden_test_cases),
        "",
        "## Risks",
        *_risks(report),
        "",
        "## Owner",
        f"- {report.governance_plan.owner}",
        "",
        "## Privacy Mode",
        f"- {report.executive_summary.overall_privacy_mode_recommendation}",
        "",
        "## Human Gates",
        *_human_gates(report),
        "",
        "## Reviewer Checklist",
        *_reviewer_checklist(review),
        "",
        "## Local Boundary",
        "- Local Markdown artifact only. It does not deploy automation or mutate external systems.",
        "",
    ]
    return "\n".join(lines)


def _implementation_tasks(report: RoadmapReport) -> list[str]:
    lines: list[str] = []
    for index, card in enumerate(report.recommendations, start=1):
        lines.extend(
            [
                f"### TASK-{index}: {card.recommendation}",
                f"- Recommendation ID: {card.recommendation_id}",
                f"- Workflow Step: {card.target_workflow_step}",
                f"- Solution Type: {card.implementation_option}",
                f"- Owner: {report.governance_plan.owner}",
                f"- Acceptance Criteria: {', '.join(report.evaluation_plan.acceptance_criteria)}",
                f"- Eval Cases: {', '.join(report.evaluation_plan.golden_test_cases)}",
                f"- Privacy Mode: {report.executive_summary.overall_privacy_mode_recommendation}",
                f"- Human Gate: {card.human_gate.approval_event}",
                "",
            ]
        )
    return lines


def _risks(report: RoadmapReport) -> list[str]:
    risks: list[str] = []
    for card in report.recommendations:
        risks.extend(card.risks)
    risks.extend(report.do_not_automate_rationale)
    return _bullet(risks)


def _human_gates(report: RoadmapReport) -> list[str]:
    return _bullet(
        f"{card.recommendation_id}: {card.human_gate.reviewer} approves "
        f"{card.human_gate.approval_event}"
        for card in report.recommendations
    )


def _reviewer_checklist(review: RoadmapReviewOutput) -> list[str]:
    lines: list[str] = []
    for item in review.recommendation_reviews:
        lines.extend(
            [
                f"### {item.recommendation_id}",
                f"- Accepted: {item.accepted}",
                f"- Reason: {item.reason}",
                f"- Missing Evidence: {', '.join(item.missing_evidence) or 'none'}",
                f"- Cost Realism: {item.cost_realism}",
                f"- Privacy Concern: {item.privacy_concern or 'none'}",
                f"- Would Show To Client: {item.would_show_to_client}",
                f"- Required Changes: {', '.join(item.required_changes) or 'none'}",
                "",
            ]
        )
    return lines


def _finding(
    *,
    rule_id: str,
    section: str,
    message: str,
    repair_hint: str,
) -> BlueprintValidationFinding:
    return BlueprintValidationFinding(
        rule_id=rule_id,
        severity="blocking",
        section=section,
        message=message,
        repair_hint=repair_hint,
    )


def _bullet(items) -> list[str]:
    values = list(items)
    return [f"- {item}" for item in values] if values else ["- none"]
