# Диаграмма главы 5 — replication decision flow

~~~mermaid
flowchart TD
    A["Replication requirement"] --> B{"Какая модель writes?"}

    B -- "Один writer/leader" --> S1["Single-leader"]
    S1 --> S2["Sync или async followers"]
    S2 --> S3["Monitor replication lag"]
    S3 --> S4["Follower recovery / leader failover"]
    S4 --> S5{"Какие read guarantees нужны?"}
    S5 --> R1["Read-after-write"]
    S5 --> R2["Monotonic reads"]
    S5 --> R3["Consistent prefix"]

    B -- "Несколько writers" --> M1["Multi-leader"]
    M1 --> M2["Multi-DC / offline / collaborative use"]
    M2 --> M3["Detect concurrent writes"]
    M3 --> M4["Conflict resolution"]
    M4 --> M5["Check replication topology + causal order"]

    B -- "Без leader" --> L1["Leaderless"]
    L1 --> L2["Configure n / w / r"]
    L2 --> L3{"Strict or sloppy quorum?"}
    L3 -- "Strict" --> L4["Read from r, write to w"]
    L3 -- "Sloppy" --> L5["Temporary non-home nodes"]
    L5 --> L6["Hinted handoff"]
    L4 --> L7["Read repair / anti-entropy"]
    L6 --> L7
    L7 --> L8["Version metadata / siblings"]
    L8 --> L9["Merge concurrent values"]

    R1 --> V["Verify user-visible semantics"]
    R2 --> V
    R3 --> V
    M5 --> V
    L9 --> V

    V --> K{"Acceptance?"}
    K -- "Да" --> KEEP["Keep topology/config"]
    K -- "Нет" --> RB["Revise / rollback"]
~~~

## Failure and consistency loop

~~~mermaid
flowchart LR
    F["Failure / lag / partition"] --> O["Observe replica state"]
    O --> G["Check promised guarantee"]
    G --> C["Controlled routing/config change"]
    C --> T["Repeat read/write scenario"]
    T --> D{"Guarantee holds?"}
    D -- "Да" --> K["Keep"]
    D -- "Нет" --> R["Rollback / revise"]
~~~

## Смысл

Глава показывает, что topology сама по себе не определяет корректность. Нужно отдельно определить write acknowledgment, stale-read tolerance, failover behavior и conflict semantics.
