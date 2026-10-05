# Команды, метрики и инструменты главы 4

Глава 4 не содержит shell-команд или готового CLI-runbook. Ниже перечислены только source-confirmed evaluation tools, metrics и actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды запуска `lm-evaluation-harness`, OpenAI Evals, MLflow или других инструментов, поскольку их CLI syntax в chapter RAG не приведен.

## Domain-specific evaluation

| Элемент | Класс | Что измеряет | Ограничение | Verification | Rollback |
|---|---|---|---|---|---|
| functional correctness | workload-generating | Выполняет ли output требуемую функцию | Не покрывает efficiency/readability и другие свойства | Проверка ожидаемого результата / tests | `[Not applicable]` |
| accuracy | read-only | Доля правильных closed-form/classification ответов | Зависит от class distribution | Фиксировать dataset и definition | `[Not applicable]` |
| precision / recall / F1 | read-only | Classification performance | Нужна корректная интерпретация class semantics | Использовать фиксированный evaluation set | `[Not applicable]` |
| MCQ | workload-generating | Closed-form knowledge/reasoning | Не равно open-ended generation ability; чувствительно к prompt formatting | Стабилизировать question format и сравнивать на одном наборе | `[Not applicable]` |
| pass@k | workload-generating | Code-generation functional success с k samples | Score зависит от k | Фиксировать k | `[Not applicable]` |

## Generation-quality evaluation

| Метод / tool | Класс | Назначение |
|---|---|---|
| fluency / coherence evaluation | read-only или workload-generating | Оценка естественности и структуры текста; может выполняться AI judge или через LM metric |
| local factual consistency | workload-generating | Проверка output относительно предоставленного context |
| global factual consistency | workload-generating | Проверка output относительно trusted external facts; trusted source definition зависит от application |
| AI judge | workload-generating | Универсальная subjective evaluation |
| SelfCheckGPT | workload-generating | Генерирует несколько альтернативных outputs и проверяет consistency исходного ответа |
| SAFE / search-augmented factuality evaluation | workload-generating | Разбивает ответ на claims, формирует search queries и проверяет claims по найденной информации |
| NLI-style evaluator | workload-generating | Классифицирует premise/hypothesis как entailment, contradiction или neutral |
| TruthfulQA | workload-generating benchmark | Factuality-oriented benchmark |
| toxicity/moderation classifier | workload-generating | Safety/toxicity detection |
| RealToxicityPrompts | workload-generating benchmark | Toxicity evaluation |
| BOLD | workload-generating benchmark | Bias in open-ended generation |

Source-confirmed examples специализированных toxicity tools/models:

- Facebook hate-speech detection model;
- Skolkovo toxicity classifier;
- Perspective API.

Текущая доступность/API syntax: `[Needs confirmation]`.

## Instruction-following evaluation

| Tool / method | Класс | Роль |
|---|---|---|
| IFEval | workload-generating benchmark | Автоматически проверяемые keyword/length/language/format constraints |
| INFOBench | workload-generating benchmark | Более широкие content/linguistic/style constraints |
| application-specific instruction benchmark | workload-generating | Проверка именно тех инструкций, которые важны приложению |
| heuristic format checks | read-only | JSON, keyword, length, count, language и другие детерминированные constraints |
| AI judge | workload-generating | Проверка instruction criteria, которые нельзя выразить точным правилом |

## Cost / latency metrics

Source-confirmed metrics:

- time to first token;
- time per token;
- time between tokens;
- total request latency;
- input/output token count;
- token/API cost;
- throughput / TPM как возможный scale criterion.

Класс: read-only measurement при существующем workload; workload-generating при benchmark run.

## Model-selection actions

### Hard-filter

Класс: read-only decision step.

Проверяет attributes, которые нельзя или практически нецелесообразно менять:

- licence/policy;
- privacy requirements;
- deployment/access constraints;
- provider/API limitations;
- hardware limits;
- другие application-specific hard requirements.

### Public benchmark shortlist

Класс: read-only analysis или workload-generating, если benchmark запускается самостоятельно.

Source-confirmed harnesses:

- EleutherAI `lm-evaluation-harness`;
- OpenAI Evals.

Глава не приводит команды запуска.

### Private evaluation

Класс: workload-generating.

Роль: сравнить небольшой shortlist на собственных requests, criteria и datasets.

### Production monitoring

Класс: workload-generating / observation.

Роль: обнаруживать failures и собирать feedback после release.

## API vs self-host decision

Это state-changing architectural choice, если реализуется в приложении.

Source-confirmed factors:

- data privacy;
- data provenance / copyright;
- performance;
- functionality;
- cost;
- finetuning/optimization possibilities;
- control/access/transparency;
- on-device deployment.

Effect: меняются operational boundary, control plane, vendor dependence, engineering load, cost model и доступные capabilities.

Risk: конкретный профиль риска зависит от выбранной модели/provider/deployment.

Verification: повторить private evaluation по hard requirements, quality, latency и cost.

Rollback: `[Needs confirmation]`.

## Public benchmark hygiene

Source-confirmed checks:

- benchmark relevance;
- benchmark correlation;
- aggregation/weighting;
- saturation;
- contamination.

Contamination heuristics:

- n-gram overlap;
- perplexity on evaluation data.

## Custom evaluation-pipeline actions

| Action | Класс | Purpose |
|---|---|---|
| evaluate each component separately | workload-generating | Fault localization |
| turn-level evaluation | workload-generating | Проверить каждый output/interaction |
| task-level evaluation | workload-generating | Проверить выполнение пользовательской задачи |
| rubric/scoring guide creation | state-changing if persisted | Стандартизировать критерии оценки |
| annotate evaluation data | state-changing | Создать reusable labeled evaluation set |
| data slicing | read-only analysis | Найти subgroup failures/bias |
| bootstrap resampling | workload-generating analysis | Оценить stability/variance evaluation result |
| metric correlation analysis | read-only analysis | Найти redundant или contradictory signals |
| experiment tracking | state-changing if persisted | Сохранить evaluation data/configuration/prompt/sampling variables |

Для state-changing pipeline artifacts конкретный rollback mechanism: `[Needs confirmation]`.

## Operational boundary

- Не добавлены актуальные provider-specific API команды.
- Не добавлены benchmark команды из внешней документации.
- Все перечисленные методы и tools подтверждены chapter RAG.
