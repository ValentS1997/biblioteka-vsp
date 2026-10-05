# Диаграмма: Contain Activity

```mermaid
flowchart TD
    A["Scope Findings"] --> B{"Containment Urgency"}

    B -->|Immediate harm| C["Active Containment"]
    B -->|Need intelligence| D["Passive Containment"]
    B -->|Evolving threat| E["Adaptive Containment"]

    C --> F["Identity Controls"]
    C --> G["Network / Host Controls"]
    C --> H["Cloud / SaaS / Serverless Controls"]

    D --> I["Monitor / Preserve Evidence"]
    E --> I
    I --> J["Progressive Restrictions"]

    F --> K["Credential revoke"]
    K --> L["Session terminate"]
    L --> M["Token revoke"]
    M --> N["Conditional access"]

    G --> O["Isolation / DNS / Firewall / EDR"]
    H --> P["IAM / SG-NSG / snapshots / tags"]

    O --> Q["Evidence Collection"]
    P --> Q
    N --> Q

    Q --> R["Containment Validation"]
    R --> S{"Attacker activity stopped?"}
    S -->|No| A
    S -->|Yes| T["Document / Handoff to Eradicate"]
```

## Interpretation

Containment is not one irreversible switch.

It is a controlled loop:
- choose strategy;
- act;
- preserve evidence;
- validate;
- adapt if attacker retains access.
