# Глава 9 — Mermaid: от малого количества данных к решению

**Source:** EPUB spine 36–39, `OPS/ch1-34.xhtml` → `OPS/ch1-37.xhtml`; RAG `e0036:c01`, `e0037:c01–c07`, `e0038:c01–c08`, `e0039:c01–c05`.

## 1. Beta update

```mermaid
flowchart LR
    A["Prior Beta(α,β)"] --> C["Observe hit / miss"]
    B["Binary sample"] --> C
    C --> D["α' = α + hits"]
    C --> E["β' = β + misses"]
    D --> F["Posterior Beta(α',β')"]
    E --> F
    F --> G["Updated frequency uncertainty"]
```

## 2. Multiple conditions

```mermaid
flowchart TD
    A["Many risk conditions"] --> B{"Enough combinations to estimate directly?"}
    B -->|No / fast expert model| C["LOSH: estimate each condition effect"]
    B -->|Regression skill + scenarios| D["Lens model"]
    C --> E["Check correlation / extreme combinations"]
    D --> F["30–50 scenarios per expert + averaged judgments"]
    F --> G["Logistic regression"]
    E --> H["Conditional probability model"]
    G --> H
```

## 3. Value of Information

```mermaid
flowchart TD
    A["Decision under uncertainty"] --> B["Estimate error probability"]
    A --> C["Estimate cost of error"]
    B --> D["EOL"]
    C --> D
    D --> E["Compute upper-bound value of perfect information (EVPI)"]
    E --> F{"Potential value > cost of measurement?"}
    F -->|Yes| G["Collect targeted evidence"]
    F -->|No| H["Do not over-invest in measurement"]
```

## 4. Empirical update loop

```mermaid
flowchart LR
    A["Historical X / Y data"] --> B["Estimate P(Y|X)"]
    B --> C["Beta uncertainty if sample is small"]
    C --> D["Feed conditionals into multi-condition model"]
    D --> E["Decision / control choice"]
    E --> F["New observations"]
    F --> A
```

## Boundary

ЛОШ source formula/sign conflict and `P(Y|X)` prose/formula state conflict are preserved in `source-findings.md`. Figures 9.x/tables 9.x are not reconstructed as originals.
