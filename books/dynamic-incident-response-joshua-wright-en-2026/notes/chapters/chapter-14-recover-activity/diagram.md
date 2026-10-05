# Диаграмма: Recover Activity

```mermaid
flowchart TD
    A["Eradication Output"] --> B["Pre-Restoration Verification"]

    B --> B1["Root Cause Fixed"]
    B --> B2["Persistence Removed"]
    B --> B3["Clean Backup / Trusted Rebuild"]
    B --> B4["Security Controls Ready"]

    B --> C["System Validation"]

    C --> C1["Functional"]
    C --> C2["Security"]
    C --> C3["Dependencies"]

    C --> D["System Owner Acceptance"]
    D --> E["Enhanced Monitoring"]

    E --> F{"Recovery Strategy"}
    F -->|Phased| G["Restore Batch"]
    F -->|Coordinated| H["Restore Interdependent Set"]

    G --> I["Validate"]
    H --> I

    I --> J{"Stable?"}
    J -->|No| K["Rollback / Investigate"]
    K --> B

    J -->|Yes| L["Remove Containment Incrementally"]
    L --> M["Capture Metrics / Documentation"]
    M --> N["Debrief"]
```

## Interpretation

Recover is a production-release process, not just system startup.

Each restoration step is gated by:
- evidence;
- technical validation;
- owner acceptance;
- monitoring.
