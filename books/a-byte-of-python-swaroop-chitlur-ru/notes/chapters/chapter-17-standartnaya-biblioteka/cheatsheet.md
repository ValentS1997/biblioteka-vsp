# Chapter 17 cheatsheet — «Стандартная библиотека»

## Symptom / problem framing

Нужно использовать готовые возможности Python для version checks, warnings и
persistent logging вместо самостоятельной реализации базовой инфраструктуры.

## Baseline / context

Source flow:

`sys.version_info → version decision → warnings.warn`

и:

`platform/environment → os.path.join → logging.basicConfig → log records`

## Read-only checks

Перед запуском examples проверить:

1. Какой interpreter executable используется.
2. Что возвращает `sys.version_info[0]`.
3. Какой результат даёт source platform test.
4. Какие значения возвращают `HOME`, `HOMEDRIVE`, `HOMEPATH`.
5. Какой exact path получается для `logging_file`.
6. Существует ли уже target `test.log`.
7. Допустим ли overwrite, поскольку source использует `filemode='w'`.

## Interpretation

- `sys.version_info` source использует как version tuple.
- `warnings.warn(..., RuntimeWarning)` формирует warning path для major version < 3.
- `platform.platform()` используется для source branch Windows vs other.
- `os.path.join` формирует path из components.
- `logging.basicConfig` задаёт level, format, filename и write mode.
- `logging.debug/info/warning` формируют records разных уровней.
- Source log output содержит timestamp, level и message.

## Next action

Следующая глава — «Дополнительно».

## Modifying action

### Logging file creation / overwrite

```python
logging.basicConfig(
    level=logging.DEBUG,
    filename=logging_file,
    filemode='w',
)
```

Effect: filesystem write; source target ends in `test.log`.

Risk: existing target can be overwritten.

Verification:

- source prints resolved log path;
- `test.log` contains DEBUG / INFO / WARNING lines.

Rollback: **[Needs confirmation]**.

### Warning emission

```python
warnings.warn(message, RuntimeWarning)
```

Effect: process output/diagnostic state, not persistent filesystem change in source example.

Rollback: [Not applicable].

## Verification / acceptance checks

- `sys.version_info[0] >= 3` follows shown source REPL branch.
- `python3 versioncheck.py` prints `Нормальное продолжение`.
- source Python-2 run reaches warning branch.
- `python3 use_logging.py` prints target path.
- resulting log has DEBUG, INFO and WARNING entries in configured format.

## Rollback

Runtime warning/version checks need no rollback.

Log-file rollback: **[Needs confirmation]**.
