# Глава 12 — Mermaid: программа управления киберрисками

**Source:** EPUB spine 45; RAG `e0045:c01–c08`.

## 1. Program structure

```mermaid
flowchart TD
    B["CEO / Board"] --> R["Cyber Risk Management"]
    R --> Q["Quantitative risk analysis"]
    R --> T["Training & development"]
    R --> A["Analytics technology"]
    R --> P["Program management"]
    R --> M["Model audit / governance"]
    Q --> D["Investment / risk decisions"]
    A --> Q
    T --> Q
    P --> D
    M --> D
```

## 2. Equal model-audit principle

```mermaid
flowchart LR
    I["Intuition"] --> V["Same validation questions"]
    S["Scorecard / heat map"] --> V
    D["Deterministic model"] --> V
    Q["Quant / stochastic model"] --> V
    V --> E["Evidence of fitness / comparative performance"]
```

## 3. Adoption loop

```mermaid
flowchart LR
    A["Pilot decision"] --> B["Quant model"]
    B --> C["Measure result"]
    C --> D["Audit / learn"]
    D --> E["Training + tooling"]
    E --> F["Scale program"]
    F --> A
```

## Boundary

Рис. 12.1 не реконструируется как оригинальная оргсхема. Диаграммы — conceptual summary источника.
