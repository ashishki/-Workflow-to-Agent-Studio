# Демо для кофаундера

Цель документа: показать продукт не как набор модулей, а как понятный
коммерческий артефакт для sales/marketing обсуждения.

## One-liner

AI Roadmap Studio помогает компании понять, **где AI стоит внедрять, где не
стоит, какие риски, privacy mode, бюджет, этапы и human gates**, до начала
дорогого implementation.

## Как объяснить за 30 секунд

Компании сейчас часто хотят “внедрить AI”, но не знают, с чего начать. Мы берем
их реальные рабочие процессы: звонки, CRM steps, заявки, support flow, sales
follow-up, back-office operations. Затем превращаем это в roadmap:

- какие процессы подходят для AI;
- где достаточно обычной автоматизации;
- где нужен человек;
- где нельзя автоматизировать;
- какие данные чувствительные;
- сколько примерно стоит первый шаг;
- как проверить качество;
- что отдать implementation-команде.

## Demo story

Показываем на простом примере hair salon:

1. Есть workflow: клиент пишет, администратор проверяет календарь, подтверждает
   запись, отправляет reminder.
2. Система генерирует roadmap.
3. Roadmap говорит:
   - автоматизировать reminders и часть booking flow;
   - не автоматизировать штрафы за отмену и медицинские советы;
   - cloud можно только после redaction контактных данных;
   - нужен human gate перед live calendar writes;
   - есть cost/time/team assumptions;
   - есть eval plan.

Потом показываем legal consultancy как контраст:

1. Там restricted data: passport/legal status.
2. Система не предлагает unrestricted cloud bot.
3. Она рекомендует private/local checklist assistant и оставляет legal advice
   человеку.

Это показывает зрелость продукта: он умеет говорить не только “давайте AI”, но
и “здесь AI опасен”.

Потом показываем public-source workflow как credibility layer:

1. HVAC lead intake взят из сохраненных публичных workflow notes.
2. Система строит roadmap без customer data и без внешних credentials.
3. Roadmap показывает lead qualification, privacy, do-not-automate и handoff
   gates.

Формулировка: synthetic demos проверяют edge cases, public-source demos
показывают работу на опубликованных workflow descriptions.

Потом объясняем отдельную опцию: анализ публичных automation-паттернов.

1. Мы не копируем n8n-шаблоны как готовые решения.
2. Мы используем их как reference: какие связки и интеграции люди уже часто
   автоматизируют.
3. Для клиента это можно продавать как расширенный research: “посмотрим, какие
   похожие automation patterns уже встречаются на практике”.
4. Frontier model смотрит на workflow + краткое описание найденных паттернов и
   предлагает missed opportunities.
5. Verifier не дает модели превратить candidate в approved roadmap без human
   review.

Формулировка: n8n-паттерны помогают не начинать с пустого листа, frontier model
расширяет список вариантов, verifier удерживает качество и safety.

## Что показать в терминале

```bash
bash scripts/demo_roadmap_ru.sh
```

Ожидаемый смысл вывода:

- команда запускается локально;
- создается roadmap report;
- виден output Markdown path;
- видны ключевые секции;
- видно, что есть privacy mode, do-not-automate и verification appendix.

Дополнительный mining demo:

```bash
.venv/bin/python scripts/mine_n8n_templates.py --top 70
```

Смысл вывода:

- публичные n8n-репозитории уже склонированы в ignored `.data/n8n_sources`;
- raw workflow JSON не коммитится;
- система извлекает metadata, дедуплицирует и пишет summary;
- summary показывает archetypes, integrations и review queue.

Frontier demo с Claude Opus 4.6:

```bash
.venv/bin/python scripts/run_frontier_opportunity_discovery.py --env-check
.venv/bin/python scripts/run_frontier_opportunity_discovery.py --max-tokens 6000
```

Смысл вывода:

- `ANTHROPIC_API_KEY` доступен;
- модель `claude-opus-4-6`;
- candidates сохраняются в ignored `.data/frontier/`;
- verifier показывает, что candidates не exportable без human review.

## Что показать в репозитории

1. `README_RU.md` - понятное описание продукта.
2. `docs/demo/CLIENT_REPORT_V2_UPGRADE_STRATEGY_RU.md` - новый стандарт
   клиентского отчета v2: фазы внедрения, агенты/API/БД/инфраструктура,
   role-hours, региональные ставки РФ/Европа, LLM/API cost model, proof layer и
   commercial packaging.
3. `docs/demo/CUSTOMER_REPORT_SHOWCASE_INDEX_RU.md` - индекс 6 красивых
   customer-facing отчетов.
4. `docs/demo/ACCELERATOR_APPLICATION_REVIEW_ROADMAP_RU.md` - сложный workflow:
   заявки акселератора, CRM, звонки, review memory, cost/time/team estimates,
   n8n public signals и frontier candidates.
