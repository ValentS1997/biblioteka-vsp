# Глава 6. Масштабирование банковских данных клиентов в системе RAG с помощью Pinecone

Status: `RAG_GROUNDED`

## Scope

Канонический источник: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0161:c01–p0198:c01`
- PDF page range: `161–198`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `199`: «Создание масштабируемой RAG на основе графа знаний с помощью API Википедии и LlamaIndex»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Архитектура масштабированной RAG:
   - component 1: data collection / EDA / clustering;
   - component 2: embeddings + Pinecone index + upsert/query;
   - component 3: target-vector RAG + GPT-4o recommendations.
2. Bank Customer Churn:
   - Kaggle authentication/download;
   - CSV processing;
   - removal of selected columns;
   - EDA.
3. ML analysis:
   - StandardScaler;
   - k-means;
   - silhouette score;
   - Davies–Bouldin index.
4. Embedding pipeline:
   - row → text chunk;
   - `text-embedding-3-small`;
   - batch processing;
   - rate-limit pauses.
5. Scaling simulation:
   - duplicate chunks/embeddings;
   - 50,000-point example;
   - chapter framing extends the pattern toward 1M+ vectors.
6. Pinecone:
   - serverless spec;
   - cosine metric;
   - dimension 1536;
   - metadata;
   - batch upsert;
   - index statistics;
   - vector query.
7. RAG generation:
   - target customer vector;
   - top-k similar profiles;
   - combined context;
   - GPT-4o personalized retention email.
8. Резюме и 10 контрольных вопросов.

## Main principle

Chapter 6 treats scaling as an architecture and operations problem, not merely “more data”. The source repeatedly emphasizes dataset preparation, cost, API limits, cloud region, read/write consumption, batch sizing, latency and verification before moving to larger vector volumes.

## Operational boundaries

- Kaggle/OpenAI/Pinecone credentials are secret-bearing runtime inputs.
- Kaggle download/extraction and CSV writes modify local runtime state.
- Pinecone index creation and `upsert` modify remote state and may incur cost.
- Data duplication in this chapter is a scaling simulation; duplicated rows are not new independent observations.
- OpenAI embedding generation and GPT-4o calls are external/billable workloads.
- Pinecone cloud/region, model choice, request limits and pricing are explicitly treated as project constraints.
- Chapter timings and scores are experiment-specific, not SLOs.
- No formal rollback for remote Pinecone upserts/index creation is supplied.

## Source inconsistencies / extraction issues

### Ratio described as correlation

`p0170:c01` computes:

`sum_complain / sum_exited * 100 = 100.29%`

and the surrounding prose describes this as a strong correlation.

Status: `[Source wording/code mismatch]` — the artifact preserves the computation and the source wording separately.

### Upsert timing mismatch

- `p0188:c01`: 50,000 items, `560.66 s`.
- `p0189:c01`: prose says 10,000 points take about one minute / `56 s`.

Status: `[Source inconsistency]`.

### Query variable mismatch

`p0192:c01` defines `query_text`; `p0193:c01` then shows:

`query_embedding = get_embedding(text, model=embedding_model)`

Status: `[Source code mismatch]`.

### GPT model string extraction

`p0195:c01` contains:

`gpt_model = "gpt-4o`

without a visible closing quote.

Status: `[Source extraction issue]`.

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [summary.md](./summary.md)
- [review-questions.md](./review-questions.md)
- [review-answers.md](./review-answers.md)

## RAG provenance used

Architecture / data preparation:
- `p0161:c01–p0169:c01`

EDA / ML:
- `p0169:c01–p0176:c01`

Scaling / embeddings / Pinecone:
- `p0177:c01–p0190:c01`

RAG generation:
- `p0191:c01–p0197:c01`

Chapter-end:
- `p0197:c01–p0198:c01`

Boundary evidence:
- chapter start: `p0161:c01`
- next chapter start: `p0199:c01`
