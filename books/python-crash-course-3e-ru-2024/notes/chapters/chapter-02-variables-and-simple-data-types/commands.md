# Функции, методы, выражения и инструменты главы 2

Включены только элементы, подтверждённые RAG `e0011:c01–c10`.

## Базовые операции

| Элемент | Тип | Effect / роль | Verification | Rollback |
|---|---|---|---|---|
| `name = value` | state-changing (program state) | Связывает имя с текущим значением | `print(name)` | Повторное присваивание прежнего значения, если оно известно; иначе `[Needs confirmation]` |
| `print(...)` | workload-generating | Выводит значение/сообщение | Наблюдать stdout | `[Not applicable]` |
| f-string `f"{name}"` | read-only evaluation | Формирует новую строку с подстановкой | Вывести результат | `[Not applicable]` |
| `# comment` | read-only source annotation | Интерпретатор игнорирует текст после `#` до конца строки | Запуск выполняет только код вне комментария | `[Not applicable]` |

## Строковые методы

| Метод | Тип | Source-confirmed effect | Изменяет исходную строку? | Verification |
|---|---|---|---|---|
| `title()` | read-only transformation | Капитализирует начальные буквы слов | Нет, возвращает значение | `print(name.title())` |
| `upper()` | read-only transformation | Переводит символы в верхний регистр | Нет, возвращает значение | `print(name.upper())` |
| `lower()` | read-only transformation | Переводит символы в нижний регистр | Нет, возвращает значение | `print(name.lower())` |
| `rstrip()` | read-only transformation | Убирает пробельные символы справа | Нет без присваивания | Сравнить исходное значение и результат |
| `lstrip()` | read-only transformation | Убирает пробельные символы слева | Нет без присваивания | Сравнить результат |
| `strip()` | read-only transformation | Убирает пробельные символы с обоих краёв | Нет без присваивания | Сравнить результат |
| `removeprefix(prefix)` | read-only transformation | Возвращает строку без указанного префикса, если он присутствует | Нет без присваивания | Source example: `nostarch.com` |
| `removesuffix(suffix)` | read-only transformation | В упражнении 2.8 используется для удаления `.txt` | Нет без присваивания | `python_notes.txt` → имя без suffix |

Сохранение результата обратно в переменную, например:

~~~python
favorite_language = favorite_language.rstrip()
~~~

— state-changing для program state.

## Пробельные символы

| Последовательность | Роль |
|---|---|
| `\t` | табуляция |
| `\n` | перевод строки |
| `\n\t` | новая строка с последующей табуляцией |

## Числовые операции

| Операция | Тип | Source example |
|---|---|---|
| `+` | read-only evaluation | `2 + 3 → 5` |
| `-` | read-only evaluation | `3 - 2 → 1` |
| `*` | read-only evaluation | `2 * 3 → 6` |
| `/` | read-only evaluation | `3 / 2 → 1.5`; `4 / 2 → 2.0` |
| `**` | read-only evaluation | `3 ** 2 → 9` |
| parentheses | read-only evaluation | меняют порядок вычисления |

## Числовые литералы и присваивание

~~~python
universe_age = 14_000_000_000
x, y, z = 0, 0, 0
MAX_CONNECTIONS = 5000
~~~

- Подчёркивания улучшают читаемость числовой записи; при выводе остаются цифры.
- Множественное присваивание связывает несколько имён со значениями одной строкой.
- Верхний регистр для `MAX_CONNECTIONS` — соглашение для значений, которые предполагается считать константами; встроенного типа констант источник не заявляет.

## Диагностические элементы

### NameError

Source example:

~~~python
message = "Hello Python Crash Course reader!"
print(mesage)
~~~

Traceback указывает файл/строку и сообщает, что `mesage` не определено.

### SyntaxError

Source example с апострофом внутри строки в одинарных кавычках приводит к:

~~~text
SyntaxError: unterminated string literal
~~~

Источник связывает проблему с неверной границей строкового литерала.

## import this

~~~python
>>> import this
~~~

Тип: workload-generating.

Роль в главе: выводит Zen of Python. В RAG главы приведена только часть принципов; полный набор в артефактах не реконструируется.

## Source findings

Для упражнения 2.9 существует представительная неоднозначность: глава одновременно требует использовать деление и ранее показывает, что `/` с целыми возвращает float. См. [source-findings.md](source-findings.md).
