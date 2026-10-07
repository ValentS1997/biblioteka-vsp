# Диаграмма главы 2 — выбор модели данных и языка запросов

~~~mermaid
flowchart TD
    A["Предметная область"] --> B["Определить shape данных и relationships"]
    B --> C{"Какая структура доминирует?"}
    C -- "Автономные документы / one-to-many tree" --> D["Document model"]
    C -- "Regular entities + joins" --> R["Relational model"]
    C -- "Dense / evolving many-to-many" --> G["Graph model"]

    D --> D1["Проверить locality: читается ли документ целиком?"]
    D1 --> D2["Проверить joins и application-side reference resolution"]
    D2 --> S["Выбрать schema policy"]

    R --> R1["Нормализация + IDs"]
    R1 --> R2["Joins / declarative SQL"]
    R2 --> S

    G --> G1["Vertices + edges + labels"]
    G1 --> G2["Traversal / pattern matching"]
    G2 --> G3["Cypher / SPARQL / Datalog"]
    G3 --> S

    S --> S1{"Schema-on-write или schema-on-read?"}
    S1 --> Q["Определить query style"]

    Q --> Q1{"Можно описать результат декларативно?"}
    Q1 -- "Да" --> Q2["Declarative query"]
    Q2 --> Q3["Optimizer выбирает execution plan / parallelism"]
    Q1 -- "Нужен procedural control" --> Q4["Imperative / MapReduce-style logic"]
    Q4 --> Q5["Больше explicit mechanics и constraints"]

    Q3 --> V["Проверить representative queries"]
    Q5 --> V
    V --> P{"Одна модель подходит всем компонентам?"}
    P -- "Нет" --> PP["Polyglot persistence"]
    P -- "Да" --> K["Keep model"]
~~~

## Кардинальность и естественность модели

~~~mermaid
flowchart LR
    O["one-to-many"] --> OD["Document tree natural"]
    M["many-to-one / many-to-many"] --> MR["Relational joins natural"]
    X["complex many-to-many / variable traversal"] --> GX["Graph model natural"]
~~~

## Смысл

Глава показывает, что data model переносит сложность между storage, query language и application code. Хорошая модель — та, где частые relationships и queries выражаются естественно, а optimizer получает достаточную свободу выполнения.
