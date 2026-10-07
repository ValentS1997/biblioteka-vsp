# Диаграмма главы 10 — batch-processing dataflow

~~~mermaid
flowchart TD
    A["Bounded input dataset"] --> B{"Scale / execution model?"}

    B -- "Single machine" --> U["Unix pipeline"]
    U --> U1["stdin → small tool → stdout"]
    U1 --> U2["compose awk/sort/uniq/etc."]
    U2 --> V["Inspect / validate derived output"]

    B -- "Distributed batch" --> M["MapReduce + distributed filesystem"]
    M --> M1["Map input records"]
    M1 --> M2["Partition + shuffle + sort"]
    M2 --> M3["Reduce grouped keys"]
    M3 --> M4["Durable output files"]
    M4 --> V

    B -- "Multi-stage / low materialization" --> D["Dataflow engine"]
    D --> D1["Operator DAG"]
    D1 --> D2["Pipeline / repartition only where needed"]
    D2 --> D3["Memory/local-disk intermediate state"]
    D3 --> D4["Lineage/checkpoint recovery"]
    D4 --> V

    V --> C{"Correct and reproducible?"}
    C -- "Да" --> P["Publish/use derived dataset"]
    C -- "Нет" --> R["Fix code/config and rerun immutable input"]
~~~

## Join selection

~~~mermaid
flowchart TD
    J["Join two datasets"] --> S{"One input is small?"}
    S -- "Да" --> B["Broadcast hash join"]
    S -- "Нет" --> P{"Inputs already compatibly partitioned?"}
    P -- "Да" --> H["Partitioned hash join"]
    P -- "Нет" --> M["Sort-merge join via shuffle/sort"]
~~~

## Fault tolerance trade-off

~~~mermaid
flowchart LR
    MR["MapReduce"] --> A["Materialize intermediate state"]
    A --> B["More disk/network I/O"]
    A --> C["Cheap task-level restart"]

    DF["Spark / Tez / Flink"] --> D["Pipeline intermediate state"]
    D --> E["Less I/O / lower barriers"]
    D --> F["Recompute or restore checkpoint"]
    F --> G["Determinism matters"]
~~~

## Смысл

Batch processing deliberately restricts side effects and separates input from output. Это делает retries, recomputation и rollback намного безопаснее, чем в request-driven code, который меняет external state по ходу выполнения.
