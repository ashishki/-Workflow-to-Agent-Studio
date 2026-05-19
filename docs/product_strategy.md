# Product Strategy

Purpose: keep product direction compact and actionable for implementation planning.

Workflow-to-Agent Studio is the pre-production layer for AI automation. It should help an operator decide what is worth automating, what evidence supports that decision, what must remain human-approved, and how the future automation will be evaluated.

The product should not compete as a generic agent builder or a one-off deep research prompt. Its differentiation is evidence-linked workflow discovery: every important recommendation is tied to source material, missing evidence is surfaced before implementation, and approval/export paths stay governed.

## Target Outcome

The mature product produces useful pre-build artifacts:

- evidence-backed automation blueprint
- workflow map with actors, systems, decisions, exceptions, and data fields
- automation readiness and risk assessment
- human approval boundaries
- integration and implementation task plan
- eval cases with measurable expected behavior
- audit trail for source evidence, reviewer edits, and approvals

## Development Phases

| Phase | Name | Product Goal |
|-------|------|--------------|
| 0 | Local Evidence-Linked MVP | Prove the local CLI can generate a reviewable evidence-linked draft. |
| 1 | Evidence Capture And Corpus Expansion | Support messy real discovery inputs and evidence completeness checks. |
| 2 | Retrieval And Evidence Engine | Make source grounding reliable enough to trust and measure. |
| 3 | Structured LLM Extraction And Synthesis | Use real structured LLM calls behind schemas, evals, and cost controls. |
| 4 | Automation Readiness And Governance | Convert blueprints into readiness decisions with deterministic gates. |
| 5 | Review Workspace And Human Editing | Make human review efficient, traceable, and versioned. |
| 6 | Vertical Blueprint Packs | Add domain-specific patterns for repeatable market wedges. |
| 7 | Pilot Proof And Commercial Packaging | Prove value with real pilots and package the offer. |
| 8 | Integrations And Controlled Handoff | Import from real systems and export controlled implementation handoffs. |
| 9 | Learning System And Moat | Turn reviewed outcomes into better patterns, evals, and benchmarks. |

## Market Lens

Early wedge: teams experimenting with AI automation but lacking a repeatable discovery, governance, and evaluation process.

Buyer pain:

- too many automation ideas, too little evidence
- unclear human approval boundaries
- generic agent demos that do not survive real workflow complexity
- no durable artifact connecting discovery, implementation, and evals

The first commercial proof should show that a reviewer can turn a real workflow source into a useful blueprint in under 30 minutes, with at least 80 percent required-section acceptance after human review.

## Engineering Principles

- Keep safety-critical checks deterministic.
- Keep LLM output behind typed schemas and validation.
- Keep prompts short; link to task-specific context instead of embedding full docs.
- Require evidence or explicit assumptions for important claims.
- Treat `insufficient_evidence` as a product feature, not an error.
- Use pilot data to choose vertical packs and integration priorities.

The detailed draft that introduced these phases is archived at `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`.
