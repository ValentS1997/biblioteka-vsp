# Диаграмма: CI/CD promotion and control flow

~~~mermaid
flowchart TD
    A["Commit to version control"] --> B["Pipeline trigger"]
    B --> C["Checkout"]
    C --> D["Build once"]
    D --> E["Build artifact"]

    E --> F["Automated tests"]
    F -->|Fail| X["Stop pipeline / fix first"]
    F -->|Pass| G["Release candidate"]

    G --> H["Deploy development"]
    H --> I["Integration / acceptance tests"]
    I -->|Fail| X
    I -->|Pass| J["Deploy staging"]

    J --> K["Further tests / validation"]
    K -->|Fail| X
    K -->|Pass| L{"Production gate"}

    L -->|Human approval if required| M["Production deployment"]
    L -->|Automatic policy| M

    M --> N["Health / telemetry checks"]
    N -->|Healthy| O["Release"]
    N -->|Regression| P["Rollback / replace / traffic switch"]

    Q["Version-controlled pipeline"] --> B
    Q --> Q1["Jenkinsfile"]
    Q --> Q2["Terraform / Packer / scripts"]

    R["Secrets boundary"] --> R1["Jenkins Credentials Store"]
    R1 --> Q
    R -. "never commit secrets" .-> A

    S["Deployment strategies"] --> S1["blue-green"]
    S --> S2["rolling"]
    S --> S3["canary"]
    S3 --> N

    T["Container path"] --> T1["build container"]
    T1 --> T2["runtime image"]
    T2 --> T3["registry"]
    T3 --> T4["orchestrator"]
    T4 --> M
~~~

## Смысл диаграммы

Один build artifact последовательно продвигается через gates. Любой failed test останавливает продвижение. Pipeline/configuration хранятся в VCS, secrets — отдельно. Production deployment завершается только после health/telemetry verification.
