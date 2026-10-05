# Диаграмма: Eradicate Activity

```mermaid
flowchart TD
    A["Containment Complete Enough"] --> B["Short-Form Investigation"]
    A --> C["Long-Form Investigation"]

    B --> D["Root Cause Analysis"]
    C --> D

    D --> E["Persistence Inventory"]
    E --> F["Remove Persistence"]

    D --> G["Identity Remediation"]
    G --> G1["Users / Service Accounts"]
    G --> G2["KRBTGT / DC / Trust"]
    G --> G3["OAuth / PAT / API Keys"]

    D --> H["Vulnerability Remediation"]
    H --> H1["Patch / Config Fix"]
    H --> H2["Broader Assessment"]
    H --> H3["Compensating Controls"]

    F --> I["Validation"]
    G --> I
    H --> I

    I --> J{"Attacker access/persistence gone?"}
    J -->|No| B
    J -->|Yes| K["Document + Handoff to Recover"]

    L["Logs / Memory / Network / EDR / Cloud"] --> B
    L --> C
```

## Interpretation

Eradication is evidence-driven.

Нельзя безопасно удалить то, что команда ещё не понимает.

Главный feedback loop:
- investigation reveals new artifact;
- artifact changes remediation scope;
- remediation is validated;
- failure returns team to investigation.
