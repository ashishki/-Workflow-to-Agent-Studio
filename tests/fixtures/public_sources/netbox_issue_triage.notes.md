# NetBox Issue Triage Public Source Notes

Source URL: https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow
Accessed: 2026-05-20
Dataset kind: public-source experiment only; not operator pilot evidence.

These notes paraphrase the public NetBox GitHub issue triage workflow for a local
Workflow-to-Agent Studio experiment.

Workflow context:

- GitHub Issues is the recognized intake channel for new NetBox issue reports,
  feature requests, support-like requests, bug reports, and pull request follow-up.
- A reporter opens an issue from a provided template and is expected to answer
  maintainer questions in a timely way.
- A maintainer reviews each inbound issue report, checks whether it follows the
  expected template, and decides whether the issue can move forward.
- The maintainer may close items that do not follow the template, duplicate an
  existing issue, describe unsupported configuration help, or fall outside the
  project scope.
- For bug reports, the maintainer checks whether the report has enough detail to
  reproduce the behavior on a clean installation and whether the reporter has
  verified the behavior on a current stable release.
- For feature requests, the maintainer checks whether the request includes a
  detailed use case, proposed behavior, affected surfaces such as views or APIs,
  and enough implementation detail to be actionable.
- If details are missing, the maintainer asks the reporter for clarification
  before accepting the issue or creating follow-up work.
- Issues that remain without requested updates can become stale and can
  eventually be closed if no additional information arrives.
- Accepted issues need a clear problem statement, next action, and owner before
  engineering review or pull request work should proceed.

Actors:

- Reporter
- Maintainer or triager
- Contributor or engineering owner

Systems:

- GitHub Issues
- Issue templates
- Issue labels or GitHub issue types
- Canned maintainer responses
- Project backlog

Trigger:

- A new issue, feature request, bug report, support-like request, or pull request
  arrives in GitHub.

Decisions:

- Does the submission follow the required template?
- Is the report a duplicate, out of scope, support request, expected behavior, or
  reproducible bug?
- Does the feature request include enough detail and a justified use case?
- Should the maintainer ask for more information, close the issue, mark it stale,
  accept it, or route it to engineering review?

Data fields:

- Issue type
- Reporter
- Template completion state
- Product version
- Reproduction steps
- Expected behavior
- Actual behavior
- Use case
- Scope decision
- Owner
- Follow-up task or linked pull request

Pain points:

- Maintainers repeatedly check templates and request missing details.
- Vague reports can create manual back-and-forth before any engineering review.
- Duplicate, support, and out-of-scope submissions consume triage time.
- Stale issues require consistent follow-up and closure decisions.

Experiment note:

- This source is useful for exercising ingestion, retrieval, blueprint synthesis,
  and review exports against a public workflow.
- This source does not prove buyer demand, operator acceptance, real reviewer
  edits, or time-to-reviewable performance in a live pilot.
