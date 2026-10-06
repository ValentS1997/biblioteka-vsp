# Операции, методы и функции главы 3

Включены только элементы, подтверждённые RAG `e0012:c01–c08`.

## Создание и чтение списка

| Элемент | Тип | Effect | Verification | Rollback |
|---|---|---|---|---|
| `items = ['a', 'b']` | state-changing (program state) | Создаёт/связывает список с именем | `print(items)` | `[Needs confirmation]` |
| `items[index]` | read-only | Возвращает элемент по индексу | Вывести значение | `[Not applicable]` |
| `items[-1]` | read-only | Возвращает последний элемент непустого списка | Вывести значение | `[Not applicable]` |
| `len(items)` | read-only | Возвращает количество элементов | Сравнить с фактическим списком | `[Not applicable]` |
| `print(...)` | workload-generating | Выводит список/элемент/сообщение | Наблюдать stdout | `[Not applicable]` |

## Изменение и добавление

| Операция | Тип | Source-confirmed effect | Риск | Verification | Rollback |
|---|---|---|---|---|---|
| `items[i] = value` | state-changing | Заменяет элемент по индексу | Потеря прежнего значения, если оно отдельно не сохранено | `print(items)` | `[Needs confirmation]` |
| `append(value)` | state-changing | Добавляет значение в конец | Меняет длину/содержимое | `print(items)`, `len(items)` | `[Needs confirmation]` |
| `insert(i, value)` | state-changing | Вставляет значение в позицию и сдвигает последующие элементы | Меняет индексы последующих элементов | `print(items)` | `[Needs confirmation]` |

## Удаление

| Операция | Тип | Source-confirmed effect | Когда использовать | Verification | Rollback |
|---|---|---|---|---|---|
| `del items[i]` | state-changing | Удаляет элемент по индексу; значение после удаления недоступно через эту операцию | Значение больше не требуется | `print(items)` | `[Needs confirmation]` |
| `items.pop()` | state-changing | Удаляет и возвращает последний элемент | Удалённое значение нужно использовать | Проверить список и возвращённое значение | `[Needs confirmation]` |
| `items.pop(i)` | state-changing | Удаляет и возвращает элемент заданной позиции | Нужно сохранить удалённое значение из известной позиции | Проверить список и значение | `[Needs confirmation]` |
| `items.remove(value)` | state-changing | Удаляет первое вхождение известного значения | Известно значение, а не индекс | `print(items)` | `[Needs confirmation]` |

Ограничение `remove()`: источник прямо указывает, что удаляется только первое вхождение. Удаление всех повторов с помощью цикла отнесено к материалу главы 7.

## Сортировка и порядок

| Операция | Тип | Effect | Исходный порядок | Rollback |
|---|---|---|---|---|
| `items.sort()` | state-changing | Сортирует сам список | Меняется | `[Needs confirmation]`; источник говорит, что исходный порядок уже не восстановить автоматически |
| `items.sort(reverse=True)` | state-changing | Постоянная сортировка в обратном порядке | Меняется | `[Needs confirmation]` |
| `sorted(items)` | read-only transformation | Возвращает отсортированное представление | Сохраняется | `[Not applicable]` |
| `sorted(items, reverse=True)` | read-only transformation | Возвращает представление в обратном порядке сортировки | Сохраняется | `[Not applicable]` |
| `items.reverse()` | state-changing | Обращает текущий порядок элементов | Меняется | Повторный `reverse()` возвращает предыдущий порядок |

## Строковый метод на элементе списка

~~~python
bicycles[0].title()
~~~

Тип: read-only transformation.

Источник использует метод главы 2 для форматирования выбранного строкового элемента.

## Диагностический сигнал

Source example:

~~~python
motorcycles = ['honda', 'yamaha', 'suzuki']
print(motorcycles[3])
~~~

Результат:

~~~text
IndexError: list index out of range
~~~

Тип: workload-generating check.

Источник рекомендует проверить off-by-one и при неясной причине вывести список или его длину.

## Empty-list boundary

~~~python
motorcycles = []
print(motorcycles[-1])
~~~

Даже индекс `-1` приводит к `IndexError`, потому что в списке нет элементов.
