# Шпаргалка главы 4 — Работа со списками

## Symptom / problem framing

Типовые проблемы главы:

- действие внутри `for` выполняется только один раз;
- действие после цикла повторяется для каждого элемента;
- Python сообщает `IndentationError`;
- после `for` пропущено двоеточие;
- `range()` заканчивается на число раньше ожидаемого;
- «копия» списка меняется вместе с оригиналом;
- попытка изменить элемент кортежа даёт `TypeError`.

## Baseline / context

~~~python
magicians = ['alice', 'david', 'carolina']

for magician in magicians:
    print(magician)
~~~

- `magician` получает очередное значение.
- Тело с отступом выполняется для каждого элемента.
- Строка без отступа после тела выполняется один раз после цикла.
- Источник рекомендует содержательные имена временных переменных.

## Read-only checks

### Проверить диапазон

~~~python
print(list(range(1, 5)))
~~~

Ожидаемый source result:

~~~text
[1, 2, 3, 4]
~~~

### Проверить числовой список

~~~python
digits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
print(min(digits))
print(max(digits))
print(sum(digits))
~~~

### Проверить срез

~~~python
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:3])
print(players[:4])
print(players[2:])
print(players[-3:])
~~~

### Проверить независимость копии

~~~python
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:]

my_foods.append('cannoli')
friend_foods.append('ice cream')

print(my_foods)
print(friend_foods)
~~~

Списки должны различаться.

## Interpretation

- `IndentationError: expected an indented block` → после `for` нет требуемого блока с отступом.
- `IndentationError: unexpected indent` → отступ поставлен там, где источник не ожидает вложенного блока.
- Код работает, но одна строка выполняется только после цикла → вероятна пропущенная indentation у этой строки.
- Итоговое сообщение повторяется для каждого элемента → вероятен лишний отступ.
- `SyntaxError: expected ':'` → проверить двоеточие после `for`.
- `range(start, stop)` не включает `stop`.
- `friend_foods = my_foods` связывает два имени с одним списком; независимая копия в source example создаётся через `my_foods[:]`.
- Присваивание `tuple[index] = ...` недопустимо и вызывает `TypeError`.

## Next action

1. Для повторяющегося действия определить список и временную переменную.
2. Проверить двоеточие после `for`.
3. Проверить, какие строки должны иметь отступ.
4. Для числовой последовательности проверить конечную границу `range()`.
5. Для подмножества использовать срез.
6. Для независимой копии использовать полный срез `[:]`.
7. Для неизменяемого набора использовать кортеж.
8. После изменения повторно вывести/проверить результат.

## Modifying action

Примеры state-changing program state:

~~~python
squares = []
squares.append(value**2)

my_foods.append('cannoli')
friend_foods.append('ice cream')

dimensions = (400, 100)
~~~

Редактирование отступов, двоеточий и форматирования изменяет исходный файл программы.

## Verification / acceptance checks

- `for` выполняет тело по одному разу на каждый элемент.
- Код без отступа после цикла выполняется один раз.
- `range(1, 6)` охватывает 1–5.
- `list(range(2, 11, 2))` даёт `[2, 4, 6, 8, 10]`.
- `min/max/sum` дают source-confirmed результаты для `digits`.
- `sorted` здесь не рассматривается; chapter focus — `range`, slices и loops.
- `my_foods[:]` даёт независимый список при последующих `append()`.
- попытка изменить элемент tuple должна быть отвергнута Python.
- после присваивания нового tuple переменная содержит новый набор.

## Rollback

- Для ошибочной indentation source-supported remediation — вернуть отступ туда, где действие должно выполняться, либо убрать лишний.
- Для пропущенного `:` — добавить двоеточие.
- Для диапазона с ошибкой off-by-one — источник предлагает увеличить конечное значение на 1, если требуется включить ожидаемую верхнюю границу.
- Для state-changing `append()` отдельный rollback в главе не задан: `[Needs confirmation]`.
- Для переопределения tuple возврат прежнего tuple возможен только если его значения известны; явная rollback-процедура: `[Needs confirmation]`.

## Workload boundary

Упражнение 4.4 предлагает вывести числа от 1 до 1 000 000. Это workload-generating действие с очень большим stdout. Source-supported stop action: `Ctrl+C` или закрытие окна вывода, если операция занимает слишком много времени.
