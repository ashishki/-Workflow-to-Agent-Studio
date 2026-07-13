# Клиентский AI Roadmap отчет V2

## Клиентский пример: HVAC lead intake и service-area qualification

Статус: public-source customer-facing demo
Тип: пакет решений по AI-внедрению
Граница: public workflow notes; не доказательство спроса и не evidence из
коммерческого пилота.

---

## 1. Краткое решение для заказчика

HVAC-компания получает заявки через сайт, форму, телефон и online appointment
request. Intake должен быстро понять: service-area fit, urgent/emergency,
residential/commercial, repair/maintenance/install, missing contact details.

Рекомендация: строить **human-reviewed lead intake assistant** с deterministic
field checks, ZIP/service-area rules, emergency escalation and dispatcher
approval.

| Поле | Рекомендация |
|---|---|
| Первый use case | проверка полноты заявки + service-area qualification + dispatcher handoff |
| Не автоматизировать | diagnosis, pricing guarantee, dispatch, edge rejection |
| Scenario | Standard SMB pilot |
| Pilot-ready срок | 5-8 недель |
| Ожидаемый эффект | меньше потерянных заявок, быстрее urgent routing, меньше ручной сортировки |
| Решение | начинать после проверки CRM и service-area rules |

---

## 2. Граница данных и доказательности

| Поле | Рабочее допущение |
|---|---|
| Workflow source | public HVAC service intake notes |
| Monthly volume | 300-1,000 leads/month |
| Systems | website form, phone notes, CRM, dispatcher calendar |
| Data class | contact/address/service issue = sensitive/internal |
| Current pain | incomplete leads, missed urgent cases, manual service-area checks |
| Missing evidence before quote | CRM fields, ZIP rules, emergency policy, dispatcher workflow |

Public-source evidence supports workflow mechanics only. Real proof needs actual
lead volume, conversion, dispatcher corrections and response-time baseline.

---

## 3. Текущий процесс

```mermaid
flowchart LR
    A[Customer request] --> B[Collect contact/service fields]
    B --> C{Service area fit?}
    C -- no --> D[Manual exception/refer]
    C -- yes --> E{Emergency?}
    E -- yes --> F[Urgent phone route]
    E -- no --> G[Scheduling queue]
    G --> H[Dispatcher review]
```

| Шаг | Участник | Система | Боль | Подходит для автоматизации |
|---|---|---|---|---|
| Lead capture | customer/coordinator | form/phone | incomplete fields | high |
| Service-area check | coordinator | ZIP rules/map | repetitive | high deterministic |
| Emergency triage | dispatcher | notes/phone | urgency may be missed | medium HITL |
| Scheduling queue | dispatcher | CRM/calendar | manual routing | medium |
| Diagnosis/pricing | technician/estimator | field visit | professional judgment | do not automate |

---

## 4. Откуда взялись рекомендации

| Слой | Что дает | Граница |
|---|---|---|
| Pattern library | lead qualification, messaging support, appointment booking | known SMB pattern |
| Опция n8n-паттернов | идеи по связкам forms/webhooks, Slack/Telegram alerts, CRM routing, Sheets | источник идей, не готовое решение |
| Frontier candidates | emergency checklist, service-area exception queue | review queue |
| Verifier | blocks diagnosis, pricing guarantee and dispatch without human | deterministic gate |

**Отдельная опция для клиента: анализ публичных n8n-паттернов.**
Для HVAC это быстрый способ собрать список реалистичных integration options:
формы, webhook, CRM, alerts для диспетчера, таблицы отчетности. Мы не копируем
шаблоны, а используем их как reference для дорожной карты и оценки интеграций.

---

## 5. Целевая архитектура

```text
Форма сайта / заметка звонка / email
  -> Нормализация lead intake
  -> Проверка полноты полей
  -> ZIP и service-area rules engine
  -> Классификатор emergency signals
  -> Очередь review для диспетчера
  -> CRM task / lead writeback после approval
  -> SLA и conversion report
  -> Журнал действий
```

| Компонент | Нужен | Комментарий |
|---|---|---|
| Intake Normalizer | yes | normalizes web forms, phone notes, emails |
| Completeness Checker | yes | required contact/address/service fields |
| Service-Area Engine | yes | ZIP/address rules, exception queue |
| Emergency Classifier | yes | conservative escalation, no diagnosis |
| Dispatcher Queue | mandatory | human owns schedule/dispatch |
| CRM Connector | yes | writeback only after dispatcher approval |
| DB | Postgres for pilot | lead status, corrections, evidence |
| Reporting | yes | response time, missed fields, conversion |

---

## 6. Рекомендации

### R1. Проверка полноты lead intake

| Поле | Значение |
|---|---|
| Why | incomplete forms block scheduling |
| Data | name, phone, address/ZIP, service type, urgency |
| Human gate | coordinator approves follow-up |
| Acceptance | 90% incomplete leads get correct missing-field list |
| Not included | diagnosis or pricing |

### R2. Проверка service-area fit

| Поле | Значение |
|---|---|
| Why | deterministic ZIP/address check saves dispatcher time |
| Data | ZIP, address, service radius, branch rules |
| Human gate | exception review before rejection |
| Acceptance | 95% match with dispatcher decision on clear cases |
| Not included | automatic rejection of edge cases |

### R3. Помощник urgent/emergency routing

| Поле | Значение |
|---|---|
| Why | urgent cases need fast path |
| Data | issue description, keywords, time, customer contact |
| Human gate | phone escalation/dispatcher approval |
| Acceptance | high recall on urgent examples; false positives acceptable |
| Not included | technical diagnosis |

