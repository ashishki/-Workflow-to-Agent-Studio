# Hair Salon Workflow Input

Dataset kind: synthetic demo only. Not customer proof or pilot evidence.

## Business Context

Business: beauty salon with four stylists.

Channels:

- Instagram DM;
- WhatsApp;
- phone;
- Google Calendar.

Approximate volume: 70-100 appointments per week.

Goal: reduce missed messages, no-shows, and manual receptionist work without
introducing unsafe customer decisions.

## Current Workflow

1. Client messages on Instagram or WhatsApp.
2. Receptionist asks service type, preferred date, and stylist preference.
3. Receptionist checks Google Calendar manually.
4. Client confirms time.
5. Receptionist writes booking into calendar.
6. One day before appointment, receptionist sends reminder manually.
7. If the client cancels late or does not show, the note is kept inconsistently.
8. After visit, stylist may suggest rebooking, but follow-up is manual.

## Systems

- Instagram;
- WhatsApp;
- phone;
- Google Calendar;
- informal notes.

## Actors

- client;
- receptionist;
- stylist;
- owner.

## Pain Points

- missed messages during busy hours;
- no-shows;
- repeated questions about prices and availability;
- inconsistent rebooking;
- owner does not know which channel brings most bookings.

## Data Fields

- client name;
- phone number or social handle;
- appointment date/time;
- stylist preference;
- service type;
- service price;
- cancellation/no-show note;
- booking channel.

## Sensitive Data Notes

The workflow contains personal contact data and appointment preferences. It does
not require medical, payment-card, legal, or identity documents.

## Boundaries

Do not automate:

- stylist-specific medical or skin-condition advice;
- cancellation penalty decisions;
- customer complaint resolution;
- final calendar writes without deterministic availability check.
