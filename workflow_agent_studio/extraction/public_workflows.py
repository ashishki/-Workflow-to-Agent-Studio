"""Public workflow extraction profile registry."""

from __future__ import annotations

from dataclasses import dataclass

from workflow_agent_studio.patterns.public_workflows import WorkflowKind


@dataclass(frozen=True)
class StepTemplate:
    step_id: str
    description: str
    actor: str
    system: str


@dataclass(frozen=True)
class MissingQuestionTemplate:
    section: str
    question: str
    reason: str


@dataclass(frozen=True)
class PublicWorkflowExtractionProfile:
    profile_id: str
    workflow_kind: WorkflowKind
    required_terms: tuple[str, ...]
    actors: tuple[str, ...]
    systems: tuple[str, ...]
    triggers: tuple[str, ...]
    steps: tuple[StepTemplate, ...]
    decisions: tuple[str, ...]
    exceptions: tuple[str, ...]
    data_fields: tuple[str, ...]
    pain_points: tuple[str, ...]
    missing_questions: tuple[MissingQuestionTemplate, ...]

    def matches(self, text: str) -> bool:
        normalized = text.casefold()
        return all(term in normalized for term in self.required_terms)


NETBOX_ISSUE_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="netbox_issue_triage",
    workflow_kind="issue_triage",
    required_terms=("github issues", "issue", "triage"),
    actors=("Reporter", "Maintainer or triager", "Contributor or engineering owner"),
    systems=(
        "GitHub Issues",
        "Issue templates",
        "Issue labels or GitHub issue types",
        "Canned maintainer responses",
        "Project backlog",
    ),
    triggers=(
        "New GitHub issue, feature request, bug report, support-like request, or pull request",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description="Reporter opens a GitHub issue using the expected template.",
            actor="Reporter",
            system="GitHub Issues",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Maintainer checks template completion, issue type, scope, and duplicate status."
            ),
            actor="Maintainer or triager",
            system="Issue templates",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Maintainer asks for clarification when reproduction steps "
                "or feature details are missing."
            ),
            actor="Maintainer or triager",
            system="Canned maintainer responses",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Accepted issues move toward ownership, engineering review, "
                "or linked pull request work."
            ),
            actor="Contributor or engineering owner",
            system="Project backlog",
        ),
    ),
    decisions=(
        "Decide whether the submission follows the required issue template",
        (
            "Decide whether the issue is duplicate, out of scope, support-oriented, "
            "or expected behavior"
        ),
        "Decide whether a bug report is reproducible on a current stable release",
        (
            "Decide whether a feature request has a justified use case "
            "and enough implementation detail"
        ),
        (
            "Decide whether to ask for more information, mark stale, close, "
            "accept, or route to engineering review"
        ),
    ),
    exceptions=(
        "Missing template fields require maintainer clarification before acceptance",
        "Duplicate, support-like, or out-of-scope issues can be closed",
        "Issues without requested follow-up can become stale and eventually close",
    ),
    data_fields=(
        "issue type",
        "reporter",
        "template completion state",
        "product version",
        "reproduction steps",
        "expected behavior",
        "actual behavior",
        "use case",
        "scope decision",
        "owner",
        "linked pull request",
    ),
    pain_points=(
        "Maintainers repeatedly check issue templates and request missing details",
        "Duplicate, support, and out-of-scope submissions consume triage time",
        "Stale issues require consistent follow-up and closure decisions",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Who has final authority to accept an issue for engineering review?",
            reason="The public source describes triage decisions but not a single final approver.",
        ),
    ),
)

