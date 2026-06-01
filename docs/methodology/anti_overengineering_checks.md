# Anti-Overengineering Checks

Purpose: keep the product from recommending agents where simpler automation is
safer, cheaper, and easier to maintain.

## Required Questions

Before recommending an LLM or agent:

1. Can a reminder, rule, script, or API integration solve the pain?
2. Is the workflow stable enough to automate?
3. Is the output easy to verify?
4. Does the business have enough volume to justify the build?
5. Is there an accountable owner?
6. Are the relevant policies current?
7. Is the privacy mode safe?
8. Can the system fail closed?
9. Is a human review gate needed?
10. Can the recommendation be evaluated with examples?

## Red Flags

- "Agent" is recommended before a process map exists.
- LLM is used for deterministic lookup.
- High-autonomy appears in the MVP plan.
- Cost estimate ignores maintenance.
- Privacy mode is chosen after architecture, not before.
- The report lacks do-not-automate items.
- The recommendation cannot name a workflow step.
- The eval plan is "review manually" without sample size or criteria.
- The output recommends automatic decisions in legal, medical, financial, HR, or
  identity-sensitive contexts.

## Preferred Alternatives

| Overbuilt Recommendation | Simpler First Option |
|--------------------------|----------------------|
| Agent books appointments end-to-end | deterministic reminders + assistant draft + calendar availability check |
| AI decides refunds | assistant drafts recommendation, owner approves |
| Legal strategy agent | checklist completeness assistant with consultant review |
| Medical intake agent | intake checklist and reminder automation, no diagnosis |
| AI sales closer | lead summary and follow-up draft with human send |
| AI reporting copilot | scheduled deterministic dashboard plus LLM explanation |
