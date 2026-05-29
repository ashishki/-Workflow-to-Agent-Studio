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

Status: active framework candidate. The local evidence-linked MVP and public
workflow showcase are built; the next focus is design diversity,
Playbook-compatible export, and stronger workflow-to-agent blueprint output. See
`docs/PROJECT_PLAN.md`.

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

---

## What This Produces

For one workflow evidence packet, the framework should produce a portfolio of
agent-system design options rather than one generic agent answer:

- deterministic-first blueprint
- human-in-the-loop blueprint
- bounded-agent blueprint
- high-autonomy blueprint
- compliance-heavy blueprint
- low-cost MVP blueprint

Each option should make the tradeoffs explicit:

- autonomy level and runtime tier
- deterministic steps, LLM-owned steps, and tool-use boundaries
- required human approvals
- integration assumptions and evidence gaps
- risk, cost, observability, and eval posture
- implementation task blocks compatible with AI Workflow Playbook-style planning

Example workflow domains:

- support: triage, reply drafting, escalation, and refund approval workflows
- research: source collection, synthesis, citation checks, and reviewer approval
- sales: lead qualification, CRM updates, follow-up drafting, and approval gates
- operations: intake, routing, exception handling, and audit-ready handoffs

## Зачем это нужно

Компании хотят автоматизировать процессы с помощью AI-агентов, но часто не могут достаточно точно описать сам workflow. До реализации инженеру или консультанту приходится вручную вытаскивать:

- шаги процесса
- участников и системы
- входные и выходные данные
- edge cases
- approvals и human-in-the-loop точки
- интеграции и ограничения
- риски и failure modes
- критерии приемки и eval cases

Обычная AI-сводка помогает с текстом, но часто пропускает implementation boundaries, evidence links, security assumptions, autonomy tradeoffs и проверяемые acceptance criteria.

---

## Целевая аудитория

- AI automation consultants
- freelance AI engineers
- ops leads
- solution architects
- technical founders

Первый пользователь — человек, который должен быстро превратить messy workflow description в buildable spec.

---

## Основная гипотеза

Если дать оператору инструмент, который принимает 10-20 минут сырого описания workflow и возвращает структурированный, evidence-linked workflow-to-agent blueprint, то discovery для AI automation проектов станет быстрее и надежнее.

Критерий успеха v1:

- оператор получает reviewable blueprint менее чем за 30 минут
- минимум 80% обязательных секций принимаются после human review без полного переписывания
- критические missing questions, approval boundaries и integration risks не теряются

---

## Что именно тестируем

### H1. Скорость discovery

Проверяем, можно ли сократить путь от raw workflow input до reviewable implementation brief.

Метрика:

- время от загрузки/вставки источника до draft blueprint
- целевое значение: менее 30 минут для v1 workflow

### H2. Качество blueprint

Проверяем, получается ли не просто summary, а документ, по которому инженер может принимать решение о реализации.

Метрики:

- acceptance rate обязательных секций после human review
- количество секций, которые оператору пришлось переписать вручную
- количество critical missing questions, найденных до implementation

### H3. Evidence grounding

Проверяем, можно ли связать важные утверждения blueprint с исходными фрагментами.

Метрики:

- evidence-link coverage
- citation precision
- доля claims без evidence или explicit assumption

### H4. Safety boundaries

Проверяем, не предлагает ли система опасную или преждевременную автоматизацию.

Метрики:

- наличие human approval boundaries для risky automation candidates
- forbidden-claim violations
- количество unsafe candidates, заблокированных validation gate

### H5. RAG usefulness

Проверяем, помогает ли retrieval находить релевантные source snippets, prior patterns, integration templates и eval templates.

Метрики:

- hit@3 / hit@5
- MRR
- no-answer accuracy
- citation precision
- p50 / p95 retrieval latency

RAG/eval reference: `Dream_Motif_Interpreter` используется только как reference-only проект для формы retrieval pipeline и eval discipline. Детали зафиксированы в `docs/IMPLEMENTATION_REFERENCE_MAP.md`.

