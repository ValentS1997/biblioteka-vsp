# Глава 2. Хранение эмбеддингов RAG с помощью Deep Lake и OpenAI

Status: `RAG_GROUNDED`

## Scope

Канонический источник содержимого: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0052:c01–p0079:c01`
- PDF page range: `52–79`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `80`: «Реализация индексированной RAG с помощью LlamaIndex, Deep Lake и OpenAI»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Почему embeddings нужны при росте объемов данных.
2. Преобразование сырых данных в векторы и их хранение в vector store.
3. Прозрачность RAG: связь embedding/text/source остается доступной для просмотра.
4. Организация RAG как трехкомпонентного pipeline:
   - сбор и подготовка данных;
   - создание embeddings и сохранение в vector database;
   - retrieval + augmented generation.
5. Настройка среды и управление зависимостями.
6. Сбор/очистка набора статей, сохранение в `llm.txt`.
7. Chunking документа по `CHUNK_SIZE = 1000`.
8. Создание/загрузка Deep Lake VectorStore.
9. Создание embeddings через OpenAI.
10. Добавление chunks + metadata в Deep Lake dataset.
11. Query vector store, выбор top result и построение augmented input.
12. Generation через GPT-4o.
13. Evaluation:
    - TF-IDF cosine similarity;
    - Sentence Transformers / `all-MiniLM-L6-v2`.
14. Резюме и 10 контрольных вопросов.

## Main principle

Глава переводит концепцию RAG из главы 1 в трехэтапный практический pipeline: подготовить данные, превратить их в embeddings и сохранить в vector store, затем извлечь наиболее релевантные данные, дополнить ими пользовательский запрос и передать результат генеративной модели. Архитектура намеренно разделяется на независимые компоненты для специализации команд, параллельной разработки, масштабирования, обслуживания и разделения доступа.

## Operational boundaries

- Source recommends version pinning, but одновременно описывает риск слишком долгой фиксации версий.
- Package installation and dependency handling are environment-changing operations.
- Writing `/etc/resolv.conf` is explicitly shown for the Colab/Activeloop scenario and changes DNS configuration.
- OpenAI/Activeloop credentials are read from files and loaded into process environment; real tokens are not stored in these artifacts.
- `vector_store.add(...)` changes the remote/vector dataset and invokes embedding generation.
- OpenAI generation and embeddings may be billable; the chapter tells the reader to review provider plans before use.
- Chapter metrics are example-specific and are not universal quality thresholds.

## Source contradiction

A source-level inconsistency is preserved rather than silently corrected:

- `p0067:c01` and the code in `p0071:c01` define `embedding_function(..., model="text-embedding-3-small")`.
- prose near the end of `p0071:c01` says compatibility is provided by `text-embedding-ada-002`.

This collection treats the explicit shown code as the implementation artifact and marks the prose discrepancy as `[Source contradiction]`. No external source was used to reconcile it.

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

Conceptual / architecture:
- `p0052:c01–p0057:c01`

Environment / data preparation:
- `p0058:c01–p0065:c01`

Embeddings / vector store:
- `p0066:c01–p0070:c01`

Retrieval / augmentation / generation:
- `p0071:c01–p0074:c01`

Evaluation:
- `p0075:c01–p0077:c01`

Chapter-end artifacts:
- `p0077:c01–p0079:c01`

Boundary evidence:
- chapter start: `p0052:c01`
- next chapter start: `p0080:c01`
