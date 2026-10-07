# Диаграмма: выбор владельца

~~~mermaid
flowchart TD
    C["Several service replicas"] --> S["Shared coordination store"]

    S --> CAS["Atomic compare-and-swap"]
    CAS --> O["Current owner"]

    O --> TTL["Finite TTL"]
    TTL --> R["Periodic renewal"]
    R -->|success| O
    R -->|failure| STOP["Stop protected activity"]

    O --> V["Resource version"]
    V --> U["Conditional unlock"]
    V --> Q["Attach owner + version to protected request"]

    Q --> W["Downstream worker"]
    W --> CHECK["Validate current owner + version"]
    CHECK -->|match| EXEC["Execute"]
    CHECK -->|mismatch| REJECT["Reject stale request"]

    TTL --> RACE["Paused old owner may resume after expiry"]
    RACE --> CHECK
~~~

## Core safety progression

~~~text
CAS
→ TTL
→ version-aware release
→ renewable lease
→ downstream validation of owner + version
~~~

Each step closes a failure mode introduced or exposed by the previous step.

## Decision boundary

If singleton downtime is acceptable, explicit owner election may be unnecessary. If high availability requires multiple replicas but only one active owner, use a proven coordination store rather than implementing consensus in the application.
