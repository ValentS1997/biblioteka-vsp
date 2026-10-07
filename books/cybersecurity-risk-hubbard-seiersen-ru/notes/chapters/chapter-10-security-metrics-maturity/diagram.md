# Глава 10 — Mermaid: зрелость метрик безопасности

**Source:** EPUB spine 41–42, `OPS/ch1-39.xhtml` → `OPS/ch1-40.xhtml`; RAG `e0041:c01–c04`, `e0042:c01–c05`.

## 1. Maturity path

```mermaid
flowchart LR
    A["Decision / risk question"] --> B["Sparse Data Analysis"]
    B --> C["Security investment"]
    C --> D["Functional metrics"]
    D --> E["Security data marts"]
    E --> F["Predictive + decision models"]
    F --> G["Prescriptive analytics"]
    G --> H["Action / new evidence"]
    H --> B
```

## 2. Functional metrics

```mermaid
flowchart TD
    A["Security function"] --> B["Coverage / configuration"]
    A --> C["Mitigation"]
    B --> D["Deployment actually active?"]
    B --> E["Configuration / logs / alerts work?"]
    B --> F["FP / FN / workflow measured?"]
    C --> G["Time risk exists"]
    C --> H["Time to detect"]
    C --> I["Time to mitigate"]
```

## 3. Analytics classes

```mermaid
flowchart LR
    A["Descriptive"] --> B["What happened / trend?"]
    C["Predictive"] --> D["What outcome is plausible?"]
    E["Prescriptive"] --> F["What action should we take?"]
    D --> F
    B --> D
    G["Decision analysis"] --> F
```

## 4. Sparse-data R example

```mermaid
flowchart TD
    A["Prior belief about control coverage"] --> B["beta.select → α,β"]
    B --> C["Audit sample: successes / failures"]
    C --> D["Posterior beta"]
    D --> E["90% interval"]
    D --> F["Predict future audit outcomes"]
```

## Boundary

R source code contains typographic/extraction defects and an internally inconsistent `rbeta` line; diagrams do not silently correct it. Figures 10.1–10.3 are not reconstructed as original visuals.
