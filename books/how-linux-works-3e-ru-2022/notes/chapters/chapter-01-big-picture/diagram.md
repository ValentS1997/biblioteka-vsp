# Диаграмма: общая картина Linux по главе 1

~~~mermaid
flowchart TB
    A["Пользователь"] --> B["User space"]
    B --> C["System calls"]
    C --> D["Kernel"]
    D --> E["Hardware"]
    D --> P["Process management"]
    D --> M["Memory management"]
    D --> R["Device drivers"]
    D --> S["System calls and support"]
~~~

## Смысл

Глава задаёт базовую модель: пользовательские процессы работают в user space, ядро находится между ними и оборудованием, а основные обязанности ядра относятся к процессам, памяти, драйверам устройств и системным вызовам.

~~~mermaid
flowchart LR
    S["Shell"] --> F["fork()"]
    F --> C["Child process"]
    C --> X["exec(ls)"]
    X --> L["ls"]
~~~

Запуск <code>ls</code> используется в главе как пример взаимодействия процесса с ядром. Диагностические ветви из других глав не добавлялись.
