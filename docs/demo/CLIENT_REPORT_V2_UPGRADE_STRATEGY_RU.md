# Client Report V2 Upgrade Strategy

Статус: стандарт customer-facing отчета v2 для cofounder demo
Дата: 2026-06-02
Граница: это не коммерческое предложение конкретному клиенту. Это новый
стандарт того, как должны выглядеть будущие клиентские отчеты, чтобы они
воспринимались как инженерно-сметный decision pack, а не как список AI-идей.

---

## 1. Честный диагноз

Текущие шесть showcase reports полезны для демонстрации breadth: салон,
e-commerce, legal intake, HVAC, incident coordination, accelerator workflow. Но
для сильного buyer/cofounder разговора они выглядят слишком верхнеуровнево:

- нет детального roadmap по фазам внедрения;
- нет work breakdown по задачам, ролям и часам;
- нет bill of materials: агенты, API, базы данных, очереди, хранилища,
  мониторинг;
- стоимость и сроки выглядят как экспертная оценка, а не как расчет;
- региональная экономика смешана с US-ориентирами, хотя нам важнее РФ и Европа;
- не видно, какие assumptions меняют смету;
- не видно, где именно система страхуется от галлюцинаций;
- не встроена коммерческая упаковка Entropy Core и AI Workflow Playbook.

Вывод: отчет v2 должен быть не `AI ideas report`, а **AI Implementation Decision
Pack**.

---

## 2. Как должен выглядеть клиентский отчет v2

### 2.1 Executive decision summary

Первый экран для CEO/COO/sales founder:

- какой workflow разбираем;
- какой первый use case рекомендуем;
- какой use case явно не рекомендуем;
- expected operational effect;
- рекомендованный сценарий: lean / standard / strict;
- rough budget range по РФ и Европе;
- срок до pilot-ready версии;
- главный риск;
- решение: proceed / postpone / discovery required.

Пример формулировки:

> Рекомендуем начать не с автономного агента, а с human-in-the-loop assistant:
> он готовит черновики решений и брифы, но не пишет в CRM и не принимает
> финальное решение без reviewer. Это дешевле, быстрее и безопаснее для первого
> пилота.

### 2.2 Evidence and workflow boundary

Отчет должен начинаться с того, что мы реально знаем:

| Field | What We Need |
|---|---|
| Source documents | SOP, CRM export, call transcript, ticket samples, forms |
| Source quality | complete / partial / anecdotal |
| Workflow owner | кто отвечает за процесс |
| Current systems | CRM, telephony, email, calendar, helpdesk, spreadsheets |
| Data classes | public / internal / confidential / sensitive / restricted |
| Volumes | items per day/week/month |
| Manual time | minutes per item and exception rate |
| Missing evidence | чего не хватает для quote |

Важное правило: если нет volumes, access constraints и sample cases, отчет имеет
статус `planning estimate`, а не `fixed quote`.

### 2.3 Current-state process map

Каждый workflow должен раскладываться как as-is карта:

```text
Trigger
  -> intake channel
  -> normalization
  -> decision point
  -> system lookup
  -> human action
  -> external message
  -> CRM/helpdesk update
  -> exception path
  -> reporting
```

Для каждого шага фиксируются:

- actor;
- system;
- input data;
- output data;
- decision type;
- current pain;
- automation suitability;
- risk level.

### 2.4 Opportunity provenance

Каждая рекомендация должна иметь происхождение:

| Origin | Meaning | Can Become Recommendation |
|---|---|---|
| `known_pattern` | из нашей pattern library | да, после проверки evidence |
| `n8n_public_signal` | похожие automation patterns есть в public n8n corpus | только как supporting signal |
| `frontier_candidate` | предложено Claude/другой frontier model | только после verifier + human review |
| `human_reviewed` | принято reviewer | да |
| `blocked` | заблокировано rules/verifier | нет |

n8n нужен не как готовая библиотека решений, а как доказательство того, что
похожие automation patterns уже встречаются у практиков. Frontier model нужен
для поиска missed opportunities и альтернатив, но он не утверждает roadmap.

---

## 3. Архитектура решения в отчете

Отчет v2 должен показывать не только “что внедрить”, но и “из каких частей это
собрать”.

### 3.1 Component bill of materials

Типовая архитектура для workflow automation pilot:

