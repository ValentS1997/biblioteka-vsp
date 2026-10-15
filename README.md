# biblioteka-vsp

Приватная библиотека знаний для совместного чтения, разбора и повторного использования книг в других проектах.

## Где найти выжимки и материалы по книгам

1. Откройте [реестр библиотеки](registry/README.md) и найдите книгу в таблице **«Покрытие knowledge-проектов»**. Столбец **«Выжимки»** показывает, есть ли готовые материалы и по скольким главам.
2. В той же строке найдите **Knowledge ID** — это название папки книги в [`books/`](books/). Откройте её и перейдите в `notes/chapters/README.md`: там список разобранных глав со ссылками.
3. Выберите нужную главу. Обычно `summary.md` — конспект, `cheatsheet.md` — короткая шпаргалка, `commands.md` — команды, а `visual-cheatsheet.svg` — наглядная схема. Набор файлов зависит от главы.

**Пример:** [«Docker без секретов» — список глав](books/docker-demystified-saibal-ghosh-ru-2023/notes/chapters/README.md) → [конспект главы 1](books/docker-demystified-saibal-ghosh-ru-2023/notes/chapters/chapter-01-containerization-and-docker/summary.md).

В некоторых книгах есть также материалы по книге целиком в `notes/book-synthesis/`. **Важно:** наличие RAG не означает наличие выжимок; ориентируйтесь на столбец «Выжимки». Для открытия ссылок нужен доступ к приватному репозиторию.

## Цель

Для каждой книги репозиторий хранит:

- исходный PDF или EPUB как неизменяемый канонический источник;
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
    │   └── book.pdf | book.epub
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
BIBLIOTEKA-VSP-BOOK-ONBOARDING v1.3
  ↓
canonical source + provenance
  ↓
full-text extraction + normalization
  ↓
full-book RAG + addressable retrieval
  ↓
BIBLIOTEKA-VSP-BOOK-READINESS v1.3
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

Канонические шаблоны и контракты:

- [Templates index](templates/README.md)
- [Process compliance router v1.2](templates/process-compliance-router-v1.2.yaml)
- [Git execution policy v1.0](templates/git-execution-policy-v1.0.yaml)
- [New book branch bootstrap v1.3](templates/book-branch-bootstrap-v1.4.yaml)
- [Book onboarding v1.3](templates/book-onboarding-v1.3.yaml)
- [RAG ingestion acceptance v1.0](templates/rag-ingestion-acceptance-v1.0.yaml)
- [Book readiness v1.3](templates/book-readiness-v1.3.yaml)
- [Chapter analysis request v1.3](templates/chapter-analysis-request-v1.4.yaml)
- [Chapter artifacts v1.8](templates/chapter-artifact-collection-v1.8.yaml)
- [Chapter publication: direct Git + progress v1.0](templates/chapter-publication-v1.0.yaml)
- [Chat recovery: durable Git checkpoint v1.0](templates/session-recovery-v1.0.yaml)
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


## Git execution policy

Routine Git work is remote-first and agent-owned. Branch creation, text-file
changes, PRs, merges, CI inspection and repository read-back should be performed
through GitHub connector/API or repository automation when available.

User-local Git is exception-only. It must not be requested for convenience.
Every local request must identify a valid reason code, prove why remote methods
are insufficient, limit the local scope, define verification/rollback and state
where the workflow resumes remotely.

For book ingest the expected exception is `GIT_LFS_BINARY_UPLOAD_REQUIRED`:
the available connector cannot upload the exact canonical PDF/EPUB source as a real Git LFS object.
Only that minimal source upload may fall back to local Git; subsequent
RAG/PR/CI/readiness returns to GitHub tools.

## Canonical source storage

PDF and EPUB are supported canonical source artifacts. The uploaded format is preserved; EPUB is not silently converted to PDF and PDF is not silently converted to EPUB.

Supported source files under `books/**/source/` are tracked through Git LFS. Each book records the expected SHA-256 of the exact canonical source. The RAG build verifies that checksum before generating canonical retrieval artifacts.

## RAG automation

When `books/<book-slug>/source/book.pdf` or `book.epub` is pushed to a non-`main` ingest branch, the `Build book RAG` workflow:

1. checks out the Git LFS object;
2. verifies SHA-256;
3. extracts deterministic source units: PDF pages or EPUB spine/XHTML items;
4. generates `rag/text.md`;
5. generates source-traceable `rag/chunks.jsonl`;
6. generates addressable `rag/chunks/**/*.md`;
7. generates deterministic `rag/search-index/**/*.json`;
8. writes generation identity into `rag/manifest.yaml`;
9. runs strict RAG ingestion acceptance across source integrity, complete
   provenance/content hashes, source-unit coverage, bounded retrieval samples
   and negative exact-term behavior;
10. writes `rag/acceptance.yaml`;
11. commits generated artifacts back to the ingest branch only on ACCEPTED.

PDF provenance remains page-based. EPUB provenance uses 1-indexed spine items plus XHTML ZIP-member locators; these are not treated as printed/PDF page numbers.

New/rebuilt RAG generations carry deterministic `corpus_generation_id` and
`index_generation_id`. Addressable chunks preserve compatibility `chunk_id`
and add `chunk_uid` + `text_sha256` so silent content/chunking drift can be
detected. Existing legacy RAG is not mass-rebuilt; strict acceptance becomes
mandatory when a legacy book is rebuilt by the current pipeline.

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

## Публикация глав — только в Git

Каждый книжный чат перед анализом главы показывает число глав по проверенному
RAG-оглавлению и прогресс публикации (сколько глав уже закоммичено, сколько
осталось, какие номера опубликованы, ветка и SHA). Неизвестное общее число
глав явно помечается как `[Needs confirmation]`: нельзя брать знаменатель
из числа существующих папок. Инструмент проверки:
`scripts/chapter_publication_status.py --book-id <book_id>`.

Каждая глава публикуется как **отдельные Markdown/SVG-файлы** непосредственно
в книжную GitHub-ветку с Git read-back, ссылками на commit/PR и проверкой CI.
ZIP и другие архивы либо ссылка на скачивание вместо Git-записи запрещены.
Если все файлы текущей главы записать невозможно, ассистент обязан немедленно
сообщить точные сохранённые Git-пути, недостающие файлы и причину остановки,
не объявляя главу завершённой. Прогресс создания конспектов не изменяет
`reading/progress.yaml`.

## Восстановление после обрыва обсуждения

Если ChatGPT сообщает о предельной длине обсуждения, прерывается или после
обновления страницы исчезает промежуточный вывод, используйте команду
**«Ковальски, проверка после обрыва связи»** — в этом или новом чате проекта.

По `templates/session-recovery-v1.0.yaml` агент сначала восстанавливает
состояние **по GitHub**: последняя ветка/коммит, технический checkpoint
`.workflow/checkpoints/<task-key>.yaml`, опубликованные файлы, открытый
или уже объединённый PR, CI. После проверки продолжает с первой
незавершённой операции. Действия с неизвестным исходом повторно не запускаются
до фактического Git read-back. Для многошаговых задач checkpoint обновляется
на рабочей ветке после подтверждённых этапов. Если GitHub доказательств нет,
возвращается `RECOVERY_BLOCKED`, без выдуманных результатов.

Это не отменяет ограничение длины чата и не позволяет восстанавливать
утраченные рассуждения. Git-коммиты, файлы и PR остаются проверяемым
состоянием. Статусы чтения и сами книги не изменяются из-за обрыва.
