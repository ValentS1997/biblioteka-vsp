# Глава 6. Типы данных

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ANALYSIS-REQUEST v1.3` → `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус:** `RAG_GROUNDED`. SQL-примеры не выполнялись.

## Источник и границы

- Canonical source: `books/sql-pocket-guide-alice-zhao-4e-ru/source/book.pdf`.
- SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 6: **PDF 155–189**, **35 page-chunks** `p0155:c01`–`p0189:c01`.
- RAG path pattern: `rag/chunks/p0101-p0200/p0155-c01.md` … `p0189-c01.md`.
- Boundary evidence: начало главы в `p0155:c01`; последний фрагмент таблицы бинарных типов на `p0189:c01`; глава 7 начинается на `p0190:c01`. Оглавление главы — `p0009:c01`–`p0010:c01`.
- Режим: `rag_only`; внешняя документация, прямое чтение PDF и модельная память не используются для исправления значений/синтаксиса.
- Source/RAG согласованы; ранее book readiness прошёл в GitHub Actions run `37530593752`. Reading status остаётся `planned`.

## Главная идея

Тип данных задаёт, **какие значения может хранить столбец, как они представлены и сколько ресурсов требуют**. Автор предлагает выбирать тип как компромисс между диапазоном, точностью, размером хранения и будущей гибкостью (`p0157:c01`–`p0158:c01`).

Глава группирует типы в четыре категории:

1. **Числовые:** integer, fixed-point decimal, floating-point.
2. **Строковые:** character и Unicode.
3. **Дата/время:** DATE/TIME/DATETIME/TIMESTAMP-подобные варианты.
4. **Другие:** Boolean и binary/BLOB.

## Карта главы

| Подтема | PDF | RAG |
|---|---:|---|
| Категории типов и литералы; NULL | 155–157 | `p0155:c01`–`p0157:c01` |
| Как выбирать тип: range/storage/flexibility | 157–158 | `p0157:c01`–`p0158:c01` |
| Integer types и SERIAL | 159–162 | `p0159:c01`–`p0162:c01` |
| DECIMAL/NUMERIC: precision и scale | 162–163 | `p0162:c01`–`p0163:c01` |
| Floating-point и approximate values | 163–165 | `p0163:c01`–`p0165:c01` |
| Strings, quotes, escape sequences, CHAR/VARCHAR/TEXT | 166–170 | `p0166:c01`–`p0170:c01` |
| Unicode и NCHAR/NVARCHAR/TEXT | 171–172 | `p0171:c01`–`p0172:c01` |
| Date/time literals и conversion forms | 172–176 | `p0172:c01`–`p0176:c01` |
| MySQL/Oracle/PostgreSQL/SQL Server/SQLite datetime types | 177–183 | `p0177:c01`–`p0183:c01` |
| Boolean | 184 | `p0184:c01` |
| External files, hex/binary values, BLOB/BYTEA/VARBINARY | 185–189 | `p0185:c01`–`p0189:c01` |

## Основные выводы

1. **NULL — не тип данных.** По тексту он обозначает отсутствие значения и может встречаться в числовом, строковом, временном или другом столбце (`p0157:c01`).
2. **Integer selection:** меньший тип экономит storage, больший даёт range/flexibility. Конкретные диапазоны существенно различаются по РСУБД (`p0157:c01`–`p0162:c01`).
3. **DECIMAL/NUMERIC — exact fixed-point** в объяснении автора; `DECIMAL(5,2)`: precision=5, scale=2 (`p0162:c01`–`p0163:c01`).
4. **Floating-point — approximate.** Автор предупреждает, что сравнения/вычисления могут отличаться от ожидаемых; для фиксированного количества десятичных цифр рекомендует DECIMAL (`p0164:c01`).
5. **Strings:** одинарные кавычки — значения, двойные — identifiers по общей рекомендации главы; Oracle/PostgreSQL показывают собственные альтернативы quoting (`p0166:c01`–`p0168:c01`).
6. **Unicode:** формы типов различаются между РСУБД; PostgreSQL/SQLite в таблице автора используют обычные CHAR/VARCHAR/TEXT как Unicode-capable (`p0171:c01`–`p0172:c01`).
7. **Date/time — самая диалектно-зависимая область главы.** Literal syntax, CAST, timezone types и ranges отличаются между продуктами (`p0173:c01`–`p0183:c01`).
8. **Binary/external files:** автор сравнивает хранение file-path ссылок и бинарного содержимого; типы — BLOB/RAW/BYTEA/VARBINARY и др. (`p0185:c01`–`p0189:c01`).

## Operational boundary

Большинство демонстраций типов построены через `CREATE TABLE` + `INSERT` + `SELECT`. В артефактах:
- `SELECT`/CAST literal checks классифицируются как read-only;
- `CREATE TABLE`, `INSERT`, `ALTER SESSION` — state-changing;
- никакой state-changing SQL не выполнялся;
- chapter 6 не даёт собственного универсального rollback procedure, поэтому rollback для таких примеров — **[Needs confirmation]**.

## Source findings

Материальные проблемы source/text-layer:
- ASCII/Unicode степени извлечены как `28`, `221`, `28` вместо однозначной математической записи;
- MySQL datetime INSERT на PDF 177 имеет несогласованный порядок значений и вывод;
- текст говорит `YYYYMM-DD`, пример показывает `YYYY-MM-DD`;
- SQLite datetime demo вставляет одинаковую текстовую строку в TEXT/REAL/INTEGER, хотя следующая таблица описывает numeric storage для REAL/INTEGER;
- table tokens извлечены как `TINY TEXT`/`MEDIUM TEXT`/`LARGE TEXT` и `TINY BLOB`/`MEDIUM BLOB`/`LARGE BLOB`;
- boolean example показывает 1/0 после заявления сразу о трёх РСУБД — scope конкретного output не указан;
- version-sensitive ranges/limits remain [Needs confirmation].

Полный register: [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

В главе нет отдельного chapter-end summary/review section на `p0155:c01`–`p0189:c01`; conditional `summary.md`/review artifacts не создаются.
