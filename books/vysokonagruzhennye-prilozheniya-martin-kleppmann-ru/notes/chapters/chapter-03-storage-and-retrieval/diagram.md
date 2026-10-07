# Диаграмма главы 3 — storage engine decision flow

~~~mermaid
flowchart TD
    A["Representative workload"] --> B{"OLTP или OLAP?"}

    B -- "OLTP: many small indexed reads/writes" --> O1["Определить key/range access"]
    O1 --> O2{"Основная storage philosophy?"}

    O2 -- "Append / immutable segments" --> L1["Log-structured"]
    L1 --> L2["WAL → MemTable → SSTable"]
    L2 --> L3["Background merge / compaction"]
    L3 --> L4["Bloom filter для absent-key reads"]
    L4 --> L5["Benchmark read/write workload"]

    O2 -- "Page-oriented" --> T1["B-tree"]
    T1 --> T2["Fixed-size pages"]
    T2 --> T3["In-place page updates / splits"]
    T3 --> T4["WAL + latches"]
    T4 --> L5

    L5 --> O3{"Acceptance достигнут?"}
    O3 -- "Нет" --> O1
    O3 -- "Да" --> K["Keep configuration"]

    B -- "OLAP: fewer heavy scans/aggregates" --> A1["Изолировать analytical workload"]
    A1 --> A2["ETL → data warehouse"]
    A2 --> A3["Star / snowflake schema"]
    A3 --> A4["Column-oriented storage"]
    A4 --> A5["Compression + sort order + vectorized processing"]
    A5 --> A6["Materialized views / cubes для частых aggregates"]
    A6 --> A7["Measure scan volume / query time"]
    A7 --> A8{"Acceptance достигнут?"}
    A8 -- "Нет" --> A3
    A8 -- "Да" --> K
~~~

## Write/read trade-off

~~~mermaid
flowchart LR
    W["Добавить index"] --> R["Чтение быстрее"]
    W --> C["Запись дороже"]
    C --> M["Measure real workload"]
    R --> M
    M --> D{"Benefit > overhead?"}
    D -- "Да" --> KEEP["Keep index"]
    D -- "Нет" --> DROP["Remove / revise"]
~~~

## Смысл

Глава связывает внутреннее устройство storage engine с workload. Для OLTP центральны index lookup, write path и recovery; для OLAP — scan bandwidth, column selection, compression и precomputed aggregates.
