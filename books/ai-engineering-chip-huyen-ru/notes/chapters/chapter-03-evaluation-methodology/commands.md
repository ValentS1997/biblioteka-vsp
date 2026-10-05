# Команды, метрики и инструменты главы 3

Глава 3 не содержит shell-команд или готового CLI-runbook. Ниже перечислены только source-confirmed evaluation actions, метрики и инструменты.

## Shell / CLI commands

`[Not applicable]`

Не добавляются `curl`, `python`, `pip`, vendor CLI или иные команды, синтаксис которых отсутствует в RAG главы.

## Языковые метрики

| Элемент | Класс | Что измеряет | Ограничение / interpretation | Verification | Rollback |
|---|---|---|---|---|---|
| cross-entropy | read-only | Насколько трудно модели прогнозировать данные; включает entropy данных и расхождение learned distribution с true distribution | Зависит от данных; не является полной прикладной метрикой | Сравнивать на фиксированном наборе и одинаковой методике расчета | `[Not applicable]` |
| perplexity (PPL) | read-only | Экспонента cross-entropy; неопределенность следующего токена | Ниже обычно лучше для LM prediction, но после SFT/RLHF связь с task quality может нарушаться | Фиксировать dataset/context и метод расчета | `[Not applicable]` |
| BPC | read-only | Bits per character | Нужен учет кодировки и tokenization | Сравнивать только при сопоставимой методике | `[Not applicable]` |
| BPB | read-only | Bits per byte | Более унифицировано относительно кодировок, но остается LM metric | Сравнивать на одинаковых данных | `[Not applicable]` |

Для вычисления perplexity требуется доступ к token probabilities или log-probabilities. Не все коммерческие модели их раскрывают.

## Functional correctness

| Элемент | Класс | Роль | Effect / риск | Verification | Rollback |
|---|---|---|---|---|---|
| unit tests для generated code | workload-generating | Проверить выполняет ли код ожидаемую функцию | Выполнение непроверенного кода само по себе может быть рискованным; конкретная sandbox policy в главе не задана | Все заданные test cases проходят | `[Not applicable]` для evaluation result |
| `pass@k` | workload-generating | Доля задач, где хотя бы один из k generated samples проходит все tests | Score растет с k; нельзя сравнивать разные k как одну и ту же метрику | Фиксировать k и набор задач | `[Not applicable]` |

Source examples: HumanEval, MBPP, Spider, BIRD-SQL, WikiSQL, LeetCode, HackerRank.

## Reference-based similarity

| Метод / tool | Класс | Что измеряет | Ограничение |
|---|---|---|---|
| exact match | read-only | Полное совпадение с эталоном | Плохо подходит, если правильных формулировок много |
| edit distance / fuzzy matching | read-only | Число правок между строками | Измеряет форму, а не смысл |
| n-gram similarity | read-only | Совпадение n-грамм | Может штрафовать правильные перефразирования |
| BLEU | read-only | Лексическое сходство | Высокий score не гарантирует functional correctness |
| ROUGE | read-only | Лексическое сходство | Требует эталонных данных |
| METEOR++ | read-only | Лексическое сходство | Требует эталонных данных |
| TER | read-only | Лексическое/edit-based сходство | Требует эталонных данных |
| CIDEr | read-only | Лексическое сходство | Требует эталонных данных |
| cosine similarity | read-only | Сходство embedding vectors | Надежность зависит от embedding model |
| BERTScore | workload-generating | Semantic text similarity через BERT-based embeddings | Требует model compute |
| MoverScore | workload-generating | Semantic similarity через embedding-based method | Требует model compute |

## Embedding tools/models

Source-confirmed examples:

- BERT;
- CLIP;
- Sentence Transformers;
- proprietary embedding APIs.

Текущие API syntax, модели и размеры embeddings без внешней проверки: `[Needs confirmation]`.

## AI в роли судьи

AI-судья — workload-generating evaluator.

Source-confirmed prompt patterns:

~~~text
single-answer:
  input: question + answer
  task: score answer quality using a defined rubric

reference-based:
  input: question + reference answer + generated answer
  task: decide whether generated answer matches the reference

pairwise:
  input: question + answer A + answer B
  task: choose A or B according to stated criteria
~~~

Обязательные элементы evaluator prompt по логике главы:

- task;
- criterion;
- scoring/classification system;
- при возможности — examples с объяснением оценок.

### Source-confirmed AI-evaluation tools

| Tool | Класс | Примечание |
|---|---|---|
| Azure AI Studio | workload-generating | Встроенные evaluator criteria; значения не стандартизированы между tools |
| MLflow.metrics | workload-generating | В книге показан пример faithfulness/relevance evaluation |
| LangChain Criteria Evaluation | workload-generating | Набор встроенных criteria |
| Ragas | workload-generating | Встроенные criteria, включая faithfulness/relevance |
| LlamaIndex | workload-generating | В книге сравнивается evaluator prompt для faithfulness |

## Specialized AI judges

| Judge type / model | Класс | Что делает |
|---|---|---|
| reward model | workload-generating | `request + answer → score` |
| Cappy | workload-generating | Пример небольшой reward model |
| BLEURT | workload-generating | `candidate + reference → similarity score` |
| Prometheus | workload-generating | `request + generated + reference + criteria → quality score` |
| preference model | workload-generating | `request + answer1 + answer2 → preferred answer` |
| PandaLM | workload-generating | Preference judge с объяснением |
| JudgeLM | workload-generating | Preference judge |

## Comparative ranking

Source-confirmed ranking systems:

- Elo;
- Bradley–Terry;
- TrueSkill.

Класс: read-only analysis после сбора pairwise comparison signals.

Ограничения:

- количество model pairs растет квадратично;
- assumption о transitivity может нарушаться;
- ranking depends on comparison data quality;
- relative rank не показывает absolute usefulness.

## State-changing evaluation action

### Изменение judge model / prompt / sampling settings

Класс: state-changing, если evaluator definition сохраняется как часть pipeline.

Effect: меняется сам измерительный инструмент.

Risk: исторические scores могут стать несопоставимыми.

Verification: прогнать старую и новую evaluator definition на одном фиксированном evaluation set.

Rollback: `[Needs confirmation]` — chapter-specific configuration rollback procedure не задан.

## Operational boundary

- Provider-specific API syntax не достраивался из внешнего знания.
- Не добавлены команды установки инструментов.
- Evaluation tools и model examples рассматриваются только в контексте, явно подтвержденном RAG главы.
