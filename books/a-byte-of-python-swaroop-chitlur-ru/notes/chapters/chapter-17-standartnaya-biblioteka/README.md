# Глава 17. Стандартная библиотека

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 17 — «Стандартная библиотека». Она показывает на нескольких небольших примерах,
почему стандартная библиотека Python является важной частью практической работы:
проверка версии интерпретатора через `sys`, предупреждения через `warnings`,
файловое логирование через `logging`, а также дальнейшие источники изучения.

Разделы, подтверждённые RAG:

- 17.1 Модуль `sys`
- 17.2 Модуль `logging`
- 17.3 Серия «Модуль недели»
- 17.4 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0133:c01` — `p0136:c01`
- PDF pages: 133–136
- printed pages visible in chapter: 125–128
- chapter start: PDF page 133, heading «Стандартная библиотека»
- chapter end: PDF page 136, section 17.4 «Резюме»
- next chapter boundary: PDF page 137 begins «Дополнительно»
- boundary verified: yes

## Main principle

Source message: прежде чем писать собственную реализацию, полезно знать возможности
standard library.

Глава использует следующие modules:

- `sys` — interpreter/system-related information;
- `warnings` — user-visible warnings;
- `os` — environment/path operations;
- `platform` — platform identification;
- `logging` — persistent diagnostic/event messages.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 17.1 | `sys.version_info` as tuple-like version information; `warnings.warn` for unsupported interpreter major version. |
| 17.2 | `platform.platform()`, environment variables, `os.path.join`, `logging.basicConfig`, DEBUG/INFO/WARNING messages to a file. |
| 17.3 | Standard library contains much more; source recommends Doug Hellmann's «Module of the Week» and official Python documentation. |
| 17.4 | Only a small subset was covered; reader is encouraged to browse the standard-library documentation. |

## Core examples

### sys.version_info

```python
import sys
sys.version_info
sys.version_info[0] >= 3
```

Source REPL shows:

```text
(3, 0, 0, 'beta', 2)
True
```

### versioncheck.py

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

Source runs it with both `python2.7` and `python3`.

### use_logging.py

```python
import os, platform, logging

if platform.platform().startswith('Windows'):
    logging_file = os.path.join(
        os.getenv('HOMEDRIVE'),
        os.getenv('HOMEPATH'),
        'test.log'
    )
else:
    logging_file = os.path.join(os.getenv('HOME'), 'test.log')
```

Logging configuration:

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename=logging_file,
    filemode='w',
)

logging.debug("Начало программы")
logging.info("Какие-то действия")
logging.warning("Программа умирает")
```

## Operational acceptance

После главы читатель должен уметь:

- получить `sys.version_info`;
- проверить major version в source pattern;
- вызвать `warnings.warn`;
- определить source logging path из platform/environment inputs;
- использовать `os.path.join`;
- настроить file logging через `logging.basicConfig`;
- записать DEBUG, INFO и WARNING records;
- найти дальнейшие standard-library topics по source recommendations.

## Safety / dependency boundary

`use_logging.py` изменяет filesystem state:

- вычисляет path к `test.log`;
- `logging.basicConfig(... filename=..., filemode='w')` пишет файл;
- `filemode='w'` может перезаписать существующий target log.

Перед реальным запуском:

- resolved `logging_file`: **[Needs confirmation]**;
- наличие/значения `HOME` или `HOMEDRIVE` + `HOMEPATH`: **[Needs confirmation]**;
- overwrite intent для существующего `test.log`: **[Needs confirmation]**.

Source-specific rollback для log file не задан.

## Conditional artifacts

Раздел 17.4 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
