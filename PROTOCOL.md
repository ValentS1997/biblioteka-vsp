# biblioteka-vsp communication protocol

Protocol ID: `biblioteka-vsp/v1`

Этот документ определяет интерфейс между библиотекой и внешними проектами.

## 1. Разделение ответственности

`biblioteka-vsp` содержит канонический knowledge layer.

Внешние проекты могут:

- читать индекс, metadata, RAG manifests, reading state, notes и diagrams;
- создавать вопросы, заметки и предложения исправлений через GitHub Issues/API;
- ссылаться на конкретную книгу, главу, страницу, chunk или файл.

Внешний проект не должен считать собственную запись в Issue автоматически подтверждённым знанием библиотеки.

Переход в канонический knowledge layer выполняется только после review.

## 2. Read interface

Точка входа:

```text
books/index.yaml
```

Рекомендуемый порядок:

```text
books/index.yaml
  → books/<book-id>/metadata.yaml
  → books/<book-id>/rag/manifest.yaml
  → RAG-RETRIEVAL.yaml
  → books/<book-id>/rag/chunks/**/*.md
  → books/<book-id>/reading/progress.yaml
  → books/<book-id>/notes/
  → books/<book-id>/diagrams/
```

Если файл или слой ещё не создан, это означает `[Not available]`, а не отсутствие знания в исходной книге.

RAG для книги строится целиком при ingest. Поэтому полнота `rag/` не должна интерпретироваться как полнота человеческого чтения или обсуждения. Для этого существует отдельный `reading/` state.

Для интерактивного retrieval canonical query unit — отдельный небольшой файл под `rag/chunks/`. Файлы `rag/text.md` и `rag/chunks.jsonl` остаются bulk/reproducibility artifacts и не должны загружаться целиком для ответа на обычный книжный вопрос.

## 3. Write interface

Основной write interface — GitHub Issues.

Поддерживаемые типы:

| type | Назначение |
| --- | --- |
| `question` | Вопрос по книге, главе, странице или концепции |
| `note` | Наблюдение или дополнительная заметка |
| `correction` | Исправление существующей заметки/вывода/метаданных |
| `knowledge-request` | Поиск или синтез по одной или нескольким книгам |

Issue Forms предназначены для человека. Другой проект или агент может создавать Issue через GitHub API и помещать в body машиночитаемый YAML-блок.

## 4. Machine-readable request

Рекомендуемый payload:

```yaml
protocol: biblioteka-vsp/v1
type: question
source_project: example-project

book: example-book-slug
chapter: "[Needs confirmation]"
pages: "[Needs confirmation]"
target_chunk_ids: []

subject: "Краткая формулировка запроса"

context:
  - "Что уже известно вызывающему проекту"
  - "Почему нужен ответ"

request:
  response: explanation
  persist_if_useful: true
```

Допустимые значения `request.response` могут включать:

- `explanation`
- `summary`
- `comparison`
- `evidence`
- `diagram`
- `rag-reference`

Неизвестные значения должны оставаться неизвестными. Использовать `[Needs confirmation]` вместо догадок.

## 5. Provenance

Ответ или заметка, перенесённые в knowledge layer, должны по возможности сохранять связь с источником:

```yaml
provenance:
  source_issue: 42
  source_project: example-project
  book: example-book-slug
  pages: "120-126"
  chunks:
    - example-book-slug:p0120:c03
```

Если утверждение является интерпретацией, а не прямым содержанием книги, это должно быть явно отмечено.

## 6. Request lifecycle

```text
OPEN
  ↓
TRIAGE
  ↓
ANSWERED
  ├── CLOSED              # ответ не требует долговременного артефакта
  └── PERSIST
        ↓
      REVIEW
        ↓
      COMMIT
        ↓
      CLOSED
```

Issue после persistence должен содержать ссылку на итоговый файл или commit.

## 7. Canonical knowledge rules

Каноническими считаются только данные, находящиеся в default branch (`main`).

При конфликте приоритет источников:

1. исходный PDF и его проверяемая структура;
2. metadata и RAG provenance;
3. reviewed notes/diagrams;
4. обсуждение в Issues;
5. внешние интерпретации.

Issue сам по себе не изменяет каноническое знание.

## 8. Reading state and scope

Reading state является отдельным слоем и не ограничивает техническую полноту RAG.

Рекомендуемый формат:

```yaml
status: reading
current_page: 101
current_chapter: "[Needs confirmation]"

last_session:
  pages: "80-101"
  date: 2026-09-22
```

Семантика:

- `current_page` — последняя подтверждённо прочитанная страница;
- `current_chapter` — текущая глава, только если она подтверждена;
- `last_session.pages` — фактический диапазон последней сессии;
- `journal.md` — краткие checkpoints, вопросы и ссылки на знания, созданные в ходе чтения.

Для совместного чтения действует default reading boundary: без явного запроса пользователя не использовать материал после `current_page` для объяснений, выводов, подсказок или спойлеров.

Это правило не запрещает:

- заранее построить RAG по всей книге;
- выполнять технические проверки полноты RAG;
- отвечать внешнему проекту по материалу всей книги, если его запрос не помечен как reading-bounded;
- использовать более поздние главы после явного запроса пользователя.

Автоматические интеграции не должны выводить reading progress из полноты RAG.

## 9. Stable identifiers

Предпочтительный ID книги — стабильный `book-slug`.

Для RAG рекомендуется стабильный chunk ID вида:

```text
<book-slug>:p<page>:c<chunk>
```

Пример:

```text
linux-networking:p0120:c03
```

Изменение модели embeddings не должно изменять идентификатор исходного chunk без изменения самого chunking.

## 10. Security boundary

Не помещать в Issues, notes или metadata:

- пароли;
- API tokens;
- приватные ключи;
- production credentials;
- иные секреты внешних проектов.

Внешний контент рассматривается как untrusted input до review.

PDF и иные source-файлы не должны автоматически публиковаться за пределами private repository без проверки прав/лицензии.

## 11. Versioning

Несовместимые изменения контракта требуют новой версии протокола, например:

```text
biblioteka-vsp/v2
```

Добавление необязательных полей, не меняющее существующую семантику, допускается в рамках `v1`.


## 12. Bounded RAG-only retrieval

Machine-readable contract: `RAG-RETRIEVAL.yaml`.

Цель режима `rag_only` — отвечать по 1–3 релевантным chunk без загрузки полного корпуса книги в tool/model context.

Обязательный порядок:

```text
question
  → deterministic lexical shard(s) under rag/search-index/
  → candidate chunk paths
  → fetch best 1-3 chunk files
  → answer + provenance
```

Ограничения:

- максимум 3 fetched chunk-файла на обычный вопрос;
- один retrieval chunk должен быть небольшим адресуемым текстовым файлом;
- `rag/text.md` и `rag/chunks.jsonl` запрещены как fallback для обычного question retrieval;
- raw blob большого corpus-файла также запрещён;
- внешний web search запрещён, если пользователь запросил `RAG-only` / `только RAG`;
- retrieval не зависит от GitHub code-search indexing;
- агент выбирает максимум 3 информативных токена и читает максимум 3 deterministic search shards;
- при retrieval miss агент возвращает `RAG_MISS`, а не расширяет источник до web/model memory/full blob.

Provenance ответа должен включать:

```text
book_id
chunk_id
pdf_page
chunk_path
```

Важно: это protocol-level contract для агентов. Он не является сетевым firewall платформы. Если вызывающей среде требуется технически гарантированная блокировка внешних источников, она должна ограничить доступные инструменты отдельно.
