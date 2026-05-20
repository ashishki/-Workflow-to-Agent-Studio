# Automation Blueprint

Status: Draft
Blueprint Version ID: 1

## Workflow Summary
GitHub Issues triage workflow routes public issue submissions through template checks, duplicate and scope review, reproducibility checks, stale handling, and engineering ownership decisions.

## Actors
- Reporter: Workflow participant
- Maintainer or triager: Workflow participant
- Contributor or engineering owner: Workflow participant

## Systems
- GitHub Issues: Workflow system
- Issue templates: Workflow system
- Issue labels or GitHub issue types: Workflow system
- Canned maintainer responses: Workflow system
- Project backlog: Workflow system

## Triggers
- New GitHub issue, feature request, bug report, support-like request, or pull request

## Current Workflow
- step-1: Reporter opens a GitHub issue using the expected template. [Reporter]
- step-2: Maintainer checks template completion, issue type, scope, and duplicate status. [Maintainer or triager]
- step-3: Maintainer asks for clarification when reproduction steps or feature details are missing. [Maintainer or triager]
- step-4: Accepted issues move toward ownership, engineering review, or linked pull request work. [Contributor or engineering owner]

## Decisions
- Decide whether the submission follows the required issue template
- Decide whether the issue is duplicate, out of scope, support-oriented, or expected behavior
- Decide whether a bug report is reproducible on a current stable release
- Decide whether a feature request has a justified use case and enough implementation detail
- Decide whether to ask for more information, mark stale, close, accept, or route to engineering review

## Exceptions
- Missing template fields require maintainer clarification before acceptance
- Duplicate, support-like, or out-of-scope issues can be closed
- Issues without requested follow-up can become stale and eventually close

## Data Fields
- issue type: Workflow data field: issue type (source: GitHub Issues)
- reporter: Workflow data field: reporter (source: GitHub Issues)
- template completion state: Workflow data field: template completion state (source: GitHub Issues)
- product version: Workflow data field: product version (source: GitHub Issues)
- reproduction steps: Workflow data field: reproduction steps (source: GitHub Issues)
- expected behavior: Workflow data field: expected behavior (source: GitHub Issues)
- actual behavior: Workflow data field: actual behavior (source: GitHub Issues)
- use case: Workflow data field: use case (source: GitHub Issues)
- scope decision: Workflow data field: scope decision (source: GitHub Issues)
- owner: Workflow data field: owner (source: GitHub Issues)
- linked pull request: Workflow data field: linked pull request (source: GitHub Issues)

## Integration Map
- GitHub Issues -> Project backlog: issue type, reporter, template completion state, product version, reproduction steps, expected behavior, actual behavior, use case, scope decision, owner, linked pull request

## Pain Points
- Maintainers repeatedly check issue templates and request missing details
- Duplicate, support, and out-of-scope submissions consume triage time
- Stale issues require consistent follow-up and closure decisions

## Automation Candidates
- Draft issue triage recommendation: risk=high; implementation boundary=Draft triage recommendation only; do not close, label, or route issues automatically.; approval boundary=Maintainer approves before issue status, labels, closure, or engineering routing change.

## Human Approval Boundaries
- Approve issue triage recommendation: Maintainer or triager - Triage changes can close public issues or create engineering commitments.

## Risks And Assumptions
- risk: Missing issue details can lead to incorrect closure or delayed engineering review.
- assumption: Who has final authority to accept an issue for engineering review?

## Eval Cases
- Issue triage recommendation: when Issue includes template fields, version, reproduction details, and scope context., expect Blueprint recommends a maintainer-reviewed triage action without mutating GitHub issue state automatically.; verify by Inspect automation candidate and evidence link.

## Observability Needs
- Track draft triage recommendations, maintainer overrides, stale decisions, and blocked cases. (assumption)

## Rough Effort Band
small

## Next Implementation Tasks
- impl-1: engineer; AC: Draft triage recommendation is generated from source evidence.; Tests: Blueprint synthesis integration test.

## Unresolved Findings
- none

## Evidence Appendix
- src-public-demo-netbox-issue-triage-43ed4794166744ef / src-public-demo-netbox-issue-triage-43ed4794166744ef:chunk-17
