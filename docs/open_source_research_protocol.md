# Open-Source Workflow Research Protocol

Status: active
Date: 2026-05-23

This protocol tells future agents what to do when a workflow-blueprint task
needs source material but no prospect or customer workflow packet is available.
The agent must collect public workflow evidence and produce demo-quality
artifacts while preserving the boundary that public sources are not buyer proof.

## When To Research

Use open-source research when a task needs:

- a realistic workflow source;
- domain-specific actors, systems, decisions, exceptions, or data fields;
- public examples for a demo blueprint;
- missing questions or approval boundaries for an automation candidate;
- evidence to support a portfolio showcase.

## Allowed Sources

- public GitHub issues, discussions, PR templates, contribution guides, and
  public repository documentation;
- public operational docs, help centers, support runbooks, and product docs;
- public forum threads that describe a repeatable workflow;
- public company FAQ/booking/support pages when used only as public demo
  workflow evidence;
- public issue triage, support intake, incident response, onboarding, lead
  intake, or invoice approval examples.

Prefer sources that expose observable workflow facts: actors, intake fields,
systems, decisions, escalations, unsafe-answer boundaries, approvals,
exceptions, and handoff points. Marketing pages are allowed only when they
describe the actual public workflow being modeled.

## Forbidden Sources

- private client docs, private communities, private repositories, credentials,
  or production exports without explicit human approval;
- raw personal data, tokens, cookies, private channel IDs, or unredacted
  usernames in committed fixtures;
- copied page dumps, screenshots, or forum excerpts that cannot be redistributed
  safely as committed fixtures;
- claims that a public-source demo proves buyer acceptance, conversion lift, or
  paid demand.

## Required Source Register

Every research-backed demo pack must include:

| Field | Required |
|---|---|
| source_url_or_locator | yes |
| captured_at | yes |
| source_type | yes |
| workflow_kind | yes |
| extracted_workflow_facts | yes |
| limitations | yes |
| public_demo_only | yes |

Keep committed artifacts small: source links, short snippets, command
transcripts, generated blueprint, review workspace, and gap summary. Do not
commit large raw page dumps unless they are sanitized fixtures.

`public_demo_only` must be true for every source gathered under this protocol.
If a source cannot support a workflow fact, record that limitation instead of
turning it into an assumption-free blueprint claim.

## Claim Rule

Public sources may support demo quality and source-grounding claims. They do
not support commercial pilot pass/fail claims. A real pilot row still requires a
human-reviewed prospect or customer workflow source in `docs/pilot_measurement.md`.