KUBERNETES_ISSUE_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="kubernetes_issue_triage",
    workflow_kind="kubernetes_issue_triage",
    required_terms=("kubernetes", "github issues", "issue", "triage"),
    actors=(
        "Issue reporter",
        "Triage contributor",
        "SIG member or SIG owner",
        "Kubernetes bot",
        "Issue owner or assignee",
    ),
    systems=(
        "Kubernetes GitHub Issues",
        "GitHub labels",
        "Kubernetes bot commands",
        "Triage Party",
        "GitHub project boards",
        "DevStats dashboards",
        "Support channels",
    ),
    triggers=("New Kubernetes GitHub issue or pull request needs triage",),
    steps=(
        StepTemplate(
            step_id="step-1",
            description="Triage contributor reviews new Kubernetes GitHub issues that need triage.",
            actor="Triage contributor",
            system="Kubernetes GitHub Issues",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Triager classifies support requests, duplicates, bugs, "
                "help wanted candidates, and good first issues."
            ),
            actor="Triage contributor",
            system="GitHub labels",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Triager applies SIG ownership, priority labels, "
                "triage/needs-information, or lifecycle/stale follow-up."
            ),
            actor="SIG member or SIG owner",
            system="Kubernetes bot commands",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Issue owner or assignee follows up with a pull request, "
                "comment, stale handling, or closure."
            ),
            actor="Issue owner or assignee",
            system="GitHub project boards",
        ),
    ),
    decisions=(
        (
            "Decide whether a Kubernetes item is support, duplicate, abandoned, "
            "wrong repository, bug, help wanted, or good first issue"
        ),
        "Decide whether the issue needs triage/needs-information",
        "Decide which SIG owns the issue",
        "Decide which priority label applies",
        "Decide whether lifecycle/stale follow-up or closure is needed",
    ),
    exceptions=(
        "Support requests are redirected to support channels",
        "Unclear ownership is deferred to SIG labels",
        "Issues without activity can move to lifecycle/stale and eventual closure",
    ),
    data_fields=(
        "issue number",
        "issue kind",
        "reporter",
        "labels",
        "SIG owner",
        "priority",
        "reproduction status",
        "duplicate reference",
        "triage/needs-information",
        "lifecycle/stale",
        "assignee",
        "linked pull request",
    ),
    pain_points=(
        "High public issue volume can slow contributor response",
        "Support requests can crowd out actionable engineering issues",
        "SIG ownership can be unclear",
        "Stale or unowned issues require consistent follow-up",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Which SIG role has final authority to accept or close this issue?",
            reason="The public source describes SIG ownership but not one universal approver.",
        ),
    ),
)

OPENSTACK_BUG_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="openstack_bug_triage",
    workflow_kind="bug_triage",
    required_terms=("openstack", "bug triage", "launchpad"),
    actors=(
        "Bug reporter",
        "Bug triager",
        "Bug supervisor",
        "Core project team",
        "Project driver",
    ),
    systems=(
        "Launchpad bug tracker",
        "Bug status fields",
        "Bug importance fields",
        "Security flag",
        "Official tags",
        "Bug-count graphs",
    ),
    triggers=(
        "New or existing OpenStack bug needs confirmation, priority, consistency repair, "
        "incomplete review, stale review, or patch review",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Bug triager reviews a New OpenStack bug for completeness and reproducibility."
            ),
            actor="Bug triager",
            system="Launchpad bug tracker",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Triager sets Incomplete when reproduction details are "
                "missing or Confirmed when the report appears valid."
            ),
            actor="Bug triager",
            system="Bug status fields",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Bug supervisor prioritizes confirmed bugs as Critical, High, "
                "Medium, Low, or Wishlist."
            ),
            actor="Bug supervisor",
            system="Bug importance fields",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Triager repairs inconsistent states, reviews incomplete bugs, "
                "stale In Progress bugs, and patches."
            ),
            actor="Bug triager",
            system="Official tags",
        ),
    ),
    decisions=(
        (
            "Decide whether a bug is Incomplete, Confirmed, Invalid, security-sensitive, "
            "stale, patched, or Triaged"
        ),
        "Decide whether Critical, High, Medium, Low, or Wishlist importance applies",
        "Decide whether an In Progress bug still has an active assignee",
        "Decide whether an incomplete bug should be reminded, confirmed, or closed",
    ),
    exceptions=(
        "Security-sensitive bugs require the security flag",
        "Incomplete bugs without answers can close as Invalid after reminders",
        "In Progress bugs without active ownership can be unassigned and reset",
    ),
    data_fields=(
        "bug status",
        "importance",
        "reporter",
        "project area",
        "reproduction details",
        "security flag",
        "official tag",
        "assignee",
        "patch presence",
        "milestone",
        "reminder state",
    ),
    pain_points=(
        "Missing reproduction details create repeated follow-up",
        "Bug states can become inconsistent",
        "Stale In Progress bugs can hide inactive ownership",
        "Priority and milestone decisions require supervisor or driver authority",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Which bug supervisor or project driver approves release-blocking priority?",
            reason="The public source describes roles but not a named approver.",
        ),
    ),
)

