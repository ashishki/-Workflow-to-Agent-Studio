# Automation Blueprint

Status: Draft
Blueprint Version ID: 1

## Workflow Summary
GitLab incident workflow coordinates alert intake, PagerDuty notification, Slack
declaration, Incident.io response tracking, and shared incident documentation.

## Actors
- Engineer on call: Workflow participant
- Incident manager on call: Workflow participant
- Communications manager on call: Workflow participant
- Incident responder: Workflow participant
- Service owner: Workflow participant

## Systems
- Incident.io: Workflow system
- Slack: Workflow system
- Zoom: Workflow system
- PagerDuty: Workflow system
- Alertmanager: Workflow system
- Dead Man's Snitch: Workflow system
- Pingdom: Workflow system
- Google Docs: Workflow system
- Service-specific runbooks: Workflow system

## Triggers
- Monitoring detects a potential GitLab incident or a responder declares an
  incident with the Slack incident command

## Current Workflow
- step-1: Alertmanager, Dead Man's Snitch, or Pingdom sends a potential incident alert through PagerDuty. [Engineer on call]
- step-2: Responder declares an incident with the Slack incident command when coordination is required. [Incident responder]
- step-3: Incident.io coordinates the incident and can notify on-call incident and communications roles for high severity. [Incident manager on call]
- step-4: Team shares updates in Slack, Zoom, Incident.io, and a Google Docs incident document. [Communications manager on call]

## Decisions
- Decide whether an alert requires GitLab incident declaration
- Decide whether PagerDuty should notify only the Engineer on call or also incident roles
- Decide which service-specific runbook applies
- Decide whether to create and share a Google Docs incident document
- Decide which updates belong in Slack, Zoom, Incident.io, or the shared document

## Exceptions
- High severity incidents require expanded role notification
- Service-specific response details are outside the general incident workflow
- Communication can drift when Slack, Zoom, Incident.io, and Google Docs are not synchronized

## Data Fields
- alert source: Workflow data field: alert source (source: Incident.io)
- severity: Workflow data field: severity (source: Incident.io)
- affected service: Workflow data field: affected service (source: Incident.io)
- Engineer on call: Workflow data field: Engineer on call (source: Incident.io)
- Incident manager on call: Workflow data field: Incident manager on call (source: Incident.io)
- Communications manager on call: Workflow data field: Communications manager on call (source: Incident.io)
- incident Slack channel: Workflow data field: incident Slack channel (source: Incident.io)
- Zoom meeting: Workflow data field: Zoom meeting (source: Incident.io)
- Incident.io incident: Workflow data field: Incident.io incident (source: Incident.io)
- Google Docs link: Workflow data field: Google Docs link (source: Incident.io)
- service runbook link: Workflow data field: service runbook link (source: Incident.io)

## Automation Candidates
- Draft incident coordination recommendation: risk=high; implementation boundary=Draft coordination recommendation only; do not page responders, declare incidents, or publish updates automatically.; approval boundary=Incident lead approves before paging extra roles, declaring severity, or publishing customer-facing updates.

## Human Approval Boundaries
- Approve incident coordination recommendation: Incident manager on call - Incident coordination changes can page responders or publish operational updates.

## Risks And Assumptions
- risk: Split incident communication can delay coordinated response or stakeholder updates.
- assumption: Who approves customer-facing incident updates before publication?

## Unresolved Findings
- none
