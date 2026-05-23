# Apache Airflow Issue Triage Public Source Notes

Source URL: https://apache.googlesource.com/airflow/+/7ab6dc2ecf362916cde19f2c761cb3103dbc824b/ISSUE_TRIAGE_PROCESS.rst
Accessed: 2026-05-23
Dataset kind: public-source test example only; not customer proof or pilot evidence.

These notes paraphrase Apache Airflow's public issue reporting and triage
process for local Workflow-to-Agent Studio tests.

Workflow context:

- Apache Airflow tracks issues and discussions in GitHub.
- Users can report bugs or small feature requests through issue templates.
- Issues should represent clear, small feature requests or reproducible bugs.
- Troubleshooting or unclear reports may be converted to GitHub Discussions with
  an explanation.
- Triage values relatively quick responses so reporters do not feel ignored.
- Issue triage team members can assign, edit, close issues and pull requests,
  convert issues to discussions and back, add labels, ask for more information,
  and involve committers or other community members.
- Triage team members do not have committer privileges and cannot merge code by
  that role alone.

Actors:

- Issue reporter
- Issue triage team member
- Airflow committer
- Community helper
- Pull request author

Systems:

- GitHub Issues
- GitHub Discussions
- GitHub issue templates
- Labels
- Milestones
- Priorities
- Pull requests

Trigger:

- A new Airflow issue, discussion, or pull request needs a response, label,
  conversion, closure, assignment, or escalation.

Decisions:

- Is the report a bug, feature request, troubleshooting discussion, duplicate,
  invalid report, or clear actionable issue?
- Should the issue be converted to a discussion?
- Is additional information needed from the reporter?
- Which labels, milestone, or priority should apply?
- Should a committer or knowledgeable community member be mentioned?

Data fields:

- issue type
- template type
- reproducible steps
- discussion status
- labels
- milestone
- priority
- pending response status
- assignee
- linked pull request

Unsafe-answer boundaries:

- Do not merge code or represent triage-team privileges as committer privileges.
- Do not close or convert public issues without human reviewer authority.
- Do not treat public-source test examples as T34, T40, or pilot evidence.
