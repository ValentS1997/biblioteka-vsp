# Диаграмма главы 8 — failure and uncertainty flow

~~~mermaid
flowchart TD
    A["Remote operation"] --> B{"Response received?"}
    B -- "Да" --> C["Application-level result"]
    B -- "Нет до timeout" --> U["State is uncertain"]

    U --> U1["Request may be lost"]
    U --> U2["Remote node may be down"]
    U --> U3["Remote node may be paused/slow"]
    U --> U4["Request may be processed; response lost"]
    U --> U5["Message/response may still arrive later"]

    U1 --> D["Failure detector / retry policy"]
    U2 --> D
    U3 --> D
    U4 --> D
    U5 --> D

    D --> E["Measure latency + jitter"]
    E --> F{"Role/lock decision?"}
    F -- "Нет" --> G["Bounded retry / application semantics"]
    F -- "Да" --> Q["Quorum/coordination"]
    Q --> L["Lease / leadership"]
    L --> P["Process may pause past lease expiry"]
    P --> T["Fencing token"]
    T --> R["Protected resource rejects stale token"]

    G --> V["Fault test + verify recovery"]
    R --> V
~~~

## Clock choice

~~~mermaid
flowchart LR
    X["Need time"] --> C{"What kind?"}
    C -- "Elapsed duration / timeout" --> M["Monotonic clock"]
    C -- "Calendar timestamp" --> W["Time-of-day clock"]
    W --> N["NTP reduces skew but uncertainty remains"]
    N --> O["Do not infer causal order from timestamp alone"]
~~~

## Correctness model

~~~mermaid
flowchart TD
    M["System model"] --> T["Timing: synchronous / partially synchronous / asynchronous"]
    M --> F["Failures: crash-stop / crash-recovery / Byzantine"]
    T --> A["Algorithm assumptions"]
    F --> A
    A --> S["Safety: must never be violated"]
    A --> L["Liveness: eventually progresses under stated recovery conditions"]
    S --> P["Proof / reasoning"]
    L --> P
    P --> E["Empirical fault testing"]
~~~

## Смысл

Главная проблема — uncertainty. Timeout, local clock или мнение одного node недостаточны для вывода о глобальном состоянии. Надежность строится через явную model of failure, quorum/coordination, fencing и проверяемые safety/liveness properties.
