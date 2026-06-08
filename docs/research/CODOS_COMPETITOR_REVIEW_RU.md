# Codos: конкурентный разбор

Date: 2026-06-08

Source boundary: использована только публичная поверхность `https://www.codos.ai/`.
Глубина ограничена тем, что сайт отдает marketing page и React bundle, а не
полный продуктовый whitepaper.

## Что видно из публичного сайта

- Codos позиционируется как слой для AI-transformation.
- Обещание сформулировано вокруг диагностики, установки AI-слоя и развития
  компании через агентов по разным функциям.
- На сайте есть маршруты и формы для apply, partnerships, quiz, report,
  download.
- В bundle видны роли Founding Engineer, Founding Product, Founding Growth и
  партнерские варианты Partnership / Acquihire / Apply for other role.
- В публичной форме есть вопросы про AI setup, agents, workflows, automation и
  опыт построения AI brain.

## Вероятная стратегия Codos

Это не выглядит как узкий workflow-анализатор. Скорее, Codos продает широкую
категорию: AI-transformation operating layer для компаний, которым нужно быстро
получить результат от AI across functions.

Сильная сторона:

- понятный ambitious narrative;
- высокий perceived value для фаундеров и руководителей;
- упаковка ближе к "мы трансформируем компанию", а не "мы делаем отчет".

Риск такого позиционирования:

- buyer может ожидать слишком много автономности;
- обещание agents across functions требует сильной proof discipline;
- без явного блока "что агент не заменит" легко получить красивое демо и
  разочарование на production rollout.

## Вывод для Workflow-to-Agent Studio

Нам не надо копировать широкое обещание Codos. Более сильный wedge:

> pre-implementation AI roadmap studio, который до внедрения показывает, где AI
> имеет смысл, где нужен обычный workflow/script, где нужен человек, сколько это
> стоит, какие данные нужны и какие проверки доказывают готовность.

Практический ответ в продукте:

- добавить обязательную секцию `What The Agent Will Not Replace`;
- показывать realistic autonomy level для каждого roadmap;
- связывать автономность с рисками, human gates, regression tests и stop
  conditions;
- продавать не "магического агента", а AI Roadmap Sprint + pilot runbook +
  evaluation/proof layer;
- использовать n8n/public templates как pattern inspiration, но не как
  автоматическое доказательство, что workflow можно запускать без ревью.

## Как объяснять кофаундеру

Codos играет на большом рынке AI-transformation. Это подтверждает, что боль и
категория реальные. Но у нас может быть более точный entry point для компаний,
которые пока не знают, с чего начать:

- они дают нам discovery материалы;
- мы строим evidence-linked roadmap;
- показываем 1-3 безопасных первых шага;
- считаем стоимость, сроки, роли, API, БД, LLM и gates;
- честно показываем, что агент не заменит;
- после этого можно продавать implementation sprint или proof-layer pilot.

Такой подход менее хайповый, но лучше подходит для B2B presale: он снижает
страх, дает управляемый первый шаг и оставляет место для дальнейшей продажи.