```text
Source connectors
  -> Intake Normalizer
  -> Privacy / Redaction Gate
  -> Workflow State Store
  -> Deterministic Rules Engine
  -> LLM Draft / Research Worker
  -> Pattern and Policy Verifier
  -> Human Review Queue
  -> Approved Action Executor
  -> Evidence Receipt / Audit Log
  -> Dashboard / Export
```

### 3.2 Agents and services

| Component | Responsibility | Model/Logic | Can Act Without Human |
|---|---|---|---|
| Intake Parser | приводит входящие заявки/письма/тикеты к схеме | deterministic + small LLM optional | no |
| Workflow Mapper | извлекает шаги, actors, systems, decisions | LLM draft + schema validation | no |
| Pattern Matcher | подбирает known automation pattern | deterministic | no |
| Privacy Gate | определяет data class и allowed mode | deterministic policy | no |
| Cost Engine | считает role-hours, infra, API usage | deterministic formula | no |
| Frontier Candidate Generator | ищет missed opportunities | Claude Opus/Sonnet class | no |
| Verifier | блокирует unsafe/autonomous claims | deterministic | no |
| Review Queue | собирает human decisions and corrections | app UI / CRM task / Notion | human-owned |
| Action Executor | пишет в CRM/calendar/helpdesk после approval | API integration | only after approval |
| Evidence Logger | пишет receipts, source hashes, decisions | DB/object storage | no |

### 3.3 APIs and integrations

В отчете должна быть отдельная таблица integrations:

| System | Access Needed | Mode | Risk | Fallback |
|---|---|---|---|---|
| CRM | read contacts/deals, write task/status after approval | OAuth/API token | PII exposure, wrong write | CSV export + manual import |
| Telephony | call metadata, transcript webhook | webhook/API | consent, retention | uploaded transcript sample |
| Email | inbound/outbound drafts | IMAP/Gmail/Microsoft API | accidental send | draft-only mode |
| Calendar | availability read, event write after approval | API | double booking | read-only calendar export |
| Helpdesk | ticket read, tag/write after approval | API | wrong routing | labels in CSV |
| Knowledge base | SOP/FAQ/policy retrieval | sync/export | outdated docs | curated docs folder |

### 3.4 Databases and storage

| Stage | Good Enough | When To Upgrade |
|---|---|---|
| Demo | local files + SQLite | no live data |
| Lean pilot | Postgres + object storage | multiple users, audit log |
| Standard pilot | Postgres, object storage, queue, backups | live-adjacent workflow |
| Strict/private | private Postgres, encrypted object storage, retention policy, audit export | sensitive/restricted data |
| RAG needed | vector index over approved docs | only when answer quality depends on knowledge retrieval |

Recommendation: do not add vector DB by default. Add it only when the workflow
requires retrieval over a real knowledge corpus.

---

## 4. Roadmap by implementation phase

Каждая инициатива должна иметь фазовый план с deliverables, hours, risks and
exit criteria.

### Phase 0. Discovery and evidence pack

Goal: prove there is a real workflow and enough evidence to estimate.

Tasks:

- interview workflow owner and 2-3 operators;
- collect SOP, sample tickets/forms/transcripts, CRM fields;
- map current process and exception paths;
- estimate volumes and current manual time;
- define pilot metric: time saved, SLA, quality, error reduction, throughput;
- classify data and decide privacy mode.

Deliverables:

- source register;
- as-is workflow map;
- data field inventory;
- metric definition;
- missing evidence list;
- proceed/postpone decision.

Typical roles and hours:

| Role | Lean | Standard | Strict |
|---|---:|---:|---:|
| AI solution architect | 4-8h | 8-14h | 12-20h |
| Business analyst / PM | 8-14h | 14-24h | 20-36h |
| Domain owner/reviewer | 3-6h | 6-10h | 8-16h |
| Data/privacy reviewer | 0-2h | 3-6h | 8-16h |

Exit criteria:

- workflow owner confirms map;
- at least 20-50 representative examples for pilot or explicit reason why not;
- data class known;
- success metric has baseline or baseline collection plan.

### Phase 1. Architecture and data readiness

Goal: turn workflow into buildable architecture.

Tasks:

- choose implementation pattern: script/API/LLM assistant/RAG/HITL/bounded agent;
- design schemas for input, decisions, outputs, audit log;
- choose deployment mode: local, private cloud, managed cloud;
- define connector strategy and fallback if API access is delayed;
- define do-not-automate boundaries;
- produce build estimate from role-hours.

