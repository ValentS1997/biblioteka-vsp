# Диаграмма главы 9 — consistency → ordering → consensus

~~~mermaid
flowchart TD
    A["Application invariant"] --> B{"Какой уровень coordination нужен?"}

    B -- "Replicas may converge later" --> E["Eventual consistency"]
    E --> E1["Handle stale/conflicting state in application"]

    B -- "Causal dependencies must be preserved" --> C["Causal consistency"]
    C --> C1["Track happens-before / versions"]
    C1 --> C2["Concurrent events may remain unordered"]

    B -- "One-copy real-time semantics" --> L["Linearizability"]
    L --> L1["Atomic read/write/CAS"]
    L1 --> L2["Coordination cost + partition availability trade-off"]

    B -- "All nodes need same final sequence" --> T["Total-order broadcast"]
    T --> T1["Reliable delivery"]
    T --> T2["Same delivery order"]
    T1 --> X["Consensus-equivalent boundary"]
    T2 --> X

    B -- "One irreversible decision" --> X

    X --> Q["Epoch/term + quorum"]
    Q --> S["Safety even if majority lost"]
    Q --> V["Liveness when majority/recovery assumptions hold"]

    X --> U["Use cases"]
    U --> U1["Leader election"]
    U --> U2["Uniqueness / locks"]
    U --> U3["Atomic commit"]
    U --> U4["Membership / coordination"]
~~~

## Distributed atomic commit

~~~mermaid
flowchart LR
    A["Transaction across nodes"] --> P["Coordinator: PREPARE"]
    P --> R{"All participants vote YES?"}
    R -- "No" --> AB["Durable ABORT decision"]
    R -- "Yes" --> CM["Durable COMMIT decision"]
    AB --> D["Tell all participants"]
    CM --> D
    D --> F["All participants resolve same outcome"]
    P --> I["Coordinator failure after PREPARE"]
    I --> ID["Participants may remain in-doubt + hold locks"]
~~~

## Ordering relationship

~~~mermaid
flowchart LR
    CA["Causality"] --> LA["Lamport timestamps"]
    LA --> TO["Total order compatible with causality"]
    TO --> N["But order alone is not finality"]
    N --> TB["Total-order broadcast"]
    TB <--> CS["Consensus"]
    TB <--> LR["Linearizable CAS/register"]
~~~

## Смысл

Сильная consistency — не цель сама по себе. Нужно определить invariant и минимальную точку, где система обязана координироваться. Consensus требуется для единого окончательного решения; causal consistency допускает concurrency и требует меньше coordination.
