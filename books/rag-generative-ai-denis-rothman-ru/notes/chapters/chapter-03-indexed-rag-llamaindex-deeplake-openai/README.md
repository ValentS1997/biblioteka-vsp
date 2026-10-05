# Глава 3. Реализация индексированной RAG с помощью LlamaIndex, Deep Lake и OpenAI

Status: `RAG_GROUNDED`

## Scope

Канонический источник содержимого: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0080:c01–p0109:c01`
- PDF page range: `80–109`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `110`: «Мультимодальная RAG»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Зачем индексировать RAG:
   - ускорение retrieval на больших датасетах;
   - организация неструктурированных chunks в nodes;
   - provenance/traceability до исходного файла и местоположения.
2. Архитектура:
   - component 1: сбор и подготовка документов + metadata;
   - component 2: Deep Lake vector store + chunking + embeddings + storage;
   - component 3: indexed retrieval + LLM synthesis;
   - E1: время выполнения и качество ответа.
3. Сравнение vector similarity search и indexed search:
   - indexed search быстрее и масштабируемее в source framing;
   - цена — предварительная структура и необходимость reindex при обновлениях.
4. Подготовка noisy/unstructured drone corpus.
5. SimpleDirectoryReader:
   - text;
   - file metadata;
   - source paths/names;
   - автоматическая разбивка и node metadata.
6. Deep Lake dataset:
   - text;
   - metadata;
   - embedding;
   - id.
7. Четыре механизма индексирования:
   - VectorStoreIndex;
   - TreeIndex;
   - ListIndex / SummaryIndex;
   - KeywordTableIndex.
8. Query engines with fixed comparison parameters:
   - `similarity_top_k = 3`;
   - `temperature = 0.1`;
   - `num_output = 1024`.
9. Evaluation:
   - semantic cosine similarity via Sentence Transformers;
   - query execution time;
   - combined performance indicator.
10. Резюме и 10 контрольных вопросов.

## Main principle

Глава делает акцент не только на скорости поиска, но и на контролируемости. Indexed RAG организует chunks как nodes и связывает их с metadata, что позволяет получать не только synthesized answer, но и сведения об источниках ответа. LlamaIndex, Deep Lake и OpenAI используются как интегрированный pipeline, а несколько index strategies сравниваются на одном user input и одинаковых query parameters.

## Key operational boundaries

- `overwrite=True` при создании Deep Lake vector store перезаписывает существующий dataset; это state-changing action с повышенным риском.
- Source states that indexed search requires reindexing after data updates.
- Dataset numeric index positions are unstable after dataset changes; unique IDs remain the more stable identity in source discussion.
- The chapter intentionally includes noisy/unrelated documents to test indexed RAG under imperfect data conditions.
- Performance numbers are example-specific and stochastic; source explicitly warns not to generalize one run.
- No source-defined production acceptance threshold is provided.
- Metadata is central to traceability; removing it would undermine one of the chapter’s main goals.

## Source inconsistencies

### Package version

- `p0085:c01`: `llama-index-vector-stores-deeplake==0.1.6`
- `p0097:c01`: prose says the model/query mechanism is installed with `llama-index-vector-stores-deeplake==0.1.2`

Status: `[Source contradiction]`.

### Dataset visualization path

- dataset path used in code: `hub://.../drone_v2`
- one visualization URL in `p0091:c01` points to `drone_v1`

Status: `[Source contradiction]`.

### Extracted syntax

`p0090:c01` contains an isolated closing parenthesis after `VectorStoreIndex.from_documents(...)`. The intended call is structurally clear, but the artifact records this as `[Source extraction issue]` rather than treating it as a substantive code instruction.

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

Architecture and motivation:
- `p0080:c01–p0085:c01`

Data collection / metadata / vector store:
- `p0086:c01–p0094:c01`

Query setup and vector index:
- `p0095:c01–p0100:c01`

Tree / list / keyword indexes:
- `p0100:c01–p0107:c01`

Chapter-end artifacts:
- `p0108:c01–p0109:c01`

Boundary evidence:
- chapter start: `p0080:c01`
- next chapter start: `p0110:c01`
