# Workflow Decomposer Prompt Contract

Purpose: convert source evidence into structured workflow maps.

## Inputs

- source snippets;
- business intake;
- domain hints;
- existing evidence anchor format.

## Output Schema

- workflow_id;
- workflow_name;
- trigger;
- actors;
- systems;
- steps;
- decisions;
- exceptions;
- inputs;
- outputs;
- pain_points;
- data_fields;
- evidence_refs;
- assumptions;
- missing_questions.

## Instructions

- Extract only what is supported by evidence.
- Each step must include evidence or assumption marker.
- Preserve order when the source provides order.
- Mark missing actors, systems, decisions, exceptions, data fields, and approval
  boundaries.
- Do not recommend architecture in this step.

## Failure Conditions

- invented steps;
- no evidence refs;
- solution recommendations included too early;
- missing approvals ignored.
