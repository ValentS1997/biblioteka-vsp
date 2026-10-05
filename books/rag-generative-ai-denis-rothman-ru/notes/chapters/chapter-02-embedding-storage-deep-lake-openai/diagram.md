# Diagram — глава 2

Provenance: `p0052:c01–p0079:c01`.

```mermaid
flowchart LR
    subgraph C1["Component 1 — Data collection / preparation"]
      A[External/source documents] --> B[Fetch]
      B --> C[Clean]
      C --> D[llm.txt]
    end

    subgraph C2["Component 2 — Embeddings / storage"]
      D --> E[Read + verify source]
      E --> F[Chunk text]
      F --> G[Embedding function]
      G --> H[Deep Lake VectorStore]
      F --> H
      H --> I[Text + metadata + embedding + id]
    end

    subgraph C3["Component 3 — Augmented generation"]
      J[User prompt] --> K[Embed/query]
      H --> K
      K --> L[Top result]
      L --> M[Augmented input]
      J --> M
      M --> N[GPT-4o]
      N --> O[Generated response]
      O --> P[Evaluation]
      M --> P
    end

    P --> P1[TF-IDF cosine similarity]
    P --> P2[SentenceTransformer similarity]

    Q[Environment / dependencies / credentials] -.-> C1
    Q -.-> C2
    Q -.-> C3
```

## Interpretation

- Component 1 owns collection and cleaning.
- Component 2 owns chunking, embedding generation and vector storage.
- Component 3 owns retrieval, augmentation, generation and evaluation.
- The pipeline is intentionally decomposed so teams can develop/maintain components independently.
- Source example keeps metadata linking stored chunks back to `llm.txt`.
- Evaluation compares generated output to the original or augmented input; the chapter demonstrates that metric choice changes the numeric result.
