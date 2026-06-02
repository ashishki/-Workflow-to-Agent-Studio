# Customer Report Showcase Index

Статус: demo index for cofounder/sales discussion  
Граница: эти отчеты показывают формат и глубину продукта, но не являются buyer
proof.

## Six Showcase Reports

| # | Report | Workflow | Why It Matters |
|---:|---|---|---|
| 1 | `ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md` | заявки акселератора, review memory, звонки | сложный AI-native workflow с frontier candidates |
| 2 | `SALON_BOOKING_ROADMAP_RU.md` | запись клиентов, reminders, analytics | простой SMB quick-win, где AI не нужен везде |
| 3 | `ECOMMERCE_SUPPORT_RETURNS_ROADMAP_RU.md` | Shopify support, returns, order status | понятный коммерческий support workflow |
| 4 | `LEGAL_INTAKE_ROADMAP_RU.md` | legal/immigration intake | restricted data и сильные do-not-automate границы |
| 5 | `HVAC_LEAD_INTAKE_ROADMAP_RU.md` | service-area lead intake | public-source SMB lead qualification example |
| 6 | `INCIDENT_COORDINATION_ROADMAP_RU.md` | incident response coordination | internal ops workflow с high-risk human gates |

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
> не делать, почему, сколько это займет, какие данные нужны, какие риски, и какие
> идеи пришли из public automation patterns или frontier model.
