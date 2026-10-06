# Шпаргалка: промт-инжиниринг по главе 5

Цель: проектировать prompts как тестируемые, версионируемые production artifacts и не использовать prompt text как единственную границу безопасности.

## Symptom / problem framing

Типовые симптомы:

- небольшая правка формулировки резко меняет результат;
- модель игнорирует формат или продолжает ввод пользователя;
- сильный prompt работает в playground, но ломается в приложении;
- после смены model/version quality деградирует без очевидной причины;
- длинный контекст формально помещается в window, но нужная информация теряется;
- prompt chain стала дорогой и медленной;
- prompt optimization tool создает неожиданные API calls;
- внешний документ/tool output способен изменить поведение модели;
- sensitive/state-changing action выполняется без отдельного system control.

## Baseline / context

Перед изменением prompt зафиксировать:

1. Model/version.
2. Chat template.
3. System prompt.
4. User/task template.
5. Few-shot examples.
6. Context source и размер.
7. Sampling settings.
8. Expected output schema.
9. Evaluation dataset и metrics.
10. Cost/latency baseline.
11. Security assumptions и доступные tools/actions.

## Read-only checks

### 1. Проверить final prompt

Перед отправкой в модель вывести/инспектировать окончательный prompt и убедиться, что system/user content соответствует model-specific chat template.

Особенно проверить:

- специальные tags/tokens;
- лишние переводы строк;
- порядок system/user sections;
- delimiters;
- output marker;
- examples;
- фактический context.

### 2. Проверить prompt robustness

Вносить небольшие изменения:

- число ↔ слово;
- регистр;
- whitespace;
- порядок нейтральных элементов;
- небольшие переформулировки.

Если output резко меняется, prompt/model combination чувствительна к формулировке и требует более тщательной evaluation.

### 3. Проверить эффективную длину контекста

Максимальная длина context window не равна эффективной.

Source-confirmed методы:

- NIAH;
- RULER-подобные проверки.

Если модель хуже находит информацию по мере роста контекста, уменьшить prompt или изменить context-building strategy.

### 4. Проверить формат вывода

Явно определить:

- allowed values;
- JSON keys/schema;
- length limits;
- нужны ли preambles;
- delimiter между input и output.

Delimiter следует выбирать таким, чтобы он с низкой вероятностью встретился во входных данных.

### 5. Проверить security boundary

Prompt-level instructions недостаточны для dangerous actions.

Проверить:

- есть ли isolation/sandbox;
- требуют ли state-changing commands human approval;
- есть ли input/output guardrails;
- фильтруется ли PII/toxic output;
- анализируются ли suspicious usage patterns;
- можно ли внешнему tool/document output переопределить trusted instruction.

## Interpretation

### Prompt работает в одном клиенте, но хуже в другом

Проверить chat template и финальную serialized form. Разные wrappers могут собирать один и тот же logical prompt по-разному.

### Few-shot улучшает качество, но растут cost/latency

Это нормальный trade-off. Проверить, нужен ли каждый example и не даст ли более сильная model тот же quality с меньшим количеством examples.

### Длинный context ухудшает ответы

Проверить effective context usage, особенно информацию в середине prompt. Сократить нерелевантные данные или перестроить context.

### Большой монолитный prompt трудно отлаживать

Разбить на подзадачи. Это дает промежуточные observability points, но может увеличить число model calls и latency.

### CoT/self-critique повышает local metric

Проверить end-to-end system metric, latency и cost. Локальное улучшение не гарантирует улучшения всей системы.

### Prompt tool «оптимизировал» качество

Проверить generated prompt, number of API calls, hidden evaluators и используемый chat template. Tool output не считать trusted автоматически.

### Violation rate низкий, но пользователи часто получают отказ

Проверить false refusal rate. Безопасность не должна достигаться путем блокировки всех запросов.

## Next action

Для нового prompt workflow:

1. начать с простого ручного prompt;
2. задать ясную task definition;
3. добавить required output format;
4. добавить минимально достаточный context;
5. при необходимости добавить examples;
6. inspect final serialized prompt;
7. оценить на фиксированном evaluation set;
8. измерить cost/latency;
9. при сложной задаче разбить workflow на подзадачи;
10. версионировать prompt + metadata;
11. провести adversarial/security evaluation;
12. добавить system-level controls;
13. после каждого изменения re-evaluate.

## Modifying action

### Изменение prompt

Что меняется: instructions/examples/context formatting.

Risk:

- regression на других data slices;
- изменение output schema;
- рост token usage;
- несовместимость с новой model/template.

Verification:

- fixed evaluation set;
- end-to-end system test;
- output-schema validation;
- token/cost/latency measurement;
- security regression tests.

Rollback: вернуть предыдущую versioned prompt definition. Конкретный storage/deploy mechanism зависит от системы — `[Needs confirmation]`.

### Разбиение prompt на chain

Что меняется: один model call превращается в несколько подзадач/calls.

Effect:

- лучше observability/debugging;
- возможен parallel execution независимых шагов;
- можно использовать разные модели;
- меняются cost/latency.

Verification:

- сравнить end-to-end metric;
- проверить каждый intermediate output;
- измерить total calls/tokens/latency.

Rollback: вернуть предыдущую monolithic prompt version — конкретный deployment mechanism `[Needs confirmation]`.

### Добавление prompt-engineering tool

Что меняется: появляется automation layer, который может генерировать prompts и hidden model calls.

Risk:

- неожиданный API spend;
- template bugs;
- tool updates меняют behavior;
- слишком длинные chains.

Verification:

- inspect generated prompts;
- count API calls;
- pin/test tool behavior;
- compare against manual baseline.

Rollback: вернуться к сохраненной ручной prompt version; конкретный package/config rollback `[Needs confirmation]`.

### Усиление defensive controls

Что меняется: model/prompt/system safeguards.

Risk: повышение false refusal rate и latency/cost.

Verification:

- violation rate;
- false refusal rate;
- benign workload regression;
- adversarial test set.

Rollback: `[Needs confirmation]` для конкретной implementation; security weakening без повторной evaluation недопустимо.

## Verification / acceptance checks

Prompt workflow соответствует логике главы, если:

- final prompt известен и inspectable;
- model-specific template проверен;
- prompt versioned;
- evaluation set и metrics зафиксированы;
- output format deterministic enough for downstream use;
- context минимально достаточен;
- prompt changes сравниваются систематически;
- tool-generated prompts не принимаются вслепую;
- cost/latency измеряются;
- security testing включает violation и false refusal;
- dangerous actions защищены system-level boundary.

## Rollback

- Read-only evaluation: `[Not applicable]`.
- Prompt text/version change: возврат к предыдущей версии возможен концептуально; exact deployment procedure — `[Needs confirmation]`.
- Model/chat-template change: `[Needs confirmation]`.
- Prompt-chain topology change: `[Needs confirmation]`.
- Security-policy change: `[Needs confirmation]`.

## Минимальная карта памяти

~~~text
Prompt engineering
├─ prompt structure
│  ├─ task description
│  ├─ examples
│  ├─ task/input
│  └─ context
├─ execution correctness
│  ├─ chat template
│  ├─ final prompt inspection
│  ├─ output schema
│  └─ context effectiveness
├─ optimization
│  ├─ clear instructions
│  ├─ few-shot
│  ├─ decomposition
│  ├─ CoT / self-critique
│  └─ iteration + evaluation
├─ lifecycle
│  ├─ metadata
│  ├─ versioning
│  └─ experiment tracking
└─ defense
   ├─ model level
   ├─ prompt level
   └─ system level
~~~
