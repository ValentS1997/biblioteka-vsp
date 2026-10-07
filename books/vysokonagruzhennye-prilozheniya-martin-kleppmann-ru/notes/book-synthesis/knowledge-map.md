# Knowledge map — «Высоконагруженные приложения»

## Concept flow

~~~mermaid
flowchart TD
    A["Workload + SLO + invariants"] --> B["Data model / query model"]
    B --> C["Storage engine / indexes"]
    C --> D["Encoding / schema evolution"]

    D --> E["Replication"]
    E --> F["Partitioning"]
    F --> G["Transactions / isolation"]
    G --> H["Network + time uncertainty"]
    H --> I["Ordering / consistency / consensus"]

    I --> J["Batch processing"]
    J --> K["Stream processing"]
    K --> L["Derived state / data integration"]
    L --> M["Integrity / audit / responsibility"]

    M --> A
~~~

The book is circular rather than linear: later chapters feed back into the first chapter's reliability, scalability and maintainability goals.

## Part I — local data-system mechanics

~~~mermaid
flowchart LR
    W["Workload"] --> DM["Data model"]
    DM --> SE["Storage engine"]
    SE --> IX["Indexes / OLTP / OLAP"]
    IX --> EN["Encoding / schema contract"]
    EN --> EV["Evolvability"]
~~~

Operational reading:

- Query pattern chooses the useful data model.
- Storage/index choice converts query requirements into I/O/write-amplification trade-offs.
- Encoding and compatibility determine whether deployments can be staged safely.

## Part II — distributed state

~~~mermaid
flowchart TD
    R["Replication"] --> L["Lag / stale reads / failover"]
    L --> P["Partitioning / skew / routing"]
    P --> T["Transactions / isolation"]
    T --> U["Network / clock / pause uncertainty"]
    U --> O["Ordering / linearizability / causality"]
    O --> C["Consensus / quorum / epochs"]
~~~

Operational reading:

- Replication gives availability and locality but creates multiple versions of state.
- Partitioning distributes load but creates placement/routing/rebalance problems.
- Transactions protect invariants within a concurrency model.
- Network/time uncertainty prevents a node from knowing global truth by itself.
- Consensus is the expensive mechanism used only where one shared decision is required.

## Part III — derived state

~~~mermaid
flowchart LR
    S["Authoritative state / event history"] --> B["Batch replay"]
    S --> ST["Stream changes"]
    B --> D["Derived views"]
    ST --> D
    D --> R["Rebuild / migrate / audit"]
    R --> S
~~~

Operational reading:

- Batch is bounded replay.
- Stream processing is continuous replay with offsets/time/state.
- Derived state becomes safer when it is replaceable.
- Data integration becomes an explicit graph instead of ad hoc dual writes.

## Cross-chapter dependency map

| Concept | Introduced/refined | Depends on |
|---|---|---|
| Reliability / operability | ch. 1 | failure observation, recovery |
| Workload-based design | ch. 1–3 | metrics, query patterns |
| Evolvability | ch. 1, 4, 12 | compatibility, replay |
| Replication lag | ch. 5 | async propagation |
| Hot spots / skew | ch. 6, 10, 11 | partition keys and workload |
| Invariants | ch. 7, 9, 12 | isolation/coordination |
| Partial failure | ch. 8 | network/time uncertainty |
| Fencing | ch. 8–9 | epochs/monotonic ordering |
| Causality | ch. 5, 8, 9, 11 | event ordering |
| Consensus | ch. 9 | quorum, epochs, failure model |
| Replay | ch. 10–12 | immutable/logged input |
| Idempotence / dedup | ch. 10–12 | retry/replay |
| Derived state | ch. 10–12 | source of truth + transformations |
| Integrity / audit | ch. 12 | provenance + deterministic derivation |

## Mental models worth retaining

### State has an owner

For every fact, identify the authoritative source. Caches, indexes, warehouses and projections should normally be treated as derived state.

### Order is scoped

Ask: order of what, observed by whom, and under which partition/failure assumptions?

Per-partition order, causal order, total order and wall-clock order are different guarantees.

### Retry changes semantics

Retry is safe only if the operation is idempotent/deduplicated or its duplicate effects are acceptable.

### Availability is not binary correctness

A system can be available but stale, divergent or semantically incorrect. Safety and liveness should be evaluated separately.

### Recovery should be designed before failure

Snapshot positions, logs, checkpoints, offsets, fencing tokens and replay paths are part of normal architecture, not emergency additions.
