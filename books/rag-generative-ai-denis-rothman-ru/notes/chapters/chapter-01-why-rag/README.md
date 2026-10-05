# Глава 1. Почему именно генерация с дополненной выборкой (RAG)

Status: `RAG_GROUNDED`

## Scope

Канонический источник содержимого: addressable RAG книги `rag-generative-ai-denis-rothman-ru`.

- Source format: PDF
- RAG chunk range: `p0020:c01–p0051:c01`
- PDF page range: `20–51`
- Printed page range: `[Needs confirmation]`
- Chapter boundary: verified
- Next chapter starts at PDF page `52`: «Хранение эмбеддингов RAG с помощью Deep Lake и OpenAI»
- Source SHA-256: `9a2928c7e1e8047f8374d8d196cfac5527a4cffffe81810f5173cc5cbacae332`

No external web or model-memory content is used.

## Chapter map

1. Зачем нужен RAG: ограничение знаний генеративной модели и дополнение внешними данными.
2. Три конфигурации: простая, продвинутая и модульная RAG.
3. RAG и fine-tuning: параметрические и непараметрические знания, выбор и сочетание подходов.
4. Экосистема RAG:
   - Retriever (D): сбор, обработка, хранение, запрос данных.
   - Generator (G): ввод, human feedback, prompt engineering, генерация.
   - Evaluation (E): метрики и оценка человеком.
   - Teacher (T): предварительное обучение и тонкая настройка.
5. Практическая реализация на Python:
   - среда и OpenAI API;
   - generator на GPT-4o;
   - подготовленный `db_records`;
   - пользовательский запрос;
   - cosine similarity и enhanced similarity;
   - keyword search;
   - vector search;
   - indexed search;
   - модульный `RetrievalComponent`.
6. Резюме главы и 10 контрольных вопросов.

## Main principle

RAG добавляет к генеративной модели внешний механизм извлечения информации: релевантный фрагмент находится ретривером, присоединяется к пользовательскому вводу и затем передается генератору. Выбор механизма извлечения зависит от структуры и масштаба данных, а качество нельзя оценивать только одной автоматической метрикой — в главе отдельно подчеркивается роль человеческой оценки.

## Key operational boundaries

- Keyword search показан как простой вариант для структурированных данных и небольших задач.
- Vector search в примере использует TF-IDF и cosine similarity.
- Indexed search использует заранее вычисленную TF-IDF-матрицу для более быстрого сопоставления.
- Модульный подход позволяет выбирать `keyword`, `vector` или `indexed` внутри одного retrieval-компонента.
- Пример главы учебный: сложная обработка больших документов и полноценные vector stores переносятся в последующие главы.
- Числовые значения метрик из примера относятся к конкретному учебному запросу `define a rag store` и конкретному `db_records`; они не являются универсальными порогами качества.

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

Primary conceptual chunks:
- `p0020:c01–p0029:c01`

Primary implementation chunks:
- `p0030:c01–p0049:c01`

Chapter-end artifacts:
- `p0050:c01–p0051:c01`

Boundary evidence:
- chapter start: `p0020:c01`
- next chapter start: `p0052:c01`
