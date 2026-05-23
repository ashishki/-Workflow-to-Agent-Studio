# Lead Intake Public Workflow Corpus

Status: public-source demo corpus; not customer proof
Date: 2026-05-23
Selected vertical: residential and light-commercial HVAC service intake

This corpus follows `docs/open_source_research_protocol.md`. It uses public HVAC
service pages, appointment forms, FAQs, service-area pages, and contact
instructions to model a local-service lead-intake workflow.

Public-source boundary:

- these artifacts are demo-quality workflow evidence only;
- every source row is marked `public_demo_only`;
- no source row claims buyer demand, conversion lift, pricing accuracy, or pilot
  acceptance;
- the corpus does not satisfy T34, T40, or any real pilot proof gate in
  `docs/pilot_measurement.md`.

Artifacts:

- `source_register.md` records the public sources and required protocol fields.
- `source_notes.md` extracts shared workflow facts for blueprint generation.
- `tests/fixtures/public_sources/hvac_lead_intake.notes.md` is the sanitized
  committed fixture for local eval and demo-pack work.
