# Диаграмма — работа со списками

## Обработка списка

~~~mermaid
flowchart TD
    A["Список"] --> B{"Нужно обработать сколько элементов?"}
    B -- "Все" --> C["for item in items:"]
    C --> D["Indented body"]
    D --> E["Повторить для каждого элемента"]
    E --> F["Код без отступа после цикла"]
    B -- "Часть" --> G["slice: items[start:stop]"]
    G --> H["for item in slice / отдельная обработка"]
    B -- "Новая числовая коллекция" --> I["range()"]
    I --> J["list(range(...)) или comprehension"]
~~~

## Диагностика цикла

~~~mermaid
flowchart TD
    A["Цикл ведёт себя неверно"] --> B{"Есть exception?"}
    B -- "IndentationError" --> C["Проверить обязательный/лишний отступ"]
    B -- "SyntaxError expected ':'" --> D["Проверить двоеточие после for"]
    B -- "Нет, но действие повторяется неверно" --> E["Проверить область indentation"]
    C --> F["Исправить одну структурную причину"]
    D --> F
    E --> F
    F --> G["Повторить запуск и сверить вывод"]
~~~

## Копия или общее состояние

~~~mermaid
flowchart LR
    A["my_foods"] --> B["my_foods[:]"]
    B --> C["friend_foods — отдельный список"]
    A --> D["friend_foods = my_foods"]
    D --> E["Два имени → один список"]
~~~

## Кортеж

~~~mermaid
flowchart LR
    A["dimensions = (200, 50)"] --> B["Чтение / for разрешены"]
    A --> C["dimensions[0] = 250"]
    C --> D["TypeError"]
    A --> E["dimensions = (400, 100)"]
    E --> F["Новый tuple связан с переменной"]
~~~
