# Диаграмма: monitoring lifecycle

~~~mermaid
flowchart TD
    A["Service / system / application"] --> B["Define dependencies and useful signals"]

    B --> C["Collect telemetry"]
    C --> C1["Real-time metrics"]
    C --> C2["Events / logs"]
    C --> C3["Network / system probes"]
    C --> C4["Application / business metrics"]
    C --> C5["Security telemetry"]

    C1 --> D["Normalize / transport"]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E["Store / retain time series"]
    E --> F["Evaluate thresholds, history and context"]

    F --> G{"Action needed?"}
    G -->|No| H["Dashboard / trend / later review"]
    G -->|Yes| I["Actionable alert"]

    I --> J["Owner / on-call / ticket"]
    J --> K["Runbook / investigation"]
    K --> L{"Expected change?"}

    L -->|Yes| M["Update baseline / close alert"]
    L -->|No| N["Incident response / remediation"]

    H --> O["Review usefulness and noise"]
    M --> O
    N --> O

    O --> P["Tune checks, thresholds, retention and coverage"]
    P --> B

    Q["Monitoring platform"] --> R["Independent monitoring of monitoring"]
    R --> I

    S["Production gate"] --> T{"Monitoring ready?"}
    T -->|No| U["Do not release into production"]
    T -->|Yes| A
~~~

## Логика

Глава строит monitoring как замкнутый эксплуатационный цикл. Сбор данных сам по себе не является целью: telemetry должна поддерживать comparison, alerts, investigation и improvement. После missed failure coverage расширяется; false-positive не игнорируется, а устраняется. Production readiness включает monitoring до запуска сервиса.
