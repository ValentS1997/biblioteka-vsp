# Cheatsheet — глава 6. Типы данных

**Source:** PDF 155–189, RAG `p0155:c01`–`p0189:c01`. SQL не выполнялся.

## Symptom / problem framing

Нужно выбрать тип столбца так, чтобы:
- диапазон покрывал реальные значения;
- точность соответствовала задаче;
- storage не был избыточным;
- тип поддерживался конкретной РСУБД;
- строка/дата/Unicode/binary интерпретировались ожидаемо.

Книга подчёркивает: одинаковое концептуальное значение может иметь разный тип/синтаксис в MySQL, Oracle, PostgreSQL, SQL Server и SQLite.

## Baseline / context

| Категория | Основная развилка | Source |
|---|---|---|
| Integer | range vs storage | `p0157:c01`–`p0162:c01` |
| Decimal | exact value, precision/scale | `p0162:c01`–`p0163:c01` |
| Floating | approximate, single/double precision | `p0163:c01`–`p0165:c01` |
| String | CHAR vs VARCHAR vs TEXT; quoting | `p0166:c01`–`p0170:c01` |
| Unicode | NCHAR/NVARCHAR or native Unicode-capable text | `p0171:c01`–`p0172:c01` |
| Date/time | DATE/TIME/DATETIME/TIMESTAMP variants | `p0173:c01`–`p0183:c01` |
| Boolean | BOOLEAN / CHAR/NUMBER / BIT patterns | `p0184:c01` |
| Binary | BLOB/RAW/BYTEA/VARBINARY | `p0185:c01`–`p0189:c01` |

**RDBMS/version/schema/actual value distribution:** [Needs confirmation].

## Read-only checks

### Тип и literal semantics

Source-confirmed read-only examples:

```sql
SELECT DATE '2021-02-25';
```
MySQL/PostgreSQL form from `p0173:c01`; support on target version [Needs confirmation].

```sql
SELECT CAST('2021-02-25' AS DATE);
```
Shown across multiple products with dialect differences (`p0173:c01`).

```sql
SELECT TIME('10:30');
```
SQLite/MySQL-style source example depending on product (`p0175:c01`).

```sql
SELECT TRUE, True, FALSE, False;
```
Boolean literal demonstration `p0184:c01`; exact displayed representation on target RDBMS [Needs confirmation].

```sql
SELECT TO_NUMBER('AF12', 'XXXX') FROM dual;
```
Oracle hexadecimal conversion example `p0186:c01`; no external validation performed.

### Existing schema

Перед type change source points back to `ALTER TABLE` but chapter 6 itself does not define a read-only schema-inspection workflow. Current column definitions therefore need separate confirmation: **[Needs confirmation]**.

## Interpretation

### Integer

Choose based on range + storage. Source tables list different families:
- MySQL: TINYINT/SMALLINT/MEDIUMINT/INT/BIGINT.
- PostgreSQL: SMALLINT/INT/BIGINT plus SMALLSERIAL/SERIAL/BIGSERIAL.
- SQL Server: TINYINT/SMALLINT/INT/BIGINT.
- Oracle: NUMBER.
- SQLite: INTEGER.

Exact current ranges/version behavior: source-derived values only; external current verification not performed.

### Decimal versus floating-point

`DECIMAL(5,2)` → 5 total digits, 2 after decimal in book explanation.

Floating-point keeps approximations and may produce comparison/calculation differences. For values requiring fixed decimal accuracy, author recommends fixed-point type rather than FLOAT (`p0164:c01`).

### String and Unicode

- `VARCHAR(n)`: variable length.
- `CHAR(n)`: fixed length, padded in author explanation.
- `TEXT`: long text without length input in the conceptual description.
- Unicode types differ across engines.

The extracted ASCII/Unicode math on `p0171:c01` is damaged; do not use its numerical superscripts as reliable values. See source findings.

### Date/time

Do not treat a date-looking string as universally equivalent to a typed date. The chapter repeatedly uses DATE/TIME/TIMESTAMP/CAST forms and gives product-specific variants.

Timezone-capable types differ markedly:
- Oracle: TIMESTAMP WITH TIME ZONE / LOCAL TIME ZONE.
- PostgreSQL: TIME/TIMESTAMP WITH TIME ZONE.
- SQL Server: DATETIMEOFFSET.
- SQLite: TEXT/REAL/INTEGER storage according to table 6.18.

### Binary/files

Source presents two storage strategies:
1. path/reference outside DB;
2. binary content inside DB.

The “>1 MB use links” rule is a source heuristic, not a measured requirement for an arbitrary system.

## Next action

Для реального design/change:
1. Собрать sample/min/max/null/cardinality/length requirements.
2. Подтвердить РСУБД и версию.
3. Определить required precision и timezone/Unicode semantics.
4. Проверить storage/limits именно целевого диалекта.
5. Только затем выбрать тип.
6. Для существующей колонки отдельно оценить conversion/data-loss risk и rollback: [Needs confirmation].
7. Тестировать на копии/не-production среде перед schema change.

## Modifying action

Source examples часто создают test table:

```sql
CREATE TABLE my_table (
   my_decimal_column DECIMAL(5,2)
);
```

и вставляют данные:

```sql
INSERT INTO my_table VALUES
   (123.45),
   (-123),
   (12.3);
```

Класс: **state-changing**. Effect: schema + rows. Risk: object collision, unsupported type/range, coercion/truncation/rounding semantics. Verification: source follows with `SELECT * FROM my_table;`. Rollback: **[Needs confirmation]** — глава 6 не содержит универсальной rollback procedure.

Также `ALTER SESSION SET NLS_DATE_FORMAT = ...` на `p0179:c01` меняет Oracle session state; effect локализован session semantics по source, но конкретный rollback/reset [Needs confirmation].

## Verification / acceptance checks

- Категория данных определена.
- Required min/max/precision/scale/length/timezone/Unicode support известны.
- Type exists in target RDBMS/version.
- Test values round-trip without unexpected changes.
- Approximate FLOAT не используется там, где source требует exact fixed-point semantics.
- Date/time literals parse as intended.
- Unicode sample survives round-trip.
- Binary strategy соответствует размеру/backup requirements.
- Existing data conversion проверена до ALTER.

Фактические tests: **[Not executed]**.

## Rollback

- Read-only SELECT/CAST examples: [Not applicable].
- CREATE/INSERT/session/schema change: **[Needs confirmation]**; текущая глава не даёт универсального rollback.
- Не предлагать inverse DDL из общей памяти как автоматический rollback.
