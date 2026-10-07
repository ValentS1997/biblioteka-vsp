# Source-confirmed SQL examples — глава 6

**Source:** PDF 155–189, RAG `p0155:c01`–`p0189:c01`.  
**Execution:** не выполнялось. Реальная РСУБД, версия, schema, privileges и rollback — [Needs confirmation].

## Классификация

- `SELECT`/literal conversion examples: **read-only**.
- `CREATE TABLE`, `INSERT`: **state-changing** (schema/data).
- `ALTER SESSION`: **state-changing** для session configuration.
- Глава 6 не даёт универсального rollback для этих действий: **[Needs confirmation]**.

## 1. Базовая типизация

**PDF 155, `p0155:c01`:**
```sql
CREATE TABLE my_table (
   id INT,
   name VARCHAR(30),
   dt DATE
);
```
Effect: создаёт таблицу. Risk: object conflict/type mismatch. Verification: schema inspection + test inserts. Rollback: [Needs confirmation].

## 2. Integer

**PDF 160, `p0160:c01`:**
```sql
CREATE TABLE my_table (
   my_integer_column INT
);

INSERT INTO my_table VALUES
   (25),
   (-525),
   (2500252);

SELECT * FROM my_table;
```

- CREATE/INSERT: **state-changing**.
- SELECT: **read-only**.
- Диапазоны различаются по продуктам (`p0160:c01`–`p0162:c01`).

**MySQL UNSIGNED, PDF 161:**
```sql
CREATE TABLE my_table (
   my_integer_column INT UNSIGNED
);
```
State-changing; target dialect/version [Needs confirmation].

## 3. Decimal / exact numeric

**PDF 162, `p0162:c01`:**
```sql
CREATE TABLE my_table (
   my_decimal_column DECIMAL(5,2)
);

INSERT INTO my_table VALUES
   (123.45),
   (-123),
   (12.3);

SELECT * FROM my_table;
```

Source interpretation: precision=5, scale=2. CREATE/INSERT state-changing; SELECT read-only. Check round-trip and rounding/coercion behavior on target: [Needs confirmation].

## 4. Floating point

**PDF 164, `p0164:c01`:**
```sql
CREATE TABLE my_table (
   my_float_column FLOAT,
   my_double_column DOUBLE
);
```

Source warns these values are approximate. `DOUBLE` is not a portable type name across all products in the chapter; Oracle specifically uses `BINARY_FLOAT`/`BINARY_DOUBLE` in `p0165:c01`. Target syntax [Needs confirmation].

## 5. Strings

**PDF 168, `p0168:c01`:**
```sql
CREATE TABLE my_table (
   my_character_column VARCHAR(50)
);
```

Source string literals:
```sql
SELECT 'hello', 'he\'llo', '\thello';
```
MySQL example, read-only (`p0168:c01`).

PostgreSQL example:
```sql
SELECT 'hello', E'he\'llo', e'\thello';
```
Read-only. Exact escape semantics on current server settings/version: [Needs confirmation].

Oracle/PostgreSQL alternative quoting in `p0167:c01`:
- Oracle: `Q'[This is a string.]'`
- PostgreSQL: `$$This is a string.$$`

These are source fragments, not tested here.

## 6. Unicode

**PDF 171–172, `p0171:c01`–`p0172:c01`:**
```sql
CREATE TABLE my_table (
   ascii_text VARCHAR(10),
   unicode_text NVARCHAR(10)
);

INSERT INTO my_table VALUES
   ('abc', 'abc'),
   (N'赵欣婉', N'赵欣婉');

SELECT * FROM my_table;
```

State-changing CREATE/INSERT, read-only SELECT. The output shown in source has `???` for the VARCHAR sample and preserved Unicode in NVARCHAR; behavior across products is not universalized here.

## 7. Date/time literal checks

**PDF 173, `p0173:c01`:**
```sql
SELECT DATE '2021-02-25';
SELECT CAST('2021-02-25' AS DATE);
```
Read-only forms shown for selected RDBMSs; see source table for product-specific variants.

**PDF 175, `p0175:c01`:**
```sql
SELECT CAST('10:30' AS TIME);
```

**PDF 176, `p0176:c01`:**
```sql
SELECT TIMESTAMP '2021-02-25 10:30';
```

Do not assume one form works identically everywhere; chapter explicitly lists different forms.

## 8. Oracle session format

**PDF 179, `p0179:c01`:**
```sql
ALTER SESSION
SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH:MI:SS';
```

Class: **state-changing / session configuration**.  
Effect: changes current Oracle session format per source.  
Risk: subsequent parsing/display assumptions change.  
Verification: source reads `nls_session_parameters`.  
Rollback/reset: [Needs confirmation].

Read-only source check:
```sql
SELECT value
FROM nls_session_parameters
WHERE parameter in ('NLS_DATE_FORMAT',
                    'NLS_TIMESTAMP_FORMAT');
```

## 9. Boolean

**PDF 184, `p0184:c01`:**
```sql
SELECT TRUE, True, FALSE, False;
```

Read-only. Source output renders 1/0 but does not clearly bind that output to all three previously named systems; see `source-findings.md`.

State-changing demo:
```sql
CREATE TABLE my_table (
   my_boolean_column BOOLEAN
);
```
Source says MySQL/PostgreSQL/SQLite support BOOLEAN; current exact semantics/version [Needs confirmation].

## 10. Hex / binary

**PDF 186, `p0186:c01`:**
```sql
SELECT X'AF12', x'AF12', 0xAF12;
```
Source says MySQL supports all three, PostgreSQL first two, SQL Server/SQLite third. Current dialect verification not performed.

Oracle conversion source example:
```sql
SELECT TO_NUMBER('AF12', 'XXXX') FROM dual;
```

**PDF 187:**
```sql
CREATE TABLE my_table (
   my_binary_column BLOB
);
```
State-changing. Source later differentiates BLOB/RAW/BYTEA/VARBINARY by RDBMS.

Oracle/SQL Server conversion snippets:
```sql
SELECT RAWTOHEX('ae$ iou') FROM dual;
```
```sql
SELECT CONVERT(VARBINARY, 'ae$ iou');
```
Read-only conversions in source context; exact target-version behavior [Needs confirmation].

## Verification / rollback

For any CREATE/INSERT:
1. Confirm target RDBMS/version and schema.
2. Confirm object name does not collide.
3. Insert only test values in non-production.
4. SELECT back values and compare precision/length/encoding/timezone.
5. Confirm no truncation/coercion before wider migration.

**Rollback:** chapter 6 does not supply one. Do not invent DROP/DELETE as automatic rollback. Status: **[Needs confirmation]**.