Deliverables:

- target architecture;
- integration matrix;
- DB/storage plan;
- prompt/model boundary;
- risk register;
- role-hour estimate v1.

Typical roles and hours:

| Role | Lean | Standard | Strict |
|---|---:|---:|---:|
| AI solution architect | 8-14h | 16-28h | 28-48h |
| AI automation engineer | 8-16h | 16-32h | 24-48h |
| Integration engineer | 4-10h | 12-24h | 24-48h |
| Data/privacy reviewer | 2-4h | 6-12h | 16-32h |

Exit criteria:

- no high-risk recommendation without human gate;
- no direct live write without rollback plan;
- infra and API dependencies are named;
- estimate has assumptions and confidence level.

### Phase 2. Prototype / shadow mode

Goal: build local or live-adjacent prototype that makes recommendations but
does not mutate production.

Tasks:

- implement input parser and normalized schema;
- implement deterministic checks;
- implement LLM draft/research worker where needed;
- implement eval/golden set;
- run shadow processing on historical samples;
- compare output with human decisions;
- log evidence and failures.

Deliverables:

- prototype service or notebook/CLI;
- golden dataset;
- eval report;
- failure analysis;
- updated cost/time estimate.

Typical roles and hours:

| Role | Lean | Standard | Strict |
|---|---:|---:|---:|
| AI automation engineer | 24-48h | 60-120h | 120-220h |
| Integration engineer | 8-24h | 32-80h | 80-160h |
| QA/eval engineer | 8-16h | 24-48h | 48-96h |
| Domain reviewer | 6-12h | 16-32h | 32-64h |

Exit criteria:

- prototype beats agreed baseline or reveals that automation is not worth it;
- output quality passes human review threshold;
- no blocked privacy violation;
- known failure modes are documented.

### Phase 3. Pilot with human gates

Goal: move from shadow mode to controlled operational pilot.

Tasks:

- connect approved read APIs;
- enable draft-only or approval-only write flow;
- create human review queue;
- train operators on accept/edit/reject;
- add monitoring and rollback;
- measure operational effect weekly.

Deliverables:

- pilot workflow;
- reviewer dashboard/workspace;
- weekly pilot report;
- approval logs;
- rollout/stop recommendation.

Typical roles and hours:

| Role | Lean | Standard | Strict |
|---|---:|---:|---:|
| AI automation engineer | 24-50h | 60-120h | 120-220h |
| Integration engineer | 16-40h | 60-120h | 120-240h |
| PM/operator | 10-20h | 24-48h | 48-96h |
| Domain reviewers | 10-30h | 30-80h | 80-160h |

Exit criteria:

- live-adjacent pilot runs for 2-4 weeks;
- quality and SLA metrics are measured;
- human override rate is acceptable;
- there is a scale/stop decision.

### Phase 4. Production-lite and handoff

Goal: make the workflow stable enough for daily use without pretending it is an
enterprise platform.

Tasks:

- harden deployment;
- add backups, alerts, access controls;
- document runbook and owner responsibilities;
- freeze model/prompt versions;
- add regression eval before changes;
- define maintenance cadence.

Deliverables:

- production-lite service;
- operator runbook;
- admin handoff;
- eval suite;
- incident/rollback procedure;
- monthly operating estimate.

Typical roles and hours:

| Role | Lean | Standard | Strict |
|---|---:|---:|---:|
| AI/backend engineer | 24-60h | 80-160h | 180-320h |
| DevOps/infrastructure | 8-24h | 32-80h | 80-160h |
| QA/eval engineer | 8-24h | 32-80h | 80-160h |
| PM/operator | 8-20h | 24-48h | 48-96h |

Exit criteria:

- owner can operate the workflow;
- rollback tested;
- cost monitoring in place;
- monthly review cadence agreed.

### Phase 5. Governance and improvement loop

Goal: turn one pilot into repeatable AI adoption discipline.

Tasks:

- maintain evidence index and decision log;
- review drift, failures, user corrections;
- update prompts/models/policies with change control;
- evaluate next workflow candidates;
- decide whether to add proof layer or internal playbook.

Deliverables:

- monthly eval report;
- recommendation change log;
- evidence receipts;
- next-workflow shortlist;
- scale/stop decision.

---

