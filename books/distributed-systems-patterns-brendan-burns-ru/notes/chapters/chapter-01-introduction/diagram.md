# Диаграмма: зачем распределенным системам паттерны

~~~mermaid
flowchart TD
    A["Современные приложения<br/>always-on + API + быстрый рост"] --> B["Распределенные системы"]
    B --> C["Потенциальные преимущества<br/>надежность / масштабирование"]
    B --> D["Цена<br/>сложнее проектировать, строить, отлаживать"]

    D --> E["Нужны инструменты, практики и паттерны"]

    H1["Специализированные машины"] --> H2["General-purpose computers"]
    H2 --> H3["Time-sharing"]
    H3 --> H4["Networks / client-server"]
    H4 --> H5["Internet + data centers"]
    H5 --> B

    P1["Формализация алгоритмов"] --> P2["Общие переносимые идеи"]
    P2 --> P3["OOP design patterns"]
    P3 --> P4["Reusable libraries"]
    P4 --> E

    O1["Open source"] --> O2["Collective development"]
    O2 --> E

    T1["Containers + images + orchestrators"] --> T2["Standardized building blocks"]
    T2 --> E

    E --> F["Generalized architecture pattern"]

    F --> V1["Учиться на чужом опыте"]
    F --> V2["Общий язык"]
    F --> V3["Reusable components"]

    V3 --> R["Реализовать один раз<br/>использовать многократно"]
    R --> Q["Больше использования<br/>выше шанс обнаружить defects"]

    F --> G["Не vendor recipe<br/>не product-specific install guide"]
~~~

## Логика

Глава строит аргумент от роста требований к современным приложениям к росту сложности распределенных систем. Исторические примеры алгоритмов, OOP patterns и open source показывают, как formalization и reuse уже уменьшали сложность в других областях разработки.

Контейнеры и оркестраторы выступают в chapter framing как технологические строительные блоки, на которых можно оформлять reusable distributed-system components.

Три результата pattern approach:
1. использовать накопленный опыт;
2. говорить на общем архитектурном языке;
3. создавать общие повторно используемые компоненты.
