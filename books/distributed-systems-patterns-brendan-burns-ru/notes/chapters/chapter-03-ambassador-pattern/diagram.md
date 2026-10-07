# Диаграмма: паттерн Ambassador

~~~mermaid
flowchart TD
    A["Application container"] --> L["Stable local endpoint"]
    L --> M["Ambassador container"]
    M --> X["External world"]

    M --> S["Sharding"]
    S --> S1["Choose target shard"]
    S1 --> S2["Redis shard 0"]
    S1 --> S3["Redis shard 1"]
    S1 --> S4["Redis shard 2"]

    M --> B["Service broker"]
    B --> B1["Inspect environment"]
    B1 --> B2["Discover / create dependency"]
    B2 --> B3["Target service, e.g. MySQL"]

    M --> E["Experiment / request splitting"]
    E --> E1["Production service"]
    E --> E2["Experimental service"]
    E1 --> R["Return production result"]
    E2 --> T["Test / alternate traffic"]

    S --> D["Client-side vs central-service trade-off"]
    B --> D
    E --> D

    D --> D1["Client-side Ambassador:<br/>more client deployment complexity"]
    D --> D2["Separate service:<br/>operate / scale / monitor another service"]
~~~

## Core abstraction

~~~text
application
→ one stable local contract
→ Ambassador
→ external topology / discovery / routing policy
~~~

## Chapter-supported decision rule

Ambassador is useful when external interaction logic is:
- separable from application business logic;
- reusable;
- naturally placed beside application.

A separate shared service may make more sense when the capability becomes a persistent architecture-level service that should be operated independently.