## 5. Cost model: how estimates must be calculated

### 5.1 Formula

```text
one_time_cost =
  sum(role_hours_by_phase * regional_rate_by_role)
  + setup/licensing
  + integration risk reserve
  + QA/eval overhead
  + contingency

monthly_cost =
  hosting
  + database/storage/logs
  + LLM/API usage
  + SaaS/integration subscriptions
  + reviewer time
  + maintenance/support hours
```

Recommended contingency:

- lean: 10-15%;
- standard: 15-25%;
- strict/private: 25-40%.

Cost must never be a single number. It should be a range with assumptions.

### 5.2 Region-aware rate cards

These are planning ranges for June 2026, not permanent truth and not a final
quote. Before a paid proposal, the report must attach a `rate_card_version` and
refresh contractor/provider prices.

#### Russia-oriented planning rates

| Role | Planning Rate |
|---|---:|
| PM / implementation owner | 2,500-5,000 RUB/hour |
| Business analyst | 3,000-5,500 RUB/hour |
| AI automation engineer | 3,500-6,500 RUB/hour |
| Senior backend/integration engineer | 3,800-7,500 RUB/hour |
| AI solution architect / tech lead | 5,000-10,000 RUB/hour |
| Data/privacy reviewer | 3,500-8,000 RUB/hour |
| QA/eval engineer | 2,500-5,500 RUB/hour |
| Domain reviewer/operator | 1,500-4,000 RUB/hour |

Reasoning:

- public Russian salary snapshots show Senior Python around 247,500-290,000
  RUB/month and Lead around 300,000-350,000 RUB/month depending on format;
- public rate sheets show backend senior, architect and LLM engineer examples
  around 3,800-4,800 RUB/hour before VAT in one 2026 agency snapshot;
- public educational/procurement-style materials list broad Python hourly
  ranges around 900-10,300 RUB/hour depending on employment model and seniority;
- AI architecture, integrations and privacy work should be above ordinary
  implementation because mistakes create expensive rewrites.

#### Europe-oriented planning rates

| Region/Role | Planning Rate |
|---|---:|
| Eastern Europe middle/senior contractor | 45-85 EUR/hour |
| Eastern Europe senior agency | 80-130 EUR/hour |
| Western Europe senior engineer | 80-165 USD/hour equivalent |
| Western Europe tech lead/architect | 150-200 USD/hour equivalent |
| UK/DACH agency MVP reference | 8,000-50,000 GBP/EUR-class project bands |

Reasoning:

- Eastern European rate guides place senior ranges roughly from 55-120 EUR/hour
  depending on country and agency/contractor model;
- European project guides show Western/Northern Europe materially above CEE;
- US rates should not be the default for our target packaging because they make
  early adoption look unnecessarily expensive.

### 5.3 Example estimate card

For a medium workflow with CRM, email and review queue:

| Scenario | One-Time Build | Monthly Run | Best For |
|---|---:|---:|---|
| Lean RF | 700k-1.6m RUB | 35k-120k RUB | proof-of-value, one workflow |
| Standard RF | 1.8m-4.5m RUB | 120k-350k RUB | real pilot with integrations |
| Strict RF | 4.5m-10m+ RUB | 350k-1.2m+ RUB | sensitive data, audit, private deployment |
| Lean Europe | 12k-28k EUR | 300-1.2k EUR | proof-of-value |
| Standard Europe | 30k-80k EUR | 1.2k-4k EUR | integrated pilot |
| Strict Europe | 80k-200k+ EUR | 4k-15k+ EUR | regulated/private setup |

These ranges are intentionally broad. The final estimate narrows only after:

- real monthly volume is known;
- API access is confirmed;
- data class is verified;
- sample cases are reviewed;
- buyer chooses lean/standard/strict scenario.

---

## 6. Infrastructure and API costs

### 6.1 EU-oriented pilot

For a low-volume pilot, EU infra can be materially cheaper than AWS/GCP-heavy
defaults:

| Component | Planning Range | Notes |
|---|---:|---|
| Small app VM | 4-14 EUR/month | Hetzner CX/CPX class after 2026 price adjustments |
| Medium app VM | 25-50 EUR/month | enough for app + workers in small pilot |
| Managed/object storage | 6-30 EUR/month | depends on retained logs/files |
| Volume/snapshots | usage-based | include backup policy |
| Monitoring/logging | 0-100 EUR/month | open-source first, SaaS if needed |
| Postgres | same VM for lean, managed/private for standard | managed service raises cost but reduces ops risk |

