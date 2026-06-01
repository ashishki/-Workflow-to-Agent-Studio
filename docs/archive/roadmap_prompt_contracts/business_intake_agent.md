# Business Intake Agent Prompt Contract

Purpose: extract structured business context and missing questions from a messy
business/workflow description.

## Inputs

- business description;
- selected domain if provided;
- selected privacy mode if provided;
- source evidence snippets;
- existing project metadata.

## Output Schema

- company_type;
- size_band;
- region_if_known;
- channels;
- systems;
- workflows_mentioned;
- goals;
- constraints;
- known_volumes;
- missing_questions;
- evidence_refs;
- assumptions.

## Instructions

- Do not invent company facts.
- Mark unclear details as missing questions.
- Separate observed facts from assumptions.
- Do not request secrets, credentials, production tokens, or raw regulated data.
- Prefer narrow workflow scope over company-wide claims.

## Failure Conditions

- raw sensitive data requested;
- unsupported business model inferred;
- missing questions omitted when input is vague;
- evidence refs absent for observed facts.
