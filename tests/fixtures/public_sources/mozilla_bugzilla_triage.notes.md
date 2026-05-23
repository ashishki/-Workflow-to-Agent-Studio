# Mozilla Bugzilla Triage Public Source Notes

Source URL: https://wiki.mozilla.org/Bug_Triage/Projects/Bug_Handling/Triage_Rules
Accessed: 2026-05-23
Dataset kind: public-source test example only; not customer proof or pilot evidence.

These notes paraphrase Mozilla's public Bugzilla triage guidance for local
Workflow-to-Agent Studio tests.

Workflow context:

- Mozilla bug triage uses Bugzilla queries for components a triager is
  responsible for.
- Untriaged query setup filters open bugs for selected components, excludes
  already triaged whiteboard tags, and excludes bugs with active needinfo.
- A second saved query tracks triaged bugs by looking for triage whiteboard tags.
- Triage may run daily for components with enough incoming bugs.
- Triagers are encouraged to close work early when a bug or enhancement will not
  be pursued.
- Bugs with crash, regression, or security keywords receive higher attention.
- Triage outcomes use whiteboard tags such as fix now, active, fix later,
  backlog, needs component, and follow-up.
- Follow-up outcomes require needinfo or dependency tracking when the triager
  cannot make a decision yet.

Actors:

- Bug reporter
- Component triager
- Engineer or volunteer
- Component team
- Release or priority owner

Systems:

- Bugzilla
- Saved bug queries
- Component fields
- Whiteboard tags
- Needinfo flag
- Dependency bugs
- Release flags

Trigger:

- A new open Bugzilla bug in a component needs categorization, priority, closure,
  follow-up, or assignment.

Decisions:

- Is the bug already triaged or still untriaged?
- Is the issue a critical crash, regression, or security-sensitive item?
- Should the bug be fixed now, active in an iteration, fixed later, backlogged,
  sent to another component, closed, or followed up?
- Is needinfo required before a decision can be made?
- Should release flags, priority, dependency, or assignment be updated?

Data fields:

- component
- bug status
- resolution
- creation date
- keywords
- whiteboard tags
- needinfo flag
- crash/regression/security markers
- priority
- release flags
- dependency bug

Unsafe-answer boundaries:

- Do not change Bugzilla state without an authorized triager or owner.
- Do not expose sensitive security-bug details in public fixtures.
- Do not treat public-source test examples as T34, T40, or pilot evidence.
