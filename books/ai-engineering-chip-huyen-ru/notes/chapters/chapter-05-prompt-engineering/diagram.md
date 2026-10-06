# Диаграммы главы 5

## Prompt lifecycle

~~~mermaid
flowchart TD
    GOAL["Define desired behavior"] --> BASE["Create simple prompt"]
    BASE --> PARTS["Task description + examples + input + context"]
    PARTS --> TEMPLATE["Serialize with model-specific chat template"]
    TEMPLATE --> INSPECT["Inspect final prompt"]
    INSPECT --> EVAL["Run fixed evaluation set"]
    EVAL --> METRICS["Quality + schema + cost + latency"]
    METRICS --> OK{"Acceptable?"}
    OK -- "no" --> ITER["Change one prompt/workflow variable"]
    ITER --> EVAL
    OK -- "yes" --> VERSION["Version prompt + metadata"]
    VERSION --> PROD["Deploy / monitor"]
    PROD --> EVAL
~~~

## Когда разбивать prompt

~~~mermaid
flowchart TD
    TASK["Complex multi-step task"] --> OBS{"Need localization / different models / parallel steps?"}
    OBS -- "yes" --> SPLIT["Split into sub-prompts"]
    SPLIT --> MID["Evaluate intermediate outputs"]
    MID --> PAR{"Independent steps?"}
    PAR -- "yes" --> P["Run in parallel where possible"]
    PAR -- "no" --> S["Run sequential chain"]
    P --> END["Measure end-to-end quality/cost/latency"]
    S --> END
    OBS -- "no" --> MONO["Keep simpler monolithic prompt"]
    MONO --> END
~~~

## Defensive prompt engineering

~~~mermaid
flowchart TD
    INPUT["User / external data / tool output"] --> THREAT{"Could contain untrusted instructions?"}
    THREAT -- "yes" --> MODEL["Model-level instruction priority"]
    THREAT -- "yes" --> PROMPT["Prompt-level explicit constraints"]
    THREAT -- "yes" --> SYS["System-level controls"]
    SYS --> ISO["Isolation / sandbox"]
    SYS --> APPROVE["Human approval for dangerous state changes"]
    SYS --> IO["Input + output guardrails"]
    SYS --> MON["Usage-pattern / anomaly monitoring"]
    MODEL --> RUN["Execute model workflow"]
    PROMPT --> RUN
    ISO --> RUN
    APPROVE --> RUN
    IO --> RUN
    MON --> RUN
    RUN --> TEST["Measure violation rate + false refusal rate"]
    TEST --> HARDEN["Iterate defenses"]
    HARDEN --> THREAT
~~~

## Trust boundary for tool-using systems

~~~mermaid
flowchart LR
    SYS["System instruction<br/>highest priority"] --> MODEL["Model"]
    USER["User input"] --> MODEL
    EXT["External/RAG/tool data<br/>untrusted content"] --> MODEL
    MODEL --> ACTION{"State-changing action?"}
    ACTION -- "no" --> OUT["Output"]
    ACTION -- "yes" --> GATE["Explicit system/human approval gate"]
    GATE --> EXEC["Execute only if approved"]
~~~
