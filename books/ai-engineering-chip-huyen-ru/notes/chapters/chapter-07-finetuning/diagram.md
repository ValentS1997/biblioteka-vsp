# Диаграммы главы 7

## Нужно ли дообучение

~~~mermaid
flowchart TD
    FAIL["Observed failure"] --> EVAL["Define evaluation criteria / baseline"]
    EVAL --> PROMPT["Prompt + few-shot experiments"]
    PROMPT --> TYPE{"Failure type?"}
    TYPE -- "missing / stale information" --> RAG["Add RAG / data access"]
    RAG --> REVAL["Re-evaluate"]
    REVAL --> STILL{"Failure remains?"}
    STILL -- "information" --> RAG2["Improve retrieval"]
    STILL -- "behavior / format / safety" --> FT["Consider finetuning"]
    TYPE -- "behavior / format / safety" --> FT
    FT --> COMB["Optionally combine RAG + finetuning"]
    COMB --> FINAL["Evaluate quality + cost + latency + regressions"]
~~~

## Memory pressure

~~~mermaid
flowchart TD
    TRAIN["Training memory"] --> W["Model weights"]
    TRAIN --> A["Activations"]
    TRAIN --> G["Gradients"]
    TRAIN --> O["Optimizer states"]
    LIMIT{"Does it fit?"}
    W --> LIMIT
    A --> LIMIT
    G --> LIMIT
    O --> LIMIT
    LIMIT -- "no" --> PEFT["Reduce trainable params<br/>PEFT / LoRA"]
    LIMIT -- "no" --> Q["Reduce bits<br/>quantization / mixed precision"]
    LIMIT -- "no" --> CKPT["Reduce activation storage<br/>gradient checkpointing"]
    LIMIT -- "no" --> OFF["Offload where supported"]
    PEFT --> MEASURE["Remeasure memory + quality + time"]
    Q --> MEASURE
    CKPT --> MEASURE
    OFF --> MEASURE
~~~

## LoRA

~~~mermaid
flowchart LR
    W["Frozen W"] --> ADD["W' = W + (α/r)·A·B"]
    A["Trainable A"] --> ADD
    B["Trainable B"] --> ADD
    ADD --> TRAIN["Train A/B only"]
    TRAIN --> MERGE["Optional merge into base weights"]
    MERGE --> EVAL["Evaluate adapted model"]
~~~

## Finetuning experiment strategy

~~~mermaid
flowchart TD
    CODE["Check code on cheap/fast model"] --> DATA["Validate data on mid-level model"]
    DATA --> STRONG["Test ceiling on strongest affordable model"]
    STRONG --> COMPARE["Compare models/methods"]
    COMPARE --> PICK["Choose cost/performance point"]
    PICK --> HP["Tune LR · batch · epochs · prompt-loss weight"]
    HP --> REG["Regression + validation checks"]
~~~
