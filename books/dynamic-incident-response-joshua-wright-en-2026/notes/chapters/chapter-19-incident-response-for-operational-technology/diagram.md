# Диаграмма: OT Incident Response

```mermaid
flowchart TD
    A["OT Alert / Observation"] --> B["Verify + Triage with Engineering"]

    B --> C{"Threat can affect process?"}
    C -->|Unclear| D["Collect OT Evidence"]
    D --> B

    C -->|Yes| E["Scope Control Layer"]
    C -->|No immediate reach| F["Monitor / Controlled Response"]

    E --> E1["Network / Protocol"]
    E --> E2["Engineering Workstation"]
    E --> E3["Controller Logic"]
    E --> E4["Operator / Historian"]

    E --> G{"Containment Strategy"}
    G --> H["Selective Restriction"]
    G --> I["Island / Manual Mode"]
    G --> J["Controlled Shutdown if Required"]

    H --> K["Eradicate"]
    I --> K
    J --> K

    K --> L["Validate Logic / Access / Trust"]
    L --> M["Recover"]

    M --> M1["Restore Support Systems"]
    M --> M2["Validate Controllers"]
    M --> M3["Physical Walkthrough"]
    M --> M4["Controlled Startup"]

    M --> N["Debrief"]
    N --> O["Architecture / Visibility / Remote Access Improvements"]

    P["Safety + Process Stability"] -. constrains .-> B
    P -. constrains .-> G
    P -. constrains .-> M
```

## Interpretation

OT response is engineering-constrained.

A technically valid cyber action is not acceptable if it creates greater process or safety risk than the incident itself.
