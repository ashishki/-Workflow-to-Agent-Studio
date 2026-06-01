# LLM Boundaries

Purpose: define which parts of roadmap generation may use model judgment and
which parts must remain deterministic.

## LLM-Owned Drafting

Allowed:

- extract tentative workflow steps from messy prose;
- propose clarifying questions;
- summarize business context;
- infer pain points from evidence;
- suggest pattern matches;
- draft recommendation rationale;
- draft report prose;
- flag uncertainty.

## Deterministic Ownership

Required:

- schema validation;
- source fingerprinting;
- evidence reference format;
- privacy policy gates;
- redaction;
- cost formulas;
- scoring formulas;
- forbidden-claim checks;
- high-risk domain gates;
- export path safety;
- audit event creation;
- approval state transitions.

## Model Output Rules

- Model output must be parsed into typed schemas before storage.
- Model output must not be trusted for policy gates.
- Unsupported model claims must become assumptions or validation findings.
- Prompt versions must be recorded with each generation attempt.
- Raw private source text must not be logged.
- Provider-backed runs must be reproducible enough to audit: model, provider,
  prompt version, schema version, and source hashes must be recorded.

## Forbidden Model Behaviors

The system must not allow model prose to:

- claim guaranteed ROI;
- claim full compliance;
- recommend sending unrestricted sensitive data to cloud;
- remove human review gates for high-risk workflows;
- recommend autonomous legal, medical, financial, HR, or identity decisions;
- produce implementation handoff without approval.