### R4. Handoff в CRM и очередь диспетчера

| Поле | Значение |
|---|---|
| Why | reduces lost leads and duplicate manual entry |
| Data | normalized lead, qualification status, notes |
| Human gate | dispatcher approves schedule/dispatch |
| Acceptance | lead writeback works with rollback and audit log |

---

## 7. План внедрения по этапам

| Этап | Срок | Что делаем | Критерий завершения |
|---|---:|---|---|
| 0. Discovery | 1 week | map lead sources, CRM fields, ZIP rules, emergency policy | service manager confirms rules |
| 1. Data readiness | 1 week | define normalized lead schema and required fields | dispatcher approves schema |
| 2. Prototype | 2 weeks | field checker + ZIP rules on historical/exported leads | quality measured against dispatcher labels |
| 3. Pilot | 2-3 weeks | dispatcher queue, CRM writeback, urgent alerts | no unapproved dispatch/rejection |
| 4. Production-lite | 1 week | monitoring, runbook, backup, SLA dashboard | daily ops handoff complete |
| 5. Improvement loop | monthly | tune rules, review conversion, add channels | lead metrics reviewed |

---

## 8. Оценка ролей и часов

| Роль | Lean | Standard | Strict / private |
|---|---:|---:|---:|
| AI solution architect | 10-18h | 20-34h | 36-60h |
| AI automation engineer | 45-90h | 110-220h | 220-380h |
| CRM/integration engineer | 25-60h | 80-160h | 160-300h |
| QA/eval engineer | 12-30h | 40-80h | 80-140h |
| Dispatcher/domain reviewer | 20-50h | 60-120h | 120-220h |
| PM/operator | 10-24h | 30-60h | 60-110h |

---

## 9. Оценка стоимости: РФ и Европа

| Сценарий | Разовая сборка | Ежемесячные расходы | Для чего подходит |
|---|---:|---:|---|
| Lean RF | 600k-1.4m RUB | 30k-100k RUB | lead schema + field checker |
| Standard RF | 1.6m-4m RUB | 100k-300k RUB | CRM/dispatcher pilot |
| Strict RF | 4m-8m+ RUB | 300k-850k RUB | multi-branch/private setup |
| Lean Europe | 10k-24k EUR | 250-900 EUR | proof-of-value |
| Standard Europe | 28k-70k EUR | 900-3.5k EUR | integrated pilot |
| Strict Europe | 70k-160k+ EUR | 3.5k-10k EUR | multi-location operation |

Cost drivers:

- CRM/service-management system complexity;
- address validation/provider cost;
- number of branches/service areas;
- phone transcript availability;
- urgency routing requirements;
- whether lead writeback is enabled.

---

## 10. LLM, API и инфраструктура

| Компонент | Lean setup | Standard setup |
|---|---|---|
| Hosting | small VM | app VM + Postgres + monitoring |
| LLM | small/Sonnet for messy text classification | not used for ZIP truth |
| Address/ZIP | deterministic rules first | optional geocoding API |
| CRM | CSV/manual import | API writeback after approval |
| Alerts | email/Slack/Telegram | CRM task + urgent notification |
| Storage | lead metadata | metadata + correction/audit logs |

LLM should not own service-area truth. It can summarize messy issue text and
flag potential urgency, while deterministic rules and dispatcher review control
actions.

---

## 11. Риски и зоны, которые нельзя автоматизировать

| Риск | Контроль |
|---|---|
| false emergency miss | conservative escalation and dispatcher review |
| wrong service-area rejection | exception queue before rejection |
| pricing/arrival promise | blocked content category |
| unapproved dispatch | dispatcher gate required |
| customer data exposure | redact/log only necessary fields |

Stop conditions:

- lead rejected without human review when service-area confidence is low;
- dispatch scheduled without dispatcher approval;
- assistant gives diagnosis or price guarantee;
- urgent lead alert fails without fallback.

---

## 12. План проверки качества

Тестовый набор:

- 100 исторических leads;
- 30 примеров с неполными полями;
- 30 service-area edge cases;
- 20 urgent/emergency examples;
- 20 не срочных repair/maintenance/install cases.

Критерии приемки:

- missing-field detection выше 90%;
- clear service-area match выше 95%;
- для urgent cases recall важнее precision;
- dispatcher correction rate отслеживается каждую неделю;
- improvement по response time виден после пилота.

---

## 13. Контроль и доказательность

Для HVAC важно объяснить, почему заявка попала в очередь диспетчера, почему она
считается urgent и почему edge case не был автоматически отклонен.

Что получает заказчик:

- версию service-area правил;
- версию urgent/emergency policy;
- журнал approval от диспетчера;
- список заявок, отправленных в exception queue;
- weekly baseline по response time, SLA и conversion.

Слой доказательности на базе Entropy Core полезен, если у компании несколько
филиалов, франшизные правила или нужно объяснять маршрутизацию заявок. AI
Workflow Playbook имеет смысл, если после lead intake команда хочет по той же
схеме внедрять maintenance reminders, quote follow-up и knowledge workflow для
техников.

---

## 14. Коммерческая рекомендация

Рекомендованный оффер: **диагностика lead intake + pilot для service-area,
urgent routing и handoff диспетчеру**.

Начинать, если:

- поток заявок уже создает bottleneck для диспетчера;
- CRM rules можно экспортировать или описать;
- менеджер согласен оставить dispatch и rejection за человеком.

Откладывать, если:

- service-area или pricing rules не описаны;
- заказчик ожидает автономную диагностику HVAC-проблем;
- нет владельца, который будет смотреть исправления диспетчера.
