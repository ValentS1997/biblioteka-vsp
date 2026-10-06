# Шпаргалка: проектирование наборов данных по главе 8

Цель: создать training dataset, который демонстрирует требуемое поведение модели и выдерживает проверки качества, coverage, compliance и downstream effectiveness.

## Symptom / problem framing

Типовые симптомы:

- модель учится неправильному стилю или формату;
- performance растет слабо несмотря на увеличение dataset;
- разные annotators дают противоречивые labels;
- отдельные user patterns отсутствуют в training data;
- dataset содержит duplicates;
- train/test contamination;
- synthetic data выглядят правдоподобно, но не улучшают model;
- model становится менее разнообразной после обучения на generated data;
- training examples не совпадают с production prompt/chat format;
- pipeline повредил source data.

## Baseline / context

Перед сбором или изменением dataset зафиксировать:

1. Desired model behavior.
2. Training stage:
   - self-supervised;
   - supervised/instruction;
   - preference;
   - reward model.
3. Evaluation criteria.
4. Production/request distribution.
5. Existing data sources and provenance.
6. Compliance restrictions.
7. Current dataset size.
8. Coverage dimensions.
9. Annotation guidelines.
10. Model/tokenizer/chat template.
11. Data budget + compute budget.
12. Baseline model performance.

## Read-only checks

### 1. Проверить качество

Source-confirmed dimensions:

- relevance;
- task alignment;
- consistency;
- formatting correctness;
- sufficient uniqueness;
- compliance.

### 2. Проверить coverage

Dataset должен отражать real-use diversity:

- short/long instructions;
- topics/domains;
- languages;
- programming languages where applicable;
- typos/noise patterns;
- output formats;
- single-turn/multi-turn;
- long-context/tool-use behavior if required.

### 3. Проверить quantity

Не начинать с предположения «больше = лучше».

Проверить:

- method: full finetuning vs PEFT;
- task complexity;
- base-model capability;
- improvement on a small, high-quality pilot.

Если небольшой качественный dataset дает явный gain, дальнейшее масштабирование выглядит обоснованнее.

### 4. Проверить annotation consistency

- label a sample yourself;
- compare with existing labels;
- measure annotator disagreement;
- inspect contradictory examples;
- refine labeling guidelines when needed.

### 5. Проверить distributions

Строить и сравнивать distributions:

- token frequency;
- input length;
- output length;
- ratings/scores;
- source;
- time;
- annotator;
- topics/languages.

Искать outliers и systematic annotator/source patterns.

### 6. Проверить duplicates

Возможные уровни:

- full-document duplication;
- within-document duplication;
- cross-document passages;
- exact/fuzzy/semantic near-duplicates.

Дубликаты могут искажать distribution и загрязнять train/test split.

## Interpretation

### Small dataset already improves model

Это evidence, что data-driven scaling может быть полезным.

### Small clean dataset не дает signal

Не считать, что просто больше данных исправит ситуацию. Проверить task definition, base model, method, hyperparameters и data quality.

### High annotator disagreement

Labeling rubric недостаточно однозначна или task inherently subjective. Пересмотреть guidelines и conflict resolution.

### Хороший aggregate dataset, но слабый production slice

Coverage gap. Добавлять targeted examples, а не просто общий объем.

### Synthetic data выглядят качественно, но model performance падает

Synthetic verification недостаточна. Проверить hallucinations, distribution shift, bias amplification, imitation quality и provenance.

### Dataset содержит много duplicates

Deduplicate до дорогих processing steps, если это экономит compute; exact order зависит от cost каждого stage.

### Training format отличается от inference format

Высокий риск silent performance issues. Align tokenizer/chat template/input-output formatting.

## Next action

Рекомендуемый chapter flow:

1. Define desired behavior.
2. Define quality/coverage/quantity targets.
3. Collect small representative seed set.
4. Create labeling/evaluation guidelines.
5. Run small pilot.
6. Inspect data manually.
7. Add targeted coverage.
8. Use augmentation/synthesis where justified.
9. Verify synthetic examples.
10. Deduplicate.
11. Clean/filter/compliance-check.
12. Format for target model.
13. Train and evaluate.
14. Iterate based on observed failures.

## Modifying action

### Добавление synthetic data

Что меняется: training distribution и provenance mix.

Risk:

- hallucinated examples;
- superficial imitation;
- bias amplification;
- model collapse under recursive generation;
- unknown copyright/benchmark provenance.

Verification:

- programmatic checks where possible;
- AI/factuality checks;
- distribution comparison;
- downstream model evaluation.

Rollback: exclude the synthetic-data version and return to previous dataset snapshot; exact storage mechanism `[Needs confirmation]`.

### Deduplication

Что меняется: duplicate examples are removed.

Effect:

- less distribution distortion;
- lower compute waste;
- lower train/test contamination risk.

Verification:

- duplicate-rate before/after;
- dataset-size change;
- preserved coverage;
- re-run evaluation.

Rollback: restore previous immutable dataset snapshot — exact implementation `[Needs confirmation]`.

### Cleaning / compliance filtering

Что меняется: disallowed, malformed or low-quality records are removed/normalized.

Risk:

- over-filtering can remove useful rare examples;
- heuristic bias.

Verification:

- inspect removed sample;
- compare coverage distributions;
- re-evaluate model.

Rollback: previous dataset snapshot — `[Needs confirmation]`.

### Reformatting

Что меняется: examples are serialized for target tokenizer/chat template.

Risk: silent mismatch between training and inference format.

Verification:

- inspect rendered examples;
- test with target tokenizer/template;
- compare downstream model behavior.

Rollback: previous formatted dataset version — `[Needs confirmation]`.

## Verification / acceptance checks

Dataset workflow соответствует логике главы, если:

- desired behavior сформулировано;
- quality/coverage/quantity рассматриваются отдельно;
- provenance известен настолько, насколько возможно;
- annotation guidelines существуют;
- disagreement и errors проверяются;
- manual inspection выполнена;
- duplicates измерены;
- compliance filtering выполнено;
- synthetic data имеют verification step;
- source data не изменяются in place;
- processing pipeline сначала проходит trial run;
- final format соответствует target model;
- dataset usefulness подтверждается downstream evaluation.

## Rollback

- Read-only inspection: `[Not applicable]`.
- Dedup/clean/format changes: restore previous immutable dataset snapshot — exact mechanism `[Needs confirmation]`.
- Synthetic-data addition: remove synthetic subset/version and re-run evaluation — exact version control `[Needs confirmation]`.
- Labeling-guideline change: revert to previous guideline/data version — `[Needs confirmation]`.

## Минимальная карта памяти

~~~text
Dataset design
├─ define desired behavior
├─ quality
│  ├─ relevance
│  ├─ task alignment
│  ├─ consistency
│  ├─ formatting
│  ├─ uniqueness
│  └─ compliance
├─ coverage
├─ quantity
├─ collect / label
├─ augment / synthesize
│  ├─ rules
│  ├─ simulation
│  └─ AI generation
├─ verify synthetic data
├─ process
│  ├─ inspect
│  ├─ deduplicate
│  ├─ clean/filter
│  └─ format
└─ train → evaluate → iterate
~~~
