# Cheatsheet — глава 3

Provenance: `rag-generative-ai-denis-rothman-ru:p0080:c01–p0109:c01`.

## Symptom / problem framing

Vector similarity search becomes less attractive as datasets grow because retrieval compares embeddings across many records. The chapter introduces indexing to organize data for faster retrieval and to improve traceability of generated answers back to source documents.

## Baseline / context

Source architecture keeps the same three-component decomposition as chapter 2, but adds index-specific behavior:

| Component | Role |
|---|---|
| Component 1 | collect/clean source documents and preserve source metadata |
| Component 2 | create/populate Deep Lake vector store and let the integration handle chunks/embeddings |
| Component 3 | build/query indexes, synthesize answer with LLM and expose source nodes |
| E1 | evaluate quality and execution time |

## Read-only checks

Before changing anything:

1. Inspect `./data/` and confirm source documents loaded.
2. Inspect first `SimpleDirectoryReader` document and metadata.
3. Confirm expected metadata:
   - `file_path`;
   - `file_name`;
   - file type/size/timestamps where present;
   - node/document identifiers.
4. Load Deep Lake dataset and inspect:
   - text;
   - metadata;
   - embedding;
   - id.
5. Display a record before relying on source traceability.
6. For a query result inspect:
   - `response.source_nodes`;
   - node IDs;
   - scores;
   - node text;
   - file/source metadata.
7. Measure query execution time separately from output quality.
8. Keep comparison parameters identical when comparing index strategies.

## Interpretation

### Vector similarity vs indexed search

Source comparison:

| Property | Vector similarity search | Indexed search |
|---|---|---|
| Flexibility | high | medium / precomputed structure |
| Speed | degrades as dataset grows | optimized for faster retrieval |
| Scalability | limited by real-time processing | better for large datasets |
| Complexity | simpler | extra indexing stage |
| Updates | easy | data updates require reindexing |

### Provenance

Traceability is implemented through metadata and nodes. Source data is loaded as documents; chunks become nodes; metadata allows the response path to be traced back toward the original file.

### Automatic processing

In this chapter the integrated tooling takes over several tasks that were explicit in chapter 2:
- chunking;
- embedding creation;
- vector-store population;
- indexing-related processing.

The chapter explicitly notes that chunk size may be selected automatically rather than fixed.

### Index strategies

- **VectorStoreIndex**: embedding-based vector index.
- **TreeIndex**: hierarchical tree organization for navigation through relevant nodes.
- **ListIndex**: source shows resulting class as `SummaryIndex`; query traverses a list-like structure and was slower in the example.
- **KeywordTableIndex**: maps extracted keywords to node/document IDs.

No universal winner is declared. The chapter repeatedly instructs the reader to test strategies on the actual project dataset.

## Next action

Source-grounded sequence:

1. Collect and clean source documents.
2. Store each source in its own file.
3. Load documents with `SimpleDirectoryReader`.
4. Verify source metadata.
5. Create/load Deep Lake vector store.
6. Build initial vector index.
7. Inspect dataset and metadata.
8. Define one baseline `user_input`.
9. Fix comparison parameters.
10. Test:
    - VectorStoreIndex;
    - TreeIndex;
    - ListIndex;
    - KeywordTableIndex.
11. For each:
    - run query;
    - measure execution time;
    - compute similarity metric;
    - inspect source nodes;
    - compare performance indicator.
12. Select index strategy based on actual project requirements rather than the chapter’s single run.

## Modifying action

Source-confirmed state-changing actions:

- package installs;
- `!mkdir data`;
- external HTTP collection;
- writing one source document per file;
- creating/populating Deep Lake dataset;
- `overwrite=True` dataset replacement;
- creation of in-memory/index structures;
- external LLM/embedding workloads through integrated frameworks.

Details and risk classification: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported checks:

- documents load successfully;
- source metadata is visible;
- Deep Lake dataset exists;
- expected tensors are present;
- query returns answer and source nodes;
- top nodes have scores/text/source information;
- execution time is recorded;
- similarity metric is computed;
- performance indicator is comparable across strategies only when parameters/input remain the same.

The chapter provides sample metrics, not production thresholds.

## Rollback

The chapter does not provide a formal rollback for:
- package changes;
- files created in `./data/`;
- remote Deep Lake dataset overwrite;
- index creation;
- API calls.

Rollback: `[Needs confirmation]`.

Especially for `overwrite=True`, the source does not define restoration of the previous dataset.
