# Диаграмма: Detect Activity

```mermaid
flowchart TD
    A["Detection Inputs"] --> B["Methodologies"]
    A --> C["Data Sources"]
    A --> D["Human Reports"]

    B --> B1["Signature"]
    B --> B2["Behavioral"]
    B --> B3["ML"]
    B --> B4["Hybrid"]

    C --> C1["EDR / NDR"]
    C --> C2["SIEM / SOAR"]
    C --> C3["Cloud / Container"]
    C --> C4["Network / TLS Metadata"]

    D --> D1["Employees"]
    D --> D2["Admins / Help Desk"]
    D --> D3["Researchers / Partners"]

    B1 --> E["EOI"]
    B2 --> E
    B3 --> E
    B4 --> E
    C1 --> E
    C2 --> E
    C3 --> E
    C4 --> E
    D1 --> E
    D2 --> E
    D3 --> E

    E --> F["Document evidence"]
    F --> G["Verify + Triage"]

    H["Threat Hunting"] --> E
    I["Purple Team / Tuning"] --> B
    J["New TTP / CTI"] --> B
```

## Interpretation

Detect имеет два направления:

- passive intake;
- active hunting.

Оба должны приводить не к premature incident declaration, а к хорошо документированному EOI для следующей DAIR activity.
