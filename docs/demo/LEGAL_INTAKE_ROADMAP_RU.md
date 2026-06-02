# Клиентский AI Roadmap отчет V2

## Клиентский пример: legal / immigration intake

Статус: демонстрационный customer-facing отчет  
Тип: пакет решений по AI-внедрению  
Граница: synthetic demo; не legal advice, не compliance certification, не fixed
quote.

---

## 1. Краткое решение для заказчика

Immigration consultancy тратит много времени на intake, missing documents и
status questions. При этом данные restricted: passport, legal status, family
details, employment history.

Рекомендация: строить **private checklist and case-prep assistant**, а не cloud
legal advisor и не autonomous eligibility engine.

| Поле | Рекомендация |
|---|---|
| Первый use case | missing-document tracker + private checklist assistant |
| Не автоматизировать | legal eligibility, legal strategy, final advice, authority submissions |
| Scenario | Strict/private pilot |
| Pilot-ready срок | 7-10 недель |
| Ожидаемый эффект | меньше back-and-forth, лучше подготовка консультанта, меньше forgotten documents |
| Решение | начинать только после согласования data retention и private mode |

---

## 2. Граница данных и доказательности

| Поле | Рабочее допущение |
|---|---|
| Workflow source | synthetic immigration/legal intake workflow |
| Monthly volume | 50-200 active cases/month |
| Systems | intake form, shared drive, checklist, case tracker, email |
| Data class | restricted identity/legal/family/employment data |
| Current pain | incomplete docs, repeated status questions, manual case prep |
| Чего не хватает перед сметой | checklist taxonomy, document types, retention policy, access model |

Этот отчет намеренно консервативнее, чем SMB booking/support отчеты: privacy и
liability сильно влияют на архитектуру и стоимость.

---

## 3. Текущий процесс

```mermaid
flowchart LR
    A[Lead inquiry] --> B[Intake questions]
    B --> C[Consultant call]
    C --> D[Document checklist]
    D --> E[Client uploads docs]
    E --> F[Completeness check]
    F --> G[Consultant legal review]
    G --> H[Client status updates]
```

| Шаг | Участник | Система | Боль | Подходит для автоматизации |
|---|---|---|---|---|
| Intake questions | coordinator | form/email | repeated data collection | medium |
| Checklist generation | consultant | templates | manual selection | medium HITL |
| Document upload | client/coordinator | drive/portal | missing files | high deterministic |
| Completeness check | coordinator | checklist/drive | tedious verification | high private assistant |
| Legal review | consultant | case file | professional judgment | do not automate |
| Status questions | client/coordinator | email/chat | repeated updates | medium with strict boundaries |

---

## 4. Откуда взялись рекомендации

| Слой | Что дает | Граница |
|---|---|---|
| Pattern library | legal checklist assistant, document extraction, internal knowledge | known pattern |
| Опция n8n-паттернов | идеи по связкам Drive/Notion/Sheets, document processing, AI summaries | источник идей, не готовое решение |
| Frontier candidates | missing-doc prioritization, internal case brief, status FAQ | human review required |
| Verifier | blocks legal advice, eligibility decisions and unrestricted cloud | deterministic gate |

**Отдельная опция для клиента: анализ публичных n8n-паттернов.**  
Для legal/intake это полезно только как research layer: посмотреть, какие
административные связки обычно автоматизируют вокруг документов, drive, таблиц и
статусов. Это не значит, что можно копировать шаблон или отправлять restricted
data в публичный cloud.

---

## 5. Целевая архитектура

```text
Client intake / upload portal
  -> Проверка доступа и класса данных
  -> Private extractor метаданных документов
  -> Checklist rules engine
  -> Missing document tracker
  -> Черновик внутреннего case brief
  -> Очередь review для консультанта
  -> Черновик статуса клиенту после approval
  -> Подтверждение доказательности и журнал аудита
```

| Компонент | Нужен | Комментарий |
|---|---|---|
| Private intake store | yes | raw identity docs should not go to unrestricted cloud |
| Checklist Rules Engine | yes | deterministic jurisdiction/case-type mapping where possible |
| Document Metadata Extractor | yes | extracts type/status, not legal conclusion |
| Internal Brief Worker | optional | drafts summary for consultant only |
| Client Status Draft | optional | no legal interpretation |
| Review Queue | mandatory | consultant owns legal meaning |
| DB | private Postgres | cases, checklist status, approvals |
| Object Storage | encrypted/private | documents, receipts, retention controls |

---

## 6. Рекомендации

### R1. Трекер недостающих документов

| Поле | Значение |
|---|---|
| Why | high-volume admin pain with low legal judgment |
| Data | checklist, uploaded files, due dates |
| Human gate | coordinator approves client reminders |
| Acceptance | 90% checklist statuses correct on sample cases |
| Not included | legal interpretation of documents |

### R2. Приватный помощник по checklist

| Поле | Значение |
|---|---|
| Why | reduces repeated checklist assembly |
| Data | case type, jurisdiction, approved template library |
| Human gate | consultant approves checklist before client use |
| Acceptance | consultant accepts 70%+ checklist drafts after edits |
| Not included | eligibility decision or legal strategy |

### R3. Внутренний case brief

| Поле | Значение |
|---|---|
| Why | consultant prepares faster before call/review |
| Data | intake answers, uploaded document status, notes |
| Human gate | consultant reviews before relying on it |
| Acceptance | brief cites source fields and flags missing evidence |
| Not included | final advice to client |

### R4. Черновики ответов по статусу дела

