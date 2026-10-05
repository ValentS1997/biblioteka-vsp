# Диаграммы главы 4

## Рабочий процесс выбора модели

~~~mermaid
flowchart TD
    GOAL["Business goal + utility threshold"] --> CRIT["Define evaluation criteria"]
    CRIT --> HARD["Define hard vs soft attributes"]
    HARD --> FILTER["1. Filter models by hard attributes"]
    FILTER --> PUBLIC["2. Use public benchmarks / leaderboards<br/>for shortlist"]
    PUBLIC --> PRIVATE["3. Run private application-specific evaluation"]
    PRIVATE --> TRADE["Compare quality · cost · latency · scale"]
    TRADE --> SELECT["Select candidate"]
    SELECT --> PROD["4. Production monitoring + user feedback"]
    PROD --> CRIT
~~~

Публичная оценка сужает список. Решение принимается после private evaluation на собственном workload.

## Собственный evaluation pipeline

~~~mermaid
flowchart TD
    SYSTEM["AI system"] --> COMPONENTS["Step 1: evaluate each component<br/>and task/turn levels"]
    COMPONENTS --> GUIDE["Step 2: evaluation guide"]
    GUIDE --> CRITERIA["Define criteria:<br/>what is good / bad"]
    CRITERIA --> SCALE["Scoring scales + examples"]
    SCALE --> BUSINESS["Map scores to business metrics<br/>and utility threshold"]
    BUSINESS --> METHODS["Step 3: choose methods + data"]
    METHODS --> DATA["Representative data + labels + slices"]
    DATA --> RUN["Run evaluations"]
    RUN --> REL["Analyze reliability:<br/>repeatability · variance · bootstrap"]
    REL --> META["Check metric correlation · cost · latency"]
    META --> ITERATE["Iterate and track every changed variable"]
    ITERATE --> GUIDE
~~~

## Public benchmark interpretation

~~~mermaid
flowchart LR
    BENCH["Public benchmarks"] --> RELV{"Relevant to application?"}
    RELV -- "no" --> DROP["Do not use for selection"]
    RELV -- "yes" --> CORR["Check overlap/correlation"]
    CORR --> CONTAM["Check contamination risk"]
    CONTAM --> AGG["Understand aggregation/weights"]
    AGG --> SHORT["Use as shortlist signal"]
    SHORT --> PRIVATE["Private evaluation"]
~~~

## Factual consistency

~~~mermaid
flowchart TD
    OUT["Generated output"] --> CTX{"Trusted context supplied?"}
    CTX -- "yes" --> LOCAL["Local factual consistency<br/>output vs context"]
    CTX -- "no" --> GLOBAL["Global factual consistency"]
    GLOBAL --> RETRIEVE["Find trusted evidence"]
    LOCAL --> JUDGE["Exact / classifier / AI-judge methods"]
    RETRIEVE --> JUDGE
    JUDGE --> RESULT["Factuality signal"]
~~~
