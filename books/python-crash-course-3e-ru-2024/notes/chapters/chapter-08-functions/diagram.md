# Диаграмма — функции

## Вызов функции

~~~mermaid
flowchart LR
    A["Аргументы"] --> B["Function call"]
    B --> C["Параметры"]
    C --> D["Тело функции"]
    D --> E{"Результат"}
    E -- "print" --> F["stdout"]
    E -- "return" --> G["Значение в caller"]
~~~

## Выбор параметров

~~~mermaid
flowchart TD
    A["Какие данные нужны?"] --> B{"Обязательны?"}
    B -- "Да" --> C["regular parameter"]
    B -- "Нет" --> D["default value"]
    A --> E{"Количество заранее известно?"}
    E -- "Нет, positional" --> F["*args"]
    E -- "Нет, keyword" --> G["**kwargs"]
~~~

## Mutability boundary

~~~mermaid
flowchart TD
    A["Передать list"] --> B{"Можно менять original?"}
    B -- "Да" --> C["function(original)"]
    C --> D["Изменения постоянны"]
    B -- "Нет" --> E["function(original[:])"]
    E --> F["Изменяется copy"]
~~~

## Модуль

~~~mermaid
flowchart LR
    A["pizza.py"] --> B["import pizza"]
    B --> C["pizza.make_pizza()"]
    A --> D["from pizza import make_pizza"]
    D --> E["make_pizza()"]
    A --> F["aliases"]
    F --> G["mp() / p.make_pizza()"]
~~~
