# Условные конструкции и операции главы 5

Только элементы, подтверждённые RAG `e0014:c01–c11`.

## Сравнения

| Элемент | Тип | Source-confirmed meaning |
|---|---|---|
| `==` | read-only evaluation | равенство |
| `!=` | read-only evaluation | неравенство |
| `<` | read-only evaluation | меньше |
| `<=` | read-only evaluation | меньше или равно |
| `>` | read-only evaluation | больше |
| `>=` | read-only evaluation | больше или равно |

## Строковая нормализация для проверки

~~~python
car.lower() == 'audi'
~~~

Классификация: read-only evaluation.

Источник явно показывает, что исходное значение `car` при этом не изменяется.

## Комбинация условий

| Конструкция | Тип | Source-confirmed rule |
|---|---|---|
| `A and B` | read-only evaluation | True только если обе части True |
| `A or B` | read-only evaluation | True если хотя бы одна часть True |
| `value in items` | read-only evaluation | проверка наличия |
| `value not in items` | read-only evaluation | проверка отсутствия |

## Простой if

~~~python
if age >= 18:
    print("You are old enough to vote!")
~~~

Классификация: workload-generating control flow.

Effect: блок выполняется только при True.

## if-else

~~~python
if age >= 18:
    print("You are old enough to vote!")
else:
    print("Sorry, you are too young to vote.")
~~~

Классификация: workload-generating control flow.

Rule: выполняется ровно один из двух блоков.

## if-elif-else

~~~python
if age < 4:
    price = 0
elif age < 18:
    price = 25
else:
    price = 40
~~~

Классификация: state-changing, потому что выбранная ветвь присваивает `price`.

Effect: Python проверяет условия по порядку и выполняет первый истинный блок.

Risk: поздние условия не проверяются после первого True.

Verification: тестировать representative значения для каждой ветви.

Rollback: `[Needs confirmation]`.

## Серия независимых if

~~~python
if 'mushrooms' in requested_toppings:
    print("Adding mushrooms.")

if 'pepperoni' in requested_toppings:
    print("Adding pepperoni.")
~~~

Классификация: workload-generating control flow.

Rule: каждая проверка выполняется независимо; могут выполниться несколько блоков.

## Проверка списка на пустоту

~~~python
if requested_toppings:
    ...
else:
    ...
~~~

Классификация: read-only condition + workload-generating branches.

Source rule: непустой список оценивается как True, пустой — как False.

## Проверка допустимых значений

~~~python
for requested_topping in requested_toppings:
    if requested_topping in available_toppings:
        print(f"Adding {requested_topping}.")
    else:
        print(f"Sorry, we don't have {requested_topping}.")
~~~

Классификация: workload-generating.

Effect: каждый запрос проверяется по списку доступных значений перед обработкой.

## Boolean values

~~~python
game_active = True
can_edit = False
~~~

Классификация: state-changing program state.

Role: хранение состояния/условия.

## Formatting

Source-only style rule главы:

~~~python
if age < 4:
~~~

Один пробел до и после оператора сравнения. Это изменение исходного кода, но не runtime state.
