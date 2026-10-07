# Source-confirmed commands — глава 5

**Source:** PDF 105–154, RAG `p0105:c01`–`p0154:c01`.  
**Execution:** не выполнялось. Реальная БД, версия, права, backup и change approval — [Needs confirmation].

> Этот файл документирует команды из книги. Он **не** является готовым production-runbook.

## 1. Read-only baseline

### Базы данных

**PDF 108, `p0108:c01`:**
- MySQL: `SHOW databases;`
- Oracle: `SELECT * FROM global_name;`
- PostgreSQL: `\l`
- SQL Server: `SELECT name FROM master.sys.databases;`
- SQLite: `.database`

**Текущая БД, PDF 108:**
- MySQL: `SELECT database();`
- PostgreSQL: `SELECT current_database();`
- SQL Server: `SELECT db_name();`
- Oracle/SQLite — формы из таблицы автора.

Класс: **read-only / session metadata**. Риск: раскрытие metadata в неподходящем контексте; права [Needs confirmation]. Rollback: [Not applicable].

### Таблицы и столбцы

**PDF 114, `p0114:c01`:**
- MySQL: `SHOW tables;`
- Oracle: `SELECT table_name FROM user_tables;`
- PostgreSQL: `\dt`
- SQL Server: `SELECT table_name FROM information_schema.tables;`
- SQLite: `.tables`

**PDF 130, `p0130:c01`:**
- MySQL/Oracle: `DESCRIBE my_table;`
- PostgreSQL: `\d my_table`
- SQL Server: query against `information_schema.columns`
- SQLite: `pragma table_info(my_table);`

Класс: **read-only**. Acceptance: убедиться, что target object действительно тот, который планируется менять.

## 2. Database-level changes

### CREATE DATABASE

**PDF 110, `p0110:c01`:**
```sql
CREATE DATABASE my_new_db;
```

Класс: **state-changing / DDL**.  
Effect: создаёт БД (в перечисленных РСУБД; SQLite использует файловый путь).  
Risk: неправильный instance, имя, storage/config, privilege.  
Verification: повторный list-current DB check из `p0108:c01`–`p0109:c01`.  
Rollback: [Needs confirmation]; источник не задаёт универсальный безопасный rollback для CREATE DATABASE.

### DROP DATABASE

**PDF 110–111, `p0110:c01`–`p0111:c01`:**
```sql
DROP DATABASE my_new_db;
```

Класс: **state-changing / destructive DDL**.  
Effect: удаляет БД и данные.  
Risk: полный data loss; книга говорит, что без backup отмена невозможна.  
Verification before: имя текущей БД, target DB, backup.  
Rollback: restore from backup only as source-level concept; точная procedure [Needs confirmation].  
**Не выполнять по этому документу.**

PostgreSQL/SQL Server source examples предварительно переключаются на default DB (`postgres` / `master`) на `p0111:c01`.

## 3. CREATE TABLE / INSERT

**PDF 112, `p0112:c01`:**
```sql
CREATE TABLE my_simple_table (
   id INTEGER,
   country VARCHAR(2),
   name VARCHAR(15)
);
```

Effect: создаёт пустую таблицу. Risk: naming/schema conflict, incorrect types. Verify: table list + describe. Rollback: [Needs confirmation].

**PDF 112:**
```sql
INSERT INTO my_simple_table (id, country, name)
VALUES (1, 'US', 'Sam');
```

Effect: добавляет строку. Risk: duplicate/wrong data/constraint errors. Verify:
```sql
SELECT * FROM my_simple_table;
```
Rollback: transaction `ROLLBACK` only if operation is inside a supported uncommitted transaction; otherwise [Needs confirmation].

Oracle multi-row `INSERT ALL ... SELECT * FROM dual;` is shown on `p0113:c01`; other systems use multi-row `VALUES`.

## 4. Constraints

