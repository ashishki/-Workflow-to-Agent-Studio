# Workflow-to-Agent Studio - Project Plan

Status: active framework candidate
Role: convert human workflows into bounded agent system designs
Priority: P0

## Strategic Role

Workflow-to-Agent Studio should become the portfolio's second serious framework
next to AI Workflow Playbook.

The core problem: teams ask for "AI agents" before they understand the workflow,
permission boundaries, deterministic steps, eval needs, and human approvals. This
project should turn messy workflow evidence into an agent-ready blueprint.

## Product Direction

The project should not generate one magical agent. It should generate a design
portfolio:

- deterministic-first design
- human-in-the-loop design
- bounded-agent design
- high-autonomy design
- compliance-heavy design
- low-cost MVP design

Then it should compare tradeoffs and produce implementation tasks.

## Near-Term Roadmap

### P0 - Reposition README

- Present as a serious workflow-to-agent design framework.
- Add "What this produces" with concrete artifacts.
- Add examples for support, research, sales, and operations workflows.

### P0 - Add Design Diversity

- Add Gensyn DEI-inspired candidate generation:
  - different architecture lenses
  - different risk/cost/autonomy profiles
  - archive of candidate blueprints
- Add consolidation step with evidence and tradeoffs.
- Follow `docs/entropy_core_gensyn_integration.md`: use Gensyn as a bounded
  design reference and Entropy Core as optional receipt vocabulary.

### P1 - Agent Boundary Output

- Generate:
  - deterministic steps
  - LLM-owned steps
  - tool-use boundaries
  - human approvals
  - runtime tier
  - eval plan
  - observability plan
  - implementation task graph

### P1 - Playbook Export

- Export AI Workflow Playbook-compatible task blocks.
- Export Implementation Contract deltas.
- Export evaluation artifact skeletons.
- Export receipt-compatible blueprint artifacts when useful.

### P2 - Demo Surface

- Add one polished CLI demo.
- Later add a simple visual workflow map if it helps sales/demo clarity.

## AI-Development Tasks

- Use AI to draft candidate blueprints from evidence packs.
- Use deterministic validation for required fields.
- Use reviewers to challenge over-autonomous designs.
- Use runtime verification when generated tasks modify project docs.

## Stop Conditions

- Do not become a general agent runner.
- Do not generate implementation code before the workflow blueprint is approved.
