# Команды, параметры и инструменты главы 2

Глава 2 не содержит shell-команд или готового CLI-runbook. Ниже перечислены только явно подтвержденные RAG главы controls/actions/tools.

## Shell / CLI commands

`[Not applicable]`

Не добавляются `curl`, `python`, `pip`, `npm` или vendor CLI-команды: их синтаксис в главе не приведен.

## Inference controls

| Элемент | Класс | Что меняет / наблюдает | Риск / ограничение | Verification | Rollback |
|---|---|---|---|---|---|
| `temperature` | workload-generating, request-level | Перераспределяет logits перед softmax; выше — больше редких токенов/разнообразия, ниже — более вероятные токены/предсказуемость | Более высокая temperature может снижать связность; 0 реализуется provider-ом как выбор max-logit, а не буквальное деление на 0 | Повторить одинаковый набор запросов и сравнить outputs | `[Needs confirmation]` |
| `top-k` | workload-generating, request-level | Оставляет k наиболее высоких logits и выполняет sampling среди них | Меньший k делает текст предсказуемее, но беднее; конкретный оптимум зависит от приложения | Сравнить качество/разнообразие на baseline-наборе | `[Needs confirmation]` |
| `top-p` | workload-generating, request-level | Выбирает минимальный набор токенов, накопленная вероятность которого достигает p | Не обязательно уменьшает вычисление softmax; результат зависит от распределения для конкретного контекста | Сравнить outputs при фиксированных остальных настройках | `[Needs confirmation]` |
| stop token / stop word / fixed output length | workload-generating, request-level | Ограничивает длину генерации | Ранняя остановка может оборвать предложение или сделать structured output невалидным/неполным | Проверить полноту и парсинг вывода | `[Needs confirmation]` |
| `logprobs` | read-only observation | Показывает вероятности модели в логарифмической шкале, если provider их раскрывает | Доступность и лимиты зависят от provider; текущее API-состояние `[Needs confirmation]` | Сопоставить возвращенные logprobs с выбранными токенами | `[Not applicable]` |
| random seed | workload-generating, request-level | Фиксирует старт генератора случайных чисел, если API/stack поддерживает это | Даже вместе с прочими фиксированными настройками не гарантирует 100% одинаковый output | Повторить идентичный запрос | `[Needs confirmation]` |

## Inference-time compute

| Элемент | Класс | Роль | Риск / стоимость | Verification | Rollback |
|---|---|---|---|---|---|
| best-of-N / несколько вариантов | workload-generating | Генерировать несколько outputs и выбрать лучший | Больше inference compute, latency и cost | Сравнить выбранный ответ с single-sample baseline | `[Not applicable]` для отдельного вызова |
| reward model / verifier | workload-generating | Оценивать варианты и выбирать более высокий score | Дополнительная модель/проверка и вычисления | Проверить improvement на целевых задачах | `[Needs confirmation]` |
| majority / self-consistency | workload-generating | Для задач с точным ответом выбирать наиболее часто встречающийся результат из нескольких | Требует нескольких генераций | Сравнить accuracy с single-sample baseline | `[Not applicable]` для отдельного вызова |

На странице 129 приводится исторический пример provider-specific параметра OpenAI `best_of`; его текущая доступность: `[Needs confirmation]`.

## Structured-output controls and tools

### Source-confirmed approaches

1. prompting;
2. повторная генерация/проверка;
3. post-processing;
4. constrained sampling;
5. fine-tuning.

### Source-confirmed tools

| Tool / interface | Класс | Роль в главе | Команда |
|---|---|---|---|
| Guidance | workload-generating | Ограничение/структурирование генерации | `[Needs confirmation]` |
| Outlines | workload-generating | Structured output | `[Needs confirmation]` |
| instructor | workload-generating | Structured output | `[Needs confirmation]` |
| llama.cpp structured-output capabilities | workload-generating | Ограничение возможных outputs | `[Needs confirmation]` |
| JSON mode у model provider | workload-generating, provider-specific | Синтаксически структурированный JSON-output | API availability/syntax: `[Needs confirmation]` |

Глава не дает команд установки или точного API-синтаксиса этих инструментов.

## Model-changing actions

| Action | Класс | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|
| SFT | state-changing | Изменяет веса модели на демонстрационных данных, направляя ее от text-completion к желаемому interaction pattern | Качество зависит от демонстрационных данных | Сравнить модель до/после на целевых задачах | `[Needs confirmation]` |
| preference finetuning | state-changing | Настраивает поведение под предпочтения; в главе: RLHF, DPO, RLAIF | Предпочтения неоднозначны; alignment не гарантирует отсутствие ошибок | Сравнить предпочтение/качество ответов до/после | `[Needs confirmation]` |
| fine-tuning для structured output | state-changing | Обучает модель примерам требуемого формата | Требует ресурсов и не гарантирует идеальный формат во всех случаях | Проверить долю корректно структурированных outputs | `[Needs confirmation]` |

## Operational boundary

- Provider-specific API details из текущей документации не добавлялись.
- Исторические API-примеры книги не трактуются как актуальные без проверки.
- Незнакомые chapter-external команды не достраивались из model memory.
