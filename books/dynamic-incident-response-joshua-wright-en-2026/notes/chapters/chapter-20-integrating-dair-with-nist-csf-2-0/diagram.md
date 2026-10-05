# Диаграмма: DAIR mapped to NIST CSF 2.0

```mermaid
flowchart LR
    GV["Govern"] --> DM["Decision Maker Coordination"]
    ID["Identify"] --> DM

    PR["Protect"] --> P["Prepare"]
    DE["Detect"] --> D["Detect → Verify → Triage"]
    RS["Respond"] --> R["Scope ↔ Contain ↔ Eradicate ↔ Recover"]
    RC["Recover"] --> RD["Recover + Debrief"]

    P --> A["Compliance Artifacts"]
    D --> A
    R --> A
    RD --> A
    DM --> A

    A --> E["Control Effectiveness Evidence"]
    E --> AU["Audit / Assessment"]
    AU --> CI["Continuous Improvement"]
```

## Interpretation

DAIR does not replace CSF 2.0.

DAIR provides the tactical incident-response operating model that can generate evidence demonstrating CSF-aligned capability and effectiveness.
