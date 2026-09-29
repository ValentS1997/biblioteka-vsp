# biblioteka-vsp

Приватная библиотека знаний для совместного чтения, разбора и повторного использования книг в других проектах.

## Цель

Для каждой книги репозиторий хранит:

- исходный PDF как неизменяемый источник;
- metadata и provenance;
- воспроизводимый слой подготовки под RAG;
- состояние фактического чтения;
- заметки, вопросы, выводы и глоссарий;
- диаграммы и схемы;
- историю изменений через Git.

Готовые embeddings не считаются каноническими данными и по умолчанию не коммитятся. Канонический RAG-слой должен позволять пересоздать embeddings другой моделью без потери привязки к источнику.

## Структура

```text
books/
├── index.yaml
└── <book-slug>/
    ├── README.md
    ├── source/
    │   └── book.pdf
    ├── metadata.yaml
    ├── rag/
    │   ├── manifest.yaml
    │   ├── text.md
    │   └── chunks.jsonl
    ├── reading/
    │   ├── progress.yaml
    │   └── journal.md
    ├── notes/
    │   ├── glossary.md
    │   ├── questions/
    │   └── chapters/
    └── diagrams/
```

Конкретная папка книги создаётся только после добавления книги в библиотеку.

## Жизненный цикл книги

Inventory, reading и RAG — независимые capabilities. Книга может быть
reading-only и оставаться валидной без RAG.

Когда требуется RAG-dependent работа (например, chapter artifacts), выполняется
одноразовый book onboarding:

```text
BIBLIOTEKA-VSP-BOOK-ONBOARDING v1.0
  ↓
canonical source + provenance
  ↓
full-text extraction + normalization
  ↓
full-book RAG + addressable retrieval
  ↓
BIBLIOTEKA-VSP-BOOK-READINESS v1.0
  ↓
READY_FOR_CHAPTER_ANALYSIS
```

После этого чтение и обучение идут независимо, в фактическом темпе чтения:

```text
reading session
  ↓
reading/progress.yaml
  ↓
reading/journal.md
  ↓
discussion / verification
  ↓
notes / glossary / Q&A / diagrams
  ↓
reviewed commit
```

RAG readiness и reading progress — разные состояния. Наличие всей книги в RAG не означает, что вся книга уже прочитана или обсуждена. И наоборот, `status: in_progress` не означает, что RAG или chapter analysis готовы.

Канонические контракты:

- [Book onboarding v1.0](templates/book-onboarding-v1.0.yaml)
- [Book readiness v1.0](templates/book-readiness-v1.0.yaml)
- [Chapter artifacts v1.4](templates/chapter-artifact-collection-v1.4.yaml)
- [Book lifecycle matrix](docs/BOOK-LIFECYCLE.md)

Readiness вычисляется, а не хранится как новый canonical status:

```bash
python scripts/check_book_readiness.py --book-id <book_id> --capability chapter-analysis
```

## Reading state

`reading/progress.yaml` хранит последний подтверждённый прогресс чтения. Пример:

```yaml
status: reading
current_page: 101
current_chapter: "[Needs confirmation]"

last_session:
  pages: "80-101"
  date: 2026-09-22
```

`reading/journal.md` хранит компактные checkpoints по сессиям:

- что реально прочитано;
- какие вопросы возникли;
- какие понятия были разобраны;
- что осталось непроверенным или неясным;
- ссылки на созданные notes/diagrams.

По умолчанию обсуждение книги ограничивается уже прочитанным диапазоном и ранее обсуждённым материалом. Материал после `current_page` не используется для объяснений, выводов или подсказок без явного запроса пользователя. Это ограничение относится к совместному чтению, а не к технической доступности полного RAG.


## Source PDF storage

PDF is the canonical source artifact and must not be recompressed or rewritten without changing provenance.

PDF files under `books/**/source/` are tracked through Git LFS. Each book records the expected SHA-256 of its source. The RAG build verifies that checksum before generating canonical retrieval artifacts.

## RAG automation

When `books/<book-slug>/source/book.pdf` is pushed to a non-`main` ingest branch, the `Build book RAG` workflow:

1. checks out the Git LFS object;
2. verifies SHA-256;
3. extracts the embedded text layer page by page;
4. generates `rag/text.md`;
5. generates page-traceable `rag/chunks.jsonl`;
6. generates addressable `rag/chunks/**/*.md`;
7. generates deterministic `rag/search-index/**/*.json`;
8. writes `rag/manifest.yaml`;
9. commits generated artifacts back to the same ingest branch.

The workflow does not write directly to `main`.

## Retrieval architecture

Для обычного вопроса по книге retrieval выполняется по небольшим адресуемым chunk-файлам:

```text
question
  → books/<book-slug>/rag/search-index/<deterministic-shard>.json
  → candidate chunk IDs/paths
  → books/<book-slug>/rag/chunks/**/*.md
  → fetch best 1-3 chunks
  → answer + provenance
```

`rag/text.md` и `rag/chunks.jsonl` остаются bulk/reproducibility artifacts. Они не являются query interface и не должны загружаться целиком для обычного ответа.

Machine-readable ограничения режима `RAG-only` находятся в [RAG-RETRIEVAL.yaml](RAG-RETRIEVAL.yaml). В этом режиме запрещён fallback на внешний web и на большие corpus blobs; retrieval miss должен оставаться retrieval miss.

Retrieval использует собственный детерминированный lexical index и не зависит от наличия GitHub code-search index для private repository. Это не vector-semantic search: агент выбирает до трёх информативных токенов, получает до трёх небольших index-shards и затем читает только 1–3 candidate chunks.

## Интеграция с другими проектами

Чтение:

```text
books/index.yaml
  → books/<book-slug>/metadata.yaml
  → books/<book-slug>/rag/manifest.yaml
  → reading/progress.yaml
  → notes / diagrams
```

Запись и вопросы:

```text
external project
  → GitHub Issue / API
  → triage / discussion / verification
  → reviewed knowledge artifact
  → commit
```

Внешние проекты не должны напрямую изменять канонический knowledge layer без review. Основной входящий интерфейс — GitHub Issues. Машиночитаемый контракт описан в [PROTOCOL.md](PROTOCOL.md).

## Source provenance и права

Для каждой книги фиксируется происхождение источника, например:

```yaml
source:
  ownership: purchased        # purchased | freely_available | self_authored
  physical_copy: true
  repository_access: private
  license: "[Needs confirmation]"
```

Факт покупки или владения бумажным экземпляром используется как provenance и сам по себе не трактуется как разрешение на публичное распространение PDF. Исходники хранятся в private repository; иное распространение допускается только при наличии соответствующих прав или лицензии.

## Communication protocol

Текущая версия протокола: `biblioteka-vsp/v1`.

Типы входящих запросов:

- `question` — вопрос по книге или материалу;
- `note` — заметка/наблюдение внешнего проекта;
- `correction` — предложение исправить существующее знание;
- `knowledge-request` — запрос на поиск/синтез знания по библиотеке.

Подробности: [PROTOCOL.md](PROTOCOL.md).

## Текущее состояние

Registry/knowledge lifecycle используется в рабочем режиме. Репозиторий
поддерживает одновременно reading-only и RAG-ready книги; chapter-level RAG
разрешён только после capability-specific readiness check.
