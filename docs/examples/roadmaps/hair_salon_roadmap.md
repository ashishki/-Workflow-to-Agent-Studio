# Hair Salon AI Implementation Roadmap

Dataset kind: synthetic demo only. Not customer proof or pilot evidence.

## Executive Summary

Recommended privacy mode: lightweight cloud after redaction.

The workflow is a good low-risk SMB demo because it contains repeated booking
coordination, reminders, and reporting needs. It contains personal contact data,
but no medical, legal, financial, identity-document, or payment-card data is
required for roadmap analysis.

Top recommendations:

1. Deterministic appointment reminder automation.
2. Booking assistant with deterministic calendar availability check and human
   review before final calendar write.
3. Monthly booking analytics report.

Do not automate yet:

- stylist-specific service recommendations;
- cancellation penalty decisions;
- customer complaint handling.

30/60/90 day plan:

- 30 days: clean service menu, cancellation policy, calendar fields, and reminder
  rules; launch deterministic reminders.
- 60 days: pilot booking assistant for FAQs and slot suggestions with human
  confirmation.
- 90 days: add channel/source analytics and rebooking follow-up experiments.

Overall confidence: medium. Volume is estimated and should be verified.

## Evidence Packet

Primary source: `docs/examples/domains/hair_salon_input.md`

Evidence snippets:

- appointments flow through Instagram, WhatsApp, phone, and Google Calendar;
- receptionist manually checks calendar and sends reminders;
- pain points include missed messages, no-shows, repeated questions, and weak
  channel visibility.

Missing evidence:

- exact no-show rate;
- weekly inbound message count by channel;
- final service list and prices;
- cancellation policy.

## Workflow Map

Workflow: booking and rebooking.

Actors:

- client;
- receptionist;
- stylist;
- owner.

Steps:

1. Client asks for an appointment.
2. Receptionist asks service, date, and stylist preference.
3. Receptionist checks Google Calendar.
4. Client confirms slot.
5. Receptionist creates calendar event.
6. Receptionist sends manual reminder.
7. No-show/cancellation note is recorded inconsistently.
8. Stylist may suggest rebooking manually.

## Process Inventory

| Process | Recommended Type | Impact | Readiness | Privacy | Priority |
|---------|------------------|--------|-----------|---------|----------|
| Appointment reminders | Classic script/API integration | high | high | sensitive | quick win |
| Booking FAQ and slot suggestion | LLM assistant + deterministic availability | medium-high | medium | sensitive | strategic pilot |
| Booking source analytics | Script/reporting | medium | high | internal/sensitive | quick win |
| Cancellation penalties | Do not automate yet | medium | low | sensitive | human-only |

## Recommendation REC-001: Appointment Reminder Automation

Solution type: classic script or calendar integration.

Why: reminders have a clear trigger and do not require AI.

Required data:

- appointment date/time;
- phone/social handle;
- reminder template;
- cancellation policy link.

Privacy class: sensitive.

Estimated cost:

- one-time: 500-3000 USD;
- monthly: 0-100 USD plus messaging provider cost.

Estimated time: 3-7 days.

Required people:

- automation engineer;
- receptionist or owner.

Risks:

- wrong time sent if calendar data is inaccurate;
- message consent rules may vary by channel.

Validation:

- test on 20 upcoming appointments;
- confirm reminder timing and opt-out language.

Success metrics:

- no-show rate;
- receptionist time spent on reminders.

Confidence: high after calendar field review.

Fallback: manual reminders from a daily calendar report.

## Recommendation REC-002: Booking Assistant

Solution type: LLM assistant plus deterministic calendar availability and human
confirmation.

Why: repeated service/price/availability questions can be drafted by an
assistant, but final booking needs deterministic availability and review.

Required data:

- service menu;
- price list;
- stylist availability;
- cancellation policy;
- booking rules.

Privacy class: sensitive.

Estimated cost:

- one-time: 3000-15000 USD;
- monthly: 50-500 USD depending on message volume and model choice.

Estimated time: 2-5 weeks.

Required people:

- AI automation engineer;
- receptionist;
- owner.

Risks:

- wrong price;
- wrong slot;
- customer frustration if handoff is poor.

Human gate:

- final calendar write is confirmed by receptionist or deterministic booking
  service after availability check.

Validation:

- test 50 historical/synthetic booking messages;
- review assistant replies before live use;
- track incorrect slot/price suggestions.

Success metrics:

- response time;
- missed message count;
- booking conversion after response.

Confidence: medium until message volume and service policy are verified.

Fallback: FAQ snippets and manual calendar booking.

## Recommendation REC-003: Booking Analytics Report

Solution type: script/reporting.

Why: owner lacks visibility by channel and service; no LLM is required.

Required data:

- booking channel;
- service type;
- stylist;
- appointment status;
- no-show/cancellation flag.

Privacy class: internal/sensitive.

Estimated cost:

- one-time: 1000-5000 USD;
- monthly: 0-200 USD.

Estimated time: 1-2 weeks.

Validation:

- compare weekly report to manual counts for two weeks.

Success metrics:

- bookings by channel;
- no-show rate;
- rebooking rate.

Confidence: medium because current notes are inconsistent.

Fallback: manual Google Sheet template.

## Verification Appendix

Claims:

- CLM-001: reminders are currently manual. Evidence: domain input current
  workflow step 6.
- CLM-002: no-shows are a pain point. Evidence: domain input pain points.
- CLM-003: personal contact data is used. Evidence: domain input data fields.

Assumptions:

- ASM-001: appointment volume is 70-100 per week.
- ASM-002: salon has permission to message customers on selected channels.
- ASM-003: service menu and prices can be made stable enough for assistant use.

Blocking findings: none for deterministic reminder pilot; booking assistant
requires policy and availability validation.
