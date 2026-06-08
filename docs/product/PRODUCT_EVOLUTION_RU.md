# Эволюция продукта

Purpose: сохранить стратегическую траекторию продукта от AI Roadmap Studio к
более широкому AI operating layer для компаний.

## Короткая мысль

Сейчас мы не строим прямого конкурента Codos. Мы строим нижний слой, из которого
может вырасти похожая категория.

Codos продает vision: AI layer для компании, company brain, agents across
functions, transformation partnership.

Наш более безопасный entry point:

> сначала доказать на конкретных workflow, где AI полезен, где опасен, сколько
> это стоит, кто владелец, какие данные нужны и какие proof gates нужны до
> запуска.

## Почему не надо сразу копировать Codos

Широкое обещание "AI layer for the company" хорошо звучит для рынка и
инвесторов, но для раннего продукта оно создает высокий delivery risk:

- нужно быстро подключаться к множеству систем;
- нужно хранить и обновлять company brain;
- нужно доказывать качество агентов в разных функциях;
- нужно отвечать за безопасность действий;
- клиент может ожидать автономность, которую нельзя честно дать на первом
  пилоте.

Поэтому наш wedge лучше:

- меньше обещаний;
- быстрее первый коммерческий deliverable;
- проще продать как diagnostic;
- проще доказать value;
- ниже риск испортить доверие клиента.

## Лестница развития

### 1. AI Roadmap Studio

Текущий слой.

Вход:

- discovery notes;
- SOP;
- transcript;
- public workflow notes;
- описание CRM/support/sales/backoffice процесса.

Выход:

- workflow map;
- do-not-automate list;
- recommendation cards;
- cost/time/team ranges;
- privacy mode;
- realistic autonomy level;
- proof gates;
- implementation handoff.

Коммерческий продукт:

- AI Roadmap Sprint;
- 1-2 недели;
- 3-5 workflow;
- decision artifact для владельца бизнеса.

### 2. Workflow Pattern Library

Следующий слой.

Мы копим реальные кейсы:

- какой workflow был на входе;
- какую рекомендацию дали;
- что клиент выбрал;
- что внедрили;
- сколько заняло;
- сколько стоило;
- какие роли понадобились;
- какие API/БД/интеграции были нужны;
- какие риски проявились;
- какие proof gates сработали;
- какой outcome получили.

Ценность:

- система лучше выбирает похожие паттерны;
- отчеты становятся точнее;
- оценки стоимости и сроков становятся менее "planning range" и более
  эмпирическими;
- появляется собственный корпус workflow knowledge.

### 3. Workflow Intelligence Platform

Слой для команд, которые хотят не один отчет, а постоянную карту процессов.

Возможности:

- хранить карту workflow компании;
- видеть владельцев процессов;
- отслеживать automation backlog;
- хранить decisions, assumptions, gates и evals;
- сравнивать похожие workflow между клиентами в anonymized form;
- обновлять roadmap после новых данных.

Коммерческий продукт:

- ежемесячная подписка для AI adoption office;
- managed backlog для AI/automation initiatives;
- quarterly AI roadmap refresh.

### 4. Company Workflow Memory

Ближе к Codos-подобному направлению.

Для каждого клиента появляется operational memory:

- как устроены процессы;
- какие системы используются;
- какие данные чувствительные;
- какие rules и exceptions есть;
- какие pilots уже запускались;
- какие метрики были до/после;
- какие automation patterns разрешены;
- какие actions запрещены.

Важно: это не "сырая база всех документов клиента для обучения модели". Это
структурированная, permissioned, reviewable память.

### 5. Agent Operating Layer

Только после накопления паттернов, evals и trust.

Агенты запускаются не с пустого листа, а из проверенной карты:

- sales follow-up assistant;
- CRM hygiene agent;
- support triage assistant;
- application review assistant;
- incident/runbook assistant;
- reporting analyst;
- backoffice document assistant.

Ограничения:

- tool permissions;
- human gates;
- logs;
- evals;
- rollback;
- proof receipts;
- stop conditions.

## Как продукт "дообучается"

Сначала не через fine-tuning большой LLM.

Правильный порядок:

1. Структурированные кейсы.
2. Улучшение pattern matching.
3. Улучшение retrieval/RAG.
4. Улучшение scoring и cost estimates.
5. Улучшение evals.
6. Только потом fine-tuning узких моделей, если данных достаточно и есть
   понятная задача.

## Data flywheel

Самые ценные данные:

- workflow на входе;
- recommendation на выходе;
- human review;
- implementation decision;
- фактическая стоимость;
- фактические сроки;
- фактические роли;
- ошибки пилота;
- gates, которые сработали;
- outcome metrics.

Это может стать moat, потому что такие данные сложно получить из интернета.

## Privacy и consent

Клиентские данные нельзя просто использовать для общего обучения.

Нужны режимы:

- private workspace per client;
- raw data never reused by default;
- anonymized pattern extraction;
- explicit consent for case reuse;
- redaction before pattern mining;
- proof receipts;
- local/private deployment for sensitive customers.

## Стратегическая формулировка

Сейчас:

> AI Roadmap Studio для компаний, которые не знают, с чего начать с AI.

Дальше:

> Workflow Intelligence Platform, которая учится на внедрениях и помогает
> компаниям постоянно выбирать, запускать и проверять AI-автоматизации.

Позже:

> Company AI Operating Layer, где агенты работают поверх проверенной workflow
> memory, а не поверх хаотичного промпта.
