# Команды, code patterns и инструменты главы 5

Глава 5 не содержит shell-команд или готового CLI-runbook. Ниже приведены только source-confirmed code patterns, tools и operational actions.

## Shell / CLI commands

`[Not applicable]`

Не добавляются команды установки/запуска Promptbreeder, DSPy, PyRIT, garak и других инструментов: CLI syntax в chapter RAG не приведен.

## Source-confirmed code pattern: отделение prompts от application code

Класс: `state-changing`, если используется как persistent application structure.

~~~python
# prompts.py
GPT4o_ENTITY_EXTRACTION_PROMPT = [YOUR PROMPT]

# application.py
from prompts import GPT4o_ENTITY_EXTRACTION_PROMPT

def query_openai(model_name, user_prompt):
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": GPT4o_ENTITY_EXTRACTION_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
~~~

Effect:

- prompts можно переиспользовать;
- код и prompts тестируются отдельно;
- повышается читаемость.

Risk:

- при совместном использовании одного prompt несколькими приложениями изменение общей версии может затронуть всех consumers.

Verification:

- проверить, какая prompt version фактически используется каждым application;
- прогнать evaluation после изменения prompt.

Rollback:

- вернуть предыдущую versioned prompt definition; конкретный repository/deployment mechanism в главе не задан — `[Needs confirmation]`.

## Source-confirmed metadata pattern

Класс: `state-changing`, если metadata persist в prompt catalog.

~~~python
from pydantic import BaseModel

class Prompt(BaseModel):
    model_name: str
    date_created: datetime
    prompt_text: str
    application: str
    creator: str
~~~

Глава также рекомендует хранить при необходимости:

- model endpoint URL;
- sampling settings, включая temperature/top-p;
- input schema;
- expected output schema.

## Read-only / diagnostic actions

| Action | Класс | Purpose |
|---|---|---|
| inspect/print final serialized prompt | read-only | Проверить model-specific chat template |
| compare small prompt perturbations | workload-generating | Проверить robustness |
| NIAH-style test | workload-generating | Проверить effective long-context use |
| RULER-like long-context evaluation | workload-generating | Проверить degradation с ростом context |
| compare zero-shot vs few-shot | workload-generating | Определить ценность examples |
| validate output format/schema | read-only или workload-generating | Проверить downstream compatibility |
| compare monolithic vs decomposed prompt | workload-generating | Оценить quality/cost/latency trade-off |
| repeat fixed evaluation after prompt change | workload-generating | Проверить regression |

## Prompt-engineering tools

| Tool | Класс | Source-confirmed role |
|---|---|---|
| OpenPrompt | workload-generating | Автоматизация prompt workflow |
| DSPy | workload-generating | Поиск prompt/chain, максимизирующих evaluation metric |
| Promptbreeder | workload-generating | Эволюционная генерация и отбор вариантов prompt |
| TextGrad | workload-generating | AI-assisted prompt optimization |
| Guidance | workload-generating | Направление модели к structured output |
| Outlines | workload-generating | Structured-output guidance |
| Instructor | workload-generating | Structured-output guidance |
| Dotprompt | state-changing if persisted | Хранение prompt definitions/metadata |
| Humanloop | state-changing if persisted | Prompt storage/workflow |
| Continue Dev prompt format | state-changing if persisted | Prompt storage/workflow |
| Promptfile | state-changing if persisted | Prompt storage/workflow |

Operational risk: prompt tools могут делать скрытые model calls. В главе приведен пример: 30 evaluation examples × 10 prompt variants = 300 API calls при одном вызове на вариант/example.

Verification:

- inspect generated prompts;
- count model/API calls;
- validate templates;
- measure cost/latency.

Rollback: вернуться к последней проверенной prompt/tool configuration — exact mechanism `[Needs confirmation]`.

## Defensive evaluation tools

| Tool / benchmark | Класс | Роль |
|---|---|---|
| AdvBench | workload-generating | Adversarial robustness evaluation |
| PromptRobust | workload-generating | Prompt-attack robustness evaluation |
| Azure/PyRIT | workload-generating | Автоматизированное security probing/red teaming |
| NVIDIA garak | workload-generating | Security probing |
| greshake/llm-security | workload-generating | Security probing/examples |
| persuasive_jailbreaker | workload-generating | Automated adversarial testing |

Глава не приводит команды запуска.

## Security metrics

| Metric | Класс | Interpretation |
|---|---|---|
| violation rate | read-only analysis после adversarial run | Доля успешных атак |
| false refusal rate | read-only analysis после benign run | Доля безопасных запросов, ошибочно отклоненных |

Обе метрики должны рассматриваться вместе.

## Defensive actions

### Model-level instruction hierarchy

Класс: `state-changing` на уровне обучения/model behavior.

Source-confirmed priority example:

1. system prompt;
2. user prompt;
3. model output;
4. tool output.

Effect: конфликтующие lower-priority instructions должны уступать higher-priority instructions.

Risk/verification: требует safety + capability evaluation.

Rollback: модель/обучение-зависимый — `[Needs confirmation]`.

### Prompt-level constraints

Класс: `state-changing` для persisted prompt.

Source-confirmed examples:

- явно указать, какие данные нельзя выводить;
- повторить основную system instruction после user/context section;
- заранее предупредить модель о типичных attack patterns.

Effect: может снизить attack success.

Risk: больше tokens → выше cost/latency; гарантий соблюдения нет.

Verification: adversarial + benign evaluation.

Rollback: предыдущая prompt version; deployment procedure — `[Needs confirmation]`.

### System-level isolation

Класс: `state-changing` architectural control.

Source-confirmed principles:

- generated code выполнять в isolated VM, не связанном с primary user environment;
- потенциально опасные database modifications не выполнять без explicit human approval;
- input/output guardrails;
- PII/toxicity filtering;
- suspicious-intent/anomaly detection;
- monitoring unusual repeated request patterns.

Effect: уменьшает blast radius даже при успешном prompt attack.

Risk: false positives, added latency, operational complexity.

Verification:

- adversarial testing;
- benign task regression;
- confirm approval gate before state-changing operation.

Rollback: `[Needs confirmation]`; weakening a security boundary should not be done without re-evaluation.

## Dangerous SQL keywords cited by the source

Глава приводит `DELETE`, `DROP`, `UPDATE` как примеры операций, которые system policy должна отправлять на human approval перед исполнением.

Они не являются рекомендуемыми командами к выполнению и здесь не снабжаются runnable examples.

## Operational boundary

- Не добавлены provider-specific API commands из внешней документации.
- Не добавлены shell-команды для перечисленных tools.
- Attack examples не превращены в executable offensive runbook.
- Все tools/actions выше подтверждены chapter RAG.
