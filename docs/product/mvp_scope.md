# MVP Scope

## MVP Goal

Prove that one operator can take a business workflow description and produce a
useful, evidence-linked AI implementation roadmap with privacy, risk, cost,
priority, rollout, and verification reasoning.

## In Scope

- Business intake schema.
- Text, Markdown, and CSV-like workflow inputs.
- Clarifying questions.
- Workflow decomposition.
- Data inventory.
- AI opportunity map.
- Do-not-automate list.
- Pattern matching for 10-15 SMB patterns.
- Privacy sensitivity classification.
- Security risk classification.
- Cost/time/team estimate ranges.
- Priority scoring bands.
- Roadmap report generator.
- Claims, assumptions, evidence, and recommendation trace registry.
- Markdown export.
- Three polished synthetic demo reports:
  - hair salon / beauty business;
  - small e-commerce store;
  - immigration/legal consultancy.
- Golden fixture evals.

## Out Of Scope

- Multi-tenant SaaS.
- Production agent builder.
- Automatic deployment.
- Live CRM/helpdesk writes.
- SOC 2, HIPAA, GDPR, or legal compliance claims.
- On-prem installer.
- Full BPMN editor.
- Real-time process mining.
- Autonomous legal, medical, financial, or HR decisions.
- ROI guarantee.

## MVP Success Criteria

- One command can generate each synthetic demo report locally.
- Every recommendation has evidence or explicit assumptions.
- Every recommendation includes privacy class, cost range, time range, risks,
  validation method, and fallback.
- High-risk workflows include human approval gates.
- Privacy-restricted workflows cannot recommend unrestricted cloud processing.
- The export includes a verification appendix.
- A reviewer can mark a report as client-ready or not with specific findings.

## 20 Percent That Delivers 80 Percent

- Roadmap report contract.
- Recommendation card schema.
- Privacy classifier.
- Cost and priority engines.
- Pattern library.
- Verification receipt.
- Three polished demo reports.

## Commercial Boundary

The MVP can support productized consulting experiments. It cannot support public
claims of buyer validation until real pilot rows exist in
`docs/pilot_measurement.md`.
