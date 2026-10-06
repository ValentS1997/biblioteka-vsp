# Глава 7. Создание масштабируемой RAG на основе графа знаний с помощью API Википедии и LlamaIndex

Status: `RAG_GROUNDED`

## Scope

- Book ID: `rag-generative-ai-denis-rothman-ru`
- RAG chunk range: `p0199:c01–p0226:c01`
- PDF pages: `199–226`
- Printed page range: `[Needs confirmation]`
- Next chapter starts at PDF page `227`: «Создание динамических RAG с помощью Chroma и Hugging Face Llama»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

Source policy: strict `rag_only`. No external web/model-memory fallback used.

## Chapter map

1. Why a knowledge graph:
   - visualize relationships in heterogeneous data;
   - add semantic structure to a growing RAG corpus.
2. Three-component architecture:
   - Wikipedia API collection and metadata/citations;
   - Deep Lake vector storage;
   - LlamaIndex KnowledgeGraphIndex and querying.
3. Wikipedia corpus generation:
   - root topic;
   - page summary;
   - links and URLs;
   - citations file;
   - URLs file.
4. Deep Lake ingestion:
   - reuse of the chapter-3 data/vector pipeline;
   - metadata + text + embedding traceability.
5. Knowledge graph:
   - `KnowledgeGraphIndex.from_documents(...)`;
   - `max_triplets_per_chunk=2`;
   - `include_embeddings=True`.
6. Graph visualization:
   - NetworkX graph;
   - PyVis;
   - HTML output.
7. Query / reranking:
   - query engine;
   - source nodes;
   - SentenceTransformer cosine similarity;
   - reranking of returned nodes.
8. Evaluation:
   - ten examples;
   - cosine scores;
   - human feedback scores;
   - descriptive statistics.
9. Explicit chapter-end summary and 10 review questions.

## Main principle

The chapter combines source acquisition, vector storage and graph indexing into one scalable RAG workflow. The knowledge graph is used to expose relationships between documents/nodes, while metadata and source files retain provenance. The source also stresses that graph-index loading can become a scaling constraint as the vector database grows.

## Operational boundaries

- Wikipedia retrieval is an external workload.
- Citation/URL files are local state-changing writes.
- Deep Lake population is remote state-changing.
- `ow=True` explicitly enables overwrite of an existing Deep Lake dataset.
- Knowledge-graph generation is compute-intensive; source example reports ~372 s.
- PyVis graph export writes a local HTML file.
- SentenceTransformer installation changes the runtime environment.
- LLM/query results are stochastic; source warns scores may differ across runs.
- Human feedback is treated as separate evidence from cosine similarity.
- No formal rollback procedure is defined for a Deep Lake overwrite.

## Source issues

### Invalid exception form

`p0209:c01` shows:

`except page.exists()==False:`

This is not valid Python exception syntax.

Status: `[Source code issue]`.

### Hugging Face token extraction/import

`p0218:c01` is extracted as:

`from google.colab import`
`userdata userdata.get('HF_TOKEN')`

Status: `[Source extraction issue]`.

### Destructive dataset setting

`p0211:c01` defines `ow=True` and explicitly says that this rewrites the existing dataset.

Status: source-confirmed remote overwrite risk.

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [summary.md](./summary.md)
- [review-questions.md](./review-questions.md)
- [review-answers.md](./review-answers.md)

## Provenance

- Architecture: `p0199:c01–p0205:c01`
- Wikipedia collection: `p0206:c01–p0211:c01`
- Deep Lake: `p0211:c01–p0212:c01`
- Knowledge graph/query: `p0214:c01–p0219:c01`
- Evaluation: `p0220:c01–p0224:c01`
- Summary/questions: `p0225:c01–p0226:c01`
