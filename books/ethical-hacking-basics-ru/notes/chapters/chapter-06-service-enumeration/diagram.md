# Диаграммы — глава 6

## 1. Service → enumeration → evidence

```mermaid
flowchart TD
  A["Known authorized service"] --> B["Protocol-specific enumeration"]
  B --> RPC["RPC/RMI metadata"]
  B --> SMB["SMB names / shares / users"]
  B --> SNMP["SNMP MIB / OID data"]
  B --> SMTP["SMTP capabilities"]
  B --> WEB["Web/CMS metadata"]
  RPC --> E["Evidence + provenance"]
  SMB --> E
  SNMP --> E
  SMTP --> E
  WEB --> E
  E --> V{"Validated and within scope?"}
  V -- "Yes" --> R["Report / next authorized step"]
  V -- "No" --> U["Unverified / stop"]
```

## 2. Enumeration is not exploitation

```mermaid
flowchart LR
  S["Service exposed"] --> M["Metadata obtained"]
  M --> H["Attack-surface hypothesis"]
  H --> A{"Separate authorization?"}
  A -- "No" --> STOP["Stop at evidence"]
  A -- "Yes" --> NEXT["Additional validation under new scope"]
```

## 3. Service-specific defenses

```mermaid
flowchart TD
  SMB["SMB"] --> S1["Disable SMBv1 / unnecessary shares / NetBIOS"]
  SMB --> S2["Host + network firewall restrictions"]
  SNMP["SNMP"] --> N1["Prefer v3 / auth / encryption"]
  SNMP --> N2["Restrict managers"]
  SMTP["SMTP"] --> M1["Reduce address/user disclosure"]
  SMTP --> M2["Prevent open relay"]
  WEB["Web"] --> W1["Reduce headers/error metadata"]
  WEB --> W2["Access control / disable directory listing"]
```

## 4. Evidence quality

```mermaid
flowchart TD
  O["Tool output"] --> Q1["Source/version/date known?"]
  Q1 --> Q2["Authenticated or unauthenticated?"]
  Q2 --> Q3["Response proves existence or only suggests it?"]
  Q3 --> Q4["Sensitive data handled appropriately?"]
  Q4 --> D["Defensible finding"]
```

Source basis: `p0140:c01`–`p0168:c02`.
