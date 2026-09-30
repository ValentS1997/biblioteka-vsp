# Диаграмма — первые шаги с Python

~~~mermaid
flowchart TD
    A["Определить ОС"] --> B{"Windows?"}
    B -- "Да" --> C["Запустить python"]
    B -- "Нет: macOS/Linux" --> D["Запустить python3"]
    C --> E{"Интерпретатор доступен и версия по книге >= 3.9?"}
    D --> E
    E -- "Нет" --> F["Установить/обновить Python по сценарию своей ОС"]
    E -- "Да" --> G["Проверить print(...) в >>>"]
    F --> G
    G --> H["Установить VS Code"]
    H --> I["Установить Python extension"]
    I --> J["Создать python_work/hello_world.py"]
    J --> K["print('Hello Python world!')"]
    K --> L["Run Without Debugging"]
    L --> M{"Вывод Hello Python world!?"}
    M -- "Да" --> N["Минимальная среда готова"]
    M -- "Нет" --> O["Прочитать traceback"]
    O --> P["Проверить регистр, кавычки, скобки и точность кода"]
    P --> Q{"Исправлено?"}
    Q -- "Да" --> L
    Q -- "Нет" --> R["Пересоздать hello_world.py / повторить шаги / обратиться к инструкциям"]
    R --> L
~~~

## Запуск сохранённой программы из терминала

~~~mermaid
flowchart LR
    W1["Windows"] --> W2["cd Desktop\\python_work"]
    W2 --> W3["dir"]
    W3 --> W4["python hello_world.py"]
    W4 --> O["Hello Python world!"]

    U1["macOS/Linux"] --> U2["cd Desktop/python_work/"]
    U2 --> U3["ls"]
    U3 --> U4["python3 hello_world.py"]
    U4 --> O
~~~

## Смысл

Глава не строит сложную архитектуру приложения. Она формирует проверяемую цепочку среды: обнаружить Python, настроить редактор, выполнить минимальную программу и локализовать ошибку до перехода к следующим темам.
