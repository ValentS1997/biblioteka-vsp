# Chapter 2 conceptual / diagnostic flow

```mermaid
flowchart TD
    P["Process<br/>resource container + address space"] --> T["Thread(s)<br/>execution streams"]
    T --> U["User-level threads"]
    T --> K["Kernel-level threads"]
    T --> H["Hybrid / scheduler activations"]

    P --> ST["Process state"]
    ST --> RUN["Running"]
    ST --> RDY["Ready"]
    ST --> BLK["Blocked"]
    RUN -->|"scheduler preemption"| RDY
    RDY -->|"selected"| RUN
    RUN -->|"wait / blocking I/O"| BLK
    BLK -->|"event completes"| RDY

    T --> SH["Shared data / resources"]
    SH --> RACE["Race condition?"]
    RACE -->|"yes"| CS["Define critical section"]
    CS --> SYNC["Choose synchronization"]
    SYNC --> SEM["Semaphore"]
    SYNC --> MUT["Mutex + condition"]
    SYNC --> MON["Monitor"]
    SYNC --> MSG["send / receive"]
    SYNC --> BAR["Barrier"]
    SYNC --> RCU["RCU for suitable read-mostly case"]

    RDY --> SCH["Scheduler"]
    SCH --> ENV{"Environment"}
    ENV --> BATCH["Batch<br/>throughput / turnaround"]
    ENV --> INT["Interactive<br/>response"]
    ENV --> RT["Real-time<br/>deadlines"]
    BATCH --> ALG["FCFS · SJF · shortest remaining"]
    INT --> ALG2["Round-robin · priority · multilevel<br/>guaranteed · lottery · fair-share"]
    RT --> TEST["Schedulability<br/>sum(Ci/Pi) ≤ 1"]

    SYNC --> CHECK["Verify invariants<br/>no race · no lost wakeup<br/>no deadlock/starvation"]
    SCH --> CHECK
```

## Operational reading

```text
not progressing
  ├─ blocked? → identify awaited event
  ├─ ready?   → inspect scheduling/fairness
  ├─ running? → useful work or spin?
  └─ shared state? → race / lock / ordering / deadlock analysis
```
