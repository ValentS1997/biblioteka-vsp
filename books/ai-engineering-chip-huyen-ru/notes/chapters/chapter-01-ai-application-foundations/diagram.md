# Диаграммы главы 1

## Как возникает AI-инженерия

~~~mermaid
flowchart LR
    LM["Языковые модели"] --> LLM["Большие языковые модели"]
    LLM --> FM["Базовые модели<br/>больше модальностей"]
    FM --> ACCESS["Доступные модели<br/>API / model-as-a-service"]
    ACCESS --> AIE["AI-инженерия<br/>приложения на готовых моделях"]
~~~

Глава связывает рост AI-инженерии с многоцелевыми возможностями моделей, ростом инвестиций и снижением входного барьера.

## Логика планирования приложения

~~~mermaid
flowchart TD
    IDEA["Идея AI-приложения"] --> WHY{"Есть веская причина?"}
    WHY -- "нет / неясно" --> RESEARCH["Исследовать влияние AI<br/>или не строить продукт"]
    WHY -- "да" --> BUY{"Build or buy?"}
    BUY --> ROLE["Определить роль AI<br/>и роль человека"]
    ROLE --> METRICS["Задать бизнес-метрики<br/>и порог полезности"]
    METRICS --> BASE["Оценить существующие модели"]
    BASE --> VALUE{"Ресурсы до порога<br/>оправданы?"}
    VALUE -- "нет" --> REVISE["Пересмотреть цель<br/>или отказаться"]
    VALUE -- "да" --> APP["Собрать слой приложения"]
    APP --> MEASURE["Оценить качество<br/>latency · cost · feedback"]
    MEASURE --> ADAPT{"Нужна адаптация?"}
    ADAPT -- "промты/контекст" --> APP
    ADAPT -- "изменение весов" --> MODEL["Дообучение / model layer"]
    MODEL --> MEASURE
    ADAPT -- "нет" --> MAINT["Эксплуатация и обслуживание"]
    MAINT --> MEASURE
~~~

Rollback для продуктовых изменений глава отдельно не задаёт: `[Needs confirmation]`.

## Три уровня стека AI

~~~mermaid
flowchart TB
    APP["Application development<br/>evaluation · prompting/context · interface"]
    MODEL["Model development<br/>training/fine-tuning · data · inference optimization"]
    INFRA["Infrastructure<br/>serving · data · compute · monitoring"]
    APP --> MODEL
    MODEL --> INFRA
~~~

Глава рекомендует при разработке приложения начинать с верхнего уровня и спускаться ниже по мере необходимости.