GITLAB_INCIDENT_WORKFLOW_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="gitlab_incident_workflow",
    workflow_kind="incident_response",
    required_terms=("gitlab", "incident.io", "pagerduty"),
    actors=(
        "Engineer on call",
        "Incident manager on call",
        "Communications manager on call",
        "Incident responder",
        "Service owner",
    ),
    systems=(
        "Incident.io",
        "Slack",
        "Zoom",
        "PagerDuty",
        "Alertmanager",
        "Dead Man's Snitch",
        "Pingdom",
        "Google Docs",
        "Service-specific runbooks",
    ),
    triggers=(
        "Monitoring detects a potential GitLab incident or a responder declares "
        "an incident with the Slack incident command",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Alertmanager, Dead Man's Snitch, or Pingdom sends a potential "
                "incident alert through PagerDuty."
            ),
            actor="Engineer on call",
            system="PagerDuty",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Responder declares an incident with the Slack incident command "
                "when coordination is required."
            ),
            actor="Incident responder",
            system="Slack",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Incident.io coordinates the incident and can notify on-call "
                "incident and communications roles for high severity."
            ),
            actor="Incident manager on call",
            system="Incident.io",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Team shares updates in Slack, Zoom, Incident.io, and a "
                "Google Docs incident document."
            ),
            actor="Communications manager on call",
            system="Google Docs",
        ),
    ),
    decisions=(
        "Decide whether an alert requires GitLab incident declaration",
        ("Decide whether PagerDuty should notify only the Engineer on call or also incident roles"),
        "Decide which service-specific runbook applies",
        "Decide whether to create and share a Google Docs incident document",
        "Decide which updates belong in Slack, Zoom, Incident.io, or the shared document",
    ),
    exceptions=(
        "High severity incidents require expanded role notification",
        "Service-specific response details are outside the general incident workflow",
        (
            "Communication can drift when Slack, Zoom, Incident.io, "
            "and Google Docs are not synchronized"
        ),
    ),
    data_fields=(
        "alert source",
        "severity",
        "affected service",
        "Engineer on call",
        "Incident manager on call",
        "Communications manager on call",
        "incident Slack channel",
        "Zoom meeting",
        "Incident.io incident",
        "Google Docs link",
        "service runbook link",
    ),
    pain_points=(
        "Incident coordination spans multiple systems",
        "High severity incidents require fast role notification",
        "Service-specific response details live outside the general workflow",
        "Documentation and communication must stay synchronized during response",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Who approves customer-facing incident updates before publication?",
            reason="The public source names communication roles but not final approval rules.",
        ),
    ),
)

PUBLIC_WORKFLOW_EXTRACTION_PROFILES: tuple[PublicWorkflowExtractionProfile, ...] = (
    KUBERNETES_ISSUE_TRIAGE_PROFILE,
    OPENSTACK_BUG_TRIAGE_PROFILE,
    GITLAB_INCIDENT_WORKFLOW_PROFILE,
    NETBOX_ISSUE_TRIAGE_PROFILE,
)


def public_workflow_profile_for_text(text: str) -> PublicWorkflowExtractionProfile | None:
    return next(
        (profile for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES if profile.matches(text)),
        None,
    )
