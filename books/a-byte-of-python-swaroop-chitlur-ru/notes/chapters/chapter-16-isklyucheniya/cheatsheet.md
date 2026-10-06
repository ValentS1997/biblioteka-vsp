# Chapter 16 cheatsheet — «Исключения»

## Symptom / problem framing

Нужно не только увидеть ошибку, но и контролировать exceptional path:
перехватить ожидаемую ситуацию, сообщить результат и гарантировать cleanup.

## Baseline / context

Source model:

`try → except → optional else → optional cleanup/finally`

Explicit exception:

`condition → raise ExceptionType(...) → matching except`

## Read-only checks

При ревью exception handling проверить:

1. Какие statements могут вызвать exception.
2. Какой exact exception type ожидается.
3. Есть ли overly broad bare `except` в source discussion.
4. Что происходит, если ни один handler не совпал.
5. Выполняется ли `else` только на no-exception path.
6. Нужен ли cleanup независимо от результата.
7. Для file examples существует ли `poem.txt`.
8. Не зависит ли test от interactive Ctrl-C / Ctrl-D.

## Interpretation

- Unhandled exception source says reaches Python default handler and stops program.
- `except EOFError` and `except KeyboardInterrupt` select different branches.
- `else` source executes when no exception occurs.
- Custom exception derives from `Exception`.
- `raise` transfers execution to matching exception handling path.
- `except ShortInputException as ex` provides access to exception fields.
- `finally` is cleanup path in source example.
- `with open(...) as f` packages resource cleanup into context-manager protocol.

## Next action

Следующая глава — «Стандартная библиотека».

## Modifying action

### Runtime exception creation

```python
raise ShortInputException(len(text), 3)
```

Effect: changes runtime control flow by raising a custom exception.

Verification: one-character input reaches `ShortInputException` handler.

Rollback: [Not applicable] after process path completes.

### File handle cleanup

```python
f.close()
```

Effect: closes runtime file resource.

Verification: source cleanup message follows.

Rollback: [Not applicable].

### File creation/edit

Source files:

- `try_except.py`
- `raising.py`
- `finally.py`
- `using_with.py`

Filesystem rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- Ctrl-D in `try_except.py` → EOF handler.
- Ctrl-C in `try_except.py` → KeyboardInterrupt handler.
- normal text → `else` path.
- input shorter than 3 in `raising.py` → custom exception message.
- input length at least 3 → no-exception message.
- Ctrl-C during `finally.py` still reaches cleanup path in shown source run.
- `using_with.py` prints same file content without explicit `close()`.

## Rollback

Runtime exception/control-flow effects end with process.

Filesystem rollback for saved scripts: **[Needs confirmation]**.
