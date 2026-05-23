# Lead Intake Source Register

Status: public-source demo material; not customer proof
Captured at: 2026-05-23
Vertical: HVAC service intake

| ID | source_url_or_locator | captured_at | source_type | workflow_kind | extracted_workflow_facts | limitations | public_demo_only |
|---|---|---|---|---|---|---|---|
| HVAC-001 | https://dunriteservhvac.com/contact/ | 2026-05-23 | appointment form | lead intake | Form asks for contact details, service type, system type, preferred date, issue description, and referral source; urgent service is routed to a direct call. | One company page; no outcome or acceptance metrics. | true |
| HVAC-002 | https://ac-control.com/faq/ | 2026-05-23 | FAQ | lead intake | FAQ describes scheduled and emergency HVAC services and directs users to an appointment request form or phone contact. | FAQ-level process detail only. | true |
| HVAC-003 | https://climateprollc.com/service-areas/ | 2026-05-23 | service-area page | lead intake | Service-area page routes cooling emergencies to schedule service and lists repair, installation, maintenance, replacement, ductless, and heat pump services. | Does not expose the full request form fields. | true |
| HVAC-004 | https://acsheatandair.com/request-services/ | 2026-05-23 | request form | lead intake | Request form captures name, email, phone, service type, referral source, and additional information; page distinguishes onsite and virtual consultation. | Public page only; no internal dispatch rules. | true |
| HVAC-005 | https://preciseairandheating.com/service-areas | 2026-05-23 | service-area FAQ | lead intake | Page uses service-area confirmation, same-day or emergency scheduling, service type coverage, and response-time expectations. | Contains marketing claims that are not reused as proof. | true |
| HVAC-006 | https://gubbelshvac.com/schedule-service/ | 2026-05-23 | schedule-service page | lead intake | Page separates immediate phone assistance, online service scheduling, estimate requests, feedback, service area lookup, financing, and offers. | Embedded form fields are not fully visible in source capture. | true |
| HVAC-007 | https://www.omegahvac.com/service-request | 2026-05-23 | service request form | lead intake | Service-request flow asks users to complete a form to set an appointment and distinguishes residential or commercial requests. | Limited public detail about field options. | true |
| HVAC-008 | https://empireheating.net/faq | 2026-05-23 | FAQ | lead intake | FAQ says customers can schedule by phone, contact form, or estimate request and that the team confirms a preferred time. | FAQ does not show the full form schema. | true |
| HVAC-009 | https://www.aimservicegroup.com/contact-us/ | 2026-05-23 | contact page | lead intake | Contact page asks visitors to schedule service and positions the company for AC repair, heating service, ductwork, and installation requests. | Contact detail only; no triage outcomes. | true |
| HVAC-010 | https://metzaircontrol.com/service-area | 2026-05-23 | service-area page | lead intake | Page combines service-area coverage with appointment requests and routes HVAC, indoor-air-quality, ductless, heat pump, and plumbing services. | Includes promotional copy that is not used as evidence. | true |
| HVAC-011 | https://hbmhvac.com/ | 2026-05-23 | homepage and appointment CTA | lead intake | Page has request-appointment paths, emergency service positioning, residential/commercial/new-construction segmentation, and a service list. | Homepage-level facts only. | true |
| HVAC-012 | https://www.hlmarcohvac.com/hvac-service-area | 2026-05-23 | service-area page | lead intake | Page asks visitors to schedule service or request an estimate and lists repair, installation, maintenance, mini-split, ductwork, and indoor-air-quality services. | Does not expose internal qualification logic. | true |
| HVAC-013 | https://www.griffithenergyservices.com/service-area/ | 2026-05-23 | service-area checker | lead intake | Page uses ZIP-code service-area validation and links users toward repair service, order placement, and appointment requests. | Source is broader than HVAC-only lead intake. | true |
| HVAC-014 | https://www.all1mechanical.com/areas-we-service/ | 2026-05-23 | service-area page | lead intake | Page emphasizes 24/7 phone answering, same-day emergency scheduling when possible, and schedule minimization for business disruptions. | No exact appointment-form schema. | true |
| HVAC-015 | https://valleytemperature.com/ | 2026-05-23 | homepage and request form | lead intake | Page combines request-service CTAs, on-call emergency service, region coverage, and contact-form fields for commercial/industrial HVAC/R. | Commercial/industrial emphasis differs from residential lead intake. | true |
| HVAC-016 | https://www.seabreezeairandheat.com/ | 2026-05-23 | homepage and service-area page | lead intake | Page exposes request-appointment CTAs, service-area map, repair and installation services, and maintenance/tune-up positioning. | Promotional offer text is not reused as proof. | true |
| HVAC-017 | https://www.mightyairinc.com/request-service/ | 2026-05-23 | request-service form | lead intake | Multi-step request flow requires fields unless marked optional and routes users through appointment request steps. | Captured page does not list every step label. | true |
| HVAC-018 | https://www.falconhvac.com/schedule-appointment | 2026-05-23 | schedule-service page | lead intake | Page supports online scheduling, estimate requests, phone assistance, emergency-hour boundaries, and ZIP-code service-area lookup. | Form embed limits exact field visibility. | true |
| HVAC-019 | https://www.climatechmechanical.com/ | 2026-05-23 | homepage and service-area page | lead intake | Page routes users to request service, schedule an appointment, select service categories, and confirm service area coverage. | Does not provide dispatch rules. | true |
| HVAC-020 | https://www.airmasters.net/service-area/ | 2026-05-23 | service-area page | lead intake | Page asks users to request an appointment through phone or online form, lists local communities, and flags same-day and 24/7 emergency service. | Marketing and award claims excluded. | true |
| HVAC-021 | https://www.hvacbozeman.com/appointment-request | 2026-05-23 | appointment request form | lead intake | Form captures full name, phone, email, service address, service type, preferred date, residential/commercial status, and free-text issue details. | One regional operator; no back-office workflow details. | true |

## Boundary Notes

- Rows are source-finding support for public demo work, not buyer validation.
- Public pages may support workflow facts only when the fact is directly visible
  from the public source.
- Pricing, conversion, buyer readiness, and commercial pilot claims are out of
  scope unless a future real pilot records evidence in `docs/pilot_measurement.md`.