Source examples `p0115:c01`–`p0122:c01` include:
- `NOT NULL`
- `DEFAULT`
- `CHECK`
- `UNIQUE`
- `PRIMARY KEY`
- `FOREIGN KEY ... REFERENCES ...`

Representative source example:
```sql
CREATE TABLE customers (
   id INTEGER PRIMARY KEY,
   order_id INTEGER,
   name VARCHAR(15),
   location VARCHAR(20),
   FOREIGN KEY (order_id)
   REFERENCES orders (o_id)
);
```

Class: **state-changing / DDL**.  
Risk: rejects existing/future data, referential errors, schema dependency.  
Verification: describe/constraint metadata.  
Rollback: [Needs confirmation], because source does not give a universal transactional rollback for ALTER/CREATE constraints.

## 5. INSERT ... SELECT

**PDF 124, `p0124:c01`:**
```sql
INSERT INTO new_table_two_columns (id, name)
SELECT id, name
FROM my_simple_table
WHERE id < 3;
```

Class: **state-changing / DML**.  
Risk: unexpected cardinality or duplicate rows.  
Read-only preview: run only the `SELECT id, name ... WHERE id < 3` portion in a permitted environment.  
Verification: query destination rows.  
Rollback: transaction rollback if applicable and uncommitted; otherwise [Needs confirmation].

## 6. CSV import

`p0126:c01` provides dialect-specific commands:
- MySQL `LOAD DATA LOCAL INFILE ...`
- PostgreSQL `\copy ... FROM ... CSV HEADER`
- SQL Server `BULK INSERT ... FORMAT='CSV' ...`
- SQLite `.mode csv` + `.import ...`
- Oracle: GUI/sqlldr described rather than one canonical SQL block.

Class: **state-changing / bulk data load**.  
Risk: wrong file/path/delimiter/encoding, unexpected NULL semantics, huge row count, local-file exposure.  
Verification: schema check + row/sample SELECT.  
Rollback: [Needs confirmation], ideally transaction only if target tool/DB semantics support it.

**PDF 127:**  
`SET GLOBAL local_infile=1;` changes a **server-global setting** in MySQL source example. Class: **state-changing / server configuration**, high operational boundary. Do not apply without owner/security review and explicit rollback procedure [Needs confirmation].

## 7. ALTER TABLE / rename / add / drop

Source `p0129:c01`–`p0136:c01` includes:
- `ALTER TABLE ... RENAME TO ...`
- `RENAME COLUMN ...`
- `ADD new_column ...`
- `DROP COLUMN ...`
- `ADD CONSTRAINT ...`
- dialect-specific MODIFY/ALTER COLUMN
- `DROP CONSTRAINT ...` or MySQL `DROP CHECK ...`

Class: **state-changing / schema change**.  
Risk: incompatible application queries, data loss for dropped columns, constraints broken, locks/downtime [Needs confirmation].  
Verification: describe table, list constraints, sample SELECT.  
Rollback: source says structural changes may be permanent without backup (`p0128:c01`); universal rollback [Needs confirmation].

### SQLite manual-rebuild pattern (PDF 131–132)

Book source shows:
1. CREATE replacement table.
2. INSERT SELECT from old table.
3. SELECT verification.
4. DROP old table.
5. RENAME replacement.

This is **multi-step state-changing**. Do not copy into production as an atomic migration; transaction/locking/failure semantics are [Needs confirmation].

## 8. Row INSERT / DELETE / UPDATE

**INSERT, PDF 132:**
```sql
INSERT INTO my_table (id, country, name)
VALUES (9, 'US', 'Charlie');
```

**DELETE one row, PDF 133:**
```sql
DELETE FROM my_table
WHERE id = 9;
```

**DELETE all rows, PDF 133:**
```sql
DELETE FROM my_table;
```

The last is **destructive for all rows**. It keeps table definition according to the source.

**UPDATE all rows, PDF 137:**
```sql
UPDATE my_table
SET name = LOWER(name);
```

