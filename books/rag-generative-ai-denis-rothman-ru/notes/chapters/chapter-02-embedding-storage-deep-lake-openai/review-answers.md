# Ответы на контрольные вопросы — глава 2

These answers were derived from the chapter and cross-checked against the book's official appendix answer key. Official answer polarity follows the appendix; chapter-grounded rationale is retained, and appendix/chapter conflicts are marked explicitly.

Official appendix provenance: PDF `308–309`.

| № | Ответ | Основание |
|---:|:---:|---|
| 1 | Да | Глава описывает преобразование подготовленного текста в embeddings для vector retrieval. |
| 2 | Нет | Source contrasts rigid keyword matching with embeddings that better capture semantic similarity/context. |
| 3 | Да | Chapter explicitly recommends splitting the RAG pipeline into at least three independent components. |
| 4 | Нет | The implemented pipeline is divided into three components: data preparation, embeddings/storage, and augmented generation. |
| 5 | Да | The Deep Lake VectorStore example accepts an embedding function and stores the resulting embeddings together with text/metadata. |
| 6 | Да | The shown embedding function explicitly defaults to `text-embedding-3-small`. |
| 7 | Да | The chapter emphasizes traceability/visibility of embeddings and their associated source text/metadata. |
| 8 | Нет | The chapter argues against implementing the entire sequence as one monolithic program and separates it into components. |
| 9 | Да | The example chunks `llm.txt` into smaller fragments (`CHUNK_SIZE = 1000`) before embedding/storage. |
| 10 | Да | Cosine similarity is used to evaluate similarity/relevance in the retrieval/generation evaluation section. |

## Provenance by answer

- 1: `p0052:c01–p0054:c01`
- 2: `p0052:c01`
- 3: `p0055:c01–p0057:c01`
- 4: `p0055:c01–p0057:c01`
- 5: `p0067:c01–p0068:c01`
- 6: `p0067:c01`, `p0071:c01`
- 7: `p0054:c01`, `p0068:c01`
- 8: `p0055:c01–p0057:c01`
- 9: `p0053:c01`, `p0066:c01–p0068:c01`
- 10: `p0075:c01–p0077:c01`

## Source contradiction note

The answer to question 6 follows the explicit displayed code. The prose in `p0071:c01` also mentions `text-embedding-ada-002`; this inconsistency is preserved and not externally reconciled.
