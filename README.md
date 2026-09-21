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

Технический ingest выполняется сразу для всей книги:

```text
PDF
  ↓
Git / source provenance
  ↓
full-text extraction + normalization
  ↓
full-book RAG chunks + manifest
  ↓
book is RAG-ready
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

RAG readiness и reading progress — разные состояния. Наличие всей книги в RAG не означает, что вся книга уже прочитана или обсуждена.

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

Bootstrap-структура создана. Каталог книг пока пуст.
