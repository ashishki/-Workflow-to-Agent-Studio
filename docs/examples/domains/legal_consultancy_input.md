# Immigration And Legal Consultancy Workflow Input

Dataset kind: synthetic demo only. Not customer proof or pilot evidence.

## Business Context

Business: immigration consultancy helping individuals prepare visa/residency
applications.

Goal: reduce repeated status questions and missing-document back-and-forth while
keeping legal judgment and case strategy under consultant control.

## Current Workflow

1. Lead submits inquiry through website.
2. Coordinator asks country, visa type, deadline, and family member details.
3. Consultant schedules call.
4. After call, client receives document checklist.
5. Client uploads documents by email or shared drive.
6. Coordinator checks completeness manually.
7. Consultant reviews legal strategy.
8. Client asks repeated questions about status and missing documents.

## Actors

- lead/client;
- coordinator;
- consultant;
- document reviewer.

## Systems

- website form;
- email;
- shared drive;
- calendar;
- document checklist;
- case tracker.

## Pain Points

- missing documents;
- repeated status questions;
- slow intake;
- consultant time spent on admin;
- checklist consistency depends on coordinator memory.

## Data Fields

- passport copy;
- address;
- employment history;
- family details;
- legal status;
- deadline;
- government form names;
- document checklist status.

## Sensitive Data Notes

This workflow contains restricted identity and legal-status data. Raw documents
should not be sent to a default cloud LLM path.

## Boundaries

Do not automate:

- legal eligibility decisions;
- legal strategy;
- final advice;
- document submission to authorities;
- client-facing legal interpretation without consultant review.