### 6.2 Russia-oriented pilot

For RF customers, final pricing should be calculated via Yandex Cloud/Selectel/VK
Cloud or client-approved provider calculator.

| Component | Planning Range | Notes |
|---|---:|---|
| Small app VM | provider calculator | vCPU/RAM/disk/IP/traffic determine price |
| Object storage | provider calculator | logs, artifacts, transcripts, attachments |
| Managed DB | provider calculator | optional for lean, useful for standard |
| Email/SMS/telephony | local vendor pricing | can dominate run cost in messaging flows |
| Private deployment | 2-5x lean infra | access controls, backups, audit, ops overhead |

### 6.3 LLM usage

LLM cost should be estimated from tokens and volume:

```text
monthly_llm_cost =
  monthly_items
  * avg_input_tokens
  * input_price_per_token
  + monthly_items
  * avg_output_tokens
  * output_price_per_token
  + tool/research/search overhead
```

Model policy:

- Opus-class model: strategy, architecture review, complex missed opportunities;
- Sonnet-class model: synthesis, drafting, workflow extraction;
- Haiku/small model or deterministic code: classification, routing, extraction;
- no frontier model should approve privacy, cost, compliance or production write.

As of the current official Anthropic pricing page, Claude Opus 4.6 legacy API
pricing is 5 USD / MTok input and 25 USD / MTok output; current Opus-class
models on the same page use the same base 5/25 price. Batch and caching can
materially reduce repeated workload cost.

---

## 7. What makes the recommendation credible

### 7.1 Decision policy

The roadmap recommendation is accepted only when all are true:

- workflow step exists in evidence or explicit assumption;
- solution type matches pattern library;
- privacy mode is allowed by deterministic policy;
- cost estimate has assumptions and range;
- high-risk action has human approval gate;
- do-not-automate boundary is explicit;
- frontier candidate passed verifier and human review;
- reviewer can explain why we chose this before a more autonomous agent.

### 7.2 Anti-hallucination controls

| Risk | Control |
|---|---|
| LLM invents workflow | source register + evidence refs + hashes |
| LLM invents cost | deterministic cost engine + rate cards |
| LLM recommends unsafe cloud | deterministic privacy gate |
| LLM over-automates | do-not-automate register + human gates |
| LLM creates unsupported claim | verification appendix |
| Model drift | model/prompt/version receipt |
| Unclear ownership | implementation contract and operator handoff |

### 7.3 Proof layer

This is where Entropy Core becomes commercially valuable. It can be packaged as
an add-on for customers who need trust, governance and auditability:

- evidence receipt for each recommendation;
- artifact hashes and source references;
- verifier status;
- blocked-surface list;
- assumption registry;
- decision log;
- audit bundle export.

Simple positioning:

> We do not just say “AI should do X”. We show which evidence allowed that
> recommendation, which assumptions remain, and which actions are blocked until
> a human approves them.

---

## 8. Commercial packaging

### Package 1. AI Roadmap Sprint

Goal: help company decide whether and where to start with AI.

Typical scope:

- 3-5 workflows;
- 1-2 weeks;
- no production credentials required;
- output: AI Implementation Decision Pack.

Deliverables:

- workflow maps;
- recommendation cards;
- do-not-automate list;
- privacy and data mode;
- role-hour and regional cost estimate;
- first pilot handoff.

### Package 2. AI Workflow Playbook Adoption

Goal: install an operating system for building AI features safely.

Best for:

- customer has internal engineering team;
- they want repeatable AI delivery, not one-off automation;
- they need task graph, eval gates, review loop and operator handoff.

Deliverables:

- implementation contract;
- task graph;
- evidence index;
- eval plan;
- reviewer workflow;
- CI/eval gates;
- operator handoff.

Positioning:

> We leave the customer not only with a roadmap, but with a repeatable way to
> ship AI work without losing control.

### Package 3. Entropy Core Proof Layer

Goal: make recommendations and AI workflows auditable.

Best for:

- sensitive data;
- board/customer-facing reports;
- regulated or reputationally risky workflows;
- consulting delivery where claims must be defensible.

Deliverables:

- proof receipts;
- source hashes;
- assumption registry;
- blocked-surface registry;
- validator status;
- audit bundle.

