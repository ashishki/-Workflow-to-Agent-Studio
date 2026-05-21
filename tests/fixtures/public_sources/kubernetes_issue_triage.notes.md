# Kubernetes Issue Triage Public Source Notes

Source URL: https://www.kubernetes.dev/docs/guide/issue-triage/
Accessed: 2026-05-21
Dataset kind: public-source experiment only; not operator pilot evidence.

These notes paraphrase the public Kubernetes issue triage guidance for a local
Workflow-to-Agent Studio experiment.

Workflow context:

- Kubernetes uses GitHub Issues and pull requests as public intake channels for
  bugs, feature requests, support-like requests, and contributor work.
- New issues begin as untriaged work and need review by contributors or SIG
  members before they become actionable.
- Labels are the primary workflow controls. Examples include needs-triage,
  triage/accepted, triage/needs-information, kind/support, help wanted,
  good first issue, priority labels, SIG labels, and lifecycle labels.
- A triager reviews newly created open issues, searches for duplicates, checks
  whether the issue belongs to the repository, and decides the right issue kind.
- Support requests are redirected to support channels and can be labelled for
  closure instead of becoming engineering work.
- Bug reports should be reproduced when possible. Reproducible bugs can be
  prioritized, searched for duplicates, and routed to the right SIG.
- If a bug cannot be reproduced, the triager contacts the reporter and may close
  the issue if both sides agree it is not reproducible.
- If more details are needed, the triager comments with a needs-information
  request and applies the relevant triage label.
- SIG ownership is assigned with SIG labels or bot commands. If ownership is
  unclear, the triager should defer to SIG labelling instead of over-routing.
- Follow-up rules handle work that stalls: no pull request in the release cycle,
  no SIG movement after a waiting period, or no activity long enough to become
  stale.

Actors:

- Issue reporter
- Triage contributor
- SIG member or SIG owner
- Kubernetes bot
- Issue owner or assignee

Systems:

- GitHub Issues
- GitHub labels
- Kubernetes bot commands
- Triage Party
- GitHub project boards
- DevStats dashboards
- Support channels

Trigger:

- A new GitHub issue or pull request needs Kubernetes triage.

Decisions:

- Is the item a support request, duplicate, abandoned item, wrong repository, bug,
  help wanted candidate, or good first issue?
- Does a bug have enough information to reproduce?
- Which priority and SIG labels should be applied?
- Should the triager ask for more information, close the issue, accept triage,
  assign an owner, mark stale, or notify a SIG?

Data fields:

- issue number
- issue kind
- reporter
- labels
- SIG owner
- priority
- reproduction status
- duplicate reference
- needs-information status
- stale lifecycle state
- assignee
- linked pull request

Pain points:

- High public issue volume can slow contributor response.
- Support requests can crowd out actionable engineering issues.
- SIG ownership can be unclear.
- Stale or unowned issues require consistent follow-up.
