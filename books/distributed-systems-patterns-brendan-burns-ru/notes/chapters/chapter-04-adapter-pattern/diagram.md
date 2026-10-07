# Диаграмма: паттерн Adapter

~~~mermaid
flowchart TD
    A["Heterogeneous application container"] --> N["Native interface"]
    N --> AD["Adapter container"]
    AD --> U["Standardized operational interface"]

    U --> M["Monitoring"]
    M --> M1["Redis native metrics"]
    M1 --> M2["redis_exporter"]
    M2 --> M3["Prometheus-facing interface"]

    U --> L["Logging"]
    L --> L1["Files / stdout / API / SLOWLOG"]
    L1 --> L2["fluentd Adapter"]
    L2 --> L3["Common structured / time-ordered log"]

    U --> H["Health"]
    H --> H1["DB-specific diagnostic query"]
    H1 --> H2["Health Adapter"]
    H2 --> H3["HTTP success / failure"]
    H3 --> H4["Orchestrator decision"]

    AD --> D["Design choice"]
    D --> D1["Modify owned application directly"]
    D --> D2["Keep third-party/base image unchanged"]
    D2 --> D3["Reusable Adapter"]
~~~

## Core abstraction

~~~text
heterogeneous native interface
→ Adapter
→ one infrastructure-facing contract
~~~

## Chapter-supported decision rule

Direct application modification can be reasonable when the team owns the application/container and can maintain the change.

Adapter is favored when:
- the application is third-party or externally maintained;
- the transformation is reusable;
- separate ownership/versioning is useful;
- maintaining a forked image would create unnecessary lifecycle cost.
