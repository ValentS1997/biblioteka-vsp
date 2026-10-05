# Diagram — глава 1

Provenance: `p0020:c01–p0049:c01`.

```mermaid
flowchart TD
    A[User or automated input G1] --> B{Choose retrieval strategy}
    B -->|Simple RAG| C[Keyword search]
    B -->|Advanced RAG| D[Vector search]
    B -->|Advanced RAG| E[Indexed search]
    B -->|Modular RAG| F[RetrievalComponent selects strategy]

    C --> G[Best matching record]
    D --> G
    E --> G
    F --> G

    G --> H[Evaluate retrieval]
    H --> H1[Cosine similarity E1]
    H --> H2[Enhanced similarity E1]
    H --> H3[Human evaluation E2]

    G --> I[Augment user input G2/G3]
    I --> J[Generator G4: GPT-4o]
    J --> K[Generated response]
    K --> L[Human / metric evaluation]

    M[D1 Collect data] --> N[D2 Process / chunk / vectorize / index]
    N --> O[D3 Store]
    O --> P[D4 Query data]
    P --> G

    T[Teacher T: pretrained / fine-tuned model] --> J
```

## Interpretation

- `D1–D4` represent the retriever side of the chapter ecosystem.
- `G1–G4` represent the generator-side flow from input to generated result.
- `E1/E2` cover automated metrics and human evaluation.
- `T` represents pretrained/fine-tuned model handling.
- The practical implementation in this chapter starts with already prepared `db_records`; full collection/vector-store construction is deferred to later chapters.
