# Диаграмма главы 12 — future data-system architecture

~~~mermaid
flowchart TD
    A["Authoritative facts / user actions"] --> L["Durable event/change log"]
    L --> T1["Transformation A"]
    L --> T2["Transformation B"]
    L --> T3["Transformation C"]

    T1 --> I["Search index"]
    T2 --> C["Cache / materialized view"]
    T3 --> M["Analytics / ML model"]

    I --> U["User-facing/read systems"]
    C --> U
    M --> U

    L --> R["Replay historical events"]
    R --> N["New projection / migration candidate"]
    N --> V{"Validated?"}
    V -- "Да" --> CUT["Switch consumers"]
    V -- "Нет" --> OLD["Keep previous projection"]
~~~

## Correctness without unnecessary global coordination

~~~mermaid
flowchart TD
    Q["Operation with invariant"] --> C{"Must violation be prevented synchronously?"}
    C -- "Yes" --> K["Route conflicting requests to one coordination/partition boundary"]
    K --> S["Sequential decision / strict constraint"]
    C -- "No, compensation acceptable" --> A["Accept asynchronously"]
    A --> X["Verify constraint later"]
    X --> P["Compensate / repair if violated"]

    S --> I["Preserve integrity"]
    P --> I
~~~

## End-to-end integrity

~~~mermaid
flowchart LR
    C["Client"] -->|operation ID| S1["Service"]
    S1 -->|same ID| L["Log"]
    L -->|same ID| P["Processor"]
    P -->|effect + ID| D["Derived store"]
    D --> A["Audit / reconciliation"]
    A --> V{"Integrity holds?"}
    V -- "No" --> R["Repair / rebuild from source"]
    V -- "Yes" --> K["Continue"]
~~~

## Architecture responsibility

~~~mermaid
flowchart TD
    D["Data about people"] --> P["Purpose / use"]
    P --> R["Retention / deletion"]
    P --> A["Automated decisions"]
    A --> B["Bias / discrimination risk"]
    D --> S["Surveillance / privacy risk"]
    R --> H["Human dignity / user control"]
    B --> H
    S --> H
~~~

## Смысл

Final chapter combines the whole book: specialized systems can be composed through replayable dataflows; integrity can often be preserved without coordinating everything synchronously; and data architecture must include auditability and responsibility for human consequences.
