# Резюме главы 8

Source section: explicit «Резюме» in `p0251:c01`.

The chapter builds a lightweight, short-lived RAG system for scenarios where information is relevant only for a limited time, such as daily meetings.

The implementation uses:
- Hugging Face;
- SciQ;
- Chroma;
- ONNX Runtime;
- spaCy;
- Meta Llama 2.

The workflow:
1. prepares the SciQ science-question dataset;
2. keeps question, correct answer and support fields;
3. builds a combined completion field;
4. creates a temporary Chroma collection;
5. stores more than 10,000 completion documents as vector-searchable content;
6. validates retrieval by querying the collection and comparing retrieved documents with expected completions;
7. uses a meeting-time user prompt to retrieve one relevant document;
8. augments a Llama prompt with that document;
9. generates a short response;
10. discards the collection after the session when persistence is unnecessary.

The source emphasizes speed, low storage cost and operational simplicity. It also warns that semantic robustness degrades as user wording diverges from the dataset’s original questions, so human supervision and continued adjustment remain important.

The final source discussion states that if data should become durable/static rather than short-lived RAG context, fine-tuning is another possible direction. Chapter 9 continues with that topic.

## Provenance

- Summary source: `p0251:c01`
- Cross-check: `p0227:c01–p0250:c01`
