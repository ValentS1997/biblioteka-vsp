# Диаграмма: FaaS и событийно-ориентированная обработка

~~~mermaid
flowchart TD
    E["Discrete event / request"] --> F["FaaS function"]
    F --> R["Result / next event"]

    F --> D["Decorator"]
    D --> API["Main API"]

    F --> A["Async event handler"]
    A --> S["External side effect"]

    F --> P["Event Pipeline"]
    P --> P1["Function 1"]
    P1 --> P2["Function 2"]
    P2 --> P3["Function N"]

    F --> C["Fit check"]
    C --> G["Short-lived · stateless · variable load"]
    C --> B["Long-running · heavy warm-up · sustained load"]

    F --> O["Operational requirements"]
    O --> O1["External state"]
    O --> O2["Monitoring / alerting"]
    O --> O3["Dependency / cycle visibility"]
~~~

## Core decision flow

~~~text
discrete event?
→ short-lived work?
→ little local state?
→ FaaS candidate

otherwise:
→ consider long-running service
~~~

## Event Pipeline

Nodes are functions. Edges are HTTP/network calls or events. Context may flow through the pipeline even when functions do not share local state.
