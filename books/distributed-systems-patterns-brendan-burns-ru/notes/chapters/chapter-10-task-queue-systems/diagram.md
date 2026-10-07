# Диаграмма: система на основе очереди задач

~~~mermaid
flowchart TD
    SRC["Application-specific source container"] --> API["Versioned source API"]
    API --> QM["Generic queue manager"]
    QM --> JOBS["Kubernetes Jobs"]
    JOBS --> W["One-shot worker containers"]
    W --> DONE["Completion state"]

    QM --> DIFF["Compare source items vs existing Jobs"]
    DIFF --> PENDING["Pending items"]
    PENDING --> JOBS

    QM --> SCALE["Concurrency control"]
    SCALE --> ARR["Measure arrival interval"]
    SCALE --> DUR["Measure processing duration"]
    ARR --> CAP["Effective service rate"]
    DUR --> CAP
    CAP --> DECIDE["Scale worker parallelism"]

    W --> MW["Multi-Worker facade"]
    MW --> W1["Reusable worker A"]
    MW --> W2["Reusable worker B"]
    MW --> W3["Reusable worker C"]
~~~

## Core reconciliation loop

~~~text
source items
+ existing Jobs
→ pending items
→ create worker Jobs
→ observe completion
→ repeat
~~~

## Stability rule from chapter

~~~text
average processing time / parallelism
<
average inter-arrival interval
~~~

The chapter treats this as an average-rate scaling model, not a complete queueing-theory model.
