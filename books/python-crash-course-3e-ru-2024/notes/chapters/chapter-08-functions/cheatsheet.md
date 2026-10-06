# Шпаргалка главы 8 — Функции

## Symptom / problem framing

Типовые проблемы:

- функция вызывается с неверным числом аргументов;
- позиционные аргументы перепутаны местами;
- необязательный параметр сделан обязательным;
- функция неожиданно изменила переданный список;
- основной файл перегружен кодом функций;
- импорт создаёт конфликт имён.

## Baseline / context

~~~python
def greet_user(username):
    """Выводит простое приветствие."""
    print(f"Hello, {username.title()}!")
~~~

- `username` в определении — параметр.
- конкретное значение в вызове — аргумент.
- функция выполняется только при вызове.

## Выбор формы аргументов

| Задача | Source pattern |
|---|---|
| Порядок очевиден | positional arguments |
| Нужно явно показать роль | keyword arguments |
| Есть типичное значение | default value |
| Неизвестно число positional values | `*args` / `*toppings` |
| Неизвестны дополнительные named fields | `**kwargs` / `**user_info` |

## Read-only checks

### Проверить return

~~~python
musician = get_formatted_name('jimi', 'hendrix')
print(musician)
~~~

### Проверить список после функции

~~~python
print(unprinted_designs)
print(completed_models)
~~~

Если оригинал нужно сохранить:

~~~python
print_models(unprinted_designs[:], completed_models)
~~~

## Interpretation

- missing required positional arguments → вызов не соответствует определению;
- странный результат без exception → проверить порядок positional arguments;
- keyword name должен точно совпадать с параметром;
- default parameters идут после параметров без defaults;
- `return` передаёт значение обратно в вызывающий код;
- функция может вернуть dictionary;
- список, переданный напрямую, может быть изменён;
- `*args` source описывает как tuple;
- `**kwargs` source описывает как dictionary.

## Next action

1. Определить одну задачу функции.
2. Выбрать минимальный набор обязательных параметров.
3. Решить, какие данные могут быть optional.
4. Решить, допустимо ли изменение переданной коллекции.
5. Определить, нужен `print` или `return`.
6. Проверить representative вызовы.
7. При повторном использовании вынести функцию в module.

## Verification / acceptance checks

- функция вызывается без `TypeError`;
- positional arguments сопоставлены в правильном порядке;
- keyword arguments используют точные имена;
- default case и override case оба проверены;
- returned value сохранён и проверен;
- для list mutation проверены оба списка;
- при передаче `[:]` original list остаётся неизменным;
- variadic function проверена с разным числом arguments;
- imported function вызывается выбранным синтаксисом.

## Rollback

- вызов/read-only return: `[Not applicable]`.
- mutation переданного списка: отдельный rollback source не задаёт — `[Needs confirmation]`.
- source-supported prevention: передать копию через `[:]`, если оригинал должен сохраниться.
- изменение модульной структуры файлов: отдельная rollback-процедура в главе не задана — `[Needs confirmation]`.

## Import boundary

Предпочитаемые source варианты для ясности:

~~~python
import pizza
from pizza import make_pizza
~~~

`from pizza import *` показан для распознавания, но источник предупреждает о конфликтах имён.
