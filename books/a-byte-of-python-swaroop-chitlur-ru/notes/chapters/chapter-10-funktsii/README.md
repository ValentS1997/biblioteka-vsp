# Глава 10. Функции

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 10 — «Функции». Она вводит reusable named blocks через `def`, затем разбирает
параметры и аргументы, области видимости, default/keyword/variable/keyword-only
arguments, `return`, `pass`, docstrings, `__doc__`, `help()` и annotations.

Разделы, подтверждённые RAG:

- вводная часть: определение и вызов функции
- 10.1 Параметры функций
- 10.2 Локальные переменные
- 10.3 Зарезервированное слово `global`
- 10.4 Зарезервированное слово `nonlocal`
- 10.5 Значения аргументов по умолчанию
- 10.6 Ключевые аргументы
- 10.7 Переменное число параметров
- 10.8 Только ключевые параметры
- 10.9 Оператор `return`
- 10.10 Строки документации
- 10.11 Аннотации
- 10.12 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0067:c01` — `p0078:c01`
- PDF pages: 67–78
- printed pages visible in chapter: 59–70
- chapter start: PDF page 67, heading «Функции»
- chapter end: PDF page 78, continuation of section 10.12
- next chapter boundary: PDF page 79 begins «Модули»
- boundary verified: yes

## Main principle

Функция даёт имя блоку кода и позволяет вызывать его многократно. Поведение функции
определяется входными параметрами, scope rules и способом возврата результата. Глава
постепенно расширяет базовую форму `def name(...):` до default/keyword/varargs и
keyword-only parameters, а затем добавляет documentation mechanisms.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| Intro | `def`, имя, parentheses, colon, indented body, repeated function calls. |
| 10.1 | Parameters are names in definition; arguments are values passed at call time. |
| 10.2 | Local names are scoped to the function/block and do not change same-named outer variables. |
| 10.3 | `global` marks an outermost/global name for assignment inside a function. |
| 10.4 | `nonlocal` targets a name in an enclosing non-global function scope. |
| 10.5 | Default argument values make trailing parameters optional in source framing. |
| 10.6 | Keyword arguments bind values by parameter name instead of only by position. |
| 10.7 | `*numbers` collects positional arguments; `**keywords` collects keyword arguments. |
| 10.8 | Parameters after `*` are keyword-only; missing required keyword-only argument produces an error in source example. |
| 10.9 | `return` exits a function and can return a value; source also discusses `None` and `pass`. |
| 10.10 | Docstrings document functions; `__doc__` and `help()` expose them. |
| 10.11 | Annotations attach extra information to parameters/return values; source does not develop the topic further. |
| 10.12 | Most everyday function mechanics are considered covered; next topic is modules. |

## Core examples

Basic function:

```python
def sayHello():
    print('Привет, Мир!')

sayHello()
sayHello()
```

Parameters:

```python
def printMax(a, b):
    if a > b:
        print(a, 'максимально')
    elif a == b:
        print(a, 'равно', b)
    else:
        print(b, 'максимально')
```

Variable arguments:

```python
def total(initial=5, *numbers, **keywords):
    count = initial
    for number in numbers:
        count += number
    for key in keywords:
        count += keywords[key]
    return count
```

Return:

```python
def maximum(x, y):
    if x > y:
        return x
    elif x == y:
        return 'Числа равны.'
    else:
        return y
```

Docstring:

```python
def printMax(x, y):
    '''Выводит максимальное из двух чисел.

       Оба значения должны быть целыми числами.'''
    ...
```

## Operational acceptance

После главы читатель должен уметь:

- определить и вызвать функцию;
- отличить parameters от arguments;
- объяснить local/global/nonlocal scope на source examples;
- использовать positional, default и keyword arguments;
- объяснить роль `*args`-like и `**kwargs`-like source patterns;
- распознать keyword-only parameter;
- использовать `return` и понимать source explanation `return None`;
- использовать docstring, `__doc__` и `help(function)`.

## Safety / integrity boundary

- Все `python <file>.py` examples запускают учебный code; системную конфигурацию они
  не изменяют, но могут менять runtime state.
- Сохранение example files меняет filesystem state; source rollback не задан.
- `func_default.py` в RAG содержит отступ у вызовов `say(...)`, который конфликтует
  с показанным output; этот фрагмент не нормализован.
- Source statement «default value должно быть неизменным» сохранён как historical
  technical claim и не повышен до текущего проверенного правила.
- Exact `TypeError` text для keyword-only example сохранён как source output, без
  внешней проверки современной формулировки.
- Shebang `#!/usr/bin/python` в `func_return.py` сохранён как source variant.

## Conditional artifacts

Раздел 10.12 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
