# Резюме главы 7

Source section: explicit chapter-end «Резюме» in `p0225:c01`.

The chapter builds a scalable knowledge-graph RAG system with Wikipedia API, Deep Lake and LlamaIndex.

Three components are implemented.

1. **Document collection**
   - choose a Wikipedia topic;
   - collect page metadata, summaries and linked-page URLs;
   - save citations and source URLs;
   - prepare linked documents for ingestion.

2. **Vector database**
   - reuse/adapt the Deep Lake workflow;
   - store vectorized Wikipedia content;
   - retain file metadata, text and embeddings.

3. **Indexed knowledge-graph RAG**
   - build a `KnowledgeGraphIndex`;
   - visualize relationships through a graph;
   - query the graph using the LlamaIndex query engine;
   - inspect/rerank source nodes;
   - evaluate responses using SentenceTransformer cosine similarity and human feedback.

The chapter emphasizes that the system is reusable for topics beyond marketing. It also identifies an important scaling boundary: the vector database can grow broadly, but loading the entire dataset into the knowledge-graph index may become a constraint. The source suggests loading subsets or separating Deep Lake datasets by topic as possible project-level strategies.

Evaluation uses multiple query examples and descriptive statistics rather than one score. Human feedback is kept distinct from mathematical similarity.

The chapter transitions to short-lived/dynamic RAG in chapter 8.

## Provenance

- Summary source: `p0225:c01`
- Cross-check: `p0199:c01–p0224:c01`
