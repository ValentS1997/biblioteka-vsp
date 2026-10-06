# Ответы на контрольные вопросы — глава 3

These answers were derived from the chapter and cross-checked against the book's official appendix answer key. Official answer polarity follows the appendix; chapter-grounded rationale is retained, and appendix/chapter conflicts are marked explicitly.

Official appendix provenance: PDF `309–310`.

| № | Ответ | Основание |
|---:|:---:|---|
| 1 | Да | Source frames indexed RAG as improving retrieval speed and accuracy/quality for large datasets. |
| 2 | Да | Nodes plus metadata are used to trace generated output back to source documents/files. |
| 3 | Нет | The source comparison states indexed retrieval is optimized for faster access as datasets grow, while vector similarity search slows with scale. |
| 4 | Да | The chapter presents the LlamaIndex + Deep Lake + OpenAI integration as a compact integrated implementation. |
| 5 | Нет | The chapter presents these as mechanisms demonstrated in the chapter and explicitly says there is no universal single indexing choice; it does not claim they are the only possible index types. |
| 6 | Нет | KeywordTableIndex is described as extracting keywords and mapping them into a keyword→node/document-ID table; the source does not describe it as semantic-understanding-based retrieval. |
| 7 | Да | The chapter states that chunking, embedding generation and related processing can be handled automatically by the integrated frameworks. |
| 8 | Да | Metadata is presented as the mechanism that preserves source filename/path and enables traceability. |
| 9 | Нет | Source table says indexed search requires reindexing when data is updated. |
| 10 | Да, в смысле оценки соответствия ответа запросу | The chapter computes semantic cosine similarity between `user_input` and the RAG response as part of response/query quality evaluation. |

## Provenance by answer

- 1: `p0080:c01–p0084:c01`
- 2: `p0081:c01–p0083:c01`, `p0092:c01–p0094:c01`
- 3: `p0081:c01`, `p0084:c01`
- 4: `p0083:c01–p0085:c01`
- 5: `p0094:c01–p0096:c01`
- 6: `p0105:c01–p0106:c01`
- 7: `p0083:c01`, `p0093:c01–p0094:c01`
- 8: `p0083:c01`, `p0092:c01–p0093:c01`
- 9: `p0084:c01`
- 10: `p0095:c01–p0096:c01`, `p0102:c01–p0107:c01`

## Precision note for question 10

The source wording of the question says «точность запроса». In the implementation, cosine similarity is applied to `user_input` and the generated response to evaluate their similarity/response quality. This answer preserves that implementation meaning rather than broadening it beyond the chapter.
