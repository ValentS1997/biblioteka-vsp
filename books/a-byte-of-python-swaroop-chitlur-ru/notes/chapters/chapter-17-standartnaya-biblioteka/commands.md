# Commands and code — глава 17 «Стандартная библиотека»

## Execution / inspection commands

| Command / operation | Classification | Source role | Verification | Rollback |
|---|---|---|---|---|
| `import sys` | read-only/workload | load sys module | module available | [Not applicable] |
| `sys.version_info` | read-only | inspect interpreter version tuple | tuple displayed | [Not applicable] |
| `sys.version_info[0] >= 3` | read-only | source major-version check | Boolean | [Not applicable] |
| `python2.7 versioncheck.py` | workload-generating / historical variant | warning branch | RuntimeWarning shown | [Not applicable] |
| `python3 versioncheck.py` | workload-generating | normal branch | normal continuation | [Not applicable] |
| `python3 use_logging.py` | state-changing / workload | writes `test.log` | path printed + log contents | [Needs confirmation] |
| `import platform; help(platform)` | read-only | source points to platform help | help text | [Not applicable] |
| `os.path.join(...)` | read-only computation | construct logging path | path value | [Not applicable] |
| `logging.debug(...)` | state-changing through configured file handler | DEBUG log entry | record in log | [Needs confirmation] |
| `logging.info(...)` | state-changing through configured file handler | INFO log entry | record in log | [Needs confirmation] |
| `logging.warning(...)` | state-changing through configured file handler | WARNING log entry | record in log | [Needs confirmation] |

## Version inspection

```python
import sys
sys.version_info
sys.version_info[0] >= 3
```

Source displayed value is historical/example output:

```text
(3, 0, 0, 'beta', 2)
```

Do not treat this exact tuple as a current environment expectation.

## versioncheck.py

```python
import sys, warnings

if sys.version_info[0] < 3:
    warnings.warn(
        "Для выполнения этой программы необходима как минимум версия Python 3.0",
        RuntimeWarning
    )
else:
    print('Нормальное продолжение')
```

Source commands:

```text
python2.7 versioncheck.py
python3 versioncheck.py
```

## use_logging.py

```python
if platform.platform().startswith('Windows'):
    logging_file = os.path.join(
        os.getenv('HOMEDRIVE'),
        os.getenv('HOMEPATH'),
        'test.log'
    )
else:
    logging_file = os.path.join(os.getenv('HOME'), 'test.log')
```

Before executing, resolve and inspect `logging_file`.

Configuration:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file,
    filemode='w',
)
```

Classification: state-changing filesystem operation.

## Logging levels shown

```python
logging.debug("Начало программы")
logging.info("Какие-то действия")
logging.warning("Программа умирает")
```

Source output file shows timestamp + level + message.

## Rollback

Source provides no deletion/restore command for `test.log`.

Rollback: **[Needs confirmation]**.
