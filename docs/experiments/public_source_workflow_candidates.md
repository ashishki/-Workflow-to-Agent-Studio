# Public Source Workflow Candidates

Status: public-source candidate catalog; not customer proof.

These sources are used to expand public-source demo and eval coverage while real
prospect workflow data is unavailable. Each committed fixture is a short
paraphrase with source URL, access date, and dataset boundary. None of these
fixtures can satisfy T34, T40, or real pilot proof.

| Fixture | Source | Workflow Class | Current Use |
|---------|--------|----------------|-------------|
| `tests/fixtures/public_sources/netbox_issue_triage.notes.md` | https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow | issue triage | public demo pack baseline |
| `tests/fixtures/public_sources/kubernetes_issue_triage.notes.md` | https://www.kubernetes.dev/docs/guide/issue-triage/ | issue triage | public-source corpus stability |
| `tests/fixtures/public_sources/openstack_bug_triage.notes.md` | https://wiki.openstack.org/wiki/BugTriage | bug triage | public-source corpus stability |
| `tests/fixtures/public_sources/gitlab_incident_workflow.notes.md` | https://runbooks.gitlab.com/incidents/ | incident response | public-source corpus stability |

## Selection Rationale

- Kubernetes adds a large GitHub triage workflow with SIG ownership, label
  commands, stale handling, needs-information, priority, and support-request
  routing.
- OpenStack adds Launchpad-oriented bug triage with status transitions,
  incomplete review, security flags, importance, stale in-progress review, and
  supervisor-only steps.
- GitLab adds incident response coordination with alert sources, PagerDuty,
  Slack, Zoom, Incident.io, Google Docs, and service-specific runbooks.

## Boundary

Public-source candidates are useful for stabilizing extraction and synthesis
quality across workflow classes. They are not buyer validation, do not prove
wedge strength, and must not be counted in `docs/pilot_measurement.md`.
