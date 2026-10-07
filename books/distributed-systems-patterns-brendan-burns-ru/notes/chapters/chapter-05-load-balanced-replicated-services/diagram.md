# Диаграмма: реплицированный сервис с распределением нагрузки

~~~mermaid
flowchart TD
    C["Clients"] --> LB["Load balancer / Service"]
    LB --> R1["Ready replica 1"]
    LB --> R2["Ready replica 2"]
    LB --> RN["Ready replica N"]

    R1 --> RD["Readiness endpoint"]
    R2 --> RD
    RN --> RD

    C --> TLS["Replicated nginx SSL tier"]
    TLS --> CACHE["Replicated Varnish cache tier"]
    CACHE --> APP["Replicated application tier"]

    CACHE --> RL["Rate limiting / HTTP 429"]
    CACHE --> AFF["Affinity caution"]
    AFF --> AFF2["Proxy IP can break naive IP-based stickiness"]

    LB --> ST["Sticky sessions when needed"]
    ST --> CH["Consistent hashing / app-level cookies"]

    APP --> SCALE["Horizontal scaling"]
    CACHE --> SCALE2["Independent cache scaling"]
    TLS --> SCALE3["Independent edge scaling"]
~~~

## Core flow

~~~text
replicate stateless service
→ add stable load-balancing endpoint
→ gate traffic by readiness
→ scale horizontally

if HTTP-layer concerns grow
→ introduce independently replicated cache/proxy tier
→ optionally add independently replicated TLS edge tier
~~~

## Operational boundary

Each additional tier improves specialization and independent scaling but also adds another runtime surface that must be configured, observed and operated.
