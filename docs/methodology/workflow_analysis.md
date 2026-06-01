# Workflow Analysis Methodology

Purpose: define the analysis pipeline that turns messy workflow evidence into a
RoadmapReport.

## Pipeline

| Step | Input | Output | LLM-Owned | Deterministic-Owned | Main Risk | Validation |
|------|-------|--------|-----------|---------------------|-----------|------------|
| 1. Intake | business description, domain, goals | BusinessIntake | missing-question suggestions | schema and required fields | vague input | intake fixture tests |
| 2. Context extraction | interview, SOP, notes | company profile | summarization | IDs and source refs | wrong business model | golden examples |
| 3. Workflow decomposition | text, table, transcript | WorkflowMap | step extraction | step IDs and evidence refs | invented steps | evidence coverage |
| 4. Data inventory | workflow map, docs | DataInventory | field inference | privacy rules | missing sensitive fields | PII/regulatory tests |
| 5. Pain detection | workflow/context | pain list | inference | dedup and severity bands | generic pains | reviewer rubric |
| 6. Opportunity detection | pains/workflow | opportunity list | pattern suggestions | candidate schema | AI overreach | no-AI counterexamples |
| 7. Suitability classification | opportunity | solution type | rationale draft | decision rules | "agent everywhere" | anti-overengineering tests |
| 8. Privacy/security classification | data inventory | risk scores | context notes | policy gates | unsafe cloud advice | redaction tests |
| 9. Pattern matching | opportunity/domain | pattern matches | semantic match | versioned pattern rules | wrong pattern | pattern eval |
| 10. Cost/time/team estimate | pattern/scope | estimate | explanatory notes | formulas and ranges | false precision | sanity bounds |
| 11. Prioritization | scores | priority band | rationale | scoring formula | misleading score | score regression |
| 12. Roadmap generation | recommendations | report draft | prose synthesis | schema validation | generic PDF | report rubric |
| 13. Verification | report draft | proof receipt | contradiction suggestions | claims/evidence checks | unsupported claims | verification tests |
| 14. Human review | draft/findings | approved/revised report | none final | audit/versioning | rubber-stamp | review checklist |
| 15. Export | approved/draft | Markdown/JSON | optional formatting | deterministic export | data leakage | export privacy tests |

## Input Formats

MVP inputs:

- text description;
- Markdown SOP;
- CSV-like process table;
- pasted interview transcript;
- synthetic workflow fixture.

Later inputs:

- Google Docs;
- Notion;
- CRM/helpdesk exports;
- BPMN;
- screenshots with manual description;
- private connectors.

## Analysis Rules

- Every workflow step needs evidence or an explicit assumption.
- Every important claim must be typed as observation, inference,
  recommendation, risk, cost estimate, privacy classification, or assumption.
- Missing evidence is a first-class output.
- Solution type selection must consider non-AI options before agent options.
- Privacy mode must be chosen before recommending cloud model use.
- High-risk domains require human review gates.

## Human Review

Human review is required before:

- final client-facing export;
- cost estimates are treated as implementation assumptions;
- cloud/private/local recommendation is accepted;
- legal, medical, HR, financial, or identity data workflows are scoped;
- implementation handoff is used by builders.
