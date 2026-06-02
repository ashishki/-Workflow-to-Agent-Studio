# Клиентский AI Roadmap отчет V2

## Клиентский пример: салон красоты, запись и reminders

Статус: демонстрационный customer-facing отчет  
Тип: пакет решений по AI-внедрению  
Граница: synthetic demo; не доказательство спроса и не фиксированная смета.
Расчет ниже - planning estimate для разговора с buyer/cofounder.

---

## 1. Краткое решение для заказчика

Салон получает записи через Instagram, WhatsApp, телефон и Google Calendar.
Администратор вручную отвечает на повторяющиеся вопросы, проверяет календарь,
создает запись и отправляет reminders.

Рекомендация: начать не с автономного AI-бота, а с **booking operations layer**:
детерминированные проверки календаря, reminders, weekly analytics и AI только
для черновиков ответов.

| Поле | Рекомендация |
|---|---|
| Первый use case | reminders + booking analytics + черновики ответов в shadow mode |
| Не автоматизировать | штрафы, медицинские советы, спорные жалобы, opt-out клиентов |
| Scenario | Lean RF/EU pilot |
| Pilot-ready срок | 3-5 недель |
| Ожидаемый эффект | меньше no-shows, меньше пропущенных сообщений, меньше ручного follow-up |
| Решение | начинать lean pilot после проверки доступа к календарю и сообщениям |

---

## 2. Граница данных и доказательности

| Поле | Рабочее допущение |
|---|---|
| Workflow source | synthetic salon workflow |
| Weekly volume | 70-100 appointments/week |
| Channels | Instagram, WhatsApp, phone, Google Calendar |
| Current pain | missed messages, manual reminders, no channel analytics |
| Data class | contact details = sensitive; service/date preferences = internal |
| Missing evidence before quote | real message samples, no-show rate, calendar rules, opt-out policy |

Если реальный салон не даст 2-4 недели сообщений, календарных событий и no-show
статистики, стоимость остается broad planning range.

---

## 3. Текущий процесс

```mermaid
flowchart LR
    A[Client message] --> B[Ask service/date/stylist]
    B --> C[Check calendar]
    C --> D[Confirm slot]
    D --> E[Calendar write]
    E --> F[Reminder]
    F --> G[Visit or no-show]
    G --> H[Rebooking follow-up]
```

| Шаг | Участник | Система | Боль | Подходит для автоматизации |
|---|---|---|---|---|
| Intake message | receptionist | WhatsApp/Instagram | repeated questions | high |
| Service/date уточнение | receptionist | messenger | slow back-and-forth | medium |
| Calendar check | receptionist | Google Calendar | double-booking risk | high deterministic |
| Reminder | receptionist | messenger | forgotten manual work | high deterministic |
| Rebooking | owner/stylist | messenger | inconsistent follow-up | medium |
| Complaint/medical advice | owner/stylist | messenger | high judgment | do not automate |

---

## 4. Откуда взялись рекомендации

| Слой | Что дает | Граница |
|---|---|---|
| Pattern library | appointment booking, reminders, reporting automation | known SMB pattern |
| Опция n8n-паттернов | идеи по связкам calendar, WhatsApp/Gmail, Sheets/reporting, reminders | источник идей, не готовое решение |
| Frontier candidates | rebooking queue, source analytics, cancellation-risk list | review queue only |
| Verifier | blocks medical advice, penalties and unapproved live writes | deterministic boundary |

**Отдельная опция для клиента: анализ публичных n8n-паттернов.**  
Для салона это не “мы ставим готовый шаблон”, а быстрый способ увидеть, какие
интеграции уже часто собирают на практике: календарь, сообщения, reminders,
таблицы и отчеты. Это помогает быстрее выбрать реалистичный pilot scope.

---

## 5. Целевая архитектура

```text
Экспорт или webhook из мессенджеров
  -> Нормализация входящих сообщений
  -> Проверка контакта и согласия
  -> Проверка доступности в календаре
  -> Планировщик reminders
  -> Черновики ответов от AI
  -> Очередь approval для администратора
  -> Запись в календарь / отправка сообщения после approval
  -> Еженедельный отчет
  -> Журнал действий
```

| Компонент | Нужен | Комментарий |
|---|---|---|
| Intake Parser | yes | normalizes messages into service/date/stylist/contact fields |
| Calendar API | yes | Google Calendar read; write only after approval |
| Reminder Scheduler | yes | deterministic timing rules |
| AI Draft Worker | optional | drafts polite replies; does not decide availability |
| Review Queue | yes | receptionist approves first live messages |
| DB | SQLite for demo, Postgres for pilot | stores bookings, consent, logs, corrections |
| Monitoring | lightweight | missed reminders, failed sends, double-booking alerts |

---

## 6. Рекомендации

### R1. Автоматизация reminders

Build deterministic reminders 24h/3h before appointment with opt-out handling.

| Поле | Значение |
|---|---|
| Why | immediate value without AI risk |
| Data | calendar event, phone/messenger id, opt-out status |
| Human gate | owner approves templates and timing |
| Acceptance | 95% reminders sent; zero opt-out violations |
| Not included | penalty decisions or cancellation disputes |

### R2. Помощник подбора времени записи

Assistant suggests available slots and drafts replies. Calendar write stays
human-approved until conflict checks are proven.

| Поле | Значение |
|---|---|
| Why | reduces back-and-forth and missed leads |
| Data | service menu, duration rules, calendar, message thread |
| Human gate | receptionist approves final booking |
| Acceptance | 80% common requests get correct slot suggestions |
| Not included | fully autonomous booking for edge cases |

