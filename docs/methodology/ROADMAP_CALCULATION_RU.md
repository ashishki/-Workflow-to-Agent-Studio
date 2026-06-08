# Как считаются roadmap, стоимость, сроки и риски

Этот документ объясняет, что является источником истины в AI Roadmap Studio,
откуда берутся оценки, где может использоваться LLM и как продукт защищается от
галлюцинаций.

## Короткий ответ

Текущая версия не просит LLM "придумать бизнес-план". Roadmap собирается из
типизированных данных, versioned pattern library, deterministic privacy gates,
cost engine, scoring model и verification receipt.

LLM может помогать в будущем на этапах извлечения и чернового синтеза, но
финальные safety-critical решения не принадлежат LLM.

## Source of Truth

| Вопрос | Источник истины сейчас | Что это значит |
|---|---|---|
| Что за workflow | локальный input file или public-source fixture | модель не должна выдумывать процесс вне evidence |
| Какие шаги/актеры/системы | typed workflow/profile data | важные поля проходят Pydantic validation |
| Какой тип решения | `workflow_agent_studio/patterns/smb/*.json` + matcher | решение выбирается из versioned implementation patterns |
| Privacy class | deterministic privacy classifier + policy gate | cloud/private/local решается правилами, не вкусом модели |
| Cost/time/team | deterministic cost engine + assumptions | это planning range, не quote |
| Priority | deterministic scoring model | оценка воспроизводима и объяснима |
| Реальный уровень автономии | agent expectation check | показывает, что агент не заменит и какие gates нужны |
| Claims/evidence | verification appendix | важные claims связаны с source refs или assumptions |
| Approved handoff | reviewer checklist | без human approval handoff блокируется |

## Как считается workflow

В текущем roadmap layer workflow берется из одного из двух типов источников:

1. Synthetic SMB demo input:
   - hair salon;
   - e-commerce;
   - legal consultancy.

2. Public-source workflow fixture:
   - HVAC lead intake;
   - NetBox issue triage;
   - GitLab incident workflow.

Для public-source demos source of truth - сохраненные fixtures и source
registers в repo. Это реальные опубликованные workflow descriptions, но они не
являются customer/buyer proof.

## Как считается тип решения

Система сначала ищет implementation pattern:

- appointment booking;
- lead qualification;
- customer support triage;
- e-commerce returns;
- legal checklist;
- reporting automation;
- internal knowledge assistant;
- document extraction;
- invoice processing;
- sales email assistant;
- messaging support bot.

Pattern задает:

- recommended solution type;
- required data;
- deterministic steps;
- LLM-owned steps;
- required roles;
- risks;
- evaluation metrics;
- when-not-to-use.

Важно: продукт должен рассматривать script/API/rules/human-in-the-loop до
высокоавтономных agents. Это защита от "agent everywhere".

## Как считаются cost/time/resources

Сейчас это не рыночный quote и не live pricing. Это planning range.

Cost engine использует:

- pattern base range;
- scope multiplier: small/medium/large;
- monthly volume multiplier;
- privacy multiplier:
  - `lightweight_cloud` дешевле;
  - `private_analysis` дороже;
  - `local_on_prem` еще дороже;
- maintenance range;
- human review monthly range;
- integration/subscription range;
- assumptions;
- confidence level.

Пример:

```text
one_time = pattern_base_range * scope_multiplier * privacy_multiplier
monthly = pattern_monthly_base * volume_multiplier * privacy_multiplier
maintenance = percent_of_one_time + privacy_overhead
human_review = volume_based_review_range
```

Если нет assumptions, cost estimate невалиден. Если cost - одна точка вместо
диапазона, eval это ловит.

## Откуда берутся актуальные цены

Сейчас в коде есть planning placeholder:

`workflow_agent_studio/costing/price_cards.py`

Он специально говорит:

> Manual planning placeholder; update from official provider pricing before
> quoting.

То есть текущие оценки можно показывать как planning ranges, но нельзя выдавать
как коммерческую смету без обновления price cards.

Правильный источник актуальных цен перед quote:

- официальные pricing pages LLM providers;
- цена конкретной CRM/helpdesk/telephony integration;
- реальные объемы клиента;
- стоимость reviewer time;
- hosting/private/local deployment costs.

Это должен быть отдельный `price_card_version`, а не текст в README.

## Где помогают LLM

В текущем deterministic demo roadmap generation LLM не нужен: `model_metadata`
указывает `provider=local`, `model=deterministic-roadmap-service`.

В полной архитектуре LLM может помогать здесь:

- извлечь workflow steps из messy SOP/transcript;
- предложить missing questions;
- суммаризировать input;
- draft recommendation prose;
- draft risk notes;
- draft handoff language.

Но LLM не должен:

- финально решать privacy mode;
- утверждать cost;
- approve handoff;
- делать compliance claims;
- мутировать CRM/GitHub/Slack;
- принимать legal/medical/financial/HR decisions.

## Frontier model layer

После T84 frontier model используется только как generator дополнительных
`FrontierOpportunityCandidate`.

Разделение ролей:

| Layer | Что делает | Может ли утверждать roadmap |
|---|---|---|
| Pattern library | дает known implementation patterns | нет, это input |
| n8n mining | дает public metadata signals and clusters | нет, это research corpus |
| Frontier model | предлагает missed opportunities, alternatives, risks | нет, только candidates |
| Deterministic verifier | проверяет evidence/assumptions, privacy, human gates, autonomy | нет, только blocks/allows review |
| Human reviewer | принимает, отклоняет или просит изменения | да, после review |

Frontier candidate не может стать approved recommendation, если:

- нет evidence refs или explicit assumptions;
- нет required human gate;
- candidate privacy class слабее detected source privacy class;
- предложен high-autonomy agent;
- нет do-not-automate boundaries;
- нет cost drivers;
- candidate пытается автоматизировать high-impact decision.

## Как страхуемся от галлюцинаций

Защиты:

1. Typed schemas  
   Все важные outputs проходят Pydantic validation.

2. Evidence-or-assumption rule  
   Рекомендация должна иметь evidence или explicit assumption.

3. Deterministic validators  
   Privacy gates, forbidden claims, path constraints, single-point cost checks и
   approval gates не делегируются LLM.

4. Source hashes  
   Roadmap receipt хранит source hashes.

5. Model metadata  
   Receipt хранит provider/model/prompt/generation mode.

6. Versioned model references  
   Recommendation trace хранит pattern/cost/scoring/privacy model versions.

7. Do-not-automate list  
   Отдельно фиксирует зоны, где automation unsafe.

8. Agent expectation check  
   Отдельно фиксирует realistic autonomy level, human-owned responsibilities,
   workflow-specific myths и proof gates before rollout.

9. Human review  
   Approved handoff невозможен без approved reviewer checklist.

10. Eval suite  
   Tests ловят forbidden claims, unsafe privacy, missing evidence/assumptions,
   single-point costs и broken traces.

## Честная граница

Можно говорить:

- продукт технически работает на synthetic и public-source workflow examples;
- он генерирует typed roadmap, review checklist и approved handoff;
- он защищается deterministic gates и evals.

Нельзя говорить:

- это доказало buyer demand;
- это точная коммерческая смета;
- это compliance certification;
- это заменяет интервью с владельцем процесса;
- это может сразу подключиться к CRM и автономно работать.

Для коммерческого proof нужен real pilot: реальный workflow, реальный reviewer,
реальные объемы, реальные интеграции и recorded measurement row.
