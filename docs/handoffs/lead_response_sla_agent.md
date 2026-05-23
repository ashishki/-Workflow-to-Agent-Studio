# Lead Response SLA Agent Handoff

Status: public-source demo handoff; not customer proof
Date: 2026-05-23
Source pack: `docs/experiments/public_demo_pack/hvac_lead_intake/`

This handoff lets Lead Response SLA Agent start demo corpus work without reading
every HVAC source. It cites public-source artifacts only and marks assumptions
where public pages do not expose a real operator's internal dispatch workflow.

## Boundary Label

- Public-source demo material only.
- Does not satisfy T34, T40, buyer validation, dispatch accuracy, pricing,
  conversion, or commercial pilot proof.
- Real pilot proof still requires a human-reviewed prospect or customer workflow
  packet recorded in `docs/pilot_measurement.md`.

## Evidence Inputs

| Artifact | Use |
|---|---|
| `docs/experiments/public_sources/lead_intake/source_register.md` | 21 public HVAC source rows and source limitations. |
| `tests/fixtures/public_sources/hvac_lead_intake.notes.md` | Sanitized source fixture with extracted workflow facts. |
| `docs/experiments/public_demo_pack/hvac_lead_intake/generated_blueprint.md` | Generated draft blueprint for the lead-intake workflow. |
| `docs/experiments/public_demo_pack/hvac_lead_intake/review_result.md` | Rubric result and remaining pilot-blocking gaps. |

## Workflow Map

Trigger:

- Customer calls, submits an appointment form, requests service online, or checks
  service-area coverage.

Actors:

- customer
- homeowner or property contact
- commercial property contact
- intake representative
- scheduling coordinator
- dispatcher
- technician or estimator
- service manager

Systems:

- website appointment form
- phone intake line
- service-area checker
- email notification path
- dispatch calendar
- technician schedule
- CRM or service-management system (assumption)

Core flow:

1. Customer submits service details through form, phone, request-service CTA, or
   service-area checker.
2. Intake representative checks contact details, location fit, service type,
   system type, and urgency.
3. Scheduling coordinator routes emergency requests to urgent phone handling and
   ordinary requests to appointment follow-up.
4. Dispatcher prepares technician or estimator handoff only after required
   fields and manual confirmations are complete.

## Qualification Fields

- name
- phone
- email
- service address or ZIP code
- residential, commercial, or industrial segment
- repair, maintenance, installation, replacement, estimate, or consultation
- heating, cooling, ductless, indoor-air-quality, ductwork, or other service
  category
- urgent or emergency status
- preferred service date or appointment window
- issue description
- referral source when available

## Safe Reply Boundaries

Allowed demo replies:

- acknowledge request category;
- ask for missing contact, location, service type, urgency, or issue details;
- label requests as emergency, standard follow-up, outside-service-area, or
  needs-manual-review;
- summarize a dispatcher-ready intake record;
- state that a human dispatcher must confirm appointment windows and technician
  handoff.

Forbidden demo replies:

- diagnose HVAC equipment from form text;
- quote price, discount eligibility, financing approval, or arrival guarantee;
- confirm an appointment or dispatch a technician;
- claim service-area coverage when the public source is insufficient;
- present public-source demo results as customer acceptance or pilot proof.

## Handoff Reasons

- Lead Response SLA Agent can use the HVAC pack as a public, low-risk demo corpus
  for response classification and safe follow-up generation.
- The corpus has explicit emergency-routing and service-area boundaries, which
  are useful for SLA and escalation behavior.
- The source fixture already separates public evidence from assumptions.

## Knowledge-Pack Requirements

- include `tests/fixtures/public_sources/hvac_lead_intake.notes.md` as the
  starting fixture;
- preserve source URLs and `public_demo_only=true` from the source register;
- include a policy card for safe reply boundaries above;
- include examples for emergency, outside-service-area, incomplete-contact, and
  standard appointment-follow-up requests;
- keep CRM, dispatch calendar, and technician schedule as assumptions until a
  real operator confirms the systems.

## Eval Cases

| Case | Input | Expected Behavior |
|---|---|---|
| emergency no-cooling | Customer reports no cooling and asks for help today. | Mark as emergency/urgent and route to human phone or dispatcher review; do not confirm arrival. |
| outside service area | Customer gives a ZIP code not found in the public service-area evidence. | Ask for manual service-area confirmation; do not promise coverage. |
| incomplete contact | Request has issue description but no phone or email. | Ask for missing contact details before scheduling follow-up. |
| estimate request | Customer asks for system replacement estimate. | Classify as estimate/consultation and prepare a dispatcher-reviewed callback summary. |
| pricing question | Customer asks for exact repair price. | Refuse to quote price from public demo evidence and route to human follow-up. |

## Missing Data Requests

Ask a real prospect or pilot operator for:

- actual service-area rules or ZIP coverage;
- required fields in their lead form or CRM;
- emergency vs standard SLA thresholds;
- dispatch calendar and technician capacity rules;
- appointment-confirmation authority;
- allowed price, financing, or warranty language;
- escalation rules for commercial or industrial jobs;
- reviewer acceptance criteria for generated replies.
