# Diagram — глава 5

Provenance: `p0136:c01–p0160:c01`.

```mermaid
flowchart TD
    U[User query] --> R{Current ranking}

    R -->|1-2| N[No RAG: text_input = user_input]
    R -->|3-4 narrative| H[Expert-feedback document]
    R -->|5| K[Keyword retrieval]

    H --> G[GPT-4o generator]
    K --> G
    N --> G

    G --> A[Generated answer]
    A --> T[Response time]
    A --> C[TF-IDF cosine similarity]
    A --> UR[User rating 1-5]

    UR --> S[Update feedback statistics]
    S --> X{Expert trigger}
    X -->|triggered| UI[Thumbs up/down + comment]
    UI --> F[expert_feedback.txt]

    F --> H
```

## Interpretation

- Ranking changes the augmentation strategy.
- Automated metrics and user ratings are separate signals.
- Expert feedback is intended to become reusable retrieval/augmentation material.
- Source code has inconsistencies in the 3–4 branch and expert trigger; see README/commands.
