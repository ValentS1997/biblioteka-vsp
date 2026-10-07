# Диаграмма главы 7 — transaction/isolation decision flow

~~~mermaid
flowchart TD
    A["Application invariant + concurrent access"] --> B{"Какая операция?"}

    B -- "Single-object read-modify-write" --> C1["Prefer atomic DB operation"]
    C1 --> V["Concurrent verification"]

    B -- "Multiple rows / decision from current state" --> C2["Identify rows/predicate used by decision"]
    C2 --> C3{"Can explicit locking safely cover it?"}
    C3 -- "Да" --> C4["SELECT ... FOR UPDATE / predicate-range lock"]
    C4 --> V
    C3 -- "Нет / complex phantom risk" --> S["Require serializable isolation"]

    B -- "Long read-only consistent view" --> M["Snapshot isolation / MVCC"]
    M --> M1["Consistent snapshot; readers do not block writers"]
    M1 --> V

    S --> S1{"Serializable implementation"}
    S1 --> SE["Actual serial execution"]
    S1 --> PL["2PL"]
    S1 --> SSI["SSI"]

    SE --> SE1["Short transactions; throughput bounded by execution thread/partition"]
    PL --> PL1["Pessimistic: blocking + deadlocks + range locks"]
    SSI --> SSI1["Optimistic: snapshot + detect serialization conflicts + abort"]

    SE1 --> V
    PL1 --> V
    SSI1 --> V

    V --> R{"Invariant preserved and performance acceptable?"}
    R -- "Да" --> K["Keep"]
    R -- "Нет" --> X["Classify anomaly / contention / retry"]
    X --> A
~~~

## Isolation anomaly map

~~~mermaid
flowchart LR
    RC["Read committed"] --> D1["blocks dirty reads/writes"]
    SI["Snapshot isolation"] --> D2["consistent snapshot / MVCC"]
    D2 --> D3["write skew still possible"]
    SER["Serializable"] --> D4["prevents dirty/read skew/lost update/write skew/phantom anomalies"]
~~~

## Retry loop

~~~mermaid
flowchart LR
    A["Transaction abort"] --> B{"Transient error?"}
    B -- "Нет" --> N["Do not blindly retry"]
    B -- "Да" --> C{"Ambiguous commit or external side effect?"}
    C -- "Да" --> D["Deduplicate / application-specific handling"]
    C -- "Нет" --> E["Bounded retry + backoff"]
    E --> F["Rerun transaction"]
~~~

## Смысл

Глава требует сначала определить invariant и конкретную race condition, а затем выбирать минимальный control. Более сильная isolation уменьшает пространство ошибок приложения, но имеет разные performance trade-offs.
