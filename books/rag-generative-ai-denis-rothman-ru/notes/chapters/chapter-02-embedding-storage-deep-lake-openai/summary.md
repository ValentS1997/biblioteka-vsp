# Резюме главы 2

Source section: explicit chapter-end «Резюме» in `p0077:c01–p0078:c01`.

This file preserves source meaning with structural cleanup and concise paraphrase.

The chapter focuses on document embeddings as a practical mechanism for working with larger RAG datasets. Raw text is prepared, converted into embeddings and stored in a vector database. The source emphasizes that vector stores such as Activeloop expose APIs and visual interfaces that allow users to inspect the source text associated with embeddings, supporting RAG transparency.

The RAG workflow is organized as separate components so different teams can work independently:

1. data collection and preparation;
2. embedding generation and storage;
3. retrieval, input augmentation and generation.

The implementation:
- configures a cross-platform notebook environment;
- handles package/dependency concerns;
- collects and cleans data;
- chunks the prepared text;
- creates embeddings using an OpenAI embedding function;
- stores text, metadata and embeddings in an Activeloop Deep Lake dataset;
- queries the vector store;
- augments a user prompt with the retrieved text;
- sends the result to GPT-4o;
- evaluates similarity with TF-IDF/cosine similarity and a Sentence Transformers model.

The source presents this decomposition as useful for parallel development, specialization and independent component ownership.

The chapter closes by pointing toward the next step: more advanced retrieval and indexing techniques.

## Provenance

- Summary source: `p0077:c01–p0078:c01`
- Context cross-check: `p0052:c01–p0076:c01`
