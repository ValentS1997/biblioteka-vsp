# Диаграмма — ввод данных и циклы while

## Input → преобразование → решение

~~~mermaid
flowchart LR
    A["input(prompt)"] --> B["string"]
    B --> C{"Нужно числовое сравнение?"}
    C -- "Да" --> D["int(value)"]
    D --> E["числовая проверка / %"]
    C -- "Нет" --> F["работа со строкой"]
~~~

## Управление while

~~~mermaid
flowchart TD
    A["Начальное состояние"] --> B{"Условие while True?"}
    B -- "Да" --> C["Выполнить тело"]
    C --> D{"Exit event?"}
    D -- "flag" --> E["active = False"]
    D -- "break" --> F["break"]
    D -- "continue" --> G["следующая итерация"]
    D -- "нет" --> H["изменить управляющее состояние"]
    H --> B
    G --> B
    E --> I["Завершить после проверки условия"]
    F --> J["Немедленно выйти"]
    B -- "Нет" --> J
~~~

## Изменение коллекций

~~~mermaid
flowchart LR
    A["unconfirmed_users"] --> B["pop()"]
    B --> C["current_user"]
    C --> D["append()"]
    D --> E["confirmed_users"]

    F["pets with repeated cat"] --> G["while 'cat' in pets"]
    G --> H["remove('cat')"]
    H --> G
~~~
