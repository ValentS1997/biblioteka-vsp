# Chapter 9 cheatsheet — «Поток команд»

## Symptom / problem framing

Нужно перестать выполнять программу только сверху вниз и научиться:

- принимать решение;
- повторять block;
- досрочно выходить из loop;
- пропускать часть iteration.

## Baseline / context

Source flow-control set:

`if` → branch  
`while` → condition loop  
`for` → sequence iteration  
`break` → terminate loop  
`continue` → skip rest of current iteration

## Read-only checks

При ревью control flow проверить:

1. Condition выражает ожидаемый Boolean result.
2. После `if`, `elif`, `else`, `while`, `for` стоит `:`.
3. Block имеет consistent indentation.
4. `elif` / `else` действительно optional.
5. Для `range(start, stop[, step])` stop не входит в source sequence.
6. Если loop имеет `else`, понять, может ли path пройти через `break`.
7. `continue` не скрывает нужные действия ниже по block.

## Interpretation

- `if` выбирает branch один раз на каждой проверке.
- `while` снова проверяет condition после каждого loop block.
- Source `while ... else` выполняет `else`, когда condition становится `False`;
  при `break` этот `else` не выполняется.
- `for` получает по одному element из sequence.
- Source поясняет `range(1, 5)` через значения 1,2,3,4 и отдельно упоминает
  `list(range())` для просмотра всех values.
- `break` применим к `for` и `while`.
- `continue` также применим к обоим loop types.

## Next action

Следующая глава — «Функции»: flow-control blocks будут помещаться в reusable named
code blocks.

## Modifying action

### Runtime flag

```python
running = True
...
running = False
```

Effect: меняет runtime control state и завершает `while` после следующей проверки.

Verification: source example выходит из loop и печатает `Цикл while закончен.`.

Rollback: [Not applicable] после завершения учебного process.

### File creation/edit

Source просит сохранить examples как:

- `if.py`
- `while.py`
- `for.py`
- `break.py`
- `continue.py`

Effect: создаёт/изменяет source files.

Verification: запуск соответствующего файла даёт source-described interaction/output.

Rollback: **[Needs confirmation]** — source не приводит file rollback procedure.

## Verification / acceptance checks

- `if.py`: значения ниже/равно/выше 23 приводят к разным branches.
- `while.py`: input повторяется, пока guess не равен 23.
- `for.py`: source output — 1,2,3,4, затем loop-`else`.
- `break.py`: строка `выход` прекращает loop.
- `continue.py`: строки короче 3 characters печатают `Слишком мало` и пропускают
  остальной block.

## Rollback

Runtime control-flow effects завершаются вместе с process.

Filesystem rollback: **[Needs confirmation]**.
