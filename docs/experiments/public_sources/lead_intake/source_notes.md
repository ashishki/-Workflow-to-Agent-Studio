# Lead Intake Source Notes

Status: sanitized public-source notes; not pilot evidence
Source register: `docs/experiments/public_sources/lead_intake/source_register.md`

These notes paraphrase public HVAC service intake pages. They preserve workflow
facts needed for a demo blueprint without copying raw page dumps.

## Actors

- homeowner or property contact requesting HVAC help
- business property contact for commercial or light-commercial service
- intake representative or customer service representative
- dispatcher or scheduling coordinator
- technician or estimator
- service manager for emergency or ambiguous requests

## Systems

- public website form
- phone intake line
- appointment scheduler or embedded form
- service-area or ZIP-code checker
- email notification path
- dispatch calendar or technician schedule
- CRM or service-management system, inferred as a required downstream system
  and marked as an assumption until a real operator confirms it

## Customer Inputs

- name
- phone
- email
- service address or ZIP code
- residential or commercial request type
- service type, such as repair, maintenance, estimate, replacement, indoor air
  quality, mini-split, ductwork, heating, cooling, or emergency service
- system type when requested by the source
- preferred date or appointment window
- issue description or additional information
- referral source when requested by the source

## Qualification Fields

- is the location inside the service area?
- is the request residential, commercial, or light-commercial?
- is the issue urgent or emergency?
- is the desired service repair, maintenance, installation, estimate, or
  consultation?
- is the system heating, cooling, ductless, indoor-air-quality, ductwork, or
  another supported category?
- does the customer need phone confirmation before scheduling?
- does the source suggest same-day, 24/7, or after-hours handling?

## Escalation Points

- urgent no-cooling, no-heat, or emergency requests should route to phone or
  emergency-service handling rather than ordinary async form follow-up;
- requests outside service area should be blocked or routed to manual review;
- commercial or industrial requests may need a different estimator or technician
  queue from ordinary residential work;
- incomplete contact details should block scheduling confirmation;
- ambiguous service descriptions should trigger follow-up before dispatch.

## Unsafe-Answer Boundaries

- do not claim a price, discount eligibility, financing approval, or arrival
  guarantee unless the specific source says it and the claim is quoted in the
  demo with evidence;
- do not diagnose HVAC equipment from a short form description;
- do not promise emergency availability outside the source's stated boundary;
- do not schedule work outside the listed service area without manual
  confirmation;
- do not treat public-source demo rows as buyer proof, pilot proof, or evidence
  that an HVAC company accepted the generated blueprint.

## Candidate Automation Shape

A public-demo lead-intake assistant can classify inbound HVAC requests, check
service-area fit, extract required scheduling fields, identify emergency routing,
prepare a callback summary, and produce missing-question prompts. Human approval
or existing dispatch tooling remains responsible for final appointment
confirmation.
