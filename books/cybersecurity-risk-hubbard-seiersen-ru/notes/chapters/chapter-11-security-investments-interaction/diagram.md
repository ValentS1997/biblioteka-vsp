# Глава 11 — Mermaid: dimensional security metrics

**Source:** EPUB spine 43–44, `OPS/ch1-41.xhtml` → `OPS/ch1-42.xhtml`; RAG `e0043:c01–c02`, `e0044:c01–c06`.

## 1. Basic security mart

```mermaid
flowchart TD
    F["Fact: security event/state"]
    D["Date / time"] --> F
    A["Asset / value"] --> F
    R["Risk / vulnerability"] --> F
    M["Mitigation / control"] --> F
    W["Threat / malware"] --> F
```

## 2. Conformed dimensions connect marts

```mermaid
flowchart LR
    V["Vulnerability mart"] --> A["Conformed asset"]
    M["Threat mart"] --> A
    C["Mitigation mart"] --> A
    V --> D["Conformed date/time"]
    M --> D
    C --> D
    A --> Q["Cross-control questions"]
    D --> Q
```

## 3. ПУКД survival flow

```mermaid
flowchart LR
    A["Threat first observed"] --> B["Undetected / survives"]
    B --> C["Control/vendor learns or detects"]
    C --> D["Blocked / mitigated"]
    A --> E["Start time"]
    D --> F["End time"]
    E --> G["Survival / exposure duration"]
    F --> G
```

## 4. Accumulating snapshot

```mermaid
flowchart LR
    A["Issue created"] --> B["Analysis"]
    B --> C["Fix in progress"]
    C --> D["Validation"]
    D --> E["Closed"]
    A -.-> T["Milestone dates + duration fields"]
    B -.-> T
    C -.-> T
    D -.-> T
    E -.-> T
```

## Boundary

Figures 11.1–11.7 and tables 11.1–11.5 are not reconstructed as original layouts. No DDL/SQL is inferred from conceptual models.
