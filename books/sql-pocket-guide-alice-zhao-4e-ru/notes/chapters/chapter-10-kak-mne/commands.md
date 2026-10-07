# Source-confirmed SQL examples — глава 10

**Source:** PDF 304–315, RAG `p0304:c01`–`p0315:c01`.  
**Execution:** не выполнялось. Target RDBMS/version/schema/transaction state — [Needs confirmation].

## 1. DISTINCT: уникальные комбинации

```sql
SELECT DISTINCT tea, temperature
FROM teas;
```

Class: **read-only**.  
Purpose: убрать duplicate combinations из выбранных столбцов.  
Source: `p0305:c01`.

## 2. Найти только дублирующиеся строки

```sql
WITH dup_rows AS (
  SELECT tea, temperature,
         COUNT(*) AS num_rows
  FROM teas
  GROUP BY tea, temperature
  HAVING COUNT(*) > 1
)
SELECT t.id, d.tea, d.temperature
FROM teas t
INNER JOIN dup_rows d
  ON t.tea = d.tea
 AND t.temperature = d.temperature;
```

Class: **read-only / aggregate + JOIN**.  
Source: `p0306:c01`.

Operational note: source sample has non-NULL values. Equality JOIN does not establish behavior for duplicate NULL combinations; test explicitly on target.

## 3. Latest/max row per group

```sql
SELECT s.id, r.employee, r.recent_date, s.sales
FROM (
  SELECT employee, MAX(date) AS recent_date
  FROM sales
  GROUP BY employee
) r
INNER JOIN sales s
  ON r.employee = s.employee
 AND r.recent_date = s.date;
```

Class: **read-only**.  
Source: `p0308:c01`.

Effect: finds max date per employee, then joins back for id/sales.  
Tie behavior: if multiple rows have same max date, multiple rows may match; source sample does not cover ties.

## 4. Concatenate fields within one row

MySQL/PostgreSQL/SQL Server source:
```sql
SELECT CONCAT(id, '_', name) AS id_name
FROM my_table;
```

Oracle/PostgreSQL/SQLite source:
```sql
SELECT id || '_' || name AS id_name
FROM my_table;
```

Class: **read-only**.  
Source: `p0309:c01`–`p0310:c01`.

Exact coercion of numeric id to text is target-specific [Needs confirmation].

## 5. Aggregate values across rows

MySQL/SQLite source:
```sql
SELECT name,
       GROUP_CONCAT(calories) AS calories_list
FROM workouts
GROUP BY name;
```

Source variants on `p0311:c01`:
- Oracle: `LISTAGG(calories, ',')`
- PostgreSQL: `ARRAY_AGG(calories)`
- SQL Server: `STRING_AGG(calories, ',')`

Class: **read-only / aggregate**.  
Ordering/output type are target-specific. PostgreSQL example is preserved as source even though its result shape is not established here as the same string type as neighboring examples.

## 6. Metadata search: find tables containing a column name

MySQL source:
```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%city%'
  AND table_schema = 'my_db_name';
```

Oracle source:
```sql
SELECT table_name, column_name
FROM all_tab_columns
WHERE column_name LIKE '%CITY%'
  AND owner = 'MY_USER_NAME';
```

PostgreSQL / SQL Server source:
```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%city%'
  AND table_catalog = 'my_db_name';
```

SQLite source:
```text
.tables
pragma table_info(my_table);
```

Class: **read-only metadata inspection**.  
Source: `p0311:c01`–`p0312:c01`.

Visibility of “all tables” depends on actual catalog/user/privileges: [Needs confirmation].

## 7. Cross-table UPDATE — state-changing

### MySQL source

```sql
UPDATE deals d,
       products p
SET    d.name = p.name
WHERE  d.id = p.id;
```

### Oracle source

```sql
UPDATE deals d
SET    name = (
  SELECT p.name
  FROM products p
  WHERE d.id = p.id
);
```

### PostgreSQL / SQLite source

```sql
UPDATE deals
SET    name = p.name
FROM   deals d
       INNER JOIN products p
       ON d.id = p.id
WHERE  deals.id = p.id;
```

### SQL Server source

```sql
UPDATE d
SET    d.name = p.name
FROM   deals d
       INNER JOIN products p
       ON d.id = p.id;
```

Source: `p0314:c01`.

Class: **state-changing / UPDATE**.

### Required pre-check

Before using any dialect variant, run a read-only preview that identifies exact target ids/values. Generic conceptual preview based on the source relation:

```sql
SELECT d.id,
       d.name AS old_name,
       p.name AS new_name
FROM deals d
INNER JOIN products p
  ON d.id = p.id;
```

This preview is an operational control derived from the source relationship, not a verbatim chapter query. Target syntax/data still [Needs confirmation].

### Effect / risk / verification / rollback

**Effect:** modify `deals.name` for rows affected by dialect-specific logic.

**Risk:**
- unmatched rows;
- multiple source matches per id;
- dialect semantics differ;
- more rows changed than expected;
- Oracle scalar subquery behavior for unmatched rows is not discussed;
- PostgreSQL/SQLite source form repeats target table in FROM and needs target-specific verification.

**Verification:** SELECT `deals` after UPDATE before COMMIT.

**Rollback:** source `p0315:c01` says UPDATE cannot be reversed unless transaction was started beforehand. Exact transaction support/autocommit semantics: **[Needs confirmation]**.

## 8. Final acceptance

- Read-only queries: rollback [Not applicable].
- UPDATE: do not execute from this artifact alone.
- Required inputs before UPDATE: target DB/schema, RDBMS/version, owner/approval, transaction state, preview affected ids/count, verification query, rollback semantics.
