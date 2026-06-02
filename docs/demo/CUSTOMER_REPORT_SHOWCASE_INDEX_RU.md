# Индекс клиентских отчетов

Статус: индекс для cofounder/sales обсуждения  
Версия: report-v2 showcase pack  
Граница: эти отчеты показывают новый формат пакета решений по AI-внедрению, но
не являются доказательством спроса, фиксированной сметой или evidence из
коммерческого пилота.

## Шесть V2-отчетов

| # | Отчет | Workflow | Почему важен |
|---:|---|---|---|
| 1 | `ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md` | заявки акселератора, review memory, звонки | flagship v2: агенты/API/БД, frontier candidates, proof layer, смета РФ/Европа |
| 2 | `SALON_BOOKING_ROADMAP_RU.md` | запись клиентов, reminders, analytics | простой SMB quick-win, где AI не нужен везде |
| 3 | `ECOMMERCE_SUPPORT_RETURNS_ROADMAP_RU.md` | Shopify support, returns, order status | коммерческий support workflow с refund gates |
| 4 | `LEGAL_INTAKE_ROADMAP_RU.md` | legal/immigration intake | restricted data, private mode и proof layer |
| 5 | `HVAC_LEAD_INTAKE_ROADMAP_RU.md` | service-area lead intake | public-source SMB lead qualification с dispatcher gates |
| 6 | `INCIDENT_COORDINATION_ROADMAP_RU.md` | incident response coordination | internal ops workflow со строгими human gates и runbook proof |

## Что добавляет V2

Каждый отчет теперь включает:

- краткое решение для заказчика;
- границу данных и недостающие inputs перед сметой;
- карту текущего workflow;
- происхождение рекомендаций;
- целевую архитектуру;
- список нужных агентов, API, БД и инфраструктуры;
- рекомендации с human gates;
- поэтапный roadmap внедрения;
- оценку ролей и часов;
- смету для РФ и Европы;
- модель расходов на LLM/API/инфраструктуру;
- риски и do-not-automate список;
- план проверки качества;
- proof layer и коммерческую рекомендацию.

## Как объяснять n8n и frontier model

Каждый отчет теперь можно объяснять через происхождение рекомендаций:

```text
workflow клиента
  -> библиотека паттернов
  -> опциональный анализ публичных n8n-паттернов
  -> дополнительные идеи frontier-модели
  -> проверка правил
  -> human review
```

Главная sales мысль:

> Мы не просто придумываем AI-идеи. Мы строим decision artifact: что делать, что
> не делать, почему, какие системы и люди нужны, сколько это стоит в РФ/Европе,
> какие риски, как доказать pilot success и какие идеи пришли из public
> automation patterns или frontier model.

n8n-паттерны теперь подаются не как лишняя статистика, а как отдельная
коммерческая опция: “быстро проверить, какие похожие автоматизации уже собирают
на практике, и использовать это для более сильного roadmap”.
