# Диаграмма: координированная пакетная обработка

~~~mermaid
flowchart TD
    IN["Input dataset"] --> SH["Sharder"]
    SH --> A["Shard A"]
    SH --> B["Shard B"]
    SH --> C["Shard C"]

    A --> J["Join barrier"]
    B --> J
    C --> J

    J --> CP["Copier"]
    CP --> DEL["Delete originals"]
    CP --> REC["Recognition pipeline"]

    REC --> MW["Multi-Worker"]
    MW --> TYPE["Vehicle type/location"]
    MW --> COLOR["Color detection"]

    TYPE --> R["Reduce"]
    COLOR --> R
    R --> OUT["Global aggregate"]

    A --> RP["Partial results"]
    B --> RP
    C --> RP
    RP --> RED["Incremental Reduce"]
    RED --> OUT2["Single aggregate value"]
~~~

## Coordination semantics

~~~text
Merger → interleave/combine streams
Join   → wait for complete upstream set
Reduce → incrementally aggregate partial outputs
~~~

## Safety point

Destructive cleanup should happen only after the Join barrier confirms all prerequisite processing completed.
