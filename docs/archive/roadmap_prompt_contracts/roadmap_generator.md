# Roadmap Generator Prompt Contract

Purpose: draft prose for a structured RoadmapReport after deterministic scoring,
costing, pattern matching, and privacy gates have already produced typed inputs.

## Inputs

- business context;
- workflow map;
- process inventory;
- opportunity map;
- pattern matches;
- cost estimates;
- priority scores;
- privacy recommendations;
- verification findings.

## Output Schema

- executive_summary;
- workflow_map_summary;
- process_inventory_summary;
- recommendation_cards;
- do_not_automate_yet;
- cloud_vs_private_local;
- cost_time_team_plan;
- rollout_plan;
- evaluation_plan;
- governance_plan;
- verification_appendix_summary.

## Instructions

- Do not override deterministic privacy or verification gates.
- Preserve cost ranges and confidence exactly.
- Use specific workflow facts.
- Make assumptions visible.
- Include fallbacks.
- Include do-not-automate items.
- Avoid sales language and ROI guarantees.

## Failure Conditions

- generic PDF-style advice;
- cost range changed without model input;
- high-risk gate removed;
- unsupported claims added.
