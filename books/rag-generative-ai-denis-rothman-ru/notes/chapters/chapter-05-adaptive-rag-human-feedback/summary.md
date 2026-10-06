# Резюме главы 5

Source section: explicit chapter-end «Резюме» in `p0159:c01`.

The chapter introduces human feedback as a critical extension of RAG. Instead of treating retrieval and generation as a fixed pipeline, adaptive RAG changes its behavior using feedback from users and experts.

The practical implementation is hybrid:
- automated retrieval/generation;
- user ratings;
- expert intervention;
- reusable expert feedback.

The chapter builds the workflow from scratch:
- scrape and clean source documents;
- retrieve information by keyword;
- choose an augmentation strategy based on a rating;
- send the resulting input to GPT-4o;
- measure response time and cosine similarity;
- collect user ratings;
- trigger expert evaluation when configured conditions indicate poor results;
- save expert comments for future improvement of the RAG dataset.

The source emphasizes that automatic similarity metrics do not establish factual correctness or user satisfaction. A response can score well algorithmically and still be judged unsatisfactory by users.

The final example stores expert feedback in a local file so it can later improve the RAG dataset. The chapter concludes by presenting adaptive RAG as a continuously improvable system and prepares the move to production-scale RAG in chapter 6.

## Provenance

- Summary source: `p0159:c01`
- Context cross-check: `p0136:c01–p0158:c01`
