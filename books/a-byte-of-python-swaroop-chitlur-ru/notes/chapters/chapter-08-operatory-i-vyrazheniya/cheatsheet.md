# Chapter 8 cheatsheet — «Операторы и выражения»

## Symptom / problem framing

Нужно понимать, как Python вычисляет выражения: какие операторы участвуют, какие данные
они обрабатывают и какой порядок выполнения применяется.

## Baseline / context

Базовая модель:

`operands + operator → expression → value`.

Порядок результата определяют:

1. precedence;
2. associativity;
3. parentheses.

## Read-only checks

Для выражения проверить:

1. Какие operators присутствуют.
2. Какие operands они получают.
3. Есть ли operators с разным precedence.
4. Есть ли equal-precedence chain.
5. Явно ли parentheses задают intended grouping.
6. Не используется ли short-circuit `and` / `or`.
7. Не является ли assignment pattern кандидатом на source augmented form.

## Interpretation

- `/` — обычное деление в source examples.
- `//` — целочисленное/floor-style division по source description.
- `%` — remainder.
- `**` — exponentiation.
- `<<` / `>>` — bit shifts.
- comparisons возвращают source values `True` / `False`.
- `and` и `or` могут не вычислять правую часть, если результат уже определяется
  левой частью.
- Parentheses предпочтительны, когда делают порядок вычисления очевидным.
- Augmented assignment сокращает повторение имени variable.

## Next action

Следующая глава «Поток команд» использует expressions как conditions для `if`,
`while` и других flow-control constructs.

## Modifying action

### Runtime assignment

```python
a = 2
a *= 3
```

Effect: runtime binding `a` получает новое значение.

Verification: значение `a` после operation соответствует source arithmetic.

Rollback: [Not applicable] после завершения учебного process.

### Save/run `expression.py`

Effect: создаётся/изменяется source file и затем выполняется программа.

Verification:

```text
python expression.py
```

Expected source output:

```text
Площадь равна 10
Периметр равен 14
```

Rollback для file change: **[Needs confirmation]** — source procedure не указан.

## Verification / acceptance checks

- `2 + 3 * 4` следует source precedence.
- `(2 + 3) * 4` изменяет grouping.
- `a = 2; a *= 3` даёт source-equivalent result краткой записи.
- `expression.py` выдаёт area 10 и perimeter 14.

## Rollback

Runtime changes: [Not applicable] после завершения процесса.

Filesystem rollback для учебного файла: **[Needs confirmation]**.
