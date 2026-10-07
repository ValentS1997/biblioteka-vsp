# Диаграмма: событийно-ориентированная пакетная обработка

~~~mermaid
flowchart TD
    IN["Input task stream"] --> DAG["Batch DAG"]

    DAG --> C["Copier"]
    C --> C1["Branch A"]
    C --> C2["Branch B"]

    DAG --> F["Filter"]
    F --> F1["Matching items only"]

    DAG --> S["Splitter"]
    S --> S1["Subset A"]
    S --> S2["Subset B"]

    DAG --> SH["Sharder"]
    SH --> H1["Shard 1"]
    SH --> H2["Shard 2"]
    SH --> H3["Shard N"]

    DAG --> M["Merger"]
    M --> MO["Combined stream"]

    C1 --> PS["Pub/Sub topics"]
    C2 --> PS
    F1 --> PS
    S1 --> PS
    H1 --> PS

    PS --> NEXT["Downstream task queues"]
~~~

## Pattern semantics

~~~text
Copier   : duplicate
Filter   : discard non-matching
Splitter : route to one or more subsets
Sharder  : partition among equivalent shards
Merger   : combine streams
~~~

## Transport plane

Chapter moves from filesystem-based handoff to durable pub/sub topics, illustrated with Kafka.
