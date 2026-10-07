# Диаграмма главы 6 — partitioning decision flow

~~~mermaid
flowchart TD
    A["Dataset / request load no longer fits one node"] --> B["Measure key distribution + request distribution"]
    B --> C{"Primary access pattern?"}

    C -- "Range locality matters" --> R1["Range partitioning"]
    R1 --> R2["Choose boundaries from data distribution"]
    R2 --> R3{"Sequential/hot range?"}
    R3 -- "Да" --> R4["Revise key: add higher-cardinality prefix / avoid time-only first key"]
    R3 -- "Нет" --> I["Check secondary indexes"]

    C -- "Uniform point-key distribution matters" --> H1["Hash partitioning"]
    H1 --> H2["Map hash ranges to partitions"]
    H2 --> H3["Lose natural range locality"]
    H3 --> I

    C -- "Need both" --> C1["Composite key"]
    C1 --> C2["First part → partition; rest → sort within partition"]
    C2 --> I

    I --> I1{"Secondary index strategy?"}
    I1 -- "Local / document-partitioned" --> I2["Cheap local write"]
    I2 --> I3["Read may scatter/gather all partitions"]
    I1 -- "Global / term-partitioned" --> I4["Read targeted by term"]
    I4 --> I5["Write touches multiple index partitions"]
    I5 --> I6["Possible asynchronous visibility"]

    I3 --> RB["Rebalancing"]
    I6 --> RB
    RB --> RB1{"Partition model?"}
    RB1 --> F["Fixed partition count"]
    RB1 --> D["Dynamic split/merge"]
    RB1 --> N["Partitions proportional to nodes"]

    F --> RT["Routing metadata"]
    D --> RT
    N --> RT
    RT --> Q{"Routing model?"}
    Q --> Q1["Any node + forwarding"]
    Q --> Q2["Dedicated routing tier"]
    Q --> Q3["Partition-aware client"]

    Q1 --> V["Verify balance, availability and correct routing"]
    Q2 --> V
    Q3 --> V
~~~

## Hot spot diagnostic

~~~mermaid
flowchart LR
    O["Observed overloaded partition"] --> D{"Data or request skew?"}
    D -- "Data skew" --> K["Revisit partition key / boundaries"]
    D -- "Hot key" --> S["Application-side key spreading"]
    S --> M["Reads merge derived keys"]
    K --> V["Remeasure distribution"]
    M --> V
~~~

## Смысл

Partition key одновременно определяет placement, locality и routing cost. Rebalancing должен изменять placement с минимальным data movement и без остановки reads/writes.
