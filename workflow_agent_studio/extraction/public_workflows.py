"""Public workflow extraction profile registry."""

from __future__ import annotations

from dataclasses import dataclass

from workflow_agent_studio.domain.workflow import WorkflowKind


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

APACHE_AIRFLOW_ISSUE_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="apache_airflow_issue_triage",
    workflow_kind="apache_airflow_issue_triage",
    required_terms=("apache airflow", "github discussions", "issue triage team"),
    actors=(
        "Issue reporter",
        "Issue triage team member",
        "Airflow committer",
        "Community helper",
        "Pull request author",
    ),
    systems=(
        "GitHub Issues",
        "GitHub Discussions",
        "GitHub issue templates",
        "Labels",
        "Milestones",
        "Priorities",
        "Pull requests",
    ),
    triggers=(
        "New Airflow issue, discussion, or pull request needs response, label, "
        "conversion, closure, assignment, or escalation",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Issue reporter submits an Airflow bug or small feature request "
                "through GitHub templates."
            ),
            actor="Issue reporter",
            system="GitHub issue templates",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Issue triage team member checks whether the report is actionable, "
                "needs more information, or belongs in GitHub Discussions."
            ),
            actor="Issue triage team member",
            system="GitHub Issues",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Triage team member labels, prioritizes, assigns, closes, or converts "
                "the issue when human authority allows it."
            ),
            actor="Issue triage team member",
            system="Labels",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Committer or knowledgeable community member is involved when code "
                "ownership or merge authority is required."
            ),
            actor="Airflow committer",
            system="Pull requests",
        ),
    ),
    decisions=(
        (
            "Decide whether the report is a bug, feature request, troubleshooting "
            "discussion, duplicate, invalid report, or clear actionable issue"
        ),
        "Decide whether the issue should be converted to a GitHub Discussion",
        "Decide whether additional information is needed from the reporter",
        "Decide which labels, milestone, or priority should apply",
        "Decide whether to mention a committer or knowledgeable community member",
    ),
    exceptions=(
        "Troubleshooting or unclear reports may be converted to GitHub Discussions",
        "Triage team members cannot merge code by that role alone",
        "Issues without enough information require reporter follow-up",
    ),
    data_fields=(
        "issue type",
        "template type",
        "reproducible steps",
        "discussion status",
        "labels",
        "milestone",
        "priority",
        "pending response status",
        "assignee",
        "linked pull request",
    ),
    pain_points=(
        "Maintainers need quick responses so reporters do not feel ignored",
        "Unclear troubleshooting reports need discussion conversion",
        "Triage authority differs from committer and merge authority",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Which Airflow committer approves merge-related escalation?",
            reason="The public source distinguishes triage and committer roles.",
        ),
    ),
)

