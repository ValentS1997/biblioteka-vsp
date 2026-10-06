# Функции, операторы и действия главы 7

Только элементы, подтверждённые RAG `e0016:c01–c09`.

## input()

~~~python
message = input("Tell me something, and I will repeat it back to you: ")
~~~

Классификация: workload-generating / blocking input.

Effect: приостанавливает программу до ввода пользователя; source говорит, что результат сохраняется как строка.

Verification: вывести полученное значение.

Rollback: `[Not applicable]`.

## int()

~~~python
age = int(age)
~~~

Классификация: read-only transformation + state-changing assignment.

Effect: преобразует строковое представление числа в числовое значение в source example.

Verification: числовое сравнение `age >= 18` выполняется.

Нечисловой ввод в текущей главе не рассматривается: `[Needs confirmation]`.

## +=

~~~python
prompt += "\nWhat is your first name? "
current_number += 1
~~~

Классификация: state-changing.

Effect: source использует `+=` для добавления текста к строке и увеличения счётчика.

## Modulo %

~~~python
number % 2
~~~

Классификация: read-only evaluation.

Effect: возвращает остаток от деления.

Source use:

~~~python
if number % 2 == 0:
    ...
~~~

## while

~~~python
current_number = 1

while current_number <= 5:
    print(current_number)
    current_number += 1
~~~

Классификация: workload-generating control flow.

Risk: если состояние, влияющее на условие, не меняется, цикл может стать бесконечным.

Verification: source output 1..5 и завершение программы.

## Flag

~~~python
active = True

while active:
    message = input(prompt)
    if message == 'quit':
        active = False
~~~

Классификация: state-changing control flow.

Effect: одно Boolean state управляет продолжением цикла.

## break

~~~python
while True:
    city = input(prompt)
    if city == 'quit':
        break
~~~

Классификация: control-flow action.

Effect: немедленно завершает текущий цикл.

Source note: `break` может применяться и в `for`.

## continue

~~~python
while current_number < 10:
    current_number += 1
    if current_number % 2 == 0:
        continue
    print(current_number)
~~~

Классификация: control-flow action.

Effect: пропускает остаток текущей итерации и возвращается к началу цикла.

Source output: 1, 3, 5, 7, 9.

## Аварийное завершение бесконечного цикла

Source-supported action:

~~~text
Ctrl+C
~~~

или закрытие терминального окна с выводом программы.

Тип: process-interrupt / state-changing для текущего процесса.

## Перемещение между списками

~~~python
while unconfirmed_users:
    current_user = unconfirmed_users.pop()
    confirmed_users.append(current_user)
~~~

`pop()` удаляет элемент из первого списка и возвращает его; `append()` добавляет его во второй.

Verification: первый список становится пустым, второй содержит перенесённые элементы.

## Удаление всех вхождений

~~~python
while 'cat' in pets:
    pets.remove('cat')
~~~

Классификация: state-changing.

Effect: повторяет source `remove()`, пока значение больше не присутствует.

Verification:

~~~python
print(pets)
~~~

и проверить отсутствие `'cat'`.

## Заполнение словаря из input

~~~python
responses[name] = response
~~~

Классификация: state-changing.

Effect: связывает введённое имя с введённым ответом; повторный одинаковый ключ перезапишет значение по общей модели словаря, но отдельный scenario повторных имён в главе не анализируется.
