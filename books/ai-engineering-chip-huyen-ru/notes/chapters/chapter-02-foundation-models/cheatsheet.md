# Шпаргалка: выбор и адаптация базовой модели по главе 2

Цель: локализовать причину поведения базовой модели до данных, архитектуры/масштаба, post-training или inference/sampling, не смешивая эти уровни.

## Symptom / problem framing

Если модель плохо выполняет задачу, глава не предлагает автоматически выбирать «модель побольше». Возможная причина может находиться в разных местах:

~~~text
training data
→ architecture + scale
→ post-training
→ sampling / inference
→ structured-output layer
→ probabilistic behavior
~~~

## Baseline / context

Перед сравнением моделей зафиксировать, что известно о каждой:

- на каких языках и предметных областях представлены данные;
- архитектура и контекст;
- число параметров;
- число обучающих токенов;
- известный объем обучения в FLOP;
- плотная модель или MoE/разреженная;
- какие этапы post-training применялись;
- какие inference controls доступны;
- нужны ли приложению строгие структурированные результаты.

Если этих данных нет в документации модели: `[Needs confirmation]`.

## Read-only checks

### 1. Training-data fit

Проверить:

- представлен ли нужный язык;
- представлена ли нужная предметная область;
- нет ли признаков того, что задача требует специализированных данных;
- не делает ли токенизация нужного языка вход/выход заметно длиннее.

### 2. Scale fit

Не смотреть только на parameter count. Учитывать три величины главы:

- parameters;
- training tokens;
- training FLOP.

Для MoE отдельно различать общее и активное количество параметров.

### 3. Post-training fit

Уточнить:

- есть ли SFT;
- есть ли preference finetuning;
- какой подход использован: RLHF / DPO / RLAIF / другой;
- на каких демонстрационных/сравнительных данных выполнялась настройка: `[Needs confirmation]`, если не раскрыто.

### 4. Sampling baseline

Зафиксировать доступные request controls:

- temperature;
- top-k;
- top-p;
- stop condition / max output;
- random seed, если provider его предоставляет;
- logprobs, если provider их предоставляет.

### 5. Structured-output baseline

Проверить реальную долю корректных результатов в нужном формате. Не считать инструкцию «верни JSON» гарантией структуры.

### 6. Reliability baseline

Повторить один и тот же запрос и небольшие варианты запроса, чтобы увидеть:

- одинаковый input → разные outputs;
- немного измененный input → резко измененный output.

Глава использует это как проявления несогласованности.

## Interpretation

### Нужный язык или домен слаб

Вероятная зона проблемы — training data. Больше параметров сами по себе не гарантируют исправления.

### Большая модель не выигрывает

Проверить объем/качество данных и поколение модели. Глава прямо показывает, что параметров недостаточно как единственной метрики масштаба.

### Нужна более разговорная/инструктивная модель

Это относится к post-training. SFT оптимизирует предварительно обученную модель под демонстрационные пары «запрос — ответ».

### Нужна настройка поведения под предпочтения

Это относится к preference finetuning. В главе рассматриваются RLHF, DPO и RLAIF; RLHF включает reward model и последующую оптимизацию модели.

### Output слишком случайный

Исследовать sampling controls:

- ниже temperature → более вероятные/предсказуемые токены;
- выше temperature → больше разнообразия и потенциально меньше связности;
- меньший top-k → меньший набор кандидатов;
- top-p → динамический набор по накопленной вероятности.

### Нужен строгий JSON/YAML/regex/class output

Идти по возрастанию жесткости:

~~~text
prompt
→ generate/check again
→ post-processing
→ constrained sampling
→ fine-tuning
~~~

Prompting дешевле и проще, но не гарантирует корректность. Constrained sampling и fine-tuning дают более сильный контроль ценой сложности/ресурсов.

### Нужно повысить качество одного запроса

Inference-time compute: сгенерировать несколько ответов и выбрать лучший по probability/reward/verifier/эвристике/majority. Цена — дополнительные вычисления и latency.

### Нужна детерминированность

Фиксация temperature/top-p/top-k/seed может улучшить повторяемость, но глава явно не гарантирует 100%-ную согласованность.

## Next action

Для практического сравнения моделей:

1. проверить fit обучающих данных;
2. сравнить architecture/deployment constraints;
3. сравнить parameters + training tokens + compute, а не только parameters;
4. выяснить post-training;
5. зафиксировать sampling baseline;
6. измерить structured-output reliability, если она нужна;
7. повторить запросы для оценки consistency;
8. уже затем менять параметры или модель и повторно измерять результат.

## Modifying action

### Изменение sampling settings

Что меняется: распределение/набор кандидатов при генерации токенов.

Примеры source-confirmed controls:

- temperature;
- top-k;
- top-p;
- stop conditions.

Effect: меняются разнообразие, предсказуемость, длина и/или стоимость вывода.

Risk: слишком ранняя остановка может повредить формат; более высокая temperature может сделать вывод менее связным; чрезмерное ограничение может снизить разнообразие.

Verification: повторить набор входов и сравнить требуемые свойства output.

Rollback: точная процедура в главе не задана — `[Needs confirmation]`.

### Fine-tuning / preference tuning

Что меняется: веса/поведение модели после предварительного обучения.

Effect: SFT направляет модель на желаемый формат взаимодействия; preference tuning оптимизирует ответы под предпочтения.

Risk: стоимость/сложность и возможность нежелательных изменений поведения; конкретный rollback procedure в главе не задан.

Verification: оценивать модель до/после изменения на целевых задачах.

Rollback: `[Needs confirmation]`.

## Verification / acceptance checks

Изменение или выбор модели обоснованы по логике главы, если:

- причина проблемы локализована хотя бы до одного слоя;
- parameter count не используется как единственный аргумент;
- известен baseline до изменения;
- sampling settings зафиксированы;
- structured output проверен фактическими результатами, если он нужен;
- probabilistic variability измерена повторными вызовами;
- после modifying action выполнено повторное измерение.

## Rollback

- Request-level sampling change: chapter-specific rollback procedure `[Needs confirmation]`.
- Fine-tuning/post-training change: `[Needs confirmation]`.
- Замена модели: `[Needs confirmation]`.

Глава объясняет влияние настроек и этапов обучения, но не задает эксплуатационный rollback runbook.

## Минимальная карта памяти

~~~text
Foundation model behavior
├─ Training data
│  ├─ quantity / quality / diversity
│  ├─ language distribution
│  └─ domain distribution
├─ Model design
│  ├─ architecture
│  ├─ parameters
│  ├─ training tokens
│  └─ training FLOP
├─ Post-training
│  ├─ SFT
│  └─ preference: RLHF / DPO / RLAIF
├─ Sampling
│  ├─ temperature
│  ├─ top-k
│  ├─ top-p
│  └─ stop conditions
├─ Inference-time compute
│  └─ multiple outputs → select
└─ Risks
   ├─ inconsistency
   └─ hallucinations
~~~
