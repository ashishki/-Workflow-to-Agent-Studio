# Security and source-data reporting policy

Workflow-to-Agent Studio is a local workflow-discovery prototype, not a hosted
service. Reports are accepted only for the current default branch and its
documented local ingestion, sanitization, storage, evidence-linking, blueprint,
export, and synthetic/public-demo boundaries. There is no production
deployment, customer workflow access, external pilot, supported provider
account, or security SLA.

Do not open a public issue for a suspected vulnerability or source-data
exposure. Email `verter25@gmail.com` with subject
`Workflow-to-Agent-Studio security report`. Include the exact revision,
prerequisites, a minimal authored-synthetic reproduction, impact, and suggested
mitigation. Keep the first message minimal. Do not attach interviews, calls,
SOPs, customer workflows, screenshots, recordings, tickets, credentials,
tokens, `.env`, prompts or provider output, database content, private URLs,
local paths, or an exploit against a system or data you do not own. A safer
detail-transfer path can be agreed before details are sent.

GitHub private vulnerability reporting is not assumed to be enabled. Use a
GitHub private advisory form only if the repository Security page visibly
offers **Report a vulnerability**. This maintainer-run prototype cannot promise
a response or remediation deadline.

If a credential or private source is exposed, stop publication and rotate or
revoke affected credentials. Removing a later commit does not retract copies
already fetched. Follow `docs/SANITIZED_INTERVIEW_FIXTURES.md` for the public
fixture boundary.
