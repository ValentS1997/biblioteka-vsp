# Cheatsheet — глава 2

Provenance: `rag-generative-ai-denis-rothman-ru:p0052:c01–p0079:c01`.

## Symptom / problem framing

При росте RAG-датасета простого текстового поиска становится недостаточно для подробного семантического извлечения. Глава предлагает преобразовывать подготовленные данные в embeddings, хранить их в vector database и использовать similarity search для поиска контекста перед генерацией ответа.

## Baseline / context

Source pipeline разделен минимум на три независимых компонента:

| Компонент | Source stages | Роль |
|---|---|---|
| 1. Data collection/preparation | D1/D2 | собрать, очистить и подготовить данные |
| 2. Embeddings + storage | D2/D3 | разбить текст, создать embeddings, сохранить в Deep Lake |
| 3. Augmented generation | D4, G1–G4, E1 | запросить vector store, дополнить input, вызвать generator и оценить результат |

Причины разделения, перечисленные в главе:
- specialization;
- scalability;
- parallel development;
- independent maintenance;
- security/privacy separation.

## Read-only checks

Перед изменениями проверить:

1. Подготовлен ли source file:
   - в примере `llm.txt`;
   - source проверяет первые 20 строк.
2. Существует ли vector store:
   - `VectorStore(path=...)`;
   - source выводит `Vector store exists` либо создает новый store.
3. Какова структура dataset:
   - `vector_store.summary()`;
   - tensors: text, metadata, embedding, id в source example.
4. Загружается ли dataset:
   - `deeplake.load(vector_store_path)`.
5. Каков approximate dataset size:
   - `ds.size_approx()`.
6. Что вернул retrieval:
   - top score;
   - top text;
   - source metadata.
7. Что реально отправляется генератору:
   - inspect `augmented_input`.
8. Какие значения дают evaluation metrics:
   - TF-IDF cosine similarity;
   - embedding-based similarity.

## Interpretation

### Raw data → embeddings

Глава определяет embeddings как числовые представления данных. Подготовленный текст:
1. очищается;
2. разбивается на chunks;
3. передается embedding model;
4. сохраняется вместе с text/metadata/id.

В source example:
- `CHUNK_SIZE = 1000`;
- explicit embedding function default: `text-embedding-3-small`;
- vector store: Activeloop Deep Lake.

### Vector store

Vector database используется для:
- хранения high-dimensional embeddings;
- связи embedding с исходным text/metadata;
- optimized retrieval.

Прозрачность — важная часть главы: embedding и исходный text доступны для просмотра, в отличие от знаний, скрытых только в model parameters.

### Retrieval and augmentation

Source flow:

`user_prompt`
→ `vector_store.search(...)`
→ top result
→ `augmented_input = user_prompt + " " + top_text`
→ GPT-4o
→ evaluation.

### Metrics

Глава показывает, что одинаковая метрика может вести себя по-разному в зависимости от сравниваемых текстов:

- source example: user prompt vs generated response → cosine similarity `0.396`;
- augmented input vs generated response → `0.857`;
- Sentence Transformers example → `0.739`.

These are source example outputs, not universal thresholds.

## Next action

Source-grounded implementation sequence:

1. Разделить pipeline на независимые компоненты.
2. Зафиксировать/проверить package versions.
3. Собрать и очистить data.
4. Записать подготовленный source file.
5. Проверить source file.
6. Chunk data.
7. Load/create vector store.
8. Create embeddings with the selected embedding function.
9. Add text + embeddings + metadata to vector store.
10. Verify store summary / size.
11. Query vector store with user input.
12. Inspect top result.
13. Build augmented input.
14. Call generator.
15. Evaluate output.
16. Revisit model/metric/component choices when results do not meet project goals.

## Modifying action

Source-confirmed state-changing actions include:

- package installation;
- mounting Google Drive;
- downloading `grequests.py`;
- writing `/etc/resolv.conf`;
- loading credentials into environment variables;
- fetching external documents;
- writing `llm.txt`;
- creating/filling a Deep Lake dataset;
- downloading Sentence Transformers model/dependencies when needed.

Details and risks: [commands.md](./commands.md).

## Verification / acceptance checks

Source-supported checks:

- data file can be read;
- vector store exists/loads;
- embedding dataset has expected tensors;
- `vector_store.summary()` is inspectable;
- top retrieval result contains score/text/source;
- `augmented_input` includes retrieved context;
- generator returns a response;
- response time can be measured;
- similarity metrics can be computed;
- human interpretation is still needed when numeric similarity is misleading.

No source-defined production SLO/SLA or universal metric threshold is provided.

## Rollback

The chapter does not provide a formal rollback procedure for:
- package installation;
- DNS changes;
- environment-variable changes;
- local file overwrites;
- creation/update of Deep Lake datasets;
- external API calls.

Rollback: `[Needs confirmation]`.

For state-changing examples, perform verification before proceeding to the next pipeline stage.
