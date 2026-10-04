# Диаграмма: vocabulary and measurement model

```mermaid
flowchart TD
    A["Event stream"] --> B["Filtering / Context"]
    B --> C["Event of Interest"]
    C --> D["Correlation"]
    D --> E["IOC / IOA / Behavioral evidence"]
    E --> F["Verify against policy + risk"]
    F --> G["Incident"]

    G --> H["Detect timestamp"]
    G --> I["Occurrence estimate"]
    I --> J["MTTD"]
    H --> J

    H --> K["Response / Resolution"]
    K --> L["MTTR"]

    L --> M["Quality score"]
    M --> N["Balanced effectiveness view"]

    O["Incident Response"] --> P["Technical actions"]
    Q["Incident Management"] --> R["Coordination / Governance"]
    P --> S["Parallel execution"]
    R --> S
```

## Interpretation

Chapter 4 connects three layers:

1. **Vocabulary** — what are events, EOI, IOC, incidents.
2. **Measurement** — how fast the organization detects and responds.
3. **Organization** — who performs technical response and who coordinates the broader incident.

Если definitions inconsistent, все три слоя становятся unreliable.
