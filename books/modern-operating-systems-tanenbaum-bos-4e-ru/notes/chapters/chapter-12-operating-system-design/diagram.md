# Chapter 12 conceptual / diagnostic flow

```mermaid
flowchart TD
    G["Goals / constraints"] --> I["Interface design"]
    I --> S["Simple"]
    I --> C["Complete"]
    I --> E["Efficiently implementable"]

    I --> A["Architecture"]
    A --> L["Layering"]
    A --> X["Exokernel / end-to-end"]
    A --> M["Microkernel client-server"]

    A --> MP["Mechanism vs policy"]
    A --> O["Orthogonality"]
    A --> N["Naming / indirection"]
    A --> B["Binding time"]
    A --> D["Static vs dynamic structures"]
    A --> COMM["Sync vs async communication"]

    A --> R["Implementation discipline"]
    R --> HW["Hide hardware"]
    R --> RE["Reuse + reentrancy"]
    R --> ERR["Check errors first"]
    R --> BF["Brute force where sufficient"]

    R --> P["Performance"]
    P --> MEAS["Measure first"]
    P --> CACHE["Caching / hints"]
    P --> LOC["Locality"]
    P --> COMMON["Optimize common case"]

    P --> PM["Project management"]
    PM --> TEAM["Team structure"]
    PM --> INT["Integration + testing"]
    PM --> BROOKS["Brooks: people ≠ interchangeable time"]

    PM --> FUT["Future constraints"]
    FUT --> CLOUD["virtualization / cloud"]
    FUT --> CORE["multicore"]
    FUT --> MOBILE["battery / mobility"]
    FUT --> EMB["embedded systems"]
```

## Diagnostic boundary

```text
minimal ≠ incomplete
mechanism ≠ policy
cache ≠ hint
reuse ≠ reentrancy
more optimization ≠ better system
more developers ≠ proportionally shorter schedule
```
