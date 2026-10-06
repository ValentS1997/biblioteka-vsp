# Chapter 13 cheatsheet — «Решение задач»

## Symptom / problem framing

Нужно перейти от отдельных Python constructs к самостоятельному проектированию
полезного script и научиться улучшать его итеративно.

## Baseline / context

Source task: резервировать important files/directories в ZIP archive.

Design inputs:

- `source` — files/directories;
- `target_dir` — backup root;
- date/time — archive naming;
- external `zip` command in versions 1–4.

## Read-only checks

Перед state-changing run проверить:

1. `source` paths существуют и действительно должны резервироваться.
2. `target_dir` корректен и доступен для записи.
3. Generated `target` указывает в ожидаемое место.
4. Generated `zip_command` содержит ожидаемые source/target values.
5. External `zip` command доступен — **[Needs confirmation]**.
6. Для debugging source предлагает сначала вывести `zip_command`.
7. Version 3 intentionally broken: не использовать её как working backup implementation.

## Interpretation

- `os.sep` source использует для построения path.
- `time.strftime` формирует date/time fragments.
- `' '.join(source)` превращает source list в command fragment.
- `os.system` передаёт строку внешней shell command.
- Version 2 создаёт per-day directory.
- Version 3 показывает debugging from reported syntax location.
- Version 4 исправляет logical-line continuation и sanitizes spaces in comment with `_`.
- Section 13.6 source itself identifies replacing `os.system` with `zipfile`/`tarfile`
  as the most important improvement.

## Next action

Глава 14 переходит от procedural organization к object-oriented programming.

## Modifying action

### Create daily backup directory

```python
if not os.path.exists(today):
    os.mkdir(today)
```

Effect: filesystem directory creation.

Verification: path exists and subsequent archive target uses it.

Rollback: **[Needs confirmation]**.

### Execute archive command

```python
zip_command = "zip -qr {0} {1}".format(target, ' '.join(source))
os.system(zip_command)
```

Effect: executes external archiver and writes ZIP archive.

Risk: shell execution + filesystem modification. Actual expanded command depends on
runtime values.

Verification: source success branch + archive existence.

Rollback: **[Needs confirmation]**.

### Comment-based archive naming

```python
comment = input('Введите комментарий --> ')
comment.replace(' ', '_')
```

Effect: changes generated target filename, not source files.

## Verification / acceptance checks

- ver1: timestamp ZIP path is generated.
- ver2: date directory + time ZIP naming works in shown output.
- ver3: source intentionally yields `SyntaxError: invalid syntax`.
- ver4: both comment and empty-comment branches produce source-described archive names.
- debugging path: print generated command and test it independently, as source instructs.

## Rollback

No source-specific rollback for archives/directories: **[Needs confirmation]**.
