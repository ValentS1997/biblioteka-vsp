# Diagram — глава 7

Provenance: `p0199:c01–p0226:c01`.

```mermaid
flowchart TD
    A[Root Wikipedia topic] --> B[Wikipedia API]
    B --> C[Page summary + linked pages]
    C --> D[Citations file]
    C --> E[URL list]
    E --> F[Fetch / clean documents]
    F --> G[Deep Lake vector store]
    G --> H[Text + metadata + embeddings]

    H --> I[KnowledgeGraphIndex]
    I --> J[NetworkX / PyVis graph]
    J --> K[HTML visualization]

    I --> L[Query engine]
    M[User query] --> L
    L --> N[LLM response]
    L --> O[Source nodes]

    O --> P[SentenceTransformer reranking]
    N --> Q[Cosine score]
    P --> Q
    Q --> R[Automated scores]
    N --> S[Human feedback]
    R --> T[Descriptive statistics]
    S --> T
```

## Interpretation

- Component 1 builds a reproducible source list and citations.
- Component 2 stores prepared documents and provenance in Deep Lake.
- Component 3 derives a knowledge-graph index and exposes query/source-node behavior.
- Automated similarity and human feedback remain distinct evaluation signals.
