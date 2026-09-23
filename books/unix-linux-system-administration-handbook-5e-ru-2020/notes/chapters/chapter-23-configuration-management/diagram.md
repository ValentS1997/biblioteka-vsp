# Диаграмма: configuration-management change flow

~~~mermaid
flowchart TD
    A["Desired state change"] --> B["Version-controlled configuration"]
    B --> C["Review and representative test"]
    C --> D{"Tool"}

    D -->|Ansible| E["Inventory / playbook / roles"]
    E --> E1["SSH + Python"]
    E1 --> F["Targeted apply"]

    D -->|Salt| G["Master / minion"]
    G --> G1["Key approval"]
    G1 --> G2["grains + pillar + top.sls"]
    G2 --> F

    F --> H["Idempotent operations/states"]
    H --> I["Changed / failed report"]
    I --> J{"Accepted?"}
    J -->|No| K["Restore known-good config revision"]
    K --> F
    J -->|Yes| L["Staged rollout"]
    L --> M["Managed desired state"]

    N["Security boundaries"] --> N1["Secrets encrypted"]
    N --> N2["Control node hardened"]
    N --> N3["Credentials scoped"]
    N --> N4["No hidden manual drift"]

    O["Operational anti-patterns"] --> O1["First test in production"]
    O --> O2["Raw shell without state awareness"]
    O --> O3["Unreviewed third-party roles/formulas"]
    O --> O4["Manual CM bypass"]
~~~

## Смысл диаграммы

Configuration management работает только при дисциплине вокруг самого инструмента: version control, review, tests, scoped credentials и отсутствие unmanaged drift являются частью системы, а не внешними пожеланиями.
