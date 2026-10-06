# Диаграммы главы 10

## Постепенное построение архитектуры

~~~mermaid
flowchart TD
    MIN["Request → Model → Response"] --> CTX["1. Context construction"]
    CTX --> GR["2. Input / output guardrails"]
    GR --> ROUTE["3. Router + model gateway"]
    ROUTE --> CACHE["4. Exact / semantic cache"]
    CACHE --> AG["5. Agent loops + write actions"]
    AG --> OBS["Monitoring / observability"]
    OBS --> ORCH["Orchestration when complexity justifies it"]
    ORCH --> FB["User feedback → evaluation / product / data"]
~~~

## Request path and control boundaries

~~~mermaid
flowchart LR
    U["User"] --> IG["Input guardrail"]
    IG --> R["Router"]
    R --> C["Context / retrieval / tools"]
    C --> G["Model gateway"]
    G --> M["Selected model"]
    M --> OG["Output guardrail / evaluator"]
    OG --> U
    G --> CA["Cache"]
    C --> T["Tools"]
    T -->|"write action"| EXT["External state"]
    R --> H["Human fallback"]
~~~

## Observability loop

~~~mermaid
flowchart TD
    RUN["Production request"] --> MET["Metrics"]
    RUN --> LOG["Logs"]
    RUN --> TRACE["Trace"]
    MET --> DET["Detect failure / drift"]
    LOG --> RCA["Root-cause analysis"]
    TRACE --> RCA
    DET --> RCA
    RCA --> EVAL["Add failure to evaluation"]
    EVAL --> CHANGE["Controlled change"]
    CHANGE --> RUN
~~~

## Feedback lifecycle

~~~mermaid
flowchart TD
    UX["User interaction"] --> EX["Explicit feedback"]
    UX --> IM["Implicit feedback"]
    UX --> NL["Natural-language corrections/preferences"]
    EX --> VALID["Privacy + bias + interpretation checks"]
    IM --> VALID
    NL --> VALID
    VALID --> USE["Evaluation / product / personalization / training"]
    USE --> MODEL["Updated behavior"]
    MODEL --> EXP["What users see"]
    EXP --> UX
    USE --> LOOP{"Bias / degenerate loop?"}
    LOOP -- "yes" --> STOP["Independent evaluation / reweight / rollback"]
~~~

## Gateway responsibilities

~~~mermaid
flowchart LR
    APP["Applications"] --> GW["Model gateway"]
    GW --> A["Provider A"]
    GW --> B["Provider B"]
    GW --> L["Self-hosted model"]
    GW --> CTRL["Access · rate · cost · failover · logs"]
~~~
