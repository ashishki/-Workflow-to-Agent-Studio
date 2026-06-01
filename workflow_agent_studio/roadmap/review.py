"""Roadmap reviewer checklist generation."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from workflow_agent_studio.domain.blueprint import StrictModel
from workflow_agent_studio.domain.roadmap import RoadmapReport
from workflow_agent_studio.domain.verification import ReviewStatus

CostRealism = Literal["low", "medium", "high"]


class RoadmapReviewFinding(StrictModel):
    rule_id: str = Field(min_length=1)
    severity: Literal["blocking", "warning"]
    section: str = Field(min_length=1)
    message: str = Field(min_length=1)
    repair_hint: str = Field(min_length=1)


class RecommendationReviewOutput(StrictModel):
    recommendation_id: str = Field(min_length=1)
    accepted: bool
    reason: str = Field(min_length=1)
    missing_evidence: list[str] = Field(default_factory=list)
    cost_realism: CostRealism
    privacy_concern: str = Field(default="")
    would_show_to_client: bool
    required_changes: list[str] = Field(default_factory=list)


class RoadmapReviewOutput(StrictModel):
    report_id: str = Field(min_length=1)
    reviewer_label: str = Field(min_length=1)
    review_status: ReviewStatus
    recommendation_reviews: list[RecommendationReviewOutput] = Field(min_length=1)
    blocking_findings: list[RoadmapReviewFinding] = Field(default_factory=list)


def build_roadmap_reviewer_output(
    report: RoadmapReport,
    *,
    reviewer_label: str,
    approve: bool = False,
) -> RoadmapReviewOutput:
    findings = _blocking_findings(report)
    recommendation_reviews = [
        _review_recommendation(report=report, recommendation_id=card.recommendation_id)
        for card in report.recommendations
    ]
    if approve and not findings and all(item.accepted for item in recommendation_reviews):
        status: ReviewStatus = "approved"
    elif findings:
        status = "blocked"
    else:
        status = "needs_human_review"
    return RoadmapReviewOutput(
        report_id=report.report_id,
        reviewer_label=reviewer_label,
        review_status=status,
        recommendation_reviews=recommendation_reviews,
        blocking_findings=findings,
    )


def _review_recommendation(
    *,
    report: RoadmapReport,
    recommendation_id: str,
) -> RecommendationReviewOutput:
    card = next(
        card for card in report.recommendations if card.recommendation_id == recommendation_id
    )
    missing_evidence = [] if card.evidence else ["recommendation evidence reference"]
    required_changes = []
    if not card.human_gate.required:
        required_changes.append("add human approval gate")
    if missing_evidence and not card.assumptions:
        required_changes.append("add evidence or explicit assumptions")
    accepted = not required_changes
    return RecommendationReviewOutput(
        recommendation_id=card.recommendation_id,
        accepted=accepted,
        reason="Recommendation is traceable and bounded for a reviewed implementation handoff."
        if accepted
        else "Recommendation needs reviewer changes before handoff.",
        missing_evidence=missing_evidence,
        cost_realism=card.confidence_level,
        privacy_concern=_privacy_concern(report=report, privacy_class=card.privacy_class),
        would_show_to_client=accepted,
        required_changes=required_changes,
    )


def _blocking_findings(report: RoadmapReport) -> list[RoadmapReviewFinding]:
    findings: list[RoadmapReviewFinding] = []
    if report.verification_appendix.receipt.blocking_finding_count:
        findings.append(
            RoadmapReviewFinding(
                rule_id="ROADMAP-REVIEW-BLOCKING-FINDINGS",
                severity="blocking",
                section="verification_appendix",
                message="Roadmap receipt contains unresolved blocking findings.",
                repair_hint="Resolve blocking findings before approving handoff export.",
            )
        )
    for card in report.recommendations:
        if not card.evidence and not card.assumptions:
            findings.append(
                RoadmapReviewFinding(
                    rule_id="ROADMAP-REVIEW-EVIDENCE-OR-ASSUMPTION",
                    severity="blocking",
                    section=card.recommendation_id,
                    message="Recommendation lacks evidence and assumptions.",
                    repair_hint="Add evidence references or explicit assumptions.",
                )
            )
        if not card.human_gate.required:
            findings.append(
                RoadmapReviewFinding(
                    rule_id="ROADMAP-REVIEW-HUMAN-GATE",
                    severity="blocking",
                    section=card.recommendation_id,
                    message="Recommendation lacks a required human approval gate.",
                    repair_hint="Add a human gate before approving handoff export.",
                )
            )
    return findings


def _privacy_concern(*, report: RoadmapReport, privacy_class: str) -> str:
    if privacy_class in {"restricted", "sensitive"}:
        return report.executive_summary.overall_privacy_mode_recommendation
    return ""
