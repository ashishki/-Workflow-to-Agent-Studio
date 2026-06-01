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

## Что показать в репозитории

1. `README_RU.md` - понятное описание продукта.
2. `docs/product/report_contract.md` - контракт итогового roadmap.
3. `docs/security/privacy_modes.md` - логика cloud/private/local.
4. `docs/evals/roadmap_quality_eval.md` - как проверяем качество roadmap.
5. `docs/methodology/ROADMAP_CALCULATION_RU.md` - как считаются cost/time,
   source of truth, LLM boundaries и hallucination safeguards.
6. `tests/eval/` - автоматические проверки.
7. `.data/demo/exports/hair_salon_roadmap.md` - generated demo output после
   запуска скрипта.
8. `.data/demo/exports/public_hvac_roadmap.md` - public-source generated demo
   output после запуска скрипта.

## Proof points

Технические доказательства:

- full suite: `350 passed`;
- локальный CLI без внешних credentials;
- typed schemas через Pydantic;
- deterministic evals;
- privacy policy gates;
- cost range checks;
- forbidden-claim checks;
- approved handoff blocked unless review approved.
- public-source workflow demos reuse saved public fixtures, not invented
  customer data.

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

Говорить:

- “технический MVP работает”;
- “мы готовы проверять commercial demand”;
- “первый paid package - AI readiness / AI roadmap diagnostic”;
- “продукт помогает не потратить деньги на неправильную AI-автоматизацию”.
- “public-source demos доказывают техническую работу на опубликованных workflow,
  но buyer proof должен прийти через real pilot”.

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
