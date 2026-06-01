# Workflow-to-Agent Studio - Project Plan

Status: active framework candidate
Role: convert human workflow evidence into bounded agent designs and SMB AI
implementation roadmaps
Priority: P0
Next active work: T64 - Privacy Domain Model

## Strategic Role

Workflow-to-Agent Studio should become the portfolio's evidence-first planning
framework next to AI Workflow Playbook.

The core problem: teams ask for "AI agents" before they understand the workflow,
permission boundaries, deterministic steps, eval needs, and human approvals. This
project should turn messy workflow evidence into a reviewable blueprint and,
in Phase 14, an SMB AI implementation roadmap.

## Product Direction

The project should not generate one magical agent. The Phase 13 framework
already supports a design portfolio:

- deterministic-first design
- human-in-the-loop design
- bounded-agent design
- high-autonomy design
- compliance-heavy design
- low-cost MVP design

Phase 14 extends this into RoadmapReport v1: recommendation cards, privacy
classification, cost/time/team ranges, priority bands, rollout stages, and a
verification appendix.

## Near-Term Roadmap

### P0 - Framework Baseline

Status: complete in T58-T63.

- README and product strategy position the project as a workflow-to-agent design
  framework.
- Design candidate schema and diverse generation flow are implemented.
- Playbook export and permission/runtime boundary pack are implemented.
- Framework readiness review is recorded.

### P0 - SMB AI Roadmap Product Layer

Status: active in Phase 14, starting with T64.

- Add privacy, recommendation, costing, scoring, verification, and roadmap
  schemas.
- Add deterministic privacy classification and redaction preview.
- Add cloud/private/local policy gates.
- Add SMB pattern library, cost engine, priority scoring, roadmap assembly,
  Markdown export, CLI command, eval suite, review checklist, and handoff export.

### P1 - Pilot Packaging

- Use synthetic demo reports for mechanics only.
- Keep commercial proof blocked until `docs/pilot_measurement.md` contains a
  human-reviewed real pilot row.
- Convert approved roadmap recommendations into implementation handoff artifacts.

## AI-Development Tasks

- Use AI to draft candidate blueprints from evidence packs.
- Use deterministic validation for required fields.
- Use reviewers to challenge over-autonomous designs.
- Use runtime verification when generated tasks modify project docs.
- Use `workflow_agent_studio/proof.py` before treating a blueprint as
  implementation-ready.

## Stop Conditions

- Do not become a general agent runner.
- Do not generate implementation code before the workflow blueprint is approved.
- Do not claim ROI, compliance certification, or buyer proof from synthetic
  demos.
