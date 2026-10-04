# Диаграмма: эволюция incident response

```mermaid
flowchart LR
    A["Early cyber incidents"] --> B["Morris Worm 1988"]
    B --> C["CERT 1988"]
    C --> D["CIAC 1989"]
    D --> E["Schultz methodology 1990"]
    E --> F["US Navy P-5239-19 1996"]
    F --> G["SANS Step-by-Step 1998"]
    G --> H["NIST SP 800-61 2004"]
    H --> I["Rev.1 2008"]
    I --> J["Rev.2 2012"]
    J --> K["Rev.3 / CSF alignment 2025"]

    E -. six stages .-> G
    G -. practical checklist lineage .-> H

    K --> L["Govern"]
    K --> M["Identify"]
    K --> N["Protect"]
    K --> O["Detect"]
    K --> P["Respond"]
    K --> Q["Recover"]

    R["Modern conditions"] --> S["Cloud identities"]
    R --> T["Third-party SaaS"]
    R --> U["Supply chain"]
    R --> V["AI-orchestrated attacks"]
    R --> W["Adaptive adversaries"]

    S --> X["Need to reassess old assumptions"]
    T --> X
    U --> X
    V --> X
    W --> X
```

## Смысл

История не показывает, что старые models «плохие». Она показывает, что они были rational answers на threat landscape своего времени.

Следующая логическая задача книги — сохранить их полезные принципы, но добавить adaptation и iteration для современных incidents.
