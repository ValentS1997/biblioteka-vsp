# Шпаргалка: методология оценки по главе 3

Цель: выбрать метод оценки под конкретный failure mode и не смешивать изменение приложения с изменением измерительного инструмента.

## Symptom / problem framing

Типичная ошибка главы: команда смотрит на несколько ответов «на глаз», выбирает известный benchmark или одну красивую метрику и считает это доказательством качества.

Проблема усиливается у базовых моделей:

- outputs открытого типа;
- допустимых правильных ответов может быть много;
- сложные ответы требуют экспертной проверки;
- модели часто black-box;
- публичные benchmarks быстро насыщаются;
- оценивать приходится не только известные задачи, но и новые способности.

## Baseline / context

Перед выбором метрики зафиксировать:

1. Что именно считается сбоем?
2. Можно ли проверить функцию автоматически?
3. Есть ли эталонный ответ?
4. Если эталон есть, важна форма текста или смысл?
5. Если качество субъективно, кто является судьей — человек или AI?
6. Если используется AI-судья, какая точная версия системы:
   - model;
   - prompt;
   - sampling settings.
7. Нужен абсолютный score или только relative ranking?
8. Можно ли повторить оценку тем же evaluator-ом позже?

## Read-only checks

### 1. Можно проверить функциональную корректность?

Если output можно исполнить или проверить против измеримой цели, это сильный кандидат на exact evaluation.

Примеры из главы:

- generated code → unit tests;
- `pass@k`;
- игровой бот → измеримый игровой score;
- optimization task → измеримый objective.

### 2. Есть эталонные ответы?

Если да, выбрать уровень сравнения:

- exact match — только для очень ограниченного множества допустимых ответов;
- lexical similarity — если важна текстовая форма;
- semantic similarity — если важен смысл.

### 3. Нужна semantic similarity?

Проверить:

- какая embedding model используется;
- стабильна ли она между итерациями;
- подходит ли она для нужной модальности/домена;
- не меняется ли evaluator одновременно с приложением.

### 4. Нужен AI-судья?

Зафиксировать evaluator как версионируемый объект:

~~~text
judge = model + prompt + sampling settings
~~~

Проверить:

- criterion;
- rubric / scoring system;
- примеры в prompt;
- self-bias;
- position bias;
- verbosity bias;
- latency/cost;
- privacy/IP boundary.

### 5. Нужна comparative evaluation?

Уточнить:

- user действительно способен выбрать лучший ответ;
- вопрос про preference, а не про фактическую правильность;
- число сравнений достаточно;
- ranking algorithm известен;
- pairwise signals отражают реальный workload.

## Interpretation

### Низкая perplexity

Модель хорошо предсказывает данный текст относительно своей learned distribution. Это полезный signal, но не универсальная прикладная оценка, особенно после SFT/RLHF.

### Высокая perplexity

Текст для модели необычен/непредсказуем. Это может быть признаком domain shift, необычного текста или другого распределения; конкретная причина требует отдельной проверки.

### Высокий BLEU/ROUGE, но функция не работает

Лексическое сходство не заменяет functional correctness.

### Низкий exact match при хорошем human judgment

Возможно, эталонный набор не покрывает допустимые перефразирования; перейти к lexical/semantic similarity или другой оценке.

### Высокая semantic similarity

Ответ близок эталону в embedding space. Надежность вывода зависит от качества embedding model.

### AI-судья изменил score после изменения prompt/model

Нельзя считать это изменением качества приложения без контрольной повторной оценки прежним evaluator-ом.

### Pairwise win rate вырос

Это relative signal. Он не говорит автоматически, что новая модель достигла absolute product threshold или оправдывает более высокую стоимость.

## Next action

Для новой evaluation-задачи:

1. сформулировать failure mode;
2. выбрать exact metric, если она существует;
3. если exact metric нет — определить reference-based или subjective method;
4. зафиксировать evaluator definition;
5. измерить baseline;
6. провести повторные измерения для проверки согласованности;
7. сопоставить score с реальной прикладной целью;
8. комбинировать методы там, где один evaluator недостаточен.

## Modifying action

### Изменение evaluator definition

Что меняется: prompt, model, sampling settings, rubric или scoring scale evaluator-а.

Effect: оценки могут измениться даже при неизменном приложении.

Risk:

- ломается сопоставимость с историческими результатами;
- можно принять evaluator drift за improvement/regression приложения;
- могут измениться bias, latency и cost.

Verification:

- прогнать старый и новый evaluator на одном фиксированном наборе;
- сравнить согласованность;
- проверить корреляцию с точной или human evaluation там, где это возможно;
- версионировать evaluator definition.

Rollback: точная procedure в главе не задана — `[Needs confirmation]`. Практически необходимо сохранять предыдущую evaluator definition, но конкретный механизм хранения глава не задает.

### Увеличение числа AI-judge вызовов

Что меняется: coverage оценки и compute/API workload.

Effect: выше confidence/coverage, но выше cost и latency.

Verification: измерить прирост полезного evaluation signal относительно дополнительных затрат.

Rollback: `[Needs confirmation]`.

## Verification / acceptance checks

Evaluation design соответствует логике главы, если:

- failure mode сформулирован;
- exact evaluation используется там, где она доступна;
- reference-based metric не выдается за functional correctness;
- embedding model известна для semantic similarity;
- AI-judge definition зафиксирована как `model + prompt + sampling settings`;
- judge bias и reproducibility проверяются;
- comparative ranking не интерпретируется как absolute quality;
- результаты можно повторить на фиксированном evaluation set;
- изменение evaluator-а отделено от изменения приложения.

## Rollback

- Evaluation-only read operation: `[Not applicable]`.
- Persisted change to evaluator prompt/model/rubric: `[Needs confirmation]`.
- Replacement of ranking algorithm: `[Needs confirmation]`.

Глава подчеркивает необходимость стабильного evaluator-а во времени, но не дает repository/config rollback runbook.

## Минимальная карта памяти

~~~text
Evaluation
├─ Exact
│  ├─ functional correctness
│  ├─ pass@k
│  ├─ exact match
│  ├─ lexical similarity
│  │  ├─ BLEU / ROUGE / METEOR++ / TER / CIDEr
│  └─ semantic similarity
│     ├─ embeddings
│     ├─ cosine similarity
│     └─ BERTScore / MoverScore
├─ Subjective
│  └─ AI judge
│     ├─ model
│     ├─ prompt
│     ├─ sampling settings
│     └─ bias / consistency / cost / latency
└─ Comparative
   ├─ pairwise preference
   ├─ win rate
   └─ ranking: Elo / Bradley–Terry / TrueSkill
~~~
