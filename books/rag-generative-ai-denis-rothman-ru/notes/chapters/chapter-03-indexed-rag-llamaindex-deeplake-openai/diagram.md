# Diagram — глава 3

Provenance: `p0080:c01–p0109:c01`.

```mermaid
flowchart TD
    A[Noisy / heterogeneous source documents] --> B[Collect + clean]
    B --> C[Separate files in ./data]
    C --> D[SimpleDirectoryReader]
    D --> E[Documents + source metadata]

    E --> F[Deep Lake Vector Store]
    F --> G[Automatic chunking / embeddings / IDs]
    G --> H[Indexed nodes with provenance]

    H --> I{Index strategy}
    I --> I1[VectorStoreIndex]
    I --> I2[TreeIndex]
    I --> I3[ListIndex / SummaryIndex]
    I --> I4[KeywordTableIndex]

    J[Same user_input] --> I1
    J --> I2
    J --> I3
    J --> I4

    K[Same query parameters<br/>k=3, temp=0.1, mt=1024] --> I1
    K --> I2
    K --> I3
    K --> I4

    I1 --> L[Query engine]
    I2 --> L
    I3 --> L
    I4 --> L

    L --> M[Synthesized answer]
    L --> N[Source nodes / scores / metadata]

    M --> O[Semantic similarity]
    N --> P[Traceability check]
    L --> Q[Execution time]

    O --> R[Performance comparison]
    Q --> R
```

## Interpretation

- Source data is preserved as separate documents so metadata can identify exact source files.
- Deep Lake/LlamaIndex handle chunks, embeddings and node/index structures.
- Four index strategies are tested with the same input and parameters.
- Query output is not only the answer: source nodes and metadata are part of the observability/provenance path.
- Performance combines answer/retrieval quality with query time, but source explicitly treats it as comparative, not absolute.
