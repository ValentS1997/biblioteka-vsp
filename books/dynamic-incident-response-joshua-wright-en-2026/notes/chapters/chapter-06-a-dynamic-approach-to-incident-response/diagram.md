# Диаграмма: DAIR

```mermaid
flowchart TD
    A["Prepare"] --> B["Detect"]
    B --> C["Verify + Triage"]

    C --> D["Scope"]
    D --> E["Contain"]
    E --> F["Eradicate"]
    F --> G["Recover"]

    G --> H{"New evidence?"}
    H -->|Yes| D
    H -->|No| I["Debrief"]

    D --> H
    E --> H
    F --> H

    J["Decision Makers"] -. business context .-> C
    J -. priority / impact .-> D
    J -. acceptable disruption .-> E
    J -. recovery priorities .-> G

    K["TTP / IOC"] --> D
    D --> L["Expanded understanding"]
    L --> E
```

## Interpretation

DAIR не требует, чтобы actions выполнялись строго по часовой стрелке.

Response Actions Loop — analytical loop, а не rigid sequence.

Любой новый artifact может вернуть команду к scoping и изменить последующие actions.