5. `docs/demo/SALON_BOOKING_ROADMAP_RU.md` - SMB quick-win: booking, reminders,
   analytics.
6. `docs/demo/ECOMMERCE_SUPPORT_RETURNS_ROADMAP_RU.md` - support, order status,
   returns и refund approval.
7. `docs/demo/LEGAL_INTAKE_ROADMAP_RU.md` - restricted legal/immigration intake.
8. `docs/demo/HVAC_LEAD_INTAKE_ROADMAP_RU.md` - public-source service lead
   intake.
9. `docs/demo/INCIDENT_COORDINATION_ROADMAP_RU.md` - internal incident
   coordination и runbook assistant.
10. `docs/experiments/n8n_template_mining_summary.md` - техническое приложение
   по анализу публичных n8n-паттернов.
11. `docs/experiments/frontier_opportunity_discovery_opus46_summary.md` - что
   Claude Opus 4.6 предложил и как verifier это обработал.
12. `docs/product/report_contract.md` - контракт итогового roadmap.
13. `docs/security/privacy_modes.md` - логика cloud/private/local.
14. `docs/evals/roadmap_quality_eval.md` - как проверяем качество roadmap.
15. `docs/methodology/ROADMAP_CALCULATION_RU.md` - как считаются cost/time,
   source of truth, LLM boundaries и hallucination safeguards.
16. `docs/methodology/AGENT_EXPECTATION_CHECK_RU.md` - почему в отчете есть
   блок "что агент не заменит" и как считается realistic autonomy level.
17. `docs/research/CODOS_COMPETITOR_REVIEW_RU.md` - конкурентный контекст:
   почему рынок AI-transformation реален и чем наш wedge отличается.
18. `docs/product/PRODUCT_EVOLUTION_RU.md` - как продукт может вырасти от
   roadmap sprint к workflow intelligence platform и company AI operating layer.
19. `tests/eval/` - автоматические проверки.
20. `.data/demo/exports/hair_salon_roadmap.md` - generated demo output после
   запуска скрипта.
21. `.data/demo/exports/public_hvac_roadmap.md` - public-source generated demo
   output после запуска скрипта.

Важно для разговора: шесть showcase reports уже приведены к v2-формату. Теперь
они показывают не только breadth, но и нужную клиентскую глубину: фазы, смета,
инфраструктура, proof layer, role-hours и коммерческие пакеты.

## Proof points

Технические доказательства:

- full suite: `365 passed`;
- локальный CLI без внешних credentials;
- typed schemas через Pydantic;
- deterministic evals;
- privacy policy gates;
- cost range checks;
- forbidden-claim checks;
- approved handoff blocked unless review approved.
- public-source workflow demos reuse saved public fixtures, not invented
  customer data.
- roadmap report теперь явно показывает realistic autonomy level, что агент не
  заменит, human-owned responsibilities, myths и proof gates до rollout.
- анализ публичных n8n-паттернов используется как опциональный research layer
  для поиска похожих automation-паттернов.
- Claude Opus 4.6 produced frontier candidates, but verifier kept all of them
  non-exportable until human review.

Продуктовые доказательства:

- понятный buyer pain: компании хотят AI, но не знают с чего начать;
- понятный deliverable: AI implementation roadmap;
- понятный wedge: pre-implementation diagnostic;
- можно продать вручную до масштабирования;
- не требует production integrations на первом этапе.

## Что не говорить

Не говорить:

- “мы уже доказали рынок”;
- “это автоматизирует компанию”;
- “это готовый AI agent platform”;
- “мы гарантируем ROI”;
- “мы certified compliance solution”.
- “public-source demo доказывает спрос рынка”.
- “n8n-шаблоны доказывают, что рынок хочет именно наш продукт”.
- “Claude сам решил, что внедрять”.

Говорить:

- “технический MVP работает”;
- “мы готовы проверять commercial demand”;
- “первый paid package - AI readiness / AI roadmap diagnostic”;
- “продукт помогает не потратить деньги на неправильную AI-автоматизацию”.
- “public-source demos доказывают техническую работу на опубликованных workflow,
  но доказательство спроса должно прийти через real pilot”.
- “n8n-шаблоны - это отдельная research-опция для поиска похожих
  automation-паттернов, а не доказательство спроса”.
- “frontier model расширяет список candidates, но verifier и human review
  решают, что попадет в roadmap”.

## Первый paid offer

Название:

**AI Roadmap Sprint**

Формат:

- 1-2 недели;
- 3-5 workflows;
- локальная обработка материалов;
- roadmap report;
- prioritization;
- do-not-automate list;
- privacy/cost/risk review;
- handoff для первой инициативы.

