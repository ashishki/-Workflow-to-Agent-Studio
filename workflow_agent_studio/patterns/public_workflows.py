"""Public workflow blueprint profile registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

WorkflowKind = Literal[
    "support_intake",
    "issue_triage",
    "kubernetes_issue_triage",
    "bug_triage",
    "incident_response",
]


@dataclass(frozen=True)
class BlueprintProfile:
    kind: WorkflowKind
    summary: str
    primary_risk: str
    automation_candidate_name: str
    implementation_boundary: str
    human_approval_boundary: str
    risk_level: Literal["low", "medium", "high"]
    approval_decision: str
    approval_actor_terms: tuple[str, ...]
    approval_reason: str
    eval_case_name: str
    eval_input_condition: str
    eval_expected_behavior: str
    observability_need: str
    implementation_acceptance_criteria: str


SUPPORT_INTAKE_PROFILE = BlueprintProfile(
    kind="support_intake",
    summary="Support intake workflow routes customer requests to follow-up tasks.",
    primary_risk="Missing request details can block automation.",
    automation_candidate_name="Draft follow-up task",
    implementation_boundary="Draft task only; do not create external commitments.",
    human_approval_boundary="Operator approves before task creation.",
    risk_level="medium",
    approval_decision="Approve follow-up task",
    approval_actor_terms=("operator",),
    approval_reason="Task creation changes team expectations.",
    eval_case_name="Follow-up task candidate",
    eval_input_condition="Request includes enough details for engineering review.",
    eval_expected_behavior="Blueprint recommends a draft follow-up task.",
    observability_need="Track generated draft task count and validation failures.",
    implementation_acceptance_criteria=("Draft task candidate is generated from source evidence."),
)

ISSUE_TRIAGE_PROFILE = BlueprintProfile(
    kind="issue_triage",
    summary=(
        "GitHub Issues triage workflow routes public issue submissions through "
        "template checks, duplicate and scope review, reproducibility checks, "
        "stale handling, and engineering ownership decisions."
    ),
    primary_risk=(
        "Missing issue details can lead to incorrect closure or delayed engineering review."
    ),
    automation_candidate_name="Draft issue triage recommendation",
    implementation_boundary=(
        "Draft triage recommendation only; do not close, label, or route issues automatically."
    ),
    human_approval_boundary=(
        "Maintainer approves before issue status, labels, closure, or engineering routing change."
    ),
    risk_level="high",
    approval_decision="Approve issue triage recommendation",
    approval_actor_terms=("maintainer",),
    approval_reason="Triage changes can close public issues or create engineering commitments.",
    eval_case_name="Issue triage recommendation",
    eval_input_condition=(
        "Issue includes template fields, version, reproduction details, and scope context."
    ),
    eval_expected_behavior=(
        "Blueprint recommends a maintainer-reviewed triage action without mutating "
        "GitHub issue state automatically."
    ),
    observability_need=(
        "Track draft triage recommendations, maintainer overrides, stale decisions, "
        "and blocked cases."
    ),
    implementation_acceptance_criteria=(
        "Draft triage recommendation is generated from source evidence."
    ),
)

KUBERNETES_ISSUE_TRIAGE_PROFILE = BlueprintProfile(
    kind="kubernetes_issue_triage",
    summary=(
        "Kubernetes issue triage workflow routes GitHub issues through labels, "
        "SIG ownership, needs-information, priority, stale handling, and contributor "
        "follow-up."
    ),
    primary_risk="Incorrect labels or SIG ownership can delay contributor response.",
    automation_candidate_name="Draft Kubernetes issue triage recommendation",
    implementation_boundary=(
        "Draft Kubernetes triage recommendation only; do not apply labels, bot "
        "commands, assignment, stale state, or closure automatically."
    ),
    human_approval_boundary=(
        "SIG owner or authorized triager approves before label, priority, assignment, "
        "stale, or closure changes."
    ),
    risk_level="high",
    approval_decision="Approve Kubernetes issue triage recommendation",
    approval_actor_terms=("sig",),
    approval_reason="Triage changes can affect public issue ownership, priority, and closure.",
    eval_case_name="Kubernetes issue triage recommendation",
    eval_input_condition=(
        "Issue includes kind, labels, reporter context, reproduction details, "
        "and SIG ownership signals."
    ),
    eval_expected_behavior=(
        "Blueprint recommends an authorized triager-reviewed label, SIG, priority, "
        "or follow-up action without mutating GitHub state."
    ),
    observability_need=(
        "Track draft Kubernetes triage recommendations, SIG routing, label decisions, "
        "stale decisions, and maintainer overrides."
    ),
    implementation_acceptance_criteria=(
        "Draft Kubernetes issue triage recommendation is generated from source evidence."
    ),
)

BUG_TRIAGE_PROFILE = BlueprintProfile(
    kind="bug_triage",
    summary=(
        "OpenStack bug triage workflow routes Launchpad bug reports through "
        "Incomplete, Confirmed, priority, security, stale, and patch review decisions."
    ),
    primary_risk=(
        "Incorrect bug status or importance can hide urgent work or waste maintainer time."
    ),
    automation_candidate_name="Draft bug triage recommendation",
    implementation_boundary=(
        "Draft bug triage recommendation only; do not change Launchpad status, "
        "importance, tags, assignees, or security flags automatically."
    ),
    human_approval_boundary=(
        "Bug supervisor approves before status, importance, security flag, or milestone changes."
    ),
    risk_level="high",
    approval_decision="Approve bug triage recommendation",
    approval_actor_terms=("bug supervisor",),
    approval_reason=(
        "Bug triage changes can alter priority, security handling, and release-blocking work."
    ),
    eval_case_name="Bug triage recommendation",
    eval_input_condition=(
        "Bug report includes status, reproduction details, project area, "
        "and patch or priority context."
    ),
    eval_expected_behavior=(
        "Blueprint recommends a bug supervisor-reviewed triage action without "
        "changing bug tracker state automatically."
    ),
    observability_need=(
        "Track draft bug triage recommendations, supervisor overrides, status changes, "
        "and stale bug outcomes."
    ),
    implementation_acceptance_criteria=(
        "Draft bug triage recommendation is generated from source evidence."
    ),
)

INCIDENT_RESPONSE_PROFILE = BlueprintProfile(
    kind="incident_response",
    summary=(
        "GitLab incident workflow coordinates alert intake, PagerDuty notification, "
        "Slack declaration, Incident.io response tracking, and shared incident documentation."
    ),
    primary_risk=(
        "Split incident communication can delay coordinated response or stakeholder updates."
    ),
    automation_candidate_name="Draft incident coordination recommendation",
    implementation_boundary=(
        "Draft coordination recommendation only; do not page responders, declare "
        "incidents, or publish updates automatically."
    ),
    human_approval_boundary=(
        "Incident lead approves before paging extra roles, declaring severity, "
        "or publishing customer-facing updates."
    ),
    risk_level="high",
    approval_decision="Approve incident coordination recommendation",
    approval_actor_terms=("incident manager",),
    approval_reason=(
        "Incident coordination changes can page responders or publish operational updates."
    ),
    eval_case_name="Incident coordination recommendation",
    eval_input_condition=(
        "Alert includes severity, source, affected service, and current incident role context."
    ),
    eval_expected_behavior=(
        "Blueprint recommends a human-approved incident coordination action without "
        "paging responders or publishing updates automatically."
    ),
    observability_need=(
        "Track draft incident recommendations, role notifications, communication channel "
        "updates, and human overrides."
    ),
    implementation_acceptance_criteria=(
        "Draft incident coordination recommendation is generated from source evidence."
    ),
)

BLUEPRINT_PROFILES: dict[WorkflowKind, BlueprintProfile] = {
    profile.kind: profile
    for profile in (
        SUPPORT_INTAKE_PROFILE,
        ISSUE_TRIAGE_PROFILE,
        KUBERNETES_ISSUE_TRIAGE_PROFILE,
        BUG_TRIAGE_PROFILE,
        INCIDENT_RESPONSE_PROFILE,
    )
}


def profile_for_workflow_signals(
    *,
    systems: list[str],
    decisions: list[str],
) -> BlueprintProfile:
    systems_text = " ".join(systems).casefold()
    decisions_text = " ".join(decisions).casefold()
    if "incident.io" in systems_text:
        return INCIDENT_RESPONSE_PROFILE
    if "launchpad" in systems_text:
        return BUG_TRIAGE_PROFILE
    if "kubernetes" in systems_text and "sig" in decisions_text:
        return KUBERNETES_ISSUE_TRIAGE_PROFILE
    if "github issues" in systems_text and "duplicate" in decisions_text:
        return ISSUE_TRIAGE_PROFILE
    return SUPPORT_INTAKE_PROFILE


def profile_for_workflow_kind(kind: WorkflowKind) -> BlueprintProfile:
    return BLUEPRINT_PROFILES[kind]