| Поле | Значение |
|---|---|
| Why | reduces repeated “what is happening?” questions |
| Data | case status, checklist status, approved generic FAQ |
| Human gate | coordinator/consultant approves messages |
| Acceptance | no legal interpretation in drafts |

---

## 7. План внедрения по этапам

| Этап | Срок | Что делаем | Критерий завершения |
|---|---:|---|---|
| 0. Discovery | 1-2 weeks | map case types, documents, data retention, roles | consultant confirms boundaries |
| 1. Data readiness | 2 weeks | checklist taxonomy, private storage, access controls | privacy mode approved |
| 2. Prototype | 2-3 weeks | missing-doc tracker on historical cases | statuses match human review |
| 3. Pilot | 2-3 weeks | coordinator review queue and approved reminders | no raw restricted data leaves boundary |
| 4. Production-lite | 1-2 weeks | backups, audit log, runbook, retention controls | owner can operate safely |
| 5. Governance | monthly | review corrections, template changes, audit receipts | consultant signs off changes |

---

## 8. Оценка ролей и часов

| Роль | Lean | Standard | Strict / private |
|---|---:|---:|---:|
| AI solution architect | 16-28h | 32-56h | 60-100h |
| AI automation engineer | 80-150h | 180-320h | 320-560h |
| Integration/backend engineer | 40-90h | 100-220h | 220-420h |
| Data/privacy reviewer | 20-50h | 60-120h | 120-240h |
| QA/eval engineer | 20-40h | 60-120h | 120-220h |
| Consultant/domain reviewer | 30-70h | 80-160h | 160-300h |
| PM/operator | 20-40h | 50-100h | 100-180h |

---

## 9. Оценка стоимости: РФ и Европа

| Сценарий | Разовая сборка | Ежемесячные расходы | Для чего подходит |
|---|---:|---:|---|
| Lean RF | 1.2m-2.8m RUB | 80k-220k RUB | checklist tracker with private handling |
| Standard RF | 3m-7m RUB | 220k-650k RUB | private pilot with upload/status workflow |
| Strict RF | 7m-15m+ RUB | 650k-1.8m+ RUB | audit-heavy restricted workflow |
| Lean Europe | 20k-45k EUR | 700-2k EUR | limited private pilot |
| Standard Europe | 55k-130k EUR | 2k-7k EUR | integrated case workflow |
| Strict Europe | 130k-300k+ EUR | 7k-20k+ EUR | regulated/private deployment |

Why higher than salon/support:

- restricted data;
- private storage and retention controls;
- higher domain review time;
- legal boundary review;
- audit/proof expectations.

---

## 10. LLM, API и инфраструктура

| Компонент | Рекомендованный режим | Комментарий |
|---|---|---|
| Hosting | private cloud or client-approved environment | public cloud only after legal/privacy review |
| Storage | encrypted object storage | raw docs require retention controls |
| DB | private Postgres | case metadata, checklist status, approvals |
| LLM | private-approved provider or local/private path | no unrestricted cloud for raw docs |
| RAG | optional | only over approved templates and generic FAQ |
| Audit | required | source refs, reviewer approvals, template versions |

LLM usage should be minimized for raw documents. Use deterministic metadata
checks first, and use LLM for internal summaries only after redaction/private
mode approval.

---

## 11. Риски и зоны, которые нельзя автоматизировать

| Риск | Контроль |
|---|---|
| AI gives legal advice | blocked category + consultant review |
| unrestricted cloud exposure | private/local mode for restricted docs |
| wrong checklist | consultant approves before client use |
| stale template | template version in every output |
| authority submission error | submissions remain human-only |

Stop conditions:

- raw passport/legal data sent to unapproved cloud;
- assistant states eligibility or strategy as final advice;
- client-facing message contains legal interpretation without consultant review;
- retention/audit log fails.

---

## 12. План проверки качества

Тестовый набор:

- 30 исторических кейсов со статусом checklist;
- 20 примеров недостающих документов;
- 10 вопросов клиента по статусу;
- 10 edge cases с неоднозначными документами.

Критерии приемки:

- точность статуса документов выше 90%;
- consultant принимает больше 70% checklist drafts после правок;
- legal advice в AI output = 0;
- нарушений boundary для raw restricted data = 0;
- coordinator экономит измеримое follow-up time в пилоте.

---

## 13. Контроль и доказательность

В legal/intake workflow контроль обязателен. Здесь нельзя, чтобы AI сам решал
eligibility, давал legal advice или отправлял документы в органы. Польза AI -
ускорить административную часть и подготовку, а не заменить консультанта.

Что получает заказчик:

- ссылку на источник для каждой checklist-рекомендации;
- список спорных или неполных документов;
- подтверждение, что консультант утвердил checklist или сообщение клиенту;
- список зон, которые AI не имеет права автоматизировать: eligibility,
  strategy, submission, final advice;
- журнал изменений шаблонов, model и prompt.

Слой доказательности на базе Entropy Core здесь рекомендуется: он помогает
показать, почему рекомендация была разрешена, какие assumptions остались и где
система остановилась. AI Workflow Playbook полезен, если фирма хочет выстроить
повторяемый внутренний процесс внедрения AI для нескольких legal/admin
workflows.

---

## 14. Коммерческая рекомендация

Рекомендованный оффер: **диагностика legal intake + private pilot по документам
и checklist + слой доказательности**.

Начинать, если:

- у consultancy достаточно кейсов, чтобы экономия времени была заметна;
- консультант готов определить границы checklist;
- заказчик понимает: это ускорение admin workflow, а не автоматизация legal
  advice.

Откладывать, если:

- фирма хочет автономный legal advice;
- data governance не определен;
- нет владельца, который будет утверждать templates и версии.
