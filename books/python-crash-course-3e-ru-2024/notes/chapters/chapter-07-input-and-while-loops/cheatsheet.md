# Шпаргалка главы 7 — Ввод данных и циклы while

## Symptom / problem framing

Типовые проблемы:

- ввод выглядит числом, но сравнение с числом падает;
- цикл не завершается;
- quit value выводится как обычное сообщение;
- нужно завершить цикл по нескольким событиям;
- нужно пропустить текущую итерацию, но не завершать весь цикл;
- список меняется во время обработки;
- нужно удалить все повторения значения.

## Baseline / context

~~~python
message = input("Tell me something: ")
~~~

По source `input()` возвращает строку.

Числовой ввод:

~~~python
age = input("How old are you? ")
age = int(age)
~~~

## Read-only / low-impact checks

### Проверка типа поведения через сравнение

Source negative example:

~~~python
age = input("How old are you? ")
age >= 18
~~~

Даёт `TypeError`, потому что `age` остаётся строкой.

### Проверка modulo

~~~python
number % 2 == 0
~~~

True → число делится на 2 без остатка.

## Выбор управления while

| Намерение | Source pattern |
|---|---|
| Работать, пока условие True | `while condition:` |
| Завершить по quit value | `while message != 'quit':` |
| Несколько возможных причин завершения | Boolean flag |
| Немедленный выход из цикла | `break` |
| Пропустить остаток текущей итерации | `continue` |

## Next action

1. Задать начальное состояние.
2. Сформулировать условие продолжения.
3. Проверить, какая строка изменит состояние.
4. Если используется user input — определить quit value.
5. Для нескольких exit conditions использовать source-supported flag.
6. Для `while True` обязательно иметь достижимый `break`.
7. Проверить выход до добавления дополнительной логики.

## Modifying action

~~~python
current_number += 1
active = False
unconfirmed_users.pop()
confirmed_users.append(current_user)
pets.remove('cat')
responses[name] = response
~~~

Все эти действия меняют program state.

## Verification / acceptance checks

- числовой input преобразован через `int()` перед числовым сравнением;
- quit value действительно завершает цикл;
- quit value не выводится как обычное сообщение, если это не требуется;
- flag становится `False` при exit condition;
- `break` выводит выполнение из цикла;
- `continue` пропускает оставшуюся часть текущего прохода;
- после переноса элементов source list опустел, destination list заполнен;
- после удаления всех повторов значение отсутствует;
- результаты опроса сохранены в словаре.

## Rollback

- read-only input/checks: `[Not applicable]`.
- изменения списков через `pop()/remove()/append()`: отдельной rollback-процедуры глава не задаёт — `[Needs confirmation]`.
- словарь `responses`: rollback не описан — `[Needs confirmation]`.
- бесконечный цикл: source emergency stop — `Ctrl+C` или закрытие окна вывода.

## Infinite-loop acceptance

Для каждого `while` ответить:

1. Что делает условие False?
2. Может ли эта строка реально выполниться?
3. Есть ли `break`?
4. Проверен ли фактический выход?
