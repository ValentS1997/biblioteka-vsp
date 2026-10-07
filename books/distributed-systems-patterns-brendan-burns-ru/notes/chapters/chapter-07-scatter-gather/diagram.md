# Диаграмма: паттерн Scatter/Gather

~~~mermaid
flowchart TD
    C["Client request"] --> R["Root node"]

    R --> L1["Leaf 1"]
    R --> L2["Leaf 2"]
    R --> LN["Leaf N"]

    L1 --> P1["Partial result"]
    L2 --> P2["Partial result"]
    LN --> PN["Partial result"]

    P1 --> G["Gather / aggregate"]
    P2 --> G
    PN --> G
    G --> A["Combined response"]

    R --> O["Fan-out width"]
    O --> OH["Coordination overhead"]
    O --> ST["Straggler exposure"]

    ST --> TL["End-to-end tail latency"]

    L1 --> RS1["Replicated logical shard"]
    L2 --> RS2["Replicated logical shard"]
    LN --> RSN["Replicated logical shard"]

    RS1 --> REL["Failure tolerance / rolling update"]
    RS2 --> REL
    RSN --> REL
~~~

## Aggregation semantics

Replicated term-search example:
- different workers process different terms;
- root computes intersection.

Sharded corpus-search example:
- each shard evaluates the full predicate over its own data subset;
- root computes union.

## Performance rule

More leaves reduce useful work per node only until network, coordination and tail-latency costs dominate.
