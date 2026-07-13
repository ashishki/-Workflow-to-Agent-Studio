# Public interview-fixture and evidence-mapping guide

Status reviewed: 2026-07-13
Scope: public synthetic fixtures and unsupported evidence-mapping reports

## Publication boundary

The public repository does not need a real interview, SOP, customer workflow,
screen recording, support ticket, system export, or operator account to
reproduce an evidence-mapping defect. Public fixtures must be authored from
scratch and contain invented, people-free workflow facts. Do not start with
private material and redact or paraphrase it.

Sanitization is not a promise of anonymity. Names can be removed while unusual
steps, timings, systems, identifiers, or quoted phrasing still identify an
organization or person. Consent to review a real workflow does not imply
permission to publish it. Real-owner material remains local/private unless the
owner has approved the exact publication bytes and a separate privacy and legal
review has accepted the disclosure.

Never publish any of the following in a fixture, issue, pull request, CI log, or
evidence pack:

- interview or call transcripts, SOP text, internal notes, screenshots,
  recordings, tickets, forms, prompts, model/provider output, or database rows;
- names, contacts, account/customer identifiers, exact dates or locations,
  private URLs, local absolute paths, source-system IDs, or rare business facts;
- credentials, tokens, cookies, connection strings, configuration secrets,
  private repository content, or production endpoints;
- commercially sensitive prices, volumes, conversion or ROI figures, personnel
  decisions, health/legal/financial facts, or claims about a real owner;
- content described merely as "redacted", "anonymized", or "sanitized" without
  authored-synthetic provenance.

If a secret or private record is exposed, stop publication, remove it from the
change, rotate or revoke credentials where applicable, and use the private
security-advisory route. Deleting a later Git commit does not retract copies
that were already fetched.

## Authoring an allowed fixture

1. Choose one narrow parser or evidence-mapping behavior. Do not recreate a
   complete real workflow.
2. Write a new fictional source using generic actors such as `operator` and
   `reviewer`, generic systems such as `queue` and `record system`, and invented
   IDs that cannot map to runtime data.
3. Add a provenance header with `fixture_origin: authored-synthetic`, a stable
   fixture ID, the supported source kind, and the schema or contract revision.
4. State the exact expected source span and destination field. Include an
   explicit no-map or missing-question case so the test does not reward only
   extraction.
5. Keep the fixture minimal. Omit real company names, industry-specific rare
   details, dates, URLs, contacts, metrics, credentials, and absolute paths.
6. Add a failing-then-passing deterministic regression. Network/provider calls
   must be disabled or replaced by fake transport.
7. Review the final bytes manually. A marker scan can find known patterns but
   cannot prove non-derivation or anonymity.
8. Record the exact repository revision, command, exit code, fixture hash, and
   tested limitation.

The existing files under `tests/fixtures/sources/` are small repository-owned
fixtures for local mechanics. They are not customer records, observed workflow
evidence, or proof that a mapping generalizes to a real interview.

## Unsupported evidence-mapping report

The public issue form accepts one bounded defect where a supported synthetic
source span is missing, mapped to the wrong blueprint field, cited
incorrectly, or accepted when it should abstain. A complete report provides:

- the full 40-character repository revision;
- a repository path to an authored-synthetic fixture and its SHA-256;
- source kind, exact synthetic span, expected destination field, and observed
  destination or abstention;
- a credential-free command and exit code;
- the smallest proposed failing-then-passing test;
- the furthest boundary exercised: static, unit, local CLI, or local storage;
- explicit confirmation that no real/private source or live provider ran.

Generic feature requests, requests to process private interviews, autonomous
deployment proposals, ROI claims, hosted-product roadmaps, and source types not
supported by the documented contract are outside this intake. Opening an issue
does not grant a license to reuse repository code and does not make a proposed
mapping or source type supported.

## Reproduce the current synthetic boundary

```bash
python -m pytest \
  tests/unit/test_docs.py \
  tests/eval/test_real_world_corpus_eval.py \
  tests/eval/test_retrieval_eval.py -q
```

Despite the historical test filename `test_real_world_corpus_eval.py`, its
checked-in inputs are repository fixtures. The run tests local mapping and
retrieval mechanics only. It does not establish an observed case, real-owner
acceptance, privacy guarantees, external use, buyer validation, or production
fitness.

## Real-owner review remains separate

A real review may be recorded only with a named consenting owner, local/private
source handling, explicit retention/deletion rules, and approval of the exact
result that will be documented. Public reporting should normally contain only
aggregate process metadata and limitations, not source content. Until such a
review exists, the release and pilot gates stay open; synthetic fixtures must
not be promoted into a pilot row or owner outcome.
