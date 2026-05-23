# Automation Blueprint

Status: Draft
Blueprint Version ID: 1

## Workflow Summary
HVAC lead intake workflow routes public service requests through service-area
checks, contact capture, urgency triage, appointment follow-up, and technician
or estimator handoff.

## Actors
- Customer: Workflow participant
- Homeowner or property contact: Workflow participant
- Commercial property contact: Workflow participant
- Intake representative: Workflow participant
- Scheduling coordinator: Workflow participant
- Dispatcher: Workflow participant
- Technician or estimator: Workflow participant
- Service manager: Workflow participant

## Systems
- Website appointment form: Workflow system
- Phone intake line: Workflow system
- Service-area checker: Workflow system
- Email notification path: Workflow system
- Dispatch calendar: Workflow system
- Technician schedule: Workflow system
- CRM or service-management system: Workflow system

## Triggers
- Customer calls, submits an appointment form, requests service online, or checks
  service-area coverage

## Current Workflow
- step-1: Customer submits HVAC service details through a form, phone call, or service-area checker. [Customer]
- step-2: Intake representative checks contact details, location fit, service type, system type, and urgency. [Intake representative]
- step-3: Scheduling coordinator routes emergency requests to phone or urgent handling and ordinary requests to appointment follow-up. [Scheduling coordinator]
- step-4: Dispatcher prepares the technician or estimator handoff after required fields and manual confirmations are complete. [Dispatcher]

## Decisions
- Decide whether the address or ZIP code is inside the service area
- Decide whether the request is urgent, emergency, or standard follow-up
- Decide whether the request is repair, maintenance, installation, replacement,
  estimate, or consultation
- Decide whether the customer is residential, commercial, or industrial
- Decide whether more details are needed before dispatch

## Exceptions
- Emergency no-cooling or no-heat requests route to phone or urgent handling
- Outside-service-area requests require rejection or manual review
- Incomplete contact details block scheduling confirmation
- Commercial or industrial requests may need specialist routing

## Data Fields
- name: Workflow data field: name (source: Website appointment form)
- phone: Workflow data field: phone (source: Website appointment form)
- email: Workflow data field: email (source: Website appointment form)
- service address or ZIP code: Workflow data field: service address or ZIP code (source: Website appointment form)
- residential or commercial request type: Workflow data field: residential or commercial request type (source: Website appointment form)
- service type: Workflow data field: service type (source: Website appointment form)
- system type: Workflow data field: system type (source: Website appointment form)
- preferred service date: Workflow data field: preferred service date (source: Website appointment form)
- issue description: Workflow data field: issue description (source: Website appointment form)
- referral source: Workflow data field: referral source (source: Website appointment form)

## Integration Map
- Website appointment form -> CRM or service-management system: name, phone,
  email, service address or ZIP code, residential or commercial request type,
  service type, system type, preferred service date, issue description, referral
  source

## Pain Points
- Public forms can collect incomplete details before scheduling
- Emergency requests need faster routing than ordinary form follow-up
- Service-area fit must be checked before appointment confirmation
- Commercial or industrial jobs may require different routing

## Automation Candidates
- Draft HVAC lead intake summary: risk=medium; implementation boundary=Draft intake summary only; do not confirm appointments, prices, arrival windows, or technician dispatch automatically.; approval boundary=Dispatcher approves before appointment confirmation or technician handoff.

## Human Approval Boundaries
- Approve HVAC intake follow-up: Dispatcher - Appointment confirmation and dispatch create customer commitments.

## Risks And Assumptions
- risk: Incomplete intake details or unsupported service-area requests can lead to bad dispatch decisions.
- assumption: Who confirms the appointment window before a technician is dispatched?

## Eval Cases
- HVAC intake routing recommendation: when Request includes contact details, service area, service type, urgency, and issue description., expect Blueprint recommends a dispatcher-reviewed intake route without diagnosing equipment or confirming an appointment automatically.; verify by Inspect automation candidate and evidence link.

## Observability Needs
- Track missing intake fields, service-area rejects, emergency routing, and dispatcher overrides. (assumption)

## Rough Effort Band
small

## Next Implementation Tasks
- impl-1: engineer; AC: Draft HVAC intake summary is generated from public source evidence.; Tests: Blueprint synthesis integration test.

## Unresolved Findings
- none
