# OpenStack Bug Triage Public Source Notes

Source URL: https://wiki.openstack.org/wiki/BugTriage
Accessed: 2026-05-21
Dataset kind: public-source experiment only; not operator pilot evidence.

These notes paraphrase the public OpenStack bug triage workflow for a local
Workflow-to-Agent Studio experiment.

Workflow context:

- OpenStack bug triage is organized as a prioritized list of recurring tasks.
- Some tasks can be performed by anyone, while priority and patch-review steps
  require bug supervisor rights or core team authority.
- New bugs start in a New state and need feedback to determine whether they are
  genuine and actionable.
- A triager reviews whether the bug report is complete enough to reproduce.
- If information is missing, the triager asks the reporter for more information
  and sets the bug status to Incomplete.
- If the report has enough information and appears valid or reproducible, the
  triager sets the status to Confirmed.
- If the bug has security implications, the triager sets the security flag.
- If the bug affects a known area, an official tag can be added.
- Bug supervisors prioritize confirmed bugs using importance values such as
  Critical, High, Medium, Low, or Wishlist.
- Critical bugs block key functionality for all users or risk data loss. High
  bugs affect key functionality for some users. Lower severities cover secondary
  or cosmetic issues.
- Some bug states need consistency repair, such as New bugs that already have a
  priority or In Progress bugs without an assignee.
- Incomplete bugs are periodically reviewed. If the reporter answers, the bug can
  become Confirmed; if more detail is still needed, the triager asks again.
- If the reporter never provides enough information, the bug can be closed as
  Invalid after reminders.
- Bugs with patches are reviewed by supervisors and can be marked Triaged when a
  patch looks like a likely solution.
- Stale In Progress bugs are reviewed and can be unassigned or moved back to New
  and Undecided.

Actors:

- Bug reporter
- Bug triager
- Bug supervisor
- Core project team
- Project driver

Systems:

- Launchpad bug tracker
- Bug status fields
- Bug importance fields
- Security flag
- Official tags
- Bug-count graphs

Trigger:

- A new or existing OpenStack bug needs triage, priority, consistency repair,
  incomplete review, stale review, or patch review.

Decisions:

- Is the report incomplete, reproducible, confirmed, invalid, security-sensitive,
  stale, patched, or ready to mark Triaged?
- Which importance level should a confirmed bug receive?
- Does a stale In Progress bug still have an active assignee?
- Should an incomplete bug be reminded, confirmed, or closed as Invalid?

Data fields:

- bug status
- importance
- reporter
- project area
- reproduction details
- security flag
- official tag
- assignee
- patch presence
- milestone
- reminder state

Pain points:

- Missing reproduction details create repeated follow-up.
- Bug states can become inconsistent.
- Stale In Progress bugs can hide inactive ownership.
- Priority and milestone decisions require supervisor or driver authority.
