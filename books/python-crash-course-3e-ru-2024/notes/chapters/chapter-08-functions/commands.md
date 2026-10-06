# Синтаксис и операции главы 8

Только элементы, подтверждённые RAG `e0017:c01–c16`.

## Определение и вызов

~~~python
def greet_user():
    """Выводит простое приветствие."""
    print("Hello!")

greet_user()
~~~

Классификация: definition + workload-generating call.

## Параметры и аргументы

~~~python
def greet_user(username):
    ...
greet_user('jesse')
~~~

- `username` — parameter;
- `'jesse'` — argument.

## Positional arguments

~~~python
describe_pet('hamster', 'harry')
~~~

Risk: порядок должен соответствовать параметрам.

Verification: если вывод выглядит бессмысленно, source рекомендует проверить порядок.

## Keyword arguments

~~~python
describe_pet(animal_type='hamster', pet_name='harry')
~~~

Имена должны точно совпадать с параметрами.

## Default values

~~~python
def describe_pet(pet_name, animal_type='dog'):
    ...
~~~

Правило source: параметры с default идут после параметров без default.

## Return

~~~python
def get_formatted_name(first_name, last_name):
    full_name = f"{first_name} {last_name}"
    return full_name.title()
~~~

Классификация: read-only transformation; результат передаётся вызывающему коду.

## Optional parameter

~~~python
def get_formatted_name(first_name, last_name, middle_name=''):
    if middle_name:
        ...
~~~

Пустая строка в source используется как falsey default.

## Return dictionary

~~~python
def build_person(first_name, last_name):
    person = {'first': first_name, 'last': last_name}
    return person
~~~

Source finding для варианта `age`: код и пояснение расходятся по default; см. `source-findings.md`.

## List mutation

~~~python
def print_models(unprinted_designs, completed_models):
    while unprinted_designs:
        current_design = unprinted_designs.pop()
        completed_models.append(current_design)
~~~

Классификация: state-changing.

Effect: source list сокращается, destination list растёт.

## Prevent mutation of original list

~~~python
print_models(unprinted_designs[:], completed_models)
~~~

Срез создаёт copy для функции.

Tradeoff source: дополнительное время и память на копию.

## Arbitrary positional arguments

~~~python
def make_pizza(*toppings):
    ...
~~~

Source: Python собирает значения в tuple.

При наличии обязательного параметра:

~~~python
def make_pizza(size, *toppings):
    ...
~~~

Variadic parameter должен быть последним среди positional parameters.

## Arbitrary keyword arguments

~~~python
def build_profile(first, last, **user_info):
    ...
~~~

Source: дополнительные пары собираются в dictionary.

Обобщённое имя, встречающееся в коде: `**kwargs`.

## Imports

~~~python
import pizza
pizza.make_pizza(...)
~~~

~~~python
from pizza import make_pizza
make_pizza(...)
~~~

~~~python
from pizza import make_pizza as mp
mp(...)
~~~

~~~python
import pizza as p
p.make_pizza(...)
~~~

~~~python
from pizza import *
~~~

Последний вариант source не рекомендует для больших сторонних модулей из-за возможных name collisions.

## Formatting

Source rules:

- function/module names: lowercase + underscores;
- docstring сразу после function definition;
- default parameter: `param='value'`, без пробелов вокруг `=`;
- keyword argument: `param='value'`, без пробелов вокруг `=`;
- imports в начале файла, кроме предварительных file-level comments;
- несколько функций разделяются двумя пустыми строками;
- source cites 79-character code-line limit.
