# Opportunity Mapper Prompt Contract

Purpose: map workflow pains to candidate automation opportunities before final
scoring.

## Inputs

- workflow map;
- pain points;
- data inventory;
- pattern library summaries;
- privacy classification.

## Output Schema

- opportunity_id;
- workflow_step_id;
- pain_point;
- candidate_solution_type;
- possible_patterns;
- why_ai_may_help;
- why_ai_may_not_be_needed;
- required_data;
- risks;
- confidence;
- evidence_refs;
- assumptions.

## Instructions

- Consider deterministic/script/API options before LLM or agent options.
- Include do-not-automate candidates when risk or evidence gaps are material.
- Flag privacy risks early.
- Do not create final cost estimates.
- Do not recommend autonomous decisions in high-risk domains.

## Failure Conditions

- all opportunities become agents;
- no do-not-automate options;
- privacy risk ignored;
- candidate lacks workflow step.
