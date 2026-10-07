# Диаграммы — глава 12

## 1. Application trust boundary

```mermaid
flowchart LR
  U["Untrusted input"] --> V["Validate / normalize / authorize"]
  V --> A["Application logic"]
  A --> DB["Database / interpreter / OS / file subsystem"]
  V -- "reject" --> R["Safe error / log"]
  A --> L["Security logging"]
```

## 2. Defense against memory-corruption impact

```mermaid
flowchart TD
  B["Memory bug"] --> C{"Can control execution?"}
  C --> ASLR["ASLR"]
  C --> CAN["Stack canary"]
  C --> NX["Non-executable memory"]
  ASLR --> D["Exploitability reduced"]
  CAN --> D
  NX --> D
  D --> F["Fix underlying bug anyway"]
```

## 3. Post-compromise lateral-movement control

```mermaid
flowchart TD
  I["Initial compromised host"] --> R["Recon / identity access"]
  R --> P{"Allowed path?"}
  P -- "Blocked" --> A["Alert / investigate"]
  P -- "Allowed" --> S["Next segment/system"]
  S --> E["EDR / network / identity telemetry"]
  E --> C["Contain / isolate"]
```

## 4. Defensible architecture

```mermaid
flowchart TD
  PREV["Preventive controls"] --> VIS["Visibility: logs / SIEM / telemetry"]
  SEG["Segmentation / firewalls"] --> VIS
  END["EDR / endpoint isolation"] --> VIS
  VIS --> DET["Detect abnormal behavior"]
  DET --> RESP["Repeatable response"]
  RESP --> CONT["Contain / isolate / recover"]
```

Source basis: `p0324:c01`–`p0349:c02`.
