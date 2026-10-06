# Chapter 11 cheatsheet — «Модули»

## Symptom / problem framing

Нужно переиспользовать функции и variables между разными программами и организовать
растущее число модулей.

## Baseline / context

Source hierarchy:

`function → module (.py) → package directory → module/package collection`

Import path source model:

`current directory / sys.path → module lookup → first import executes module body`.

## Read-only checks

При ревью module usage проверить:

1. Какой import style используется: `import x` или `from x import y`.
2. Есть ли риск name collision при direct-name import.
3. Используется ли dotted access `module.name`.
4. Что содержит `sys.argv` для конкретного invocation.
5. Какие directories source example показывает в `sys.path`.
6. Что вернёт `__name__` в direct-run и imported modes.
7. Какие names показывает `dir(module)` / `dir()`.
8. Package tree содержит source-required `__init__.py`.

## Interpretation

- Plain `import` сохраняет namespace qualification и source считает его более
  безопасным для читаемости/конфликтов.
- `sys.argv[0]` source объясняет как имя запускаемого script.
- `sys.path` используется для поиска Python modules.
- `__name__ == '__main__'` — branch для direct execution.
- `from mymodule import *` source описывает как importing public names, но не
  `__version__`, начинающийся с double underscore.
- `dir()` показывает names текущего module; `dir(obj)` — attributes/names object.
- `del a` удаляет name из текущего namespace.
- Packages add directory hierarchy over modules.

## Next action

Следующая глава — «Структуры данных»: lists, tuples, dictionaries и sets.

## Modifying action

### Import with possible bytecode/cache side effect

```python
import sys
```

Effect: loads module; source says module body initializes on first import and may result
in `.pyc` creation for Python modules.

Verification: module members become available, e.g. `sys.argv`, `sys.path`.

Rollback: **[Needs confirmation]** for any generated filesystem cache.

### Namespace deletion

```python
a = 5
del a
```

Effect: removes name `a` from current module namespace.

Verification: subsequent `dir()` no longer lists `a`.

Rollback: recreate/reassign the name manually; source does not provide a generic rollback.

### Create own modules/packages

Source examples require creating `mymodule.py`, `mymodule_demo.py`,
`mymodule_demo2.py` and a package directory tree.

Effect: filesystem changes.

Verification: import/use examples produce source output.

Rollback: **[Needs confirmation]** — no file/directory removal commands in source.

## Verification / acceptance checks

- `using_sys.py` prints script name plus `we are arguments` as separate argv entries.
- `using_name.py` prints one message when run directly and another when imported.
- `mymodule_demo.py` prints greeting + version `0.1`.
- `dir()` shows `a` after assignment and no longer shows it after `del a`.
- package tree contains `__init__.py` in source example directories.

## Rollback

Runtime namespace changes end with process. Filesystem/cache rollback:
**[Needs confirmation]**.
