# Диаграмма: шардированные сервисы

~~~mermaid
flowchart TD
    R["Request / key"] --> K["Choose semantic sharding key"]
    K --> H["Deterministic + uniform sharding function"]
    H --> S1["Shard A"]
    H --> S2["Shard B"]
    H --> S3["Shard C"]

    S1 --> A1["Replica A1"]
    S1 --> A2["Replica A2"]
    S2 --> B1["Replica B1"]
    S3 --> C1["Replica C1"]

    R --> RT["Routing layer choice"]
    RT --> AMB["Local Ambassador / twemproxy"]
    RT --> SHR["Shared replicated shard router"]

    AMB --> H
    SHR --> H

    H --> CH["Shard-count change?"]
    CH --> ORD["Ordinary remapping<br/>large cache churn"]
    CH --> CON["Consistent hashing<br/>limit remapping"]

    S1 --> HOT["Observe per-shard load"]
    S2 --> HOT
    S3 --> HOT
    HOT --> HS["Hot shard?"]
    HS --> SCALE["Scale that shard independently"]

    CACHE["Cache dependency"] --> FAIL["Shard/cache failure"]
    FAIL --> BACK["More backend traffic / latency"]
    BACK --> TEST["Load-test with and without cache"]
~~~

## Core logic

~~~text
partition data/request space
→ choose correct semantic key
→ deterministic routing
→ replicate shard if shard loss is unacceptable
→ minimize remapping when topology changes
→ detect and scale hot shards
~~~

## Operational trade-off

Local Ambassador reduces an extra network hop but increases per-consumer deployment complexity.

Shared router centralizes routing deployment but itself must be replicated/scaled and adds another network hop.
