# n8n Pattern Mining

Цель: насытить pattern library реальными automation signals из публичных n8n
template repositories, но не превратить продукт в копию чужих шаблонов и не
затащить в roadmap небезопасные automation ideas.

## Два этапа

### Этап 1: насытить библиотеку без дублей

Мы используем публичные n8n templates как research corpus.

Что извлекаем:

- trigger;
- integrations;
- actions;
- AI nodes;
- human gate signals;
- risky action signals;
- data sensitivity hints;
- stable fingerprint;
- suggested archetype.

Что не извлекаем по умолчанию:

- credentials;
- webhook URLs;
- private notes;
- raw workflow JSON в committed product files;
- claims вроде "этот workflow доказал ROI".

Задача этапа 1 - получить не тысячи JSON-шаблонов, а чистую библиотеку
абстрактных паттернов:

```text
Public n8n workflow
    -> metadata signals
    -> fingerprint
    -> dedupe
    -> cluster
    -> draft pattern candidate
    -> human review
    -> SMB implementation pattern
```

### Этап 2: подключить frontier model

Frontier model нужна не для финального решения, а для расширения пространства
вариантов:

- найти missed opportunities;
- предложить alternative implementation paths;
- найти do-not-automate зоны;
- объяснить tradeoffs;
- сформулировать assumptions;
- предложить eval cases.

Модель не утверждает roadmap. Ее output становится `unapproved opportunity
candidate`, который проходит deterministic checks и human review.

## Почему сначала n8n corpus

n8n templates полезны, потому что показывают, какие процессы люди уже пытаются
автоматизировать:

- CRM lead routing;
- support triage;
- invoice/document processing;
- email drafts;
- Slack/Telegram notifications;
- spreadsheet sync;
- AI summarization;
- webhook-based back-office workflows.

Это не buyer validation, но это хороший источник для pattern discovery.

## Dedupe logic

Дубликаты надо убирать не по имени файла, а по структуре workflow.

Fingerprint строится из:

- normalized node types;
- integrations;
- operation/resource;
- trigger/action markers;
- connection edges.

Если два templates имеют одинаковый fingerprint, они считаются одним candidate,
а source locators объединяются.

## Как candidate становится pattern

Candidate можно превратить в SMB pattern только если:

- понятна бизнес-задача;
- есть workflow signals;
- clear required data;
- privacy default не слабее фактических data signals;
- есть do-not-automate boundaries;
- cost/time/resources можно оценить диапазоном;
- есть evaluation metrics;
- human reviewer принял candidate.

## Роль frontier model

Хороший prompt для frontier model должен просить:

- 3-5 дополнительных opportunities;
- почему эти opportunities могут быть полезны;
- почему они могут быть плохой идеей;
- какие данные нужны;
- где нужен human gate;
- какие assumptions критичны;
- что проверить в pilot;
- какие candidates надо reject.

Плохой prompt:

```text
Вот workflow. Что нам автоматизировать?
```

Хороший prompt:

```text
Вот workflow map, detected patterns, privacy class, known assumptions и n8n
metadata signals. Предложи missed opportunity candidates. Не утверждай финальные
recommendations. Для каждого candidate укажи evidence/assumptions, risk,
human gate, do-not-automate и confidence.
```

## Guardrails

- Pattern library остается source of structured truth.
- Frontier model предлагает candidates, но не утверждает roadmap.
- Privacy, cost, forbidden claims и approval gates остаются deterministic.
- Human reviewer решает, попадет ли candidate в библиотеку.
- Public-source templates не являются commercial proof.