### R3. Еженедельная аналитика записей

Weekly report by channel, no-shows, cancellations, service type and rebooking
opportunities.

| Поле | Значение |
|---|---|
| Why | owner currently lacks channel visibility |
| Data | booking records, source channel, status |
| Human gate | owner reviews report before changing policy |
| Acceptance | report reconciles with calendar within 5% |

---

## 7. План внедрения по этапам

| Этап | Срок | Что делаем | Критерий завершения |
|---|---:|---|---|
| 0. Discovery | 3-5 days | collect messages, calendar rules, service menu, no-show baseline | owner confirms workflow and metric |
| 1. Data readiness | 3-5 days | define booking fields, opt-out rules, calendar access, templates | fields and privacy mode approved |
| 2. Prototype | 1-2 weeks | reminders + analytics from exported data; draft replies in shadow mode | no live sends; owner validates examples |
| 3. Pilot | 2 weeks | enable approved reminders and receptionist review queue | no missed opt-outs; correction rate tracked |
| 4. Production-lite | 1 week | monitoring, backup, runbook, handoff | receptionist can operate without developer |
| 5. Improvement loop | monthly | tune templates, add rebooking experiments | no-show and manual time measured |

---

## 8. Оценка ролей и часов

| Роль | Lean | Standard | Strict / private |
|---|---:|---:|---:|
| AI solution architect | 8-14h | 16-24h | 24-40h |
| AI automation engineer | 32-60h | 80-140h | 140-220h |
| Integration engineer | 12-30h | 40-80h | 80-140h |
| QA/eval engineer | 8-16h | 20-40h | 40-70h |
| Owner/receptionist reviewer | 8-16h | 20-40h | 40-60h |
| PM/operator | 6-12h | 16-28h | 28-44h |

---

## 9. Оценка стоимости: РФ и Европа

Расчет использует v2 rate-card logic из
`docs/demo/CLIENT_REPORT_V2_UPGRADE_STRATEGY_RU.md`.

| Сценарий | Разовая сборка | Ежемесячные расходы | Для чего подходит |
|---|---:|---:|---|
| Lean RF | 250k-650k RUB | 10k-45k RUB | reminders + analytics + shadow drafts |
| Standard RF | 700k-1.7m RUB | 40k-120k RUB | approved messaging + calendar integration |
| Lean Europe | 4k-10k EUR | 80-350 EUR | one-location pilot |
| Standard Europe | 12k-28k EUR | 300-900 EUR | multi-channel workflow |

Cost drivers:

- official WhatsApp/Instagram API access versus manual/export mode;
- number of stylists and service duration rules;
- whether calendar writes are enabled;
- how much message history is processed;
- whether the salon needs Russian or EU data residency.

---

## 10. LLM, API и инфраструктура

| Компонент | Lean setup | Комментарий |
|---|---|---|
| Hosting | small VM or local server | 5-30 EUR/month in EU-style setup; RF via provider calculator |
| DB | SQLite/Postgres | Postgres once multiple users or audit log needed |
| LLM | small/Sonnet-class for draft replies | Opus-class unnecessary for routine booking |
| Messaging API | provider-specific | often bigger constraint than LLM cost |
| Calendar API | Google/Microsoft | write permissions delayed until pilot |

LLM cost should be calculated as:

```text
monthly_messages * avg_tokens_per_reply * model_price
```

For this use case, LLM cost is usually not the main cost. Integration access and
operator rollout are.

---

## 11. Риски и зоны, которые нельзя автоматизировать

| Риск | Контроль |
|---|---|
| double booking | deterministic availability check + human approval |
| opt-out violation | consent filter before every send |
| medical/cosmetology advice | blocked content category |
| wrong cancellation penalty | do not automate penalties |
| hallucinated availability | LLM never owns calendar truth |

Stop conditions:

- reminder sent to opted-out customer;
- calendar write happened without approval during pilot;
- assistant gives medical advice;
- double-booking caused by automation.

---

## 12. План проверки качества

Golden set:

- 50 historical booking messages;
- 20 cancellation/reschedule cases;
- 10 opt-out and edge cases;
- 4 stylist/service duration conflict cases.

Acceptance:

- reminder delivery success > 95%;
- opt-out violation = 0;
- slot suggestion correctness > 80% on common cases;
- owner reports at least 3-5 hours/week manual reduction before expansion.

---

## 13. Governance и proof layer

Base pilot can run without Entropy Core. Add Entropy Core Proof Layer if the
salon group has multiple locations, franchise reporting, sensitive client
complaints or owner wants audit receipts.

Proof artifacts:

- template approval receipt;
- calendar write approval log;
- reminder send log;
- correction history;
- no-show metric baseline and monthly comparison.

AI Workflow Playbook is optional here. It becomes useful if this is the first of
many automation workflows across a salon chain.

---

## 14. Коммерческая рекомендация

Продавать как: **AI Roadmap Sprint + Lean Booking Pilot**.

Лучший первый оффер:

- 1 week paid diagnostic;
- 3-5 week pilot;
- no autonomous bot promise;
- success measured by no-show rate, missed messages and receptionist time.

Начинать, если:

- у салона есть хотя бы 70 записей в неделю или несколько каналов заявок;
- владелец готов согласовать templates и opt-out правила;
- календарь можно подключить хотя бы в read-only режиме.

Откладывать, если:

- поток записей низкий;
- manual reminders уже работают надежно;
- владелец хочет автономного бота без approval.
