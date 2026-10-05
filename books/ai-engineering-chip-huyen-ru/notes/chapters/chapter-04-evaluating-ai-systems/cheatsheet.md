# Шпаргалка: оценка AI-систем по главе 4

Цель: построить evaluation workflow до масштабирования приложения и выбирать модель по собственным требованиям, а не по общему рейтингу.

## Symptom / problem framing

Типовые признаки плохой evaluation practice:

- приложение развернуто, но команда не знает, помогает ли оно пользователям;
- модель выбрана по leaderboard position без private evaluation;
- quality score не связан с бизнес-результатом;
- измеряется только end-to-end результат, поэтому невозможно локализовать сбой;
- evaluator меняется, но historical scores продолжают сравнивать напрямую;
- один aggregate score скрывает cost, latency, safety или instruction-following failures.

## Baseline / context

До разработки или выбора модели зафиксировать:

1. Бизнес-цель приложения.
2. Utility threshold — минимальный приемлемый уровень.
3. Критерии оценки.
4. Hard requirements — то, что нельзя нарушить.
5. Soft attributes — то, что можно улучшать.
6. Evaluation datasets.
7. Scoring/rubric.
8. Evaluation methods для каждого критерия.
9. Cost и latency evaluation pipeline.
10. Какие переменные должны логироваться между итерациями.

## Read-only checks

### 1. Определить критерии

Минимальная taxonomy главы:

| Группа | Что проверяет |
|---|---|
| Domain capability | Умеет ли модель решать нужную предметную задачу |
| Generation capability | Насколько качествен, фактически согласован и безопасен open-ended output |
| Instruction following | Соблюдает ли модель формат, длину, язык, content/style constraints |
| Cost / latency | Укладывается ли система в экономические и временные ограничения |

### 2. Разделить hard и soft attributes

Hard examples по логике главы могут включать:

- licence/policy restrictions;
- data privacy boundary;
- model/API availability;
- on-device requirement;
- latency, если provider-controlled latency нельзя изменить.

Soft attributes:

- accuracy;
- factual consistency;
- toxicity;
- instruction-following score;
- latency, если self-hosted stack позволяет оптимизацию.

Классификация зависит от конкретного deployment.

### 3. Проверить public benchmark fit

Для каждого benchmark спросить:

- измеряет ли он нужную способность;
- не дублирует ли сильно другой benchmark;
- насколько прозрачна aggregation logic;
- не достиг ли benchmark saturation;
- есть ли риск contamination;
- одинаковы ли условия evaluation для сравниваемых моделей.

### 4. Проверить custom evaluation set

Набор должен включать:

- representative production distribution;
- known failure cases;
- relevant slices;
- out-of-scope inputs;
- realistic instruction patterns;
- при необходимости noisy/typo examples.

### 5. Проверить evaluation reliability

- повторный run дает сопоставимый результат?
- bootstrap/repeated subsets дают приемлемую variance?
- high-scoring examples действительно лучше low-scoring?
- score коррелирует с бизнес-метрикой?
- evaluator cost/latency приемлемы?

## Interpretation

### Модель лидирует в публичной таблице

Это shortlist signal, а не доказательство application fit. Проверить свои criteria и private evaluation.

### MCQ score высокий

Подтверждает performance в закрытом формате. Не доказывает способность генерировать качественные open-ended ответы.

### Functional correctness высокий, но приложение неудобно

Добавить критерии эффективности, readability, instruction following, latency или другие свойства, релевантные продукту.

### Factual consistency низкая

Разделить:

- local factual consistency — output vs provided context;
- global factual consistency — output vs trusted external facts.

Затем подобрать evaluation method под тип factuality.

### Instruction-following failures

Отделить знания модели от выполнения constraints. Проверять format/keywords/length/language автоматически там, где это возможно.

### Public benchmark score подозрительно высокий

Рассмотреть contamination. Source-confirmed heuristics:

- n-gram overlap;
- unusually low perplexity on evaluation data.

### Aggregate score хороший, slice плохой

Не полагаться на агрегат. Проверить data slices и риск Simpson's paradox.

### Новый вариант выигрывает на 1–3%

Нужен больший evaluation set. Глава подчеркивает: чем меньше difference, тем больше sample size требуется для уверенного сравнения.

## Next action

Для нового приложения:

1. определить business outcome;
2. создать evaluation criteria до разработки;
3. определить hard/soft attributes;
4. отфильтровать невозможные модели;
5. использовать public benchmarks только для shortlist;
6. провести private evaluation;
7. оценить каждый компонент, turn и task;
8. связать score с business metrics и utility threshold;
9. проверить slices и statistical stability;
10. развернуть только после acceptance;
11. продолжить monitoring и production feedback.

## Modifying action

### Изменение модели

Что меняется: inference behavior и потенциально cost, latency, capabilities, safety и instruction following.

Risk:

- aggregate quality может улучшиться, а важный slice — ухудшиться;
- API provider/model version может иметь другие ограничения;
- public benchmark improvement может не переноситься в application workload.

Verification:

- выполнить тот же private evaluation pipeline;
- сравнить hard requirements;
- проверить major slices;
- повторно измерить cost/latency.

Rollback: точная техническая процедура зависит от deployment и в главе не задана — `[Needs confirmation]`.

### Изменение evaluation pipeline

Что меняется:

- criteria;
- scoring scale;
- evaluation data;
- AI-judge prompt/config;
- method mix;
- sample size.

Risk: historical metrics могут стать несопоставимыми.

Verification:

- зафиксировать все измененные variables;
- прогнать old/new pipeline на контрольном наборе;
- проверить variance/correlation;
- подтвердить связь с business metric.

Rollback: `[Needs confirmation]`; глава требует отслеживать experiment variables, но конкретный config rollback mechanism не задает.

## Verification / acceptance checks

Evaluation system соответствует логике главы, если:

- критерии определены до release decision;
- у каждого критерия есть понятный evaluator;
- hard requirements проверяются отдельно;
- public benchmarks используются только как один signal;
- private data отражают реальный workload;
- компоненты оцениваются отдельно для fault localization;
- rubric содержит шкалы и примеры;
- score связан с business impact / utility threshold;
- slices анализируются отдельно;
- reliability проверена повторными/bootstrapped runs;
- evaluation cost и latency измерены;
- изменения evaluator-а логируются.

## Rollback

- Read-only evaluation run: `[Not applicable]`.
- Model replacement: `[Needs confirmation]`.
- Evaluation criteria/rubric change: `[Needs confirmation]`.
- API ↔ self-host deployment change: `[Needs confirmation]`.

Глава определяет, что нужно сравнивать и логировать, но не задает инфраструктурный rollback runbook.

## Минимальная карта памяти

~~~text
Evaluate application
├─ define criteria first
│  ├─ domain capability
│  ├─ generation quality
│  ├─ instruction following
│  └─ cost / latency
├─ model selection
│  ├─ hard-filter
│  ├─ public benchmark shortlist
│  ├─ private evaluation
│  └─ production monitoring
├─ custom pipeline
│  ├─ evaluate every component
│  ├─ rubric + examples
│  ├─ business mapping + threshold
│  ├─ methods + datasets
│  ├─ slices
│  ├─ bootstrap / variance
│  └─ pipeline reliability
└─ iterate
   └─ track all evaluator variables
~~~
