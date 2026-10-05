# Глава 4. Мультимодальная RAG

Status: `RAG_GROUNDED`

## Scope

Канонический источник содержимого: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0110:c01–p0135:c01`
- PDF page range: `110–135`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `136`: «Повышение эффективности RAG за счет обратной связи от эксперта»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Что такое мультимодальная RAG:
   - специализированные модули для разных типов данных;
   - текст + изображения;
   - извлечение из нескольких источников.
2. Текстовый модуль:
   - загрузка Deep Lake dataset по БПЛА;
   - VectorStoreIndex;
   - query engine;
   - LLM response.
3. Мультимодальный модуль:
   - загрузка VisDrone;
   - tensors: `images`, `boxes`, `labels`;
   - навигация по изображениям;
   - bounding boxes.
4. Преобразование labels в документы:
   - `doc_id`;
   - LlamaIndex documents;
   - in-memory vector index.
5. Query VisDrone:
   - один user input используется в обоих модулях;
   - source nodes;
   - keyword extraction;
   - возврат к исходному изображению.
6. Обобщенный вывод:
   - user input;
   - text response;
   - image with bounding boxes.
7. Evaluation:
   - text similarity;
   - GPT-4o image analysis;
   - similarity between target label and image description;
   - combined multimodal score.
8. Резюме и 10 контрольных вопросов.

## Main principle

Мультимодальная RAG в этой главе реализована как модульная система, где один pipeline работает с текстовым dataset, а другой — с image dataset. Оба используют общий user input, но извлекают разный тип контекста. Итоговый ответ объединяет текстовый LLM response и изображение, найденное через source nodes мультимодального индекса.

## Key operational boundaries

- VisDrone загружается read-only.
- DataFrame и in-memory vector index создаются локально/runtime-side.
- `boxed_image.jpg` создается и затем удаляется/пересоздается в workflow.
- GPT-4o image analysis — внешний API workload.
- Base64 encoding не является защитой данных; в главе он используется как транспортное представление.
- Числовые similarity scores относятся только к конкретному примеру.
- Source прямо отмечает, что оценка сложных изображений остается трудной даже при высоких metric scores.
- Человеческая оценка остается важной, что подготавливает переход к главе 5.

## Source inconsistencies

### Dataset chapter reference

- `p0114:c01` говорит, что потребуется датасет «из главы 2».
- `p0115:c01` загружает `drone_v2`, созданный в главе 3.

Status: `[Source contradiction]`.

### Image MIME/type mismatch

- file path: `/content/boxed_image.jpg`
- GPT-4o data URL in `p0132:c01`: `data:image/png;base64,...`

Status: `[Source contradiction]`.

### Score wording vs code

`p0133:c01` текстом говорит о сумме показателей ответа LLM и «двух показателей» мультимодального ответа, но код вычисляет:

`(llm_similarity_score + multimodal_similarity_score) / 2`

Status: `[Source wording/code mismatch]`.

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

Concept / architecture:
- `p0110:c01–p0114:c01`

Text module:
- `p0115:c01–p0117:c01`

VisDrone loading / navigation:
- `p0117:c01–p0123:c01`

Multimodal index / query / source image:
- `p0124:c01–p0129:c01`

Evaluation:
- `p0130:c01–p0133:c01`

Chapter-end artifacts:
- `p0134:c01–p0135:c01`

Boundary evidence:
- chapter start: `p0110:c01`
- next chapter start: `p0136:c01`
