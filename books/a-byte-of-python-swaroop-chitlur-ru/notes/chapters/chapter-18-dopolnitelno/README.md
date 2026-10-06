# Глава 18. Дополнительно

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 18 — «Дополнительно». Она собирает несколько дополнительных конструкций и
идиом Python, которые дополняют основной материал книги:

- tuple unpacking и starred assignment;
- специальные методы классов;
- однострочные blocks;
- `lambda`;
- list comprehensions;
- `*args` / `**kwargs`;
- `exec` / `eval`;
- `assert`;
- `repr`;
- escape sequences;
- raw strings.

Разделы, подтверждённые RAG:

- 18.1 Передача кортежей
- 18.2 Специальные методы
- 18.3 Блоки в одно выражение
- 18.4 Lambda-формы
- 18.5 Генераторы списков
- 18.6 Передача кортежей и словарей в функции
- 18.7 `exec` и `eval`
- 18.8 Оператор `assert`
- 18.9 Функция `repr`
- 18.10 Управляющие последовательности
- 18.11 Необрабатываемые строки
- 18.12 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0137:c01` — `p0144:c01`
- substantive content: PDF pages 137–143
- PDF page 144: only running footer for chapter 18
- printed pages visible in substantive content: 129–135
- chapter start: PDF page 137, heading «Дополнительно»
- chapter summary: PDF page 143, section 18.12 «Резюме»
- next chapter boundary: PDF page 145 begins «Что дальше»
- boundary verified: yes

## Main principle

Глава показывает компактные способы:

- распаковывать значения;
- адаптировать пользовательские classes к встроенным operations;
- строить короткие anonymous functions;
- преобразовывать collections;
- принимать variable argument counts;
- выполнять/вычислять Python source text at runtime;
- проверять invariants;
- получать representations;
- управлять special characters in strings.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 18.1 | Tuple return/unpacking, starred unpacking, swap via `a, b = b, a`. |
| 18.2 | Special methods such as `__init__`, `__del__`, `__str__`, `__lt__`, `__getitem__`, `__len__`. |
| 18.3 | Single-statement block may share line with `if`; source recommends generally avoiding this style. |
| 18.4 | `lambda` creates a small anonymous function; example sorts list of dicts by `y`. |
| 18.5 | List comprehension creates a new list from source list plus expression/filter. |
| 18.6 | `*args` collects additional positional arguments; `**kwargs` maps additional keyword pairs. |
| 18.7 | `exec` executes Python source text; `eval` evaluates a Python expression string. |
| 18.8 | `assert` checks a condition and source shows `AssertionError` on false condition. |
| 18.9 | `repr` returns printable/canonical representation in source framing; `__repr__` customizes it. |
| 18.10 | Escape sequences for quotes, backslash, newline `\n`, tab `\t`, and line continuation. |
| 18.11 | Raw-string prefix `r` / `R`; source recommends raw strings for regular expressions. |
| 18.12 | Additional features are considered enough for practical work; next chapter discusses continued learning. |

## Core examples

### Tuple unpacking

```python
def get_error_details():
    return (2, 'описание ошибки No2')

errnum, errstr = get_error_details()
a, *b = [1, 2, 3, 4]
a, b = b, a
```

### Lambda

```python
points = [{'x': 2, 'y': 3}, {'x': 4, 'y': 1}]
points.sort(key=lambda i: i['y'])
print(points)
```

### List comprehension

```python
listone = [2, 3, 4]
listtwo = [2*i for i in listone if i > 2]
print(listtwo)
```

### Variable positional arguments

```python
def powersum(power, *args):
    total = 0
    for i in args:
        total += pow(i, power)
    return total
```

### Runtime code execution

```python
exec('print("Здравствуй, Мир!")')
eval('2*3')
```

### Assertions

```python
assert len(mylist) >= 1
```

### repr

```python
repr(i)
eval(repr(i))
```

### Raw string

```python
r"Перевод строки обозначается \n"
```

## Operational acceptance

После главы читатель должен уметь:

- распаковать tuple result;
- использовать starred unpacking;
- объяснить назначение нескольких special methods;
- использовать `lambda` как key-function в source example;
- построить list comprehension;
- распознать `*args` / `**kwargs`;
- различить `exec` и `eval` в source framing;
- использовать `assert` как shown invariant check;
- получить representation через `repr`;
- записать common escape sequences и raw string.

## Safety / integrity boundary

`exec` и `eval` являются code-execution boundary:

- source text passed to `exec` выполняется;
- expression passed to `eval` вычисляется;
- effect depends entirely on runtime string/expression.

Не выполнять `exec/eval` с непроверенными runtime strings.

Runtime mutations в examples:

- `points.sort(...)` меняет список in place;
- `mylist.pop()` меняет список;
- `exec` потенциально может менять любой доступный runtime state в зависимости от payload.

Сохранение `lambda.py` и `list_comprehension.py` меняет filesystem state;
source rollback не задан.

## Conditional artifacts

Раздел 18.12 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
