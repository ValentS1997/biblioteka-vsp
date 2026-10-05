# Резюме главы 1

Source section: explicit chapter-end «Резюме» in `p0050:c01`.

This file preserves the source meaning with structural cleanup and concise paraphrase.

RAG in this chapter is built around two core components: a retriever and a generator. The retriever processes available data and selects a retrieval method; the retrieved information is appended to the user input and passed to a generative model, which produces the final response.

Three configurations are distinguished:

- **Simple RAG** — basic retrieval such as keyword matching.
- **Advanced RAG** — more sophisticated retrieval with vector representations and indexing.
- **Modular RAG** — combines simple and advanced retrieval methods and can include other machine-learning techniques.

The chapter contrasts:
- parametric knowledge stored in model weights;
- non-parametric explicit data available to RAG at query time.

RAG and fine-tuning are not treated as mutually exclusive. Large, difficult-to-manage RAG datasets may motivate fine-tuning, while frequently changing information favors an external retrieval mechanism.

The broader ecosystem is described through:
- retriever;
- generator;
- evaluation;
- teacher/fine-tuning functions.

The practical section implements educational Python examples of:
- keyword matching;
- TF-IDF/vector search;
- indexed retrieval;
- modular retrieval;
- input augmentation;
- GPT-4o generation;
- retrieval evaluation with cosine and enhanced similarity.

The source closes by stating that chapter 2 moves from these basic retrieval examples to transforming data into vectors and storing them in vector databases.

## Provenance

- Summary source: `rag-generative-ai-denis-rothman-ru:p0050:c01`
- Context cross-check: `p0023:c01–p0049:c01`
