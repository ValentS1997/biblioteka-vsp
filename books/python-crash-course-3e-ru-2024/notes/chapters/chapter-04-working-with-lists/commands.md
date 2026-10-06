# Конструкции, функции и действия главы 4

Только source-confirmed элементы из `e0013:c01–c13`.

## Цикл for

~~~python
for magician in magicians:
    print(magician)
~~~

Классификация: workload-generating.

Effect: выполняет тело цикла один раз для каждого элемента списка.

Risk: неверная indentation может изменить область повторения либо вызвать exception.

Verification: сверить число/порядок выводов с элементами списка.

Rollback: для изменения indentation — вернуть source-intended структуру; универсальная процедура `[Needs confirmation]`.

## range() и list()

| Конструкция | Тип | Source-confirmed effect |
|---|---|---|
| `range(1, 5)` | read-only sequence generation | значения 1–4 |
| `range(1, 6)` | read-only sequence generation | значения 1–5 |
| `range(6)` | read-only sequence generation | значения 0–5 |
| `range(2, 11, 2)` | read-only sequence generation | шаг 2: 2,4,6,8,10 |
| `list(range(...))` | state-producing expression | создаёт числовой список |

Правило source: конечное значение `stop` не включается.

## Числовые функции

| Функция | Тип | Effect |
|---|---|---|
| `min(values)` | read-only | минимальное значение |
| `max(values)` | read-only | максимальное значение |
| `sum(values)` | read-only | сумма значений |

Source example для `digits = [1,2,3,4,5,6,7,8,9,0]`: минимум 0, максимум 9, сумма 45.

## List comprehension

~~~python
squares = [value**2 for value in range(1, 11)]
~~~

Классификация: state-producing expression.

Effect: создаёт новый список значений выражения для каждого значения диапазона.

Особенность source syntax: в comprehension после `for value in ...` двоеточие не ставится.

## Срезы

| Конструкция | Тип | Effect |
|---|---|---|
| `items[0:3]` | read-only transformation | элементы с индексами 0,1,2 |
| `items[1:4]` | read-only transformation | индексы 1,2,3 |
| `items[:4]` | read-only transformation | от начала до индекса перед 4 |
| `items[2:]` | read-only transformation | от индекса 2 до конца |
| `items[-3:]` | read-only transformation | последние три элемента |
| `items[:]` | read-only transformation | новый список-копия всех элементов |

Источник также указывает, что в срез можно передать третье значение шага, но отдельный пример в chapter RAG не приводится.

## Копирование списка

Source-supported copy:

~~~python
friend_foods = my_foods[:]
~~~

Тип: state-changing binding к новому списку.

Verification: добавить разные значения через `append()` в каждый список и сравнить вывод.

Source example «не работает как копия»:

~~~python
friend_foods = my_foods
~~~

Обе переменные связываются с одним списком.

## Кортежи

~~~python
dimensions = (200, 50)
print(dimensions[0])

for dimension in dimensions:
    print(dimension)
~~~

Чтение и перебор — read-only/workload-generating.

Попытка изменения:

~~~python
dimensions[0] = 250
~~~

Классификация: state-changing attempt; Python отклоняет её:

~~~text
TypeError: 'tuple' object does not support item assignment
~~~

Допустимая замена всего набора:

~~~python
dimensions = (400, 100)
~~~

Одноэлементный tuple в source:

~~~python
my_t = (3,)
~~~

Запятая является существенной частью определения.

## Ошибки структуры цикла

- отсутствует обязательный отступ → `IndentationError: expected an indented block...`;
- лишний отступ → `IndentationError: unexpected indent`;
- неправильный, но синтаксически допустимый отступ → logical error;
- отсутствует двоеточие после `for` → `SyntaxError: expected ':'`.

## Workload: миллион строк

Упражнение 4.4:

- создать список 1…1 000 000;
- вывести числа через `for`.

Классификация: workload-generating, potentially high-output.

Source-supported interrupt:

- `Ctrl+C`;
- либо закрытие окна вывода.

## Style actions

Источник приводит следующие рекомендации:

- четыре пробела на уровень indentation;
- редактор должен вставлять пробелы вместо символа табуляции;
- строки кода — менее 80 символов в упражнении 4.15; в пояснении обсуждается стандартная длина 79 и ориентир 80;
- комментарии PEP 8 — до 72 символов в строке;
- пустые строки использовать для группировки, без избытка.

Настройка редактора — state-changing user configuration. Конкретный rollback в главе не описан: `[Needs confirmation]`.
