# AI Suitability Classification

Purpose: prevent "agent everywhere" recommendations and route each workflow step
to the simplest sufficient solution.

## Allowed Solution Types

| Type | Use When | Avoid When |
|------|----------|------------|
| Do not automate yet | evidence is missing, risk is high, owner/eval unclear | the process is stable and low-risk |
| Classic script | deterministic trigger/action exists | natural-language judgment is central |
| API integration | source/target systems have reliable APIs | identity, permissions, or data quality are unclear |
| RPA | no API exists but UI workflow is stable | UI changes frequently or stakes are high |
| LLM assistant | drafting, summarization, classification, or operator support is useful | output will be executed without review in high-risk context |
| RAG knowledge assistant | answers should cite controlled docs | source docs are stale or access control is unresolved |
| Human-in-the-loop workflow | AI can propose, human must decide | no accountable reviewer exists |
| Bounded AI agent | repetitive multi-step task has clear tools, permissions, and stop conditions | tool boundaries or evals are unclear |
| High-autonomy agent - future only | low-risk, mature process after multiple validated pilots | MVP, regulated decisions, or unclear policies |

## Classification Questions

1. Is the step repetitive?
2. Is the process stable?
3. Is the input data available and clean?
4. Is the expected output easy to verify?
5. Is a human reviewer available?
6. What happens if the system is wrong?
7. Does a deterministic integration solve most of the pain?
8. Is sensitive or regulated data involved?
9. Is the business rule explicit or judgment-heavy?
10. Can a golden test set be created?

## Blocking Rules

- Do not recommend high-autonomy agents for legal, medical, financial, HR, or
  identity-sensitive decisions.
- Do not recommend automatic refunds, rejections, approvals, eligibility
  decisions, or legal advice in MVP.
- Do not recommend cloud LLM analysis for restricted data unless the report
  states redaction/private controls and human approval.
- Do not recommend AI when a deterministic reminder, lookup, or report solves
  the workflow.

## Required Rationale

Every classification must state:

- why this solution type fits;
- why simpler options are insufficient or sufficient;
- what data is required;
- what risk remains;
- what human gate applies;
- what fallback exists.
