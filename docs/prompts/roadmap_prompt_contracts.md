# Roadmap Prompt Contracts

Purpose: compact prompt-contract reference for future roadmap extraction,
classification, and report generation work. These are not active runtime prompts
until a task explicitly wires them into the code prompt registry.

## Business Intake

Input: business description, selected domain/privacy mode, source snippets.

Output: company type, size band, channels, systems, workflows, goals,
constraints, known volumes, missing questions, evidence refs, assumptions.

Rules: do not invent company facts; do not request secrets, credentials,
production tokens, or raw regulated data; keep scope narrow.

## Workflow Decomposition

Input: source snippets, business intake, domain hints.

Output: workflow ID/name, trigger, actors, systems, steps, decisions,
exceptions, inputs, outputs, pains, data fields, evidence refs, assumptions,
missing questions.

Rules: every step needs evidence or an assumption marker; do not recommend
architecture in this step.

## Opportunity Mapping

Input: workflow map, pain points, data inventory, pattern summaries, privacy
classification.

Output: opportunity ID, workflow step, pain point, candidate solution type,
possible patterns, why AI may help, why AI may not be needed, required data,
risks, confidence, evidence refs, assumptions.

Rules: consider deterministic/script/API options before LLM or agent options;
include do-not-automate candidates when risk or evidence gaps are material.

## Privacy Context Notes

Input: source snippets after secret scan, workflow domain, data fields, selected
privacy mode.

Output: sensitive contexts, regulated-domain hints, fields needing review,
redaction quality notes, missing privacy questions, evidence refs.

Rules: deterministic code owns final privacy class and gates; model notes cannot
weaken classification.

## Roadmap Generation

Input: typed business context, workflow map, opportunity map, pattern matches,
cost estimates, priority scores, privacy recommendations, verification findings.

Output: executive summary, process inventory, recommendation cards,
do-not-automate list, cloud/private/local rationale, cost/time/team plan,
rollout, eval plan, governance plan, verification appendix.

Rules: preserve deterministic cost/privacy/verification outputs; include
fallbacks and assumptions; avoid ROI and compliance guarantees.

## Verification Review

Input: draft roadmap, claims registry, assumptions registry, evidence table,
privacy classification, recommendation traces, forbidden claims.

Output: blocking findings, nonblocking findings, unsupported claims, unsafe
privacy recommendations, missing human gates, weak cost assumptions, missing
fallbacks, reviewer questions.

Rules: model does not approve its own output; human approval remains required.
