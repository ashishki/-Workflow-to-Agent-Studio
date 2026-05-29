# Framework Readiness Review

Date: 2026-05-29
Phase: 13
Status: ready for constrained framework demo

## Verdict

Workflow-to-Agent Studio is ready to be shown as a serious workflow-to-agent
design framework, with strict claim boundaries. It can be presented as a
local-first system that turns workflow evidence into reviewable agent-system
blueprints, candidate tradeoff comparisons, permission/runtime boundaries, and
local Playbook-compatible handoff artifacts.

It is not ready to claim buyer proof, pilot proof, autonomous deployment, or
production agent execution. T34/T40 remain blocked until a real prospect or
customer workflow packet is reviewed by a human and recorded in the pilot
measurement process.

## Evidence Reviewed

- Public positioning: `README.md`, `docs/product_strategy.md`, and
  `docs/PROJECT_PLAN.md` now describe a workflow evidence to agent blueprint
  framework, not a generic agent builder.
- Candidate diversity: T59/T60 added `design-candidate-v1`, six candidate
  variants, explicit assumptions, evidence gaps, status, and tradeoff
  comparison.
- Playbook export: T61 added local AI Workflow Playbook-compatible Markdown
  export with task blocks, Context-Refs, eval skeletons, contract deltas, runtime
  tier, tool boundaries, approval points, and convenience-artifact labeling.
- Permission boundary pack: T62 added read/write/destructive tool surfaces,
  confirmation or sandbox controls for risky actions, and runtime justification
  by mutability, privilege, and blast radius.
- Eval evidence: latest baseline is 216 passing tests, 0 skipped, 0 failed;
  ruff check and ruff format check pass for `workflow_agent_studio tests/`.

## Readiness Assessment

Pass:

- Framework framing is clear and does not claim automated deployment.
- The design candidate set covers deterministic-first, human-in-the-loop,
  bounded-agent, high-autonomy, compliance-heavy, and low-cost MVP variants.
- Consolidation no longer silently chooses one answer; it carries tradeoff
  comparison alongside a consolidated blueprint.
- `needs_review` status is preserved when evidence gaps indicate insufficient
  evidence.
- Local exports remain inside the local Markdown boundary.
- Permission/runtime boundaries are structured enough to feed training or
  review scenarios.

Needs real workflow data:

- Pilot value, buyer urgency, willingness to pay, and required-section acceptance
  cannot be claimed from public-source demos.
- Vertical-pack readiness for commercial claims remains blocked without reviewed
  real pilot evidence.
- Prospect/customer workflow complexity may reveal missing candidate variants,
  additional runtime tiers, or stricter permission-boundary requirements.

## Forbidden Claims Until Real Pilot Evidence

Do not claim:

- the framework is buyer-proven or commercially validated;
- T34 or T40 is complete;
- public-source demo packs prove customer demand, conversion, pricing, or
  implementation ROI;
- the system creates, deploys, or runs production agents;
- generated Playbook artifacts are authoritative implementation instructions;
- high-autonomy candidates are safe to implement without human review,
  confirmation boundaries, and eval gates.

Allowed claims:

- the project has a local, evidence-linked workflow-to-agent design framework
  prototype;
- it can generate multiple bounded candidate designs from one evidence packet;
- it can compare autonomy, risk, cost, eval, approval, permission, and runtime
  tradeoffs;
- it can export local convenience artifacts for human review.

## Decision

Proceed only under constrained demo language. The next operator-facing action
remains `docs/prospect_data_request_pack.md`: request one narrow real workflow
packet, process it locally, and record human review results before making any
pilot or buyer-proof claim.

