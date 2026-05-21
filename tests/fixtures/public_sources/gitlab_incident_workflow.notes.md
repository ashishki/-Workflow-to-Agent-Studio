# GitLab Incident Workflow Public Source Notes

Source URL: https://runbooks.gitlab.com/incidents/
Accessed: 2026-05-21
Dataset kind: public-source experiment only; not operator pilot evidence.

These notes paraphrase the public GitLab incident workflow runbook page for a
local Workflow-to-Agent Studio experiment.

Workflow context:

- GitLab documents a general incident workflow separate from service-specific
  runbooks.
- Incident.io is the primary automation tool for the incident process.
- Most incident information is exchanged in an incident Slack channel, an
  incident Zoom meeting, and an Incident.io incident.
- Alertmanager, Dead Man's Snitch, and Pingdom notify PagerDuty when automated
  monitoring detects a potential incident.
- PagerDuty notifies the current engineer on call.
- Incident.io can also use PagerDuty to notify incident roles for high severity
  incidents.
- A Slack command can declare an incident. That command depends on Slack and
  Incident.io.
- The workflow includes creating a shared Google Doc, making it editable for the
  company, and posting the document link in Slack.
- Service-specific runbooks contain response steps for individual services, while
  the incident workflow describes coordination and communication.

Actors:

- Engineer on call
- Incident manager on call
- Communications manager on call
- Incident responder
- Service owner

Systems:

- Incident.io
- Slack
- Zoom
- PagerDuty
- Alertmanager
- Dead Man's Snitch
- Pingdom
- Google Docs
- Service-specific runbooks

Trigger:

- Monitoring detects a potential incident or a responder declares an incident
  with the Slack incident command.

Decisions:

- Does an alert require incident declaration?
- Should PagerDuty notify the engineer on call only, or also incident and
  communications roles?
- Which service-specific runbook applies?
- Should the team create and share an incident document?
- Which updates belong in Slack, Zoom, Incident.io, or the shared document?

Data fields:

- alert source
- severity
- affected service
- engineer on call
- incident manager on call
- communications manager on call
- incident channel
- Zoom meeting
- Incident.io incident
- Google Doc link
- service runbook link

Pain points:

- Incident coordination spans multiple systems.
- High severity incidents require fast role notification.
- Service-specific response details live outside the general workflow.
- Documentation and communication must stay synchronized during response.
