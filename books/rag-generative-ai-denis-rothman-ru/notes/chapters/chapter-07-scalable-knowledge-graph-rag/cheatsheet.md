# Cheatsheet — глава 7

Provenance: `p0199:c01–p0226:c01`.

## Symptom / problem framing

As a RAG corpus grows, relationships between documents become difficult to inspect and navigate. The chapter introduces an indexed knowledge graph to make semantic relationships visible and queryable.

## Baseline / context

| Component | Role |
|---|---|
| 1 | Collect Wikipedia pages, metadata, citations and URLs |
| 2 | Store prepared text/metadata/embeddings in Deep Lake |
| 3 | Build/query a LlamaIndex knowledge graph and evaluate responses |

## Read-only checks

1. Confirm root Wikipedia page exists.
2. Inspect page summary and token count.
3. Confirm root page URL.
4. Inspect extracted linked-page URLs/summaries.
5. Verify citations/URLs files before ingestion.
6. Inspect Deep Lake record integrity:
   - ID;
   - file metadata;
   - text;
   - embedding.
7. Confirm graph-index type.
8. Inspect graph query response and source nodes.
9. Record query execution time.
10. Compare automated similarity scores with human feedback.

## Interpretation

### Wikipedia acquisition

The chapter uses a root topic (Marketing) and extracts linked pages through Wikipedia API. It stores:
- citation metadata;
- source URLs;
- page summaries/content.

### Deep Lake

The vector-store component is adapted from chapter 3. The chapter emphasizes component reuse and traceability from stored vector record back to file metadata/text.

### KnowledgeGraphIndex

Source configuration:

```python
KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=2,
    include_embeddings=True,
)
```

The source explains the triplet cap as a memory/time optimization.

### Query parameters

Source example:
- `similarity_top_k = 3`
- `temperature = 0.1`
- `num_output = 1024`

These are chapter example values, not universal defaults.

### Reranking

The chapter reranks returned source nodes using SentenceTransformer embeddings and cosine similarity. It explicitly notes that a mathematically higher-ranked raw document is not necessarily the answer a user prefers.

### Evaluation

Two arrays are kept separately:
- `scores`: automated cosine-similarity results;
- `rscores`: human-feedback scores.

The chapter then computes:
- mean;
- median;
- standard deviation;
- variance;
- min/max;
- range;
- Q1/Q3;
- IQR.

## Next action

1. Choose a root Wikipedia topic.
2. Validate page existence and summary.
3. Extract linked pages and URLs.
4. Save citations and URL list.
5. Fetch/clean linked documents.
6. Populate or connect to Deep Lake.
7. Verify stored record provenance.
8. Build KnowledgeGraphIndex.
9. Export/inspect graph.
10. Configure query engine.
11. Run a baseline query.
12. Inspect source nodes.
13. Optionally rerank nodes.
14. Run multiple evaluation examples.
15. Compare automated and human scores.
16. Analyze descriptive statistics.
17. Revisit retrieval depth, graph size and dataset partitioning if scale becomes a bottleneck.

## Modifying action

State-changing/external operations:
- install Wikipedia-API / sentence-transformers;
- HTTP/API retrieval;
- citation/URL file writes;
- Deep Lake population or overwrite;
- graph HTML file write;
- LLM/embedding workloads.

Details: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported:
- page exists;
- URLs were extracted;
- citation/URL files were written;
- Deep Lake record includes metadata/text/embedding;
- graph-index type is `KnowledgeGraphIndex`;
- graph HTML is generated;
- query returns a response;
- source nodes can be evaluated/reranked;
- ten example scores/human ratings can be collected;
- aggregate statistics can be computed.

No production SLO or universal score threshold is defined.

## Rollback

Formal rollback is not provided for:
- Deep Lake overwrite;
- package changes;
- generated local files;
- external API calls.

Rollback: `[Needs confirmation]`.
