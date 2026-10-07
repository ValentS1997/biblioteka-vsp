# Диаграмма главы 1 — проектирование информационной системы

~~~mermaid
flowchart TD
    A["Сервис / информационная система"] --> B["Определить требования и operational context"]
    B --> C{"Какая ось анализируется?"}

    C --> R1["Reliability"]
    R1 --> R2["Различить fault компонента и failure сервиса"]
    R2 --> R3["Аппаратные / программные / человеческие причины"]
    R3 --> R4["Fault tolerance, isolation, testing, monitoring, recovery"]
    R4 --> R5{"Пользовательский сервис сохраняется?"}
    R5 -- "Нет" --> R6["Локализовать механизм перехода fault → failure"]
    R5 -- "Да" --> Z["Acceptance"]

    C --> S1["Scalability"]
    S1 --> S2["Определить load parameters"]
    S2 --> S3["Измерить throughput / response time / percentiles"]
    S3 --> S4["Найти bottleneck и tail latency"]
    S4 --> S5["Vertical / horizontal / hybrid scaling"]
    S5 --> S6["Повторить тот же load test"]
    S6 --> S7{"Performance удержана?"}
    S7 -- "Нет" --> S2
    S7 -- "Да" --> Z

    C --> M1["Maintainability"]
    M1 --> M2["Operability"]
    M1 --> M3["Simplicity"]
    M1 --> M4["Evolvability"]
    M2 --> M5["Monitoring, automation, predictable operations"]
    M3 --> M6["Уменьшить incidental complexity, использовать abstractions"]
    M4 --> M7["Упростить безопасные изменения требований"]
    M5 --> M8{"Система понятна и управляемa?"}
    M6 --> M8
    M7 --> M8
    M8 -- "Нет" --> M1
    M8 -- "Да" --> Z

    Z --> K["Оставить изменение"]
    Z --> L["При провале acceptance: rollback / ограничить blast radius"]
~~~

## Load/performance loop

~~~mermaid
flowchart LR
    L1["Load parameter"] --> L2["Measurement"]
    L2 --> L3["p50 + tail percentiles / throughput"]
    L3 --> L4["Architecture decision"]
    L4 --> L5["Controlled change"]
    L5 --> L6["Same measurement"]
    L6 --> L7{"Цель достигнута?"}
    L7 -- "Да" --> L8["Keep"]
    L7 -- "Нет" --> L9["Rollback / revise assumptions"]
    L9 --> L1
~~~

## Смысл

Глава связывает архитектурное решение не с модным паттерном, а с измеримым свойством системы. Reliability проверяется через поведение при fault, scalability — через конкретный профиль нагрузки и распределение latency, maintainability — через operability, simplicity и evolvability.
