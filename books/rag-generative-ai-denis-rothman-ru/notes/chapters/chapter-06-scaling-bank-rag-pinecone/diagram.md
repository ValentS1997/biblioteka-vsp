# Diagram — глава 6

Provenance: `p0161:c01–p0198:c01`.

```mermaid
flowchart TD
    A[Kaggle Bank Customer Churn] --> B[Clean / remove columns]
    B --> C[EDA]
    C --> D[K-means evaluation]
    B --> E[Row -> text chunk]
    E --> F[OpenAI embeddings]
    F --> G[Scale simulation / duplication]
    G --> H[Pinecone serverless index]
    H --> I[Batch upsert]
    I --> J[Index stats / verification]

    K[Target customer profile] --> L[Embedding]
    L --> M[Pinecone top-k query]
    H --> M
    M --> N[Similar customer records]
    N --> O[Combined RAG context]
    K --> O
    O --> P[GPT-4o]
    P --> Q[Personalized retention recommendation]

    R[Cost / limits / latency / region] -.-> F
    R -.-> H
    R -.-> I
    R -.-> M
```

## Interpretation

- Component 1 reduces and understands the dataset before vectorization.
- Component 2 turns records into embeddings and stores them in Pinecone.
- Component 3 uses a target profile as a vector query and augments GPT-4o with similar customer records.
- Cost, API limits and latency are cross-cutting concerns, not post-processing details.