DJANGO_TICKET_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="django_ticket_triage",
    workflow_kind="django_ticket_triage",
    required_terms=("django", "trac", "ticket triage"),
    actors=(
        "Ticket reporter",
        "Triager",
        "Bug fixer",
        "Reviewer",
        "Merger",
    ),
    systems=(
        "Django Trac",
        "GitHub pull requests",
        "Trac flags",
        "Review queue",
        "Django Forum",
    ),
    triggers=(
        "New or updated Django ticket or pull request needs triage, review, "
        "flag correction, or final check-in decision",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Triager reviews unreviewed Django tickets and determines whether "
                "they are actionable."
            ),
            actor="Triager",
            system="Django Trac",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Triager sets ticket stage, type, component, severity, and flags "
                "such as needs tests or needs documentation."
            ),
            actor="Triager",
            system="Trac flags",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Reviewer checks patch or pull request readiness and requests "
                "improvements when needed."
            ),
            actor="Reviewer",
            system="GitHub pull requests",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Merger gives final review before a ready-for-checkin change is committed."
            ),
            actor="Merger",
            system="Review queue",
        ),
    ),
    decisions=(
        "Decide whether the ticket is unreviewed, accepted, ready for checkin, or closed",
        "Decide whether the ticket describes a valid and actionable issue",
        "Decide whether a patch needs tests, documentation, or improvement",
        "Decide whether the ticket is a bug, new feature, or cleanup",
        "Decide whether merger final review is required before commit",
    ),
    exceptions=(
        "Sparse tickets can be closed as needsinfo",
        "Patch-ready tickets still require final merger review",
        "Tickets may wait for author changes, tests, documentation, or review",
    ),
    data_fields=(
        "ticket stage",
        "ticket type",
        "component",
        "severity",
        "version",
        "has patch flag",
        "needs tests flag",
        "needs documentation flag",
        "patch needs improvement flag",
        "easy pickings flag",
        "reviewer comment",
    ),
    pain_points=(
        "Triagers repeatedly correct incomplete ticket metadata and flags",
        "Patch readiness depends on tests, documentation, and reviewer comments",
        "Final merger review remains a required human decision",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Which merger has final authority for this ticket or pull request?",
            reason="The public source describes the role but not a named approver.",
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

MOZILLA_BUGZILLA_TRIAGE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="mozilla_bugzilla_triage",
    workflow_kind="mozilla_bugzilla_triage",
    required_terms=("mozilla", "bugzilla", "whiteboard tags"),
    actors=(
        "Bug reporter",
        "Component triager",
        "Engineer or volunteer",
        "Component team",
        "Release or priority owner",
    ),
    systems=(
        "Bugzilla",
        "Saved bug queries",
        "Component fields",
        "Whiteboard tags",
        "Needinfo flag",
        "Dependency bugs",
        "Release flags",
    ),
    triggers=(
        "New open Bugzilla bug in a component needs categorization, priority, "
        "closure, follow-up, or assignment",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Component triager reviews untriaged Bugzilla queries for assigned components."
            ),
            actor="Component triager",
            system="Saved bug queries",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Triager checks crash, regression, security, component, and priority signals."
            ),
            actor="Component triager",
            system="Bugzilla",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Triager applies whiteboard outcomes such as fix now, active, "
                "fix later, backlog, needs component, or follow-up."
            ),
            actor="Component triager",
            system="Whiteboard tags",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Release or priority owner reviews priority, release flags, dependency, "
                "or assignment updates when needed."
            ),
            actor="Release or priority owner",
            system="Release flags",
        ),
    ),
    decisions=(
        "Decide whether the bug is already triaged or still untriaged",
        "Decide whether the issue is a critical crash, regression, or security-sensitive item",
        (
            "Decide whether to fix now, keep active, fix later, backlog, "
            "move components, close, or follow up"
        ),
        "Decide whether needinfo is required before a decision can be made",
        "Decide whether release flags, priority, dependency, or assignment should change",
    ),
    exceptions=(
        "Security-sensitive bugs require restricted handling",
        "Bugs needing more information require needinfo or dependency tracking",
        "Component ownership changes can move the bug to another team",
    ),
    data_fields=(
        "component",
        "bug status",
        "resolution",
        "creation date",
        "keywords",
        "whiteboard tags",
        "needinfo flag",
        "crash/regression/security markers",
        "priority",
        "release flags",
        "dependency bug",
    ),
    pain_points=(
        "Triagers must repeatedly scan saved queries for untriaged bugs",
        "Priority and release decisions depend on crash, regression, and security signals",
        "Follow-up cases need consistent needinfo or dependency tracking",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Which release or priority owner approves high-impact state changes?",
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

HVAC_LEAD_INTAKE_PROFILE = PublicWorkflowExtractionProfile(
    profile_id="hvac_lead_intake",
    workflow_kind="hvac_lead_intake",
    required_terms=("hvac", "service-area", "appointment"),
    actors=(
        "Customer",
        "Homeowner or property contact",
        "Commercial property contact",
        "Intake representative",
        "Scheduling coordinator",
        "Dispatcher",
        "Technician or estimator",
        "Service manager",
    ),
    systems=(
        "Website appointment form",
        "Phone intake line",
        "Service-area checker",
        "Email notification path",
        "Dispatch calendar",
        "Technician schedule",
        "CRM or service-management system",
    ),
    triggers=(
        "Customer calls, submits an appointment form, requests service online, "
        "or checks service-area coverage",
    ),
    steps=(
        StepTemplate(
            step_id="step-1",
            description=(
                "Customer submits HVAC service details through a form, phone call, "
                "or service-area checker."
            ),
            actor="Customer",
            system="Website appointment form",
        ),
        StepTemplate(
            step_id="step-2",
            description=(
                "Intake representative checks contact details, location fit, "
                "service type, system type, and urgency."
            ),
            actor="Intake representative",
            system="Service-area checker",
        ),
        StepTemplate(
            step_id="step-3",
            description=(
                "Scheduling coordinator routes emergency requests to phone or urgent "
                "handling and ordinary requests to appointment follow-up."
            ),
            actor="Scheduling coordinator",
            system="Dispatch calendar",
        ),
        StepTemplate(
            step_id="step-4",
            description=(
                "Dispatcher prepares the technician or estimator handoff after "
                "required fields and manual confirmations are complete."
            ),
            actor="Dispatcher",
            system="Technician schedule",
        ),
    ),
    decisions=(
        "Decide whether the address or ZIP code is inside the service area",
        "Decide whether the request is urgent, emergency, or standard follow-up",
        (
            "Decide whether the request is repair, maintenance, installation, "
            "replacement, estimate, or consultation"
        ),
        "Decide whether the customer is residential, commercial, or industrial",
        "Decide whether more details are needed before dispatch",
    ),
    exceptions=(
        "Emergency no-cooling or no-heat requests route to phone or urgent handling",
        "Outside-service-area requests require rejection or manual review",
        "Incomplete contact details block scheduling confirmation",
        "Commercial or industrial requests may need specialist routing",
    ),
    data_fields=(
        "name",
        "phone",
        "email",
        "service address or ZIP code",
        "residential or commercial request type",
        "service type",
        "system type",
        "preferred service date",
        "issue description",
        "referral source",
    ),
    pain_points=(
        "Public forms can collect incomplete details before scheduling",
        "Emergency requests need faster routing than ordinary form follow-up",
        "Service-area fit must be checked before appointment confirmation",
        "Commercial or industrial jobs may require different routing",
    ),
    missing_questions=(
        MissingQuestionTemplate(
            section="approval_boundaries",
            question="Who confirms the appointment window before a technician is dispatched?",
            reason="The public sources describe intake fields but not final dispatch approval.",
        ),
    ),
)

PUBLIC_WORKFLOW_EXTRACTION_PROFILES: tuple[PublicWorkflowExtractionProfile, ...] = (
    APACHE_AIRFLOW_ISSUE_TRIAGE_PROFILE,
    DJANGO_TICKET_TRIAGE_PROFILE,
    KUBERNETES_ISSUE_TRIAGE_PROFILE,
    OPENSTACK_BUG_TRIAGE_PROFILE,
    MOZILLA_BUGZILLA_TRIAGE_PROFILE,
    GITLAB_INCIDENT_WORKFLOW_PROFILE,
    HVAC_LEAD_INTAKE_PROFILE,
    NETBOX_ISSUE_TRIAGE_PROFILE,
)


def public_workflow_profile_for_text(text: str) -> PublicWorkflowExtractionProfile | None:
    return next(
        (profile for profile in PUBLIC_WORKFLOW_EXTRACTION_PROFILES if profile.matches(text)),
        None,
    )
