# Workflow-to-Agent Studio

Workflow-to-Agent Studio — это local-first инструмент для AI automation discovery: он превращает сырые описания рабочих процессов в структурированный blueprint для будущей автоматизации.

Входом могут быть SOP, расшифровка Loom/созвона, заметки из discovery, описание формы, API/интеграций или вручную собранные операционные notes. Выходом должен стать evidence-linked automation brief: карта текущего процесса, болевые точки, кандидаты на автоматизацию, интеграции, human approval boundaries, риски, eval cases, observability needs и следующие implementation tasks.

Статус: Phase 1 governance package готов, `PHASE1_AUDIT: PASS`. Реализация продукта еще не начата.

---

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

Обычная AI-сводка помогает с текстом, но часто пропускает implementation boundaries, evidence links, security assumptions и проверяемые acceptance criteria.

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

Если дать оператору инструмент, который принимает 10-20 минут сырого описания workflow и возвращает структурированный, evidence-linked automation blueprint, то discovery для AI automation проектов станет быстрее и надежнее.

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

---

## V1 Scope

Входит в v1:

- text/transcript ingestion
- normalized source documents
- text-only RAG
- structured workflow extraction
- deterministic completeness checks
- evidence-linked blueprint generation
- risk and approval map
- eval-case draft
- integration checklist
- Markdown export
- immutable blueprint versions and audit trail

Не входит в v1:

- автоматическое создание production agent
- autonomous deployment
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
- `docs/tasks.md`
- `docs/retrieval_eval.md`
- `docs/plan_eval.md`

---

## Current Project State

- Phase 1 artifacts generated
- Phase 1 validator passed
- Codex-only orchestration selected
- RAG profile ON
- Planning profile ON
- Tool-Use / Agentic / Compliance profiles OFF for v1
- Next implementation task: `T01: Project Skeleton`

To continue implementation, run Codex with:

```bash
docs/prompts/ORCHESTRATOR.md
```
