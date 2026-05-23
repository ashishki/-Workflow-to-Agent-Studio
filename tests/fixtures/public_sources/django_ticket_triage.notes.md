# Django Ticket Triage Public Source Notes

Source URL: https://docs.djangoproject.com/en/dev/internals/contributing/triaging-tickets/
Accessed: 2026-05-23
Dataset kind: public-source test example only; not customer proof or pilot evidence.

These notes paraphrase Django's public ticket triage documentation for local
Workflow-to-Agent Studio tests.

Workflow context:

- Django uses Trac for ticket management and GitHub for pull request review.
- Ticket triage is organized around stages that show what or who the ticket is
  waiting on.
- Public roles include triagers, bug fixers, reviewers, and mergers.
- Unreviewed tickets enter a triage queue and may need refinement before being
  accepted.
- Accepted tickets can wait for a patch, PR review, or author changes depending
  on flags such as has patch, needs tests, needs documentation, and patch needs
  improvement.
- Ready for checkin means a community review found the change commit-ready, but
  a merger still gives final review before commit.
- Triagers can close sparse tickets as needsinfo, correct flags, set easy
  pickings, categorize ticket type/component/severity, and leave comments.

Actors:

- Ticket reporter
- Triager
- Bug fixer
- Reviewer
- Merger

Systems:

- Django Trac
- GitHub pull requests
- Trac flags
- Review queue
- Django Forum

Trigger:

- A new or updated Django ticket or pull request needs triage, review, flag
  correction, or final check-in decision.

Decisions:

- Is the ticket unreviewed, accepted, ready for checkin, someday/maybe, or
  closed?
- Does the ticket describe a valid and actionable issue?
- Does a patch need tests, documentation, or improvement?
- Should the ticket be categorized as bug, new feature, or cleanup?
- Does a merger need to give final review?

Data fields:

- ticket stage
- ticket type
- component
- severity
- version
- has patch flag
- needs tests flag
- needs documentation flag
- patch needs improvement flag
- easy pickings flag
- reviewer comment

Unsafe-answer boundaries:

- Do not mark a ticket as merged without merger review.
- Do not claim a public Django ticket workflow proves customer demand.
- Do not treat public-source test examples as T34, T40, or pilot evidence.
