# Диаграмма: AI-assisted Incident Response

```mermaid
flowchart TD
    A["Incident Evidence"] --> B["Deterministic Tools / Parsers"]
    B --> C["Structured Facts"]

    C --> D["AI Model"]
    D --> E["Analysis / Synthesis / Draft"]
    D --> F["Tool Request"]

    F --> G["MCP / Agent Layer"]
    G --> H{"Read-only?"}

    H -->|Yes| I["Execute Allowed Tool"]
    H -->|No| J["Human Approval"]

    J -->|Approved| K["Execute State-Changing Tool"]
    J -->|Rejected| L["Stop / Revise"]

    I --> M["Tool Output"]
    K --> M
    M --> C

    E --> N["Analyst Verification"]
    N --> O{"Defensible?"}
    O -->|No| C
    O -->|Yes| P["IR Decision / Report / Playbook"]

    Q["Data Handling Policy"] -. constrains .-> D
    Q -. constrains .-> G
    R["Audit Logging"] -. records .-> G
    R -. records .-> J
```

## Interpretation

Best-case AI-assisted IR is not:

```text
evidence → model → action
```

It is:

```text
evidence
→ trusted tools
→ structured facts
→ AI reasoning
→ human verification
→ controlled action
```
