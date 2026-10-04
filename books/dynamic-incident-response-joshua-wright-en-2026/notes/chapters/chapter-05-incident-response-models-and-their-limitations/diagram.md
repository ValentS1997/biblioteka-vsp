# Диаграмма: от classic models к требованиям modern IR

```mermaid
flowchart TD
    A["PICERL"] --> D["Structured response"]
    B["NIST SP 800-61 Rev.2"] --> D
    C["NIST SP 800-61 Rev.3"] --> E["Enterprise integration"]

    D --> F["Strength: repeatable framework"]
    E --> F

    F --> G["Modern incident pressure"]

    G --> H["Scoping gap"]
    G --> I["Linear-model gap"]
    G --> J["Resource prioritization gap"]
    G --> K["Verification gap"]
    G --> L["Root-cause gap"]

    H --> M["Modern model requirements"]
    I --> M
    J --> M
    K --> M
    L --> M

    M --> N["Verify"]
    M --> O["Scope"]
    M --> P["Prioritize"]
    M --> Q["Iterate"]
    M --> R["Root Cause Analysis"]

    N --> S["Chapter 6: DAIR"]
    O --> S
    P --> S
    Q --> S
    R --> S
```

## Interpretation

Глава не отвергает existing frameworks.

Логика такая:

```text
existing models
    ↓
useful foundation
    ↓
modern complexity reveals hidden gaps
    ↓
make missing decision points explicit
    ↓
DAIR
```
