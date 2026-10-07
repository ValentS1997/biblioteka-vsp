# Диаграмма главы 11 — stream-processing model

~~~mermaid
flowchart TD
    A["Unbounded event stream"] --> B{"Transport model?"}

    B -- "Task queue / async RPC" --> Q["AMQP/JMS-like broker"]
    Q --> Q1["deliver → acknowledge → remove"]
    Q1 --> O["Consumer output"]

    B -- "Replayable ordered history" --> L["Log-based broker"]
    L --> L1["Partitioned append-only log"]
    L1 --> L2["Consumer offset"]
    L2 --> L3["Replay / independent consumers"]
    L3 --> O

    O --> C{"What is produced?"}
    C -- "Derived store" --> S["DB / cache / search index"]
    C -- "Human notification" --> H["alerts / UI / email"]
    C -- "Derived stream" --> P["Stream processor"]
~~~

## Database as a stream

~~~mermaid
flowchart LR
    DB["System of record DB"] --> LOG["Replication/change log"]
    LOG --> CDC["CDC"]
    CDC --> K["Replayable event log"]
    K --> I["Search index"]
    K --> C["Cache"]
    K --> W["Warehouse/analytics"]
    K --> N["New projection"]
~~~

## Stateful processing

~~~mermaid
flowchart TD
    E["Events"] --> T["Event-time / processing-time policy"]
    T --> W{"Operator"}
    W --> W1["Window aggregation"]
    W --> J1["Stream–stream join"]
    W --> J2["Stream–table join"]
    W --> J3["Table–table join"]

    W1 --> ST["State"]
    J1 --> ST
    J2 --> ST
    J3 --> ST

    ST --> CP["Checkpoint / replicated state / replay"]
    CP --> F{"Failure?"}
    F -- "Да" --> R["Restore state + offset and replay"]
    F -- "Нет" --> OUT["Derived output"]
    R --> OUT
~~~

## Duplicate-effect control

~~~mermaid
flowchart LR
    M["Process message at offset N"] --> E["Apply external effect"]
    E --> C["Persist applied offset/dedup metadata"]
    C --> X{"Message N replayed?"}
    X -- "Да" --> S["Skip already-applied effect"]
    X -- "Нет" --> E2["Process normally"]
~~~

## Смысл

Replayable log unifies messaging, database change propagation and stream recovery. Correctness comes from aligning ordering, offsets, state snapshots and sink-side duplicate semantics.
