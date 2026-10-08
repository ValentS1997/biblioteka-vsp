# Concept map всей книги

## Problem → pattern map

~~~mermaid
flowchart TD
    A["Distributed-system problem"] --> B{"What kind of problem?"}

    B --> C["Extend application"]
    C --> C1["Sidecar"]
    C --> C2["Ambassador"]
    C --> C3["Adapter"]

    B --> D["Scale / availability"]
    D --> D1["Replicated Service"]
    D --> D2["Sharding"]
    D --> D3["Scatter/Gather"]

    B --> E["Event / authority"]
    E --> E1["FaaS / Event Pipeline"]
    E --> E2["Owner Election"]

    B --> F["Batch processing"]
    F --> F1["Task Queue"]
    F --> F2["Copier"]
    F --> F3["Filter"]
    F --> F4["Splitter"]
    F --> F5["Sharder"]
    F --> F6["Merger"]
    F --> F7["Join"]
    F --> F8["Reduce"]
    F --> F9["Multi-Worker"]
~~~

## Decision distinctions worth preserving

### Sidecar / Ambassador / Adapter

~~~text
need extra capability beside app?
→ Sidecar

need external communication proxy/boundary?
→ Ambassador

need native interface converted to standard interface?
→ Adapter
~~~

### Replication / sharding / Scatter-Gather

~~~text
need more copies of same responsibility?
→ Replication

need partitioned data/responsibility?
→ Sharding

need one expensive request parallelized?
→ Scatter/Gather
~~~

### Merger / Join / Reduce

~~~text
need streams combined?
→ Merger

need every required result before proceeding?
→ Join

need partial results aggregated incrementally?
→ Reduce
~~~

## Failure-model overlay

~~~mermaid
flowchart LR
    R["Replication"] --> RF["readiness / replica failure"]
    S["Sharding"] --> SF["shard loss / remapping / hot shard"]
    SG["Scatter/Gather"] --> SGF["straggler / fan-out failure amplification"]
    OE["Owner Election"] --> OEF["lease expiry / stale owner / delayed request"]
    Q["Task Queue"] --> QF["backlog / insufficient service rate"]
    J["Join"] --> JF["slow or missing branch blocks barrier"]
~~~

## Reuse hierarchy

Книга постепенно moves reuse upward:

~~~text
utility container
→ reusable network/interface component
→ reusable distributed-service topology
→ reusable event/queue primitive
→ reusable batch DAG primitive
→ reusable pattern ecosystem
~~~

## Minimal design-review questions

| Question | Relevant pattern area |
|---|---|
| Что должно быть reusable и отделено от application? | Sidecar / Ambassador / Adapter |
| Мы масштабируем copies, partitions или one request? | Replication / Sharding / Scatter-Gather |
| Где authoritative state/owner? | Owner Election |
| Где создаётся backlog и каков service rate? | Task Queue |
| Какая semantics у branch/fan-in? | Copier / Filter / Splitter / Merger / Join / Reduce |
| Какой slow/failure path определяет end-to-end behavior? | Все distributed patterns |

## Book-level mental model

~~~text
DECOMPOSE responsibility
→ STANDARDIZE interface
→ DISTRIBUTE work/state deliberately
→ COORDINATE only where semantics requires
→ OBSERVE failure/capacity consequences
→ REUSE the resulting pattern implementation
~~~
