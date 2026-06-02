# Customer Report Showcase Index

Статус: demo index for cofounder/sales discussion  
Версия: report-v2 showcase pack  
Граница: эти отчеты показывают новый формат `AI Implementation Decision Pack`,
но не являются buyer proof, fixed quote или commercial pilot evidence.

## Six V2 Showcase Reports

| # | Report | Workflow | Why It Matters |
|---:|---|---|---|
| 1 | `ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md` | заявки акселератора, review memory, звонки | flagship v2: agents/API/DB, frontier candidates, proof layer, RF/EU estimate |
| 2 | `SALON_BOOKING_ROADMAP_RU.md` | запись клиентов, reminders, analytics | простой SMB quick-win, где AI не нужен везде |
| 3 | `ECOMMERCE_SUPPORT_RETURNS_ROADMAP_RU.md` | Shopify support, returns, order status | commercial support workflow with refund gates |
| 4 | `LEGAL_INTAKE_ROADMAP_RU.md` | legal/immigration intake | restricted data, private mode and proof layer |
| 5 | `HVAC_LEAD_INTAKE_ROADMAP_RU.md` | service-area lead intake | public-source SMB lead qualification with dispatcher gates |
| 6 | `INCIDENT_COORDINATION_ROADMAP_RU.md` | incident response coordination | internal ops workflow with strict human gates and runbook proof |

## What V2 Adds

Each report now includes:

- executive decision summary;
- evidence boundary and missing evidence before quote;
- current-state workflow map;
- opportunity provenance;
- target architecture;
- agents/API/DB/infrastructure bill of materials;
- recommendation cards with human gates;
- phase-by-phase implementation roadmap;
- role-hour estimate;
- RF/EU cost estimate;
- LLM/API/infrastructure cost model;
- risk and do-not-automate register;
- evaluation plan;
- governance/proof layer and commercial recommendation.

## What Changed After n8n + Frontier

Каждый отчет теперь можно объяснять через provenance:

```text
workflow source
  -> pattern library
  -> public n8n automation signals
  -> optional frontier candidates
  -> deterministic verifier
  -> human review
```

Главная sales мысль:

> Мы не просто придумываем AI-идеи. Мы строим decision artifact: что делать, что
> не делать, почему, какие системы и люди нужны, сколько это стоит в РФ/Европе,
> какие риски, как доказать pilot success и какие идеи пришли из public
> automation patterns или frontier model.
