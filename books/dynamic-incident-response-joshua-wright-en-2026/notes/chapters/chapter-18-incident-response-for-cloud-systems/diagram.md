# Диаграмма: Cloud Incident Response

```mermaid
flowchart TD
    A["Cloud Alert / EOI"] --> B["Identity Context"]
    B --> C["Effective Permissions"]
    C --> D["Resource / Region Enumeration"]
    D --> E["Control-Plane Logs"]
    D --> F["Data-Plane Logs"]
    D --> G["Network / Runtime Telemetry"]
    E --> H["Scope"]
    F --> H
    G --> H
    H --> I["Preserve Evidence"]
    I --> J["Contain / Isolate"]
    J --> K["Session / Token Control"]
    J --> L["Network Quarantine"]
    J --> M["Storage / IAM Remediation"]
    K --> N["Persistence Review"]
    L --> N
    M --> N
    N --> O["All Regions / Accounts / Projects"]
    O --> P["Validate"]
    P --> Q["Recover / Debrief"]
```

## Interpretation

Cloud scope follows identity and effective permissions before individual resources.

A single compromised workload may be only one symptom of a broader identity or control-plane problem.
