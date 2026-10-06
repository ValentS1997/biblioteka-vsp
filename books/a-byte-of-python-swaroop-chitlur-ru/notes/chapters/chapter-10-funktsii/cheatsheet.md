# Chapter 10 cheatsheet — «Функции»

## Symptom / problem framing

Нужно перестать дублировать блоки кода и научиться управлять входными данными,
scope, возвращаемыми значениями и документацией reusable code.

## Baseline / context

Базовая форма:

```python
def name(parameters):
    block
```

Вызов:

```python
name(arguments)
```

Source terminology:

- parameter — имя в function definition;
- argument — значение, переданное при call.

## Read-only checks

При ревью функции проверить:

1. Есть ли `def`, имя, parentheses и завершающий `:`.
2. Body имеет корректный indentation.
3. Parameters и arguments сопоставляются ожидаемым способом.
4. Local name не ошибочно принимается за outer/global name.
5. Использование `global` / `nonlocal` действительно намеренно.
6. Parameters with defaults стоят в source-supported порядке.
7. Keyword-only parameter передан по имени, если у него нет default.
8. `return` завершает function path там, где это ожидается.
9. Для нетривиальной function присутствует source-style docstring.
10. `__doc__` / `help()` показывают ожидаемую документацию.

## Interpretation

- Function definition создаёт reusable named behavior.
- Local assignment не меняет одноимённый outer value в example 10.2.
- `global` направляет assignment к outermost name.
- `nonlocal` в nested function направляет assignment к enclosing function scope.
- Default arguments уменьшают число обязательных arguments.
- Keyword arguments делают binding независимым от одной только позиции.
- `*numbers` и `**keywords` собирают дополнительные positional/keyword arguments.
- Keyword-only parameter после `*` нельзя передать как обычный positional value в
  source model.
- `return` завершает function and may return a value.
- `pass` обозначает empty block.
- Docstring доступна через `__doc__`; `help()` использует эту документацию по
  source explanation.

## Next action

Следующая глава — «Модули»: reusable functions/variables будут переноситься между
разными программами через module/import mechanism.

## Modifying action

### Runtime scope mutation

```python
global x
x = 2
```

Effect: изменяет global runtime binding `x`.

Verification: source `func_global.py` заканчивается значением `2`.

Rollback: [Not applicable] после завершения учебного process.

### Enclosing-scope mutation

```python
nonlocal x
x = 5
```

Effect: изменяет binding в enclosing function scope.

Verification: source output `Локальное x сменилось на 5`.

Rollback: [Not applicable] после завершения process.

### File creation/edit

Source сохраняет examples как `function1.py`, `func_param.py`, `func_local.py`,
`func_global.py`, `func_nonlocal.py`, `func_default.py`, `func_key.py`,
`total.py`, `keyword_only.py`, `func_return.py`, `func_doc.py`.

Effect: filesystem change.

Verification: соответствующий `python <file>.py` produces source-described output.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- `function1.py` печатает приветствие дважды.
- `func_param.py` source output: `4 максимально`, затем `7 максимально`.
- `func_local.py`: outer `x` остаётся 50.
- `func_global.py`: global `x` становится 2.
- `func_nonlocal.py`: enclosing `x` становится 5.
- `total.py`: source output `166`.
- `keyword_only.py`: first call prints 66, second call intentionally errors.
- `func_return.py`: source output `3`.
- `func_doc.py`: prints maximum then docstring text.

## Rollback

Runtime mutations cease with the process. Filesystem rollback:
**[Needs confirmation]**.
