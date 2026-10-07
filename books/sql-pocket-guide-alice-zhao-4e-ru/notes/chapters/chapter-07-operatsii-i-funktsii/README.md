# Глава 7. Операции и функции

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `CHAPTER-ANALYSIS-REQUEST v1.3` → `CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус:** `RAG_GROUNDED`. SQL не выполнялся.

## Источник и границы

- Canonical source: `source/book.pdf`; SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 7: **PDF 190–243**, **54 chunks**, `p0190:c01`–`p0243:c01`.
- Boundary evidence: начало `p0190:c01`, COALESCE на `p0243:c01`, глава 8 начинается `p0244:c01`.
- Оглавление: `p0010:c01`–`p0011:c01`.
- Режим `rag_only`: без web/direct-PDF/model-memory corrections.
- Source/RAG согласованы; ранее BOOK-READINESS = READY. Reading остаётся `planned`.

## Карта главы

| Раздел | PDF | RAG |
|---|---:|---|
| Operations/functions, logical/comparison | 190–200 | `p0190:c01`–`p0200:c01` |
| Arithmetic + aggregates | 200–203 | `p0200:c01`–`p0203:c01` |
| Numeric functions | 203–209 | `p0203:c01`–`p0209:c01` |
| String functions | 209–218 | `p0209:c01`–`p0218:c01` |
| Regex + string CAST | 218–226 | `p0218:c01`–`p0226:c01` |
| Date/time functions | 227–242 | `p0227:c01`–`p0242:c01` |
| NULL functions | 243 | `p0243:c01` |

## Основные выводы

1. Логика SQL трёхзначна: TRUE/FALSE/NULL; смешанные AND/OR автор рекомендует явно группировать скобками.
2. `NOT IN` с NULL в подзапросе может дать неожиданный результат; книга предлагает `NOT EXISTS`.
3. `COUNT(*)` считает строки, а другие агрегаты работают по non-NULL значениям согласно источнику.
4. Numeric/string/regex/date-time функции существенно расходятся по РСУБД.
5. CAST меняет тип выражения на время запроса, не schema.
6. COALESCE возвращает fallback при NULL; IFNULL/NVL/ISNULL приведены как dialect variants.
7. Большинство примеров — read-only, но `CREATE TABLE`+`INSERT` на PDF 228 state-changing.

## Source findings

Зафиксированы без silent correction:
- `e.id` без alias `e` в одном IN-примере;
- generic `ORDER BY RANDOM()` после product table с `RAND()`;
- extraction artifact `Server SELECT CONCAT...`;
- missing operator в PostgreSQL/SQLite time-difference snippets;
- interval-vs-day/hour mismatch в date-difference examples;
- `[[:digit::]]` в regex token;
- SQL Server `CONVERT(VARCHAR,...)` при описании string→DATETIME;
- внутреннее противоречие о SQLite date functions;
- collation/regex/math/date behavior остаётся version-sensitive [Needs confirmation].

Полный register: [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

Явного chapter-end summary/review section перед главой 8 нет.