Покупатель получает не “AI demo”, а decision artifact: что делать, что не делать
и почему.

## Новый коммерческий стандарт отчета

После критики ранних showcase reports правильная упаковка такая:

- `AI Roadmap Sprint` - базовый paid diagnostic;
- `AI Workflow Playbook Adoption` - допродажа для команд, которые хотят
  повторяемый процесс AI delivery;
- `Entropy Core Proof Layer` - допродажа для evidence receipts, assumptions,
  blocked surfaces и audit bundle;
- `Implementation Pilot` - сборка первого workflow;
- `Managed AI Ops` - ежемесячные evals, cost monitoring и improvement loop.

Формулировка для кофаундера:

> Мы продаем не “агента”, а первый уверенный шаг в AI: что строить, что не
> строить, почему, сколько это стоит в РФ/Европе, какие люди и системы нужны, и
> как доказать, что пилот сработал.

## Точки роста продукта

Главная стратегическая мысль:

> Мы не начинаем как Codos-клон. Мы начинаем как более приземленный wedge:
> evidence-linked AI roadmap для конкретных workflow. Но из этого может вырасти
> похожий большой слой - workflow intelligence и company AI operating layer.

### 1. От roadmap к pattern library

После каждого paid sprint мы можем сохранять не сырые данные клиента, а
структурированный опыт:

- какой workflow был на входе;
- что предложили;
- что клиент выбрал;
- что реально внедрили;
- сколько заняло;
- сколько стоило;
- какие API, БД, роли и gates понадобились;
- какие ошибки были;
- какой outcome получили.

Почему это важно:

- оценки стоимости и сроков становятся точнее;
- появляются повторяемые implementation patterns;
- sales получает реальные кейсы;
- продукт начинает учиться на внедрениях, а не только на промптах.

### 2. От pattern library к Workflow Intelligence Platform

Следующий продуктовый слой: не один отчет, а постоянная карта workflow компании.

Что это может дать клиенту:

- backlog AI/automation initiatives;
- владельцы процессов и approval gates;
- история decisions/assumptions;
- evals и proof receipts;
- регулярный refresh roadmap;
- понимание, какие процессы уже готовы к автоматизации, а какие еще нет.

Почему это продаваемо:

- компании не внедряют AI один раз;
- процессы, CRM, команды и политики постоянно меняются;
- им нужен не только pilot, а change-control loop.

### 3. От workflow memory к агентам

Агенты должны появляться не с пустого листа, а поверх проверенной workflow
memory:

- sales follow-up assistant;
- CRM hygiene agent;
- support triage assistant;
- application review assistant;
- incident/runbook assistant;
- reporting analyst.

Почему это безопаснее:

- у агента есть boundaries;
- есть human gates;
- есть logs/evals;
- есть rollback;
- есть список действий, которые агент не имеет права делать.

### 4. Как продукт будет "дообучаться"

Сначала не через fine-tuning большой модели.

Правильный порядок:

1. Копим структурированные кейсы.
2. Улучшаем pattern matching.
3. Улучшаем retrieval/RAG.
4. Улучшаем scoring и cost estimates.
5. Улучшаем evals.
6. Только потом рассматриваем fine-tuning узких моделей.

Почему это сильнее:

- не нарушаем privacy клиентов;
- учимся на фактических внедрениях;
- создаем собственный workflow corpus;
- можем объяснить каждую рекомендацию.

### 5. Чем это отличается от Codos

Codos продает большой vision: AI-transformation layer, company brain, agents
across functions.

Наш вход проще:

- один sprint;
- конкретные workflow;
- понятный отчет;
- понятные риски;
- понятная смета;
- понятные gates;
- следующий шаг к pilot.

Почему это может быть сильнее на ранней стадии:

- легче продать первому клиенту;
- меньше delivery risk;
- проще доказать value;
- проще накопить кейсы;
- можно постепенно прийти к company AI operating layer без завышенного обещания
  на первом разговоре.

## Главная гипотеза

Компании готовы платить не только за внедрение AI, но и за **понятный, безопасный
и практичный план внедрения**, если он помогает им выбрать первый workflow и
избежать дорогой ошибки.

## Что должен проверить sales cofounder

1. Кто быстрее всего понимает pain: CEO, COO, Head of Ops, Sales Ops, Support
   Lead или consultant.
2. За какую формулировку готовы платить:
   - AI readiness audit;
   - AI implementation roadmap;
   - AI automation opportunity map;
   - AI workflow diagnostic.
3. Какой вход проще получить:
   - интервью;
   - SOP;
   - call transcript;
   - CRM process screenshots/exports;
   - support tickets.
4. Готовы ли платить за roadmap без немедленного implementation.
5. Какой price point не вызывает долгого procurement.
