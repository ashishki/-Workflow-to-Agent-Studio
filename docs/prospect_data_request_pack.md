# Solo Prospect Data Request Pack

Status: request template; not pilot proof
Date: 2026-05-23

This pack is for a solo operator manually asking one prospect for one narrow
workflow packet. It uses the public demo packs as demonstration material only;
the public packs are not proof that the product worked for a customer.

## Request Goal

Ask for one workflow packet that is specific enough to generate a reviewable
automation blueprint without broad system access.

Accepted packet types:

- one SOP;
- one transcript;
- one pasted notes file;
- one form description;
- one integration excerpt;
- one mixed packet combining the items above for a single workflow.

Keep the request narrow: one workflow, one reviewer, one follow-up review.

## Message Template

Subject: Request for one workflow packet for a local blueprint demo

Hi [name],

I am testing a local workflow-to-automation blueprint tool. Could you share one
narrow workflow packet for a single operational process? Good examples are an
SOP, a short transcript, pasted notes, a form description, an integration
excerpt, or a mixed packet that explains one workflow.

I will process it locally, use it only to generate a draft blueprint for human
review, and send you the reviewable output before making any claim from it. I do
not need system access, credentials, private keys, exports from production
databases, or regulated personal data.

The public demo pack here is only demonstration material, not proof:
`docs/experiments/public_demo_pack/hvac_lead_intake/`

If you are open to it, I also need one named reviewer who can confirm accepted
sections, edits, critical missing questions, and whether the draft is useful
enough to count as a real pilot measurement.

## Local Processing Boundary

- Process the supplied packet locally.
- Do not request credentials, production tokens, private keys, database dumps,
  regulated personal data, or broad system access.
- Do not publish, send, or reuse the source outside the local review flow unless
  the prospect explicitly approves sanitized benchmark reuse.
- Keep raw source text out of logs, metrics, committed fixtures, and public demo
  materials.

## Human Review Request

Ask the reviewer to record:

- accepted required blueprint sections;
- substantive edits needed before use;
- critical missing questions;
- unsupported claims;
- wrong approval boundaries;
- weak eval cases;
- wrong or invented integrations;
- final pass/fail against the pilot thresholds in `docs/pilot_measurement.md`.

## Optional Sanitized Benchmark Reuse

Ask separately:

> May a sanitized summary of this workflow be reused later as an internal
> benchmark fixture? Sanitization removes common PII, credentials, customer or
> account identifiers, private URLs, and raw source text. Declining does not
> affect the pilot review.

Benchmark reuse is optional and does not convert the source into public proof.

## Public Demo Attachment

Attach or reference only public-demo material:

- `docs/experiments/public_demo_pack/hvac_lead_intake/`
- `docs/experiments/public_demo_pack/netbox_issue_triage/`
- `docs/experiments/public_demo_pack/gitlab_incident_response/`

Label these as public-source demos, not buyer validation or pilot proof.

## Minimum Intake Checklist

- one workflow packet is attached or pasted;
- packet source kind is recorded;
- packet contains no credentials, secrets, private keys, regulated personal
  data, or production database exports;
- local processing permission is explicit;
- named reviewer is identified;
- reviewer agrees to record edits, accepted sections, missing questions, and
  pass/fail outcome;
- sanitized benchmark reuse is either approved or declined separately.
