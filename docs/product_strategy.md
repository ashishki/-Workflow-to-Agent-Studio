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
| 11 | Public-Source Demo Quality | Stabilize draft quality on public workflow sources before requesting prospect data. |

## Market Lens

Early wedge: teams experimenting with AI automation but lacking a repeatable discovery, governance, and evaluation process.

Buyer pain:

- too many automation ideas, too little evidence
- unclear human approval boundaries
- generic agent demos that do not survive real workflow complexity
- no durable artifact connecting discovery, implementation, and evals

The first commercial proof should show that a reviewer can turn a real workflow source into a useful blueprint in under 30 minutes, with at least 80 percent required-section acceptance after human review.

## Commercial Pilot Package

Status: assumption-backed until `docs/pilot_measurement.md` contains a reviewed real pilot row.

Buyer: AI automation consultants, freelance AI engineers, ops leads, solution
architects, or technical founders who need to decide whether a workflow is ready
for automation before implementation starts.

Use case: turn one messy workflow source package into a reviewable,
evidence-linked automation blueprint with explicit risks, approval boundaries,
missing questions, and eval cases.

Deliverables:

- imported local source records and evidence coverage notes
- reviewable automation blueprint draft
- evidence gap report with critical missing questions
- automation readiness and governance report
- local review workspace export with comments and diffs
- pilot measurement row update after human review

Non-goals:

- no production agent creation or deployment
- no autonomous customer workflow execution
- no external handoff publication or GitHub issue creation
- no replacement for stakeholder interviews when evidence is missing
- no success claim until a human-reviewed pilot row meets the measurement gate

Success criteria:

- time to reviewable blueprint is under 30 minutes
- at least 80 percent of required blueprint sections are accepted after human review
- reviewer edits and critical missing questions are recorded
- unresolved critical missing questions force a failed pilot result

Evidence status:

- The package is commercially testable as a constrained pilot.
- The buyer, workflow, deliverables, and threshold claims are assumptions until a
  real pilot row is recorded in `docs/pilot_measurement.md`.
- Any public sales claim must cite the pilot measurement row or remain labeled as
  an assumption.

## Dataset Boundary

| Dataset Kind | Purpose | Can Support Commercial Claims? |
|--------------|---------|--------------------------------|
| Demo fixtures | Show local product mechanics and deterministic tests. | No. Demo fixtures are not buyer proof. |
| Synthetic benchmarks | Regression-test retrieval, planning, vertical-pack, and feedback behavior. | No. Synthetic results cannot satisfy pilot proof or T34. |
| Sanitized artifacts | Remove confidential values before benchmark or public artifact reuse. | Only if the source is a reviewed real pilot and the measurement row cites it. |
| Real pilot evidence | Measure value on a real workflow reviewed by a human operator. | Yes, only through `docs/pilot_measurement.md`. |

Commercial claims must use real pilot evidence. Demo, synthetic, or unreviewed
sanitized data can improve engineering quality, but they do not prove wedge
strength, buyer value, or vertical-pack readiness.

## Prospect Data Request Strategy

Public-source demo quality is the precondition for asking potential customers for
real workflow data. The current request gate is defined in
`docs/pilot_measurement.md#prospect-data-request-gate`.

Ask for prospect data only after:

- public-source evals pass for mechanics, domain-specific fact preservation, and
  demo-pack reproducibility
- at least one public demo pack can be shown without claiming buyer proof
- the requested workflow source is narrow enough to review in one pilot session
- the prospect agrees to local processing, human review, and optional sanitized
  benchmark reuse

The request should ask for one real workflow packet, not broad system access:
SOP, transcript, notes, form description, integration excerpt, or a small mixed
packet. Exclude secrets, credentials, private keys, regulated personal data, and
production database exports.

T34 and T40 remain blocked until this request yields a human-reviewed real pilot
row in `docs/pilot_measurement.md`.

## Engineering Principles

- Keep safety-critical checks deterministic.
- Keep LLM output behind typed schemas and validation.
- Keep prompts short; link to task-specific context instead of embedding full docs.
- Require evidence or explicit assumptions for important claims.
- Treat `insufficient_evidence` as a product feature, not an error.
- Use pilot data to choose vertical packs and integration priorities.

The detailed draft that introduced these phases is archived at `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`.
