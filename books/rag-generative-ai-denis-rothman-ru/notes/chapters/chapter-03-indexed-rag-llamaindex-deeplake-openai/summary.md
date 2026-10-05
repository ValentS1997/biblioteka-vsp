# Резюме главы 3

Source section: explicit chapter-end «Резюме» in `p0108:c01`.

This file preserves the source meaning with structural cleanup and concise paraphrase.

The chapter introduces indexed RAG as a way to improve retrieval speed and, importantly, traceability. Documents are converted into nodes containing chunks and metadata so generated responses can be connected back to source data.

The implementation integrates:
- LlamaIndex;
- Deep Lake;
- OpenAI models.

The pipeline remains split into components so separate teams can work in parallel on:
- document collection/preparation;
- vector-store creation and data processing;
- indexed retrieval and generation;
- evaluation.

The chapter uses a drone-related dataset and intentionally includes noisy, weakly related information to simulate imperfect project data.

Key mechanisms covered:
- vector databases;
- datasets;
- text chunking;
- embeddings;
- nodes;
- metadata;
- ranking;
- indexing.

Four index strategies are implemented or discussed in the practical flow:
- vector;
- tree;
- list;
- keyword table.

For evaluation, the source compares output/retrieval quality and query execution time. The resulting performance indicator is treated as a comparative aid rather than an absolute score.

The source concludes that provenance, indexing and integrated tooling provide a more controllable RAG pipeline, and prepares the transition to multimodal data in chapter 4.

## Provenance

- Summary source: `p0108:c01`
- Context cross-check: `p0080:c01–p0107:c01`
