# Глава 5. Создание, обновление и удаление

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.3` → `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус материалов:** `RAG_GROUNDED`. Никакие DDL/DML/TCL-команды не выполнялись.

## Источник и границы

- Canonical source: `books/sql-pocket-guide-alice-zhao-4e-ru/source/book.pdf`.
- SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 5: **PDF 105–154**, **50 page-chunks** `p0105:c01`–`p0154:c01`.
- RAG paths: `rag/chunks/p0101-p0200/p0105-c01.md` … `p0154-c01.md`.
- Boundary evidence: оглавление `p0008:c01`–`p0009:c01`, явное начало главы `p0105:c01`, финальный `ROLLBACK` на `p0154:c01`, начало главы 6 на `p0155:c01`.
- Режим: `rag_only`; внешний web, прямой PDF fallback и модельная память не используются для исправления или дополнения источника.
- Book readiness ранее подтверждён успешным GitHub Actions run `37530593752`; source SHA/RAG manifest на текущем main согласованы и не меняются. Reading status остаётся `planned`.

## Что охватывает глава

Глава переводит CRUD от чтения к изменению состояния: базы данных, таблицы, ограничения, строки, индексы, представления и транзакции. Это первая глава книги, где большинство примеров требуют повышенного operational control.

| Раздел | PDF | RAG |
|---|---:|---|
| Базы данных: список, текущая БД, переключение, CREATE/DROP | 105–111 | `p0105:c01`–`p0111:c01` |
| Создание таблиц, INSERT, просмотр таблиц | 111–114 | `p0111:c01`–`p0114:c01` |
| Ограничения: NOT NULL, DEFAULT, CHECK, UNIQUE | 115–118 | `p0115:c01`–`p0118:c01` |
| PRIMARY KEY / FOREIGN KEY / autoincrement-формы | 118–123 | `p0118:c01`–`p0123:c01` |
| INSERT ... SELECT и импорт CSV | 123–128 | `p0123:c01`–`p0128:c01` |
| ALTER TABLE: rename/add/drop columns/constraints | 128–137 | `p0128:c01`–`p0137:c01` |
| INSERT / DELETE / UPDATE и preview-before-change | 132–140 | `p0132:c01`–`p0140:c01` |
| DROP TABLE, foreign-key cascade | 140–141 | `p0140:c01`–`p0141:c01` |
| Индексы: CREATE/DROP, составные индексы | 141–145 | `p0141:c01`–`p0145:c01` |
| Views: CREATE, query, replace/alter, DROP | 145–149 | `p0145:c01`–`p0149:c01` |
| Transactions: START/BEGIN, COMMIT, ROLLBACK | 149–154 | `p0149:c01`–`p0154:c01` |

## Основные принципы

1. **Read-only discovery прежде change:** книга сначала показывает, как проверить текущую/существующие БД, таблицы, столбцы и constraints, затем — CREATE/ALTER/DROP (`p0107:c01`–`p0136:c01`).
2. **Preview before UPDATE/DELETE:** перед изменением значений автор выполняет эквивалентный `SELECT`, затем `UPDATE`/`DELETE` (`p0137:c01`–`p0139:c01`, `p0151:c01`–`p0154:c01`).
3. **WHERE — security boundary для DML:** `UPDATE` без `WHERE` обновляет всю таблицу, `DELETE FROM table;` удаляет все строки (`p0133:c01`, `p0139:c01`).
4. **DROP/CASCADE — destructive:** книга прямо предупреждает об необратимости удаления БД/таблицы/представления/индекса и необходимости backup либо полной уверенности (`p0110:c01`, `p0140:c01`–`p0145:c01`, `p0149:c01`).
5. **Транзакция как ограниченная защита:** `START/BEGIN` → изменение → проверка → `COMMIT` или `ROLLBACK`. После `COMMIT` откат в примере уже невозможен (`p0149:c01`–`p0154:c01`).
6. **Dialect-specific SQL:** CREATE/DROP/ALTER/import/index/view/transaction syntax различается между MySQL, Oracle, PostgreSQL, SQL Server, SQLite. Любой runnable action должен быть привязан к конкретной системе/версии: [Needs confirmation].

## Operational boundary

В этой коллекции **не выполняется** ни одна state-changing команда. Для любого изменения вне учебной среды нужны: target DB, owner/approval, backup/restore point, точная версия РСУБД, проверка прав, test query, verification и rollback. Неизвестные поля остаются **[Needs confirmation]**.

Особенно опасные source-confirmed действия:
- `DROP DATABASE`, `DROP TABLE`, `CASCADE`;
- `DELETE FROM table;` без WHERE;
- `UPDATE ... SET ...;` без WHERE;
- импорт файлов и изменение server-global параметра `local_infile`;
- ALTER constraints/columns;
- `COMMIT` после destructive DML.

## Source findings

Обнаружены материальные противоречия/дефекты:
- privilege `DELETE` описана для `DROP DATABASE`, хотя глава ранее/далее классифицирует DROP как DDL;
- текст CHECK говорит о `' US'`, а код использует `'US'`;
- SQL Server пример на PDF 136 содержит identifier `страна` вместо ранее используемого `country`;
- Oracle CREATE INDEX на PDF 143 показывает `'LOG_DATE'` в одинарных кавычках;
- описание транзакции местами говорит «изменения не внесены», в то время как соседние шаги показывают изменения как существующие, но ещё не постоянные;
- DELETE с `LIKE '%%'` назван удалением «всей таблицы», хотя показан пустой результат таблицы.

Все варианты сохранены в [source-findings.md](source-findings.md); никаких silent corrections.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — rollback-first карта действий.
- [commands.md](commands.md) — read-only и state-changing команды с эффектом/риском/проверкой/rollback.
- [diagram.md](diagram.md) — безопасный поток change control и объектная карта.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная SVG.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная SVG.
- [source-findings.md](source-findings.md) — register source defects.

Явного chapter-end summary или review questions в `p0105:c01`–`p0154:c01` нет; условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.
