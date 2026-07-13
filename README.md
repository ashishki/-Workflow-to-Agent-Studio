# workflow-to-agent-studio

Workflow-to-Agent Studio is a local-first workflow-discovery tool for converting workflow
evidence into bounded, reviewable agent system blueprints. It is for the design
step before implementation: understanding the workflow, deciding which parts can
be deterministic, where LLMs or tools may help, what needs human approval, and
how the future system will be evaluated.

Inputs can be SOPs, Loom or call transcripts, discovery notes, form
descriptions, API or integration excerpts, or manually collected operating
notes. Outputs are evidence-linked design artifacts: workflow maps, automation
readiness decisions, candidate agent designs, deterministic and LLM-owned step
boundaries, approval gates, risks, eval cases, observability needs, and
implementation tasks.

> **Current maturity: local prototype.** Repository tests exercise the
> deterministic workflow, fixture, and public-source demo paths.
> No external user, observed workflow outcome, or production deployment is claimed.
> Remote CI is green. A public `v0.1.0` release remains blocked until one
> consented, sanitized workflow is reviewed by its real owner.

## Public Evidence-Mapping Intake

Public reports are limited to unsupported evidence mappings that can be
reproduced with authored-from-scratch synthetic fixtures. Read the
[sanitized interview fixture guide](docs/SANITIZED_INTERVIEW_FIXTURES.md), then
use the
[bounded issue form](https://github.com/ashishki/-Workflow-to-Agent-Studio/issues/new?template=unsupported-evidence-mapping.yml).
Do not attach a real interview, SOP, customer process, credentials, private
system output, or a redacted derivative of one. A synthetic mapping test proves
only the local mechanism; it is not an observed case, pilot, or owner review.
Suspected vulnerabilities or source-data exposure follow
[SECURITY.md](SECURITY.md), not the public form.


Russian cofounder/demo package:

- `README_RU.md`
- `docs/demo/COFOUNDER_DEMO_RU.md`
- `docs/methodology/ROADMAP_CALCULATION_RU.md`
- `docs/methodology/AGENT_EXPECTATION_CHECK_RU.md`
- `docs/research/CODOS_COMPETITOR_REVIEW_RU.md`
- `scripts/demo_roadmap_ru.sh`

Reference integration: `docs/entropy_core_gensyn_integration.md`.

---

## Quickstart

Setup commands:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
ruff check workflow_agent_studio tests/ scripts/
ruff format --check workflow_agent_studio tests/ scripts/
python -m pytest tests/ -q
```

Required environment variables:

- None for the deterministic local v1 workflow.

Optional environment variables:

- `WORKFLOW_STUDIO_STORAGE_PATH`: default `.data/workflow_studio.sqlite3`
- `WORKFLOW_STUDIO_INDEX_DIR`: default `.data/index`
- `WORKFLOW_STUDIO_PATTERN_DIR`: default `patterns`
- `WORKFLOW_STUDIO_LLM_PROVIDER`: default `openai`
- `WORKFLOW_STUDIO_LLM_MODEL`: default `gpt-5.4`
- `WORKFLOW_STUDIO_EXTRACTION_MODEL`: default `gpt-5.4-mini`
- `WORKFLOW_STUDIO_EMBEDDING_MODEL`: default `text-embedding-3-small`
- `WORKFLOW_STUDIO_LOG_LEVEL`: default `INFO`

Sample run command:

```bash
workflow-agent-studio run \
  --database .data/workflow_studio.sqlite3 \
  --run-id sample-sop \
  --index-dir .data/index \
  tests/fixtures/sources/sample_sop.md
```

Local export command:

```bash
workflow-agent-studio export \
  --database .data/workflow_studio.sqlite3 \
  --blueprint-version-id 1 \
  --export-dir .data/exports \
  --output sample-sop-blueprint.md
```

Roadmap demo command:

```bash
bash scripts/demo_roadmap_ru.sh
```

---

## What This Produces

The current tool produces evidence-linked workflow-to-agent design
artifacts:

- workflow maps with actors, systems, data fields, decisions, and exceptions;
- automation candidates with deterministic, LLM-owned, and human approval
  boundaries;
- design candidates such as deterministic-first, human-in-the-loop,
  bounded-agent, compliance-heavy, and low-cost MVP;
- candidate scoring for feasibility, data readiness, eval readiness, TCO,
  risk, ROI proxy, autonomy fit, and deployment fit;
- data/eval readiness reports, harness candidate cards, autonomous deployment
  recommendations, and use-case card exports;
- evaluation cases, risks, observability notes, implementation tasks, and
  Markdown exports.

The SMB AI roadmap layer adds:

- RoadmapReport v1;
- recommendation cards;
- privacy classification and cloud/private/local policy gates;
- cost/time/team ranges;
- agent expectation check: what the agent will not replace, realistic autonomy
  level, and proof gates before rollout;
- priority scoring;
- readiness scoring for data, eval, harness, TCO, and deployment fit;
- SMB implementation patterns;
- verification receipts and roadmap evals;
- reviewer checklists;
- approved implementation handoff exports.

## Product Direction

The product is a pre-implementation AI roadmap studio, not an agent builder.

It helps an operator or consultant answer:

- what should be automated;
- what should not be automated yet;
- whether the right solution is a script, API integration, RPA, LLM assistant,
  RAG assistant, human-in-the-loop workflow, or bounded agent;
- which data is needed and how sensitive it is;
- whether cloud, private, or local analysis is safe;
- what assumptions, risks, costs, rollout stages, and human-review gates apply.

Primary users:

- AI automation consultants;
- freelance AI engineers;
- ops leads;
- solution architects;
- technical founders.

## Boundaries

The project does not:

- create production agents automatically;
- deploy automations;
- mutate production systems;
- replace stakeholder interviews when evidence is missing;
- claim ROI, buyer proof, or compliance certification from synthetic demos;
- recommend autonomous legal, medical, financial, HR, or identity-sensitive
  decisions.

## Evaluation

Focused eval commands:

```bash
python -m pytest tests/eval/test_real_world_corpus_eval.py -q
python -m pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_retrieval_eval.py tests/eval/test_plan_eval.py -q
```

Authored-synthetic corpus fixtures:

- `tests/fixtures/sources/discovery_call.transcript.txt`
- `tests/fixtures/sources/discovery_notes.notes.txt`
- `tests/fixtures/sources/intake_form.form.md`
- `tests/fixtures/sources/crm_integration.integration.txt`

Authored-synthetic corpus eval (historical test filename):

- `tests/eval/test_real_world_corpus_eval.py`

The fixture bytes and their authored-synthetic declarations are bound in
`tests/fixtures/sources/manifest.json`. The historical test filename does not
mean the checked-in inputs came from a real person, customer, or observed
workflow.

Primary metrics:

- evidence-link coverage;
- citation precision;
- no-answer accuracy;
- missing critical question count;
- forbidden-claim violations;
- reviewer acceptance rate;
- roadmap quality/privacy/cost/pattern verification.

## Documentation Map

- Active task graph: `docs/tasks.md`
- Current Codex state: `docs/CODEX_PROMPT.md`
- Orchestrator prompt: `docs/prompts/ORCHESTRATOR.md`
- Product strategy: `docs/product_strategy.md`
- Commercial pilot package: `docs/product_strategy.md#commercial-pilot-package`
- SMB roadmap index: `docs/AI_ROADMAP_STUDIO_INDEX.md`
- Architecture: `docs/ARCHITECTURE.md`
- Specification: `docs/spec.md`
- Operator guide: `docs/operator_guide.md`
- Public fixture and unsupported-mapping intake:
  `docs/SANITIZED_INTERVIEW_FIXTURES.md`
- Retrieval eval: `docs/retrieval_eval.md`
- Planning eval: `docs/plan_eval.md`
- Original long phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`

## Current Project State

- Completed: Phase 0 local evidence-linked MVP; Phase 11/12 public workflow
  showcase; Phase 13 workflow-to-agent framework upgrade; Phase 14 SMB AI
  Roadmap Product Layer through `T82`.
- Completed: the non-parsing remote CI workflow was repaired and verified on
  the current repository slug.
- Blocked on repository settings: the repository-only rename to
  `workflow-to-agent-studio`; the Python package and CLI names do not change.
- Next evidence target: one consented, sanitized workflow reviewed by its real
  owner; until then the repository remains a local prototype.
- Open commercial proof boundary: T34/T40 remain blocked until
  human-reviewed real workflow data is recorded in `docs/pilot_measurement.md`.
- Authoritative verification is the current clean-checkout command output, not
  a static test count in this README. Run the quickstart checks above and review
  `docs/evidence/WORKFLOW_P0_RENAME_PREP_2026-07-13.md` for the dated P0 result.

## Portfolio Role And Reuse Boundary

This is a standalone workflow-discovery tool in the secondary Workflow and
Adoption Tools category. It is not the portfolio flagship, an agent runtime, or
a dependency of Eval Ground Truth Lab. Its evaluated surface is limited to
local blueprint generation and review mechanics.

This repository currently has no open-source license. Public visibility permits
inspection, but does not grant permission to copy, modify, or redistribute the
code. External reuse and a broad contribution surface remain out of scope unless
a separate license and dependency review is completed.

## Development Loop

Continue implementation with the standard Codex-only loop:

```bash
codex "$(cat docs/prompts/ORCHESTRATOR.md)"
```

The orchestrator reads `docs/CODEX_PROMPT.md`, then executes the next task from
`docs/tasks.md`. Do not use archived taskgraphs as active planning input.
