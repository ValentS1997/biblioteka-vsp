# Диаграмма главы 4 — compatibility и движение данных

~~~mermaid
flowchart TD
    A["Schema / API / message change"] --> B["Определить writer и reader versions"]
    B --> C["Backward compatibility: new reader ← old data"]
    B --> D["Forward compatibility: old reader ← new data"]
    C --> E{"Обе стороны совместимы?"}
    D --> E
    E -- "Нет" --> F["Изменить schema/API delta"]
    F --> B
    E -- "Да" --> G["Controlled rolling/staged rollout"]
    G --> H["Old/new versions сосуществуют"]
    H --> I{"Канал данных?"}

    I --> DB["Database"]
    DB --> DB1["Сохранять unknown fields при read-modify-write"]

    I --> RPC["REST / RPC"]
    RPC --> RPC1["Учитывать timeout, retry, duplicate execution"]

    I --> MSG["Async messaging"]
    MSG --> MSG1["Producer/consumer deploy independently"]

    DB1 --> V["Verify compatibility behavior"]
    RPC1 --> V
    MSG1 --> V

    V --> K{"Acceptance?"}
    K -- "Да" --> KEEP["Keep rollout"]
    K -- "Нет" --> RB["Stop rollout / rollback version"]
~~~

## Schema evolution

~~~mermaid
flowchart LR
    T["Thrift / Protobuf"] --> T1["Stable field tags"]
    T1 --> T2["New fields: new tags"]
    T2 --> T3["Do not reuse removed tags"]

    A["Avro"] --> A1["Writer schema"]
    A1 --> A2["Reader schema"]
    A2 --> A3["Schema resolution + defaults"]
~~~

## Смысл

Глава связывает evolvability с возможностью независимо менять writers/readers. Формат считается пригодным не только если он компактен, а если его правила evolution позволяют old/new code безопасно сосуществовать.
