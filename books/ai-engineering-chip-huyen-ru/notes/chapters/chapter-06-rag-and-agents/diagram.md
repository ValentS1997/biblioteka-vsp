# Диаграммы главы 6

## RAG pipeline

~~~mermaid
flowchart LR
    DATA["External memory / corpus"] --> CHUNK["Chunk + metadata"]
    CHUNK --> INDEX["Index"]
    Q["User query"] --> REWRITE["Optional query rewrite"]
    REWRITE --> RET["Retrieve candidates"]
    RET --> RERANK["Optional rerank / fusion"]
    RERANK --> CTX["Relevant context"]
    CTX --> GEN["Generative model"]
    Q --> GEN
    GEN --> ANSWER["Answer"]
    RET --> EVAL["Retrieval evaluation"]
    ANSWER --> E2E["End-to-end evaluation"]
~~~

## Retrieval optimization

~~~mermaid
flowchart TD
    BASE["Lexical baseline"] --> GOOD{"Meets quality?"}
    GOOD -- "yes" --> KEEP["Keep simpler retrieval"]
    GOOD -- "no" --> EMB["Add embedding retrieval"]
    EMB --> HYB["Hybrid / reranking"]
    HYB --> CHUNK["Tune chunk size + overlap"]
    CHUNK --> QR["Query rewrite / contextual retrieval"]
    QR --> MEASURE["Remeasure precision/recall + quality + cost/latency"]
~~~

## Agent execution loop

~~~mermaid
flowchart TD
    TASK["Goal + constraints"] --> PLAN["Generate plan"]
    PLAN --> CHECK["Reflect / validate"]
    CHECK -- "bad plan" --> PLAN
    CHECK -- "valid" --> TOOL["Select tool + parameters"]
    TOOL --> GATE{"Read or write?"}
    GATE -- "read" --> EXEC["Execute"]
    GATE -- "write" --> AUTH["Authorization / safety gate"]
    AUTH --> EXEC
    EXEC --> OBS["Observe tool output"]
    OBS --> DONE{"Goal + constraints satisfied?"}
    DONE -- "no" --> PLAN
    DONE -- "yes" --> RESULT["Complete"]
~~~

## Failure localization

~~~mermaid
flowchart TD
    FAIL["Agent failure"] --> PLANERR{"Plan/tool call valid?"}
    PLANERR -- "no" --> P["Planning error:<br/>invalid tool/params/value"]
    PLANERR -- "yes" --> TOOLERR{"Tool output correct?"}
    TOOLERR -- "no" --> T["Tool failure"]
    TOOLERR -- "yes" --> GOAL{"Goal/constraints met?"}
    GOAL -- "no" --> G["Goal/reflection failure"]
    GOAL -- "yes" --> EFF{"Cost/time/steps acceptable?"}
    EFF -- "no" --> E["Efficiency failure"]
    EFF -- "yes" --> OK["Success"]
~~~

## Memory hierarchy

~~~mermaid
flowchart LR
    INT["Internal knowledge<br/>model weights"] --> TASK["Current task"]
    SHORT["Short-term memory<br/>model context"] --> TASK
    LONG["Long-term memory<br/>external store"] --> RET["Memory retrieval"]
    RET --> SHORT
    SHORT --> MOVE["Evict / summarize / merge"]
    MOVE --> LONG
~~~
