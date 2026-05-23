# HVAC Lead Intake Public Source Notes

Source Register: docs/experiments/public_sources/lead_intake/source_register.md
Accessed: 2026-05-23
Dataset kind: public-source demo only; not customer proof or pilot evidence.
Vertical: HVAC service intake

These sanitized notes paraphrase public HVAC service pages and appointment
instructions. They are a compact fixture for local Workflow-to-Agent Studio eval
and demo work.

Workflow context:

- HVAC service intake begins when a customer calls, submits an appointment form,
  requests service online, or checks whether a service area covers their address
  or ZIP code.
- Public forms commonly ask for contact details, service address or ZIP code,
  service type, system type, preferred date, residential or commercial status,
  and a short description of the issue.
- Some sources route urgent requests to a phone call or 24/7 emergency handling
  instead of relying only on a web form.
- Service-area pages make location fit a first-stage qualification question.
- Estimate requests and repair requests can be separate paths.
- Commercial or industrial service may require a different queue from
  residential service.
- Public-source pages do not reveal enough internal workflow detail to claim a
  confirmed appointment, technician dispatch, pricing result, or buyer demand.

Actors:

- Customer
- Homeowner or property contact
- Commercial property contact
- Intake representative
- Scheduling coordinator
- Dispatcher
- Technician or estimator
- Service manager

Systems:

- Website appointment form
- Phone intake line
- Service-area checker
- Email notification path
- Dispatch calendar
- Technician schedule
- CRM or service-management system, marked as an assumption

Customer inputs:

- name
- phone
- email
- service address or ZIP code
- residential or commercial request type
- service type
- system type
- preferred service date
- issue description
- referral source

Qualification fields:

- service-area fit
- urgent or emergency status
- repair, maintenance, installation, replacement, estimate, or consultation
- heating, cooling, ductless, indoor-air-quality, ductwork, or other supported
  service category
- residential, commercial, or industrial segment
- callback required before confirmation

Escalation points:

- emergency no-cooling or no-heat requests route to phone or urgent handling
- outside-service-area requests require rejection or manual review
- incomplete contact details block scheduling confirmation
- ambiguous issue descriptions need a follow-up question before dispatch
- commercial or industrial requests may need specialist routing

Unsafe-answer boundaries:

- no pricing, conversion, buyer-readiness, or pilot-success claim is supported by
  this fixture
- no diagnosis should be made from a short intake form description
- no arrival-time guarantee should be generated unless source-specific evidence
  supports it
- public demo evidence cannot satisfy T34, T40, or `docs/pilot_measurement.md`
