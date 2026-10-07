# Source findings — глава 5. Создание, обновление и удаление

**Book:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Scope:** PDF 105–154, RAG `p0105:c01`–`p0154:c01`  
**Policy:** source defects are recorded, not silently corrected. No external adjudication in `rag_only`.

## F-01 · [Source contradiction] · DELETE privilege for DROP DATABASE

On `p0110:c01`, immediately before `DROP DATABASE my_new_db;`, the prose says that the user can delete a database if they have **DELETE privileges**.

Within the same book/chapter context:
- `DROP DATABASE` is presented as database-object removal.
- Chapter 3 table of sublanguages classifies `DROP` as DDL and `DELETE` as DML (`p0068:c01`).
- Chapter 5 separately uses `DELETE FROM` for row removal (`p0133:c01`).

**Finding:** the privilege wording is internally inconsistent with the source's own distinction between `DROP` and `DELETE`. The correct privilege for any concrete RDBMS/version is **[Needs confirmation]**; do not substitute a model-memory answer into the source artifact.

## F-02 · [Source wording/code mismatch] · CHECK value ' US' versus 'US'

On `p0117:c01`, prose states that allowed country values are `'CA'` and **`' US'`** (with a leading space). The code directly below uses:
```sql
CHECK (country IN ('CA', 'US'))
```

A second form on the same page also uses `('CA','US')`.

**Finding:** prose and code differ by a leading space. The code variant is preserved in commands where a runnable fragment is required, while this register preserves the conflicting prose. Whether the space is typographic/extraction noise or intentional is **[Needs confirmation]**.

## F-03 · [Source extraction issue] · Russian identifier inside SQL Server ALTER COLUMN

Table 5.17 continuation on `p0136:c01` shows:
```sql
ALTER TABLE my_table
      ALTER COLUMN страна
      VARCHAR(2) NULL;
```

The table definition used immediately before this section (`p0134:c01`–`p0135:c01`) names the column `country`, not `страна`.

**Finding:** the SQL Server snippet contains a Russian word where the surrounding source consistently uses the English identifier. This may be translation/layout/extraction contamination. Do **not** silently change it to `country`; executable target identifier is **[Needs confirmation]**.

## F-04 · [Source wording/code mismatch] · Oracle CREATE INDEX quotes

On `p0143:c01` the prose says that for Oracle the column name should be uppercase and quoted; the code is extracted as:
```sql
CREATE INDEX my_index ON my_table
  ('LOG_DATE');
```

**Finding:** this is preserved exactly as text-layer output. The chapter does not independently explain whether those marks are intended as identifier quotes or whether extraction changed typography. Runnable Oracle syntax is **[Needs confirmation]**; no silent normalization is allowed.

## F-05 · [Source contradiction] · transaction changes described as “not made” versus “not permanent”

On `p0151:c01` and `p0153:c01`, the narrative says that while in transaction mode “no changes will be made to the database.”

However:
- `p0152:c01` executes `DELETE`, then shows a `SELECT` result where the row is already absent, and says the change “has not become permanent.”
- `p0154:c01` executes a broad `DELETE`, shows the table empty, then uses `ROLLBACK`.

**Finding:** the chapter's own examples demonstrate a distinction between an **uncommitted visible change in the transaction** and a **permanent committed change**, while some prose compresses this to “no changes.” Artifacts use the more precise source-supported phrase “uncommitted/not permanent” without asserting cross-RDBMS isolation semantics.

## F-06 · [Source wording/code mismatch] · DELETE all rows described as deleting “the whole table”

On `p0154:c01`:
```sql
DELETE FROM books WHERE title LIKE '%%';
```
is described as accidentally deleting “the whole table.” The immediately following `SELECT * FROM books;` renders an **empty table result with columns still present**, and the action is then rolled back.

Earlier, `p0133:c01` explicitly distinguishes:
- `DELETE FROM my_table;` → remove all rows while table definition remains.
- `DROP` → get rid of the table itself.

**Finding:** wording on PDF 154 conflates all-row deletion with table-object deletion. No source correction is made; commands artifact classifies it as deleting all rows because that distinction is explicitly stated elsewhere in the same chapter.

## F-07 · [Source wording/code mismatch] · “truncate” terminology mapped to DELETE FROM

On `p0114:c01` and `p0133:c01`, the source uses “truncate/truncating” in a descriptive sense while showing `DELETE FROM` to remove all rows and preserve the table definition.

**Finding:** the chapter does not present a standalone `TRUNCATE TABLE` operator in these passages. Artifacts therefore preserve `DELETE FROM` as the actual source command and do not invent a `TRUNCATE` command from general SQL knowledge.

## F-08 · [Needs confirmation] · version-sensitive dialect claims

The chapter includes version/product behavior claims that are not independently verified in `rag_only` mode:
- SQLite limitations for dropping columns/altering constraints (`p0131:c01`).
- MySQL restriction on updating a table from a subquery over itself (`p0140:c01`).
- Oracle `VARCHAR` versus `VARCHAR2` advice (`p0123:c01`).
- Compound-index usefulness based on first/second column ordering (`p0144:c01`).
- Transaction-start behavior by RDBMS (`p0151:c01`, `p0153:c01`).

These are **source assertions**, not current compatibility guarantees. Current behavior for a concrete version is **[Needs confirmation]**.

## Control policy

- Canonical RAG is unchanged.
- Conflicting variants remain visible.
- `commands.md` never upgrades a questionable snippet into an assumed-correct runnable command.
- Any cross-source verification requires a separate user instruction; until then this chapter stays `rag_only`.