### Package 4. Implementation Pilot

Goal: build the first workflow after roadmap approval.

Deliverables:

- prototype;
- shadow mode;
- human review queue;
- eval suite;
- pilot report;
- production-lite handoff.

### Package 5. Managed AI Ops

Goal: keep the workflow useful after launch.

Deliverables:

- monthly eval report;
- failure review;
- prompt/model change control;
- cost monitoring;
- new opportunity backlog;
- operator training refresh.

---

## 9. New report table of contents

Every final customer-facing report should use this structure:

1. Executive decision summary.
2. Workflow evidence and current process.
3. Data/privacy classification.
4. Automation opportunity map.
5. Recommendation cards.
6. Implementation architecture.
7. Agents/API/DB/infrastructure bill of materials.
8. Phase-by-phase implementation roadmap.
9. Role-hour estimate.
10. Regional cost estimate: RF / CEE Europe / Western Europe.
11. LLM/API/infrastructure operating cost.
12. Risk and do-not-automate register.
13. Evaluation plan and acceptance criteria.
14. Governance and proof layer.
15. Commercial options: roadmap / playbook / proof layer / pilot / managed ops.
16. Appendix: assumptions, sources, rate card version, evidence refs.

---

## 10. What to improve in the product next

Do not rewrite all six reports by hand. First make the report depth systemic:

1. Add `ReportV2CostModel` schema.
2. Add regional rate cards for RF, CEE Europe and Western Europe.
3. Add infrastructure bill-of-material schema.
4. Add implementation phase schema with role-hours.
5. Add API/integration matrix schema.
6. Add LLM usage calculator: volume x tokens x model price.
7. Add Markdown renderer for detailed v2 reports.
8. Add one full v2 exemplar for accelerator workflow.
9. Regenerate the other five reports from the same structure.
10. Add evals that fail reports without phase roadmap, role-hours, assumptions
    and source-backed price cards.

This turns the product from “roadmap generator” into a pre-sales and delivery
system for AI adoption.

---

## 11. Cofounder demo framing

What to say:

> The current product already generates safe AI roadmaps and blocks bad
> recommendations. The next commercial version packages this into an
> implementation decision pack: evidence, architecture, phase plan, roles,
> regional cost model and proof receipts.

What not to say:

- “we can calculate exact implementation price from a short workflow text”;
- “n8n templates prove market demand”;
- “Claude decides what to implement”;
- “Entropy Core is required for every small customer”;
- “we guarantee ROI”.

Sharper sales position:

> We sell the first confident step into AI: what to build, what not to build,
> why, what it costs in your region, which people and systems are needed, and
> how to prove the pilot worked.

---

## 12. Sources used

External pricing and rate sources checked on 2026-06-02:

- Yandex Cloud Compute pricing docs, updated 2026-05-14:
  https://yandex.cloud/en/docs/compute/pricing
- Hetzner official 2026 price adjustment docs:
  https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/
- Hetzner Cloud changelog, 2026 pricing update notice:
  https://docs.hetzner.cloud/whats-new
- Anthropic official Claude API pricing docs:
  https://platform.claude.com/docs/en/about-claude/pricing
- Russian Python salary snapshot using hh.ru data:
  https://sborka.work/knowledge/salaries/python-developer-salary
- Russian hourly rate PDF examples, 2025/2026 educational and agency snapshots:
  https://xn----ctb8aecph4fn.xn--p1ai/docs/2026_02_06/HzQki8Zykfndd3rA8Yt3NBE3r.pdf
  https://msocialproduction.com/rates.pdf
- Eastern Europe developer rates 2026:
  https://www.zulbera.com/insights/software-developer-rates-eastern-europe-2026/
- European software cost/rate guide 2026:
  https://mantar.io/blog/software-development-costs-europe-2026
- Regional outsourcing rate comparison:
  https://webparadox.com/ru/blog/how-much-does-custom-software-cost/

Internal product references:

- Entropy Core project:
  `~/Documents/dev/ai-stack/projects/Entropy_Protocol/products/entropy-core`
- AI Workflow Playbook:
  `~/Documents/dev/ai-stack/projects/AI_workflow_playbook`
- Entropy proof protocol:
  `~/Documents/dev/ai-stack/projects/AI_workflow_playbook/docs/entropy_core_proof_layer_protocol.md`
