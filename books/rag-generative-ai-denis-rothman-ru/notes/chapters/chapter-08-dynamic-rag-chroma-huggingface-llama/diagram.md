# Diagram — глава 8

Provenance: `p0227:c01–p0252:c01`.

```mermaid
flowchart TD
    A[Fresh daily SciQ dataset] --> B[Filter / clean]
    B --> C[completion = answer + support]
    C --> D[Temporary Chroma collection]
    D --> E[Embeddings]
    E --> F[Bulk validation queries]
    F --> G[spaCy similarity]
    G --> H[Aggregate accuracy]

    I[Meeting-time prompt] --> J[Chroma query]
    D --> J
    J --> K[Retrieved document]
    K --> L[Augmented prompt]
    L --> M[Llama 2 generation]
    M --> N[Meeting answer / summary]

    N --> O{Session finished?}
    O -->|Yes| P[Delete / discard collection]
    O -->|No| I

    Q[Session timer] -.-> B
    Q -.-> D
    Q -.-> J
    Q -.-> M
```

## Interpretation

- The collection is intentionally temporary.
- Validation happens before live meeting use.
- Retrieval and generation are separate stages.
- Human supervision remains important when prompt wording drifts.
- Collection disposal is part of the lifecycle, not an error condition.
