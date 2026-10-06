# Глава 16. Исключения

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 16 — «Исключения». Она показывает, как Python сообщает об ошибках и как
программа может перехватывать, создавать, вызывать и гарантированно завершать
обработку ресурсов при exceptional conditions.

Разделы, подтверждённые RAG:

- 16.1 Ошибки
- 16.2 Исключения
- 16.3 Обработка исключений
- 16.4 Вызов исключения
- 16.5 Try .. Finally
- 16.6 Оператор `with`
- 16.7 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0127:c01` — `p0132:c01`
- PDF pages: 127–132
- printed pages visible in chapter: 119–124
- chapter start: PDF page 127, heading «Исключения»
- chapter end: PDF page 132, section 16.7 «Резюме»
- next chapter boundary: PDF page 133 begins «Стандартная библиотека»
- boundary verified: yes

## Main principle

Source exception flow:

`exception/error → try → matching except → optional else → cleanup/finally`

Дополнительно:

- `raise` explicitly triggers an exception;
- custom exception type derives from `Exception`;
- `finally` is used for cleanup;
- `with` encapsulates a common resource-acquire/resource-release pattern.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 16.1 | Mistyped `Print` example produces traceback with `NameError`. |
| 16.2 | `input()` + Ctrl-D demonstrates `EOFError`. |
| 16.3 | `try/except` handles `EOFError` and `KeyboardInterrupt`; `else` runs when no exception occurs. |
| 16.4 | Custom `ShortInputException(Exception)`; `raise`; exception object bound with `as ex`. |
| 16.5 | `try/finally` ensures source cleanup path calls `f.close()` after normal/interrupted file reading. |
| 16.6 | `with open(...) as f` delegates cleanup to context-manager protocol in source framing. |
| 16.7 | Summary of `try/except`, `try/finally`, custom exceptions and raising exceptions. |

## Core examples

### try_except.py

```python
try:
    text = input('Введите что-нибудь --> ')
except EOFError:
    print('Ну зачем вы сделали мне EOF?')
except KeyboardInterrupt:
    print('Вы отменили операцию.')
else:
    print('Вы ввели {0}'.format(text))
```

### raising.py

```python
class ShortInputException(Exception):
    def __init__(self, length, atleast):
        Exception.__init__(self)
        self.length = length
        self.atleast = atleast

try:
    text = input('Введите что-нибудь --> ')
    if len(text) < 3:
        raise ShortInputException(len(text), 3)
except EOFError:
    print('Ну зачем вы сделали мне EOF?')
except ShortInputException as ex:
    print('ShortInputException: Длина введённой строки -- {0}; '
          'ожидалось, как минимум, {1}'.format(ex.length, ex.atleast))
else:
    print('Не было исключений.')
```

### finally.py

```python
import time

try:
    f = open('poem.txt')
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print(line, end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('!! Вы отменили чтение файла.')
finally:
    f.close()
    print('(Очистка: Закрытие файла)')
```

### using_with.py

```python
with open("poem.txt") as f:
    for line in f:
        print(line, end='')
```

## Operational acceptance

После главы читатель должен уметь:

- распознать unhandled exception traceback;
- использовать `try/except` для конкретных exception types;
- использовать `else` для no-exception path;
- определить custom exception class;
- вызвать exception через `raise`;
- получить exception object через `as ex`;
- использовать `finally` для cleanup path;
- объяснить source role `with open(...)`.

## Safety / dependency boundary

- `finally.py` и `using_with.py` читают `poem.txt`; file presence is a dependency:
  **[Needs confirmation]** для standalone запуска главы.
- `time.sleep(2)` намеренно замедляет example.
- Ctrl-C / Ctrl-D используются как interactive test inputs.
- Chapter examples не предназначены для изменения system configuration.
- Сохранение example scripts меняет filesystem state; source rollback не задан.

## Conditional artifacts

Раздел 16.7 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
