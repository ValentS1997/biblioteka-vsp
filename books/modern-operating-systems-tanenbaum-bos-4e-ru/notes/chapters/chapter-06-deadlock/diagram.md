# Chapter 6 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Loss of forward progress"] --> B{"Are processes blocked?"}
    B -->|yes| C{"Waiting on owned resources?"}
    B -->|no; retrying| L["Possible livelock"]
    C -->|yes| D["Build resource / wait-for graph"]
    C -->|no; waiting on messages/events| M["Communication deadlock candidate"]
    D --> E{"One instance per resource type?"}
    E -->|yes| F{"Cycle exists?"}
    F -->|yes| G["Resource deadlock"]
    F -->|no| H["Contention / not deadlocked"]
    E -->|no| I["Use E, A, C, R detection"]
    I --> J{"Any processes remain unfinishable?"}
    J -->|yes| G
    J -->|no| H

    G --> R{"Recovery"}
    R --> R1["Preempt resource"]
    R --> R2["Rollback checkpoint"]
    R --> R3["Terminate process"]

    G --> P{"Future prevention"}
    P --> P1["Break mutual exclusion"]
    P --> P2["Break hold-and-wait"]
    P --> P3["Allow preemption"]
    P --> P4["Global resource ordering"]

    A --> S{"Others progress but one waiter never served?"}
    S -->|yes| T["Starvation"]
    T --> T1["Use fair/FIFO policy"]

    A --> U{"Need avoidance?"}
    U --> V["Test resulting state for safety"]
    V --> W{"Safe completion sequence exists?"}
    W -->|yes| X["Grant request"]
    W -->|no| Y["Delay request"]
```

## Classification boundary

```text
contention: progress is delayed
deadlock: blocked dependency set cannot progress
livelock: active retries, no useful progress
starvation: system progresses, one participant may wait forever
unsafe state: no guaranteed completion sequence, but not necessarily deadlocked
```
