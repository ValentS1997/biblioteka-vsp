# Диаграмма: от давления инцидента к adaptive response

```mermaid
flowchart TD
    A["Incident / adverse event"] --> B["Incomplete information + time pressure"]
    B --> C["Observe / Identify"]
    C --> D["Verify"]
    D --> E["Triage"]
    E --> F["Scope"]

    F --> G["Contain"]
    G --> H["Eradicate"]
    H --> I["Recover"]

    F --> J{"New information?"}
    G --> J
    H --> J
    I --> J

    J -->|Yes| D
    J -->|No| K["Review outcome"]

    K --> L["Metrics"]
    K --> M["Lessons learned"]
    L --> N["Improve plans / procedures / strategy"]
    M --> N
    N --> A

    O["Decision makers / stakeholders"] -. guide .-> F
    O -. guide .-> G
    O -. guide .-> I

    P["SIEM / XDR / SOAR / threat intelligence"] -. support .-> C
    P -. support .-> D
```

## Смысл

Chapter 2 задаёт book-level worldview:

- tools поддерживают response;
- process структурирует response;
- judgment определяет качество решений;
- iteration нужна, когда новая информация меняет scope;
- continuous improvement завершает один incident и улучшает готовность к следующему.
