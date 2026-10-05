# Диаграмма: Prepare Activity

```mermaid
flowchart TD
    A["Prepare"] --> B["Organizational Readiness"]
    A --> C["IRT Capability"]
    A --> D["Proactive Prevention & Detection"]

    B --> B1["Policy / Plan / Playbooks"]
    B --> B2["Management Support"]
    B --> B3["Risk & Classification"]
    B --> B4["Communication / Contacts / Reporting"]
    B --> B5["ECP / Regulatory / Insurance"]

    C --> C1["Training"]
    C --> C2["RACI / Authority"]
    C --> C3["Relationships"]
    C --> C4["Tools / Evidence / Access"]
    C --> C5["Tabletops / Drills"]

    D --> D1["CTI / STIX / Platform"]
    D --> D2["Patch / Inventory / Hardening"]
    D --> D3["EDR / Sysmon"]
    D --> D4["Network Monitoring / Flow / NDR"]
    D --> D5["Detection Engineering / Hunting"]
    D --> D6["ASM / Adversary Simulation"]
    D --> D7["Logging / Retention"]

    B4 --> E["Faster coordination"]
    C5 --> E
    D7 --> F["Better detection & scoping"]
    D5 --> F

    E --> G["Lower response friction"]
    F --> G
    G --> H["Improved incident outcomes"]
```

## Interpretation

Prepare — это dependency graph, а не один task.

Слабое звено в communication, access, inventory или telemetry проявляется уже во время active incident, когда исправлять его дороже.
