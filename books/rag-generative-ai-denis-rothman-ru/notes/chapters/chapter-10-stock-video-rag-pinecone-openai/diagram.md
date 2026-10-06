# Diagram — глава 10

Provenance: `p0271:c01–p0306:c01`.

```mermaid
flowchart TD
    A[Text idea / source video] --> B[Generator]
    B --> C[MP4 video]
    C --> D[Split into JPG frames]

    D --> E[Sample frames]
    E --> F[Vision Commentator]
    F --> G[Technical comments]
    G --> H[CSV: ID / Frame / Comment / File]

    H --> I[Embedding / Pinecone ingestion]
    I --> J[Pinecone vector index]

    K[User query] --> L[Query embedding]
    L --> M[Pinecone query]
    J --> M

    M --> N[comment + score + frame_number + file_name]
    N --> O[Resolve MP4/JPG from file storage]
    O --> P[Display source media]

    N --> Q[Video Expert GPT-4o]
    Q --> R[Find inconsistencies]
    R --> S[Rewrite comment]
    S --> T[Assign label]

    S --> U[SentenceTransformer similarity]
    V[Human feedback comment] --> U
    N --> W[Retrieval score]
    U --> X[Aggregate evaluation]
    W --> X
```

## Interpretation

- Pinecone is used for semantic comment retrieval, not necessarily for storing raw video files.
- Metadata is the bridge from vector search back to exact media.
- Video Expert is a second-stage reasoning/rewrite agent after retrieval.
- Human feedback remains part of final quality evaluation.