### Real-world-style corpus fixture

Phase 1 corpus fixtures live in `tests/fixtures/sources/`:

- `tests/fixtures/sources/discovery_call.transcript.txt`
- `tests/fixtures/sources/discovery_notes.notes.txt`
- `tests/fixtures/sources/intake_form.form.md`
- `tests/fixtures/sources/crm_integration.integration.txt`

Corpus/eval commands:

```bash
python -m pytest tests/eval/test_real_world_corpus_eval.py -q
```

```bash
python -m pytest tests/eval/test_real_world_corpus_eval.py tests/eval/test_retrieval_eval.py tests/eval/test_plan_eval.py -q
```

---

## V1 Scope

Входит в v1:

- text/transcript ingestion
- normalized source documents
- text-only RAG
- structured workflow extraction
- deterministic completeness checks
- evidence-linked workflow-to-agent blueprint generation
- design candidate comparison before implementation
- risk and approval map
- eval-case draft
- integration checklist
- Markdown export
- immutable blueprint versions and audit trail

Не входит в v1:

- автоматическое создание production agent
- autonomous deployment
- generic agent generation without workflow evidence
- выполнение customer workflows
- замена stakeholder interviews
- мультимодальный parsing скриншотов/видео
- multi-user workspace
- GitHub issue export без отдельного human approval gate

---

## Architecture Direction

Минимально достаточная форма: workflow orchestration with deterministic validators and LLM synthesis.

Принципы:

- deterministic validators own safety-critical checks
- LLM drafts extraction and synthesis, but does not approve scope
- every important claim needs evidence or explicit assumption
- unsupported retrieval returns `insufficient_evidence`
- human approval remains required for client-facing proposal, implementation scope, estimates, and security assumptions

См. также:

- `docs/ARCHITECTURE.md`
- `docs/spec.md`
- `docs/product_strategy.md`
- `docs/product_strategy.md#commercial-pilot-package`
- `docs/tasks.md`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

---

## Current Project State

- Phase 0 implementation tasks T01-T20 are built and archived at `docs/archive/TASK_GRAPH_V1_T01_T20.md`
- Phase 1 implementation tasks T21-T24 are complete
- Phase 2 implementation tasks T25-T26 are complete
- Phase 3 implementation tasks T27-T28 are complete
- Phase 4 implementation tasks T29-T30 are complete
- Phase 5 implementation tasks T31-T32 are complete
- Phase 6 task T33 is complete; T34 is blocked by the T34/T40 dependency cycle
- Phase 7 implementation tasks T35-T36 are complete
- Phase 11 and Phase 12 public-source showcase work is complete and remains demo material, not buyer proof
- Phase 13 framework upgrade is active; next implementation focus is T59 design diversity schema
- Latest deep review: Cycle 13 for CODE-2 archived at `docs/archive/CYCLE13_CODE2_FIX.md`
- Verified local baseline: 199 passing tests, 0 skipped, 0 failed
- Prior README checkpoint: Verified local baseline: 127 passing tests before the later public-proof phases
- CI workflow configured for Python 3.12, ruff lint, ruff format check, and pytest
- Package skeleton, health command, settings, observability helpers, storage, ingestion, safety guards, text-only retrieval baseline, and initial v1 blueprint schema are implemented
- `FIX-1` / `CODE-1` closed: `WorkflowStep` rejects steps without evidence or an assumption marker
- Codex-only orchestration selected
- Development loop is nonstop: task -> review -> fix if needed -> docs/state update -> checkpoint -> next task or phase
- RAG profile ON
- Planning profile ON
- Tool-Use / Agentic / Compliance profiles OFF for v1
- Open findings: T34 and T40 currently form a dependency cycle
- Active task graph is ready for Phase 13 / `T59: Design Diversity Candidate Set`
- Product strategy is summarized in `docs/product_strategy.md`; the original long phase draft is archived at `docs/archive/AI_PRODUCT_DEVELOPMENT_PHASES_DRAFT.md`

To continue implementation, run Codex with:

```bash
docs/prompts/ORCHESTRATOR.md
```
