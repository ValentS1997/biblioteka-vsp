# Диаграмма: defense in depth and incident response

~~~mermaid
flowchart TD
    A["Assets / services / data"] --> B["Inventory and threat model"]

    B --> C["Prevent"]
    C --> C1["Least privilege"]
    C --> C2["Patch management"]
    C --> C3["Remove unnecessary services"]
    C --> C4["MFA / account hygiene"]
    C --> C5["Firewall / DMZ / VPN boundaries"]
    C --> C6["TLS / SSH / cryptography"]

    B --> D["Detect"]
    D --> D1["Central logging"]
    D --> D2["Nmap / audit tools"]
    D --> D3["NIDS: Bro / Snort"]
    D --> D4["HIDS: OSSEC"]
    D --> D5["File integrity / Fail2Ban"]

    B --> E["Recover"]
    E --> E1["Protected backups"]
    E --> E2["Known-good configuration/images"]

    D --> F{"Compromise suspected?"}
    F -->|No| G["Continue monitoring and hardening"]
    F -->|Yes| H["Preserve evidence / collect logs"]

    H --> I["Assess scope and impact"]
    I --> J["Isolate affected hosts if appropriate"]
    J --> K["Close discovered gaps"]
    K --> L["Recovery plan"]
    L --> M["Rebuild / restore from trusted state"]
    M --> N["Rotate affected credentials"]
    N --> O["Verify service + monitoring"]
    O --> P["Communicate / report / lessons learned"]

    Q["Security-sensitive tools"] --> Q1["Explicit authorization"]
    Q1 --> D2
~~~

## Смысл диаграммы

Security controls разделены на prevention, detection и recovery. Ни firewall, ни VPN, ни IDS не являются достаточными сами по себе. При suspected compromise сначала сохраняются evidence/logs, затем определяется scope, и только после этого выполняется isolation/remediation/recovery.