**UPDATE filtered rows, PDF 138:**
```sql
UPDATE my_table
SET awards = awards + 1
WHERE country = 'CA';
```

**UPDATE from scalar query, PDF 139:**
```sql
UPDATE my_table
SET awards = (SELECT MIN(awards) FROM my_table)
WHERE country = 'CA';
```

All are **state-changing / DML**.  
Risk: wrong predicate / entire-table blast radius / self-query dialect restriction.  
Verification: source explicitly demonstrates preview SELECT and post-change SELECT.  
Rollback: `ROLLBACK` if still in a supported transaction before COMMIT; otherwise [Needs confirmation].

## 9. DROP TABLE / CASCADE

**PDF 140:**
```sql
DROP TABLE my_table;
```

**PDF 141:**
```sql
DROP TABLE my_table CASCADE;
```

Class: **destructive state-changing / DDL**.  
Risk: full object/data loss; CASCADE may remove dependent objects/constraints.  
Source warning: do not use CASCADE without knowing what it removes.  
Verification: object/dependency inventory + backup before execution.  
Rollback: restore/recreate [Needs confirmation]; source says DROP TABLE cannot be undone without backup.

## 10. Indexes

**PDF 143:**
```sql
CREATE INDEX my_index ON my_table (log_date);
```

**PDF 144:**
```sql
CREATE INDEX my_index ON my_table (log_date, team);
```

Class: **state-changing / schema+storage, potentially workload-generating**.  
Risk: build time, locks/resources, disk, write overhead.  
Verification: [Needs confirmation]; source explains expected query speedup but does not provide EXPLAIN/benchmark procedure.  
Rollback: `DROP INDEX` exists in source but is itself state-changing; do not treat inverse command as risk-free rollback. Exact rollback [Needs confirmation].

## 11. Views

**PDF 146–147:**
```sql
CREATE VIEW owner_waterfalls_vw AS
SELECT o.id, o.name,
       COUNT(w.id) AS num_waterfalls
FROM owner o LEFT JOIN waterfall w
     ON o.id = w.owner_id
GROUP BY o.id, o.name;
```

Class: **state-changing DDL** (creates view definition).  
Verification: `SELECT AVG(num_waterfalls) FROM owner_waterfalls_vw;` or view-list commands on `p0148:c01`.  
Rollback: `DROP VIEW my_view;` is shown on `p0149:c01`, but source explicitly says deletion cannot be undone; recreation definition must be preserved.

SQLite source updates view using `DROP VIEW IF EXISTS` + `CREATE VIEW`, which has a destructive intermediate step.

## 12. Transactions

**Source pattern, PDF 150–154:**
```sql
START TRANSACTION;
-- state-changing DML
COMMIT;
```

MySQL/PostgreSQL also show `BEGIN;`; SQL Server/SQLite show `BEGIN TRANSACTION;` on `p0151:c01`, `p0153:c01`.

**Preview + delete + commit:**
```sql
SELECT * FROM books WHERE title LIKE '% %';
DELETE FROM books WHERE title LIKE '% %';
SELECT * FROM books;
COMMIT;
```

**Accidental broad delete + rollback:**
```sql
DELETE FROM books WHERE title LIKE '%%';
SELECT * FROM books;
ROLLBACK;
```

Class: transaction control + state-changing DML.  
Effect: source demonstrates keeping changes uncommitted until decision.  
Risk: `COMMIT` makes change permanent in the chapter example; wrong predicate can affect every row.  
Verification: SELECT before and after DML, before COMMIT.  
Rollback: **source-confirmed `ROLLBACK;` before COMMIT**. After COMMIT source says rollback is unavailable.

## Acceptance rule

No state-changing snippet above is authorized for execution. Before any real use, resolve:
`target_host`, `database`, `schema`, `RDBMS/version`, `owner`, `approval`, `backup/restore point`, `expected rows/objects`, `verification query`, `rollback semantics`.

Unknown values remain **[Needs confirmation]**.
