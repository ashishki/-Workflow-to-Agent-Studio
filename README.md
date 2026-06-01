# Workflow-to-Agent Studio

Workflow-to-Agent Studio is a local-first framework for converting workflow
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

Status: active framework candidate with the Phase 14 SMB AI Roadmap Product
Layer completed through the current task graph. The local evidence-linked MVP,
public workflow showcase, design candidate portfolio, Playbook export, roadmap
assembly, Markdown export, CLI command, eval suite, reviewer checklist, and
approved handoff export are built.

Russian cofounder/demo package:

- `README_RU.md`
- `docs/demo/COFOUNDER_DEMO_RU.md`
- `docs/methodology/ROADMAP_CALCULATION_RU.md`
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

The current framework produces evidence-linked workflow-to-agent design
artifacts:

- workflow maps with actors, systems, data fields, decisions, and exceptions;
- automation candidates with deterministic, LLM-owned, and human approval
  boundaries;
- design candidates such as deterministic-first, human-in-the-loop,
  bounded-agent, compliance-heavy, and low-cost MVP;
- evaluation cases, risks, observability notes, implementation tasks, and
  Markdown exports.

The SMB AI roadmap layer adds:

- RoadmapReport v1;
- recommendation cards;
- privacy classification and cloud/private/local policy gates;
- cost/time/team ranges;
- priority scoring;
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

Real-world corpus fixtures:

- `tests/fixtures/sources/discovery_call.transcript.txt`
- `tests/fixtures/sources/discovery_notes.notes.txt`
- `tests/fixtures/sources/intake_form.form.md`
- `tests/fixtures/sources/crm_integration.integration.txt`

Real-world corpus eval:

- `tests/eval/test_real_world_corpus_eval.py`

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
- Retrieval eval: `docs/retrieval_eval.md`
- Planning eval: `docs/plan_eval.md`
- Original long phase draft: `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`

## Current Project State

- Completed: Phase 0 local evidence-linked MVP; Phase 11/12 public workflow
  showcase; Phase 13 workflow-to-agent framework upgrade; Phase 14 SMB AI
  Roadmap Product Layer through `T82`.
- Active: no remaining tasks are listed after `T82` in `docs/tasks.md`.
- Next task: waiting for the next task graph or human direction.
- Open commercial proof boundary: T34/T40 remain blocked until
  human-reviewed real workflow data is recorded in `docs/pilot_measurement.md`.
- Latest full baseline after public-source roadmap demo package: 350 passing tests, 0 skipped, 0 failed.
- Documentation prep check: `.venv/bin/python -m pytest tests/unit/test_docs.py -q`
  passed with 24 tests.
- Historical checkpoint: Verified local baseline: 127 passing tests before the
  later public-proof phases.

## Development Loop

Continue implementation with the standard Codex-only loop:

```bash
codex "$(cat docs/prompts/ORCHESTRATOR.md)"
```

The orchestrator reads `docs/CODEX_PROMPT.md`, then executes the next task from
`docs/tasks.md`. Do not use archived taskgraphs as active planning input.
