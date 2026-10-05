# Диаграмма: Ransomware Response

```mermaid
flowchart TD
    A["Prepare"] --> A1["Identity / Tier-0"]
    A --> A2["Backups 3-2-1-1-0"]
    A --> A3["Comms / Holding Statement"]
    A --> A4["CTI / Training"]

    A --> B["Verify + Triage"]
    B --> B1["Attack Type"]
    B --> B2["Impact / Commander"]
    B --> B3["Extended Response Plan"]

    B --> C["Scope"]
    C --> C1["Hosts / Identity / Backup"]
    C --> C2["Lateral Movement"]
    C --> C3["Exfiltration"]
    C --> C4["Timeline / Persistence"]

    C --> D["Contain / Eradicate"]
    D --> D1["Stop Spread"]
    D --> D2["Remove Access"]
    D --> D3["Close Initial Vector"]
    D --> D4["Assess Decryption"]

    D --> E["Recover"]
    E --> E1["Clean Restore Point"]
    E --> E2["Dependency Order"]
    E --> E3["Monitor Return"]
    E --> E4["Communicate"]

    E --> F["Debrief"]
    F --> F1["Backup Survival"]
    F --> F2["Dwell Time"]
    F --> F3["Exfiltration Confidence"]
    F --> F4["Recovery Metrics"]

    G["Legal / Regulatory / Insurance"] -. spans .-> B
    G -. spans .-> E
    H["Human Sustainability"] -. spans .-> C
    H -. spans .-> D
    H -. spans .-> E
```

## Interpretation

Ransomware is a cross-functional crisis.

Technical response alone is insufficient because:
- business continuity;
- legal obligations;
- communications;
- insurance;
- workforce endurance

all influence incident outcome.
