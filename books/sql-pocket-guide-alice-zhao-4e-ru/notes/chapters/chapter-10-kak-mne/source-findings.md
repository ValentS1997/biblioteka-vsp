# Source findings — глава 10. Как мне?..

**Scope:** PDF 304–315, RAG `p0304:c01`–`p0315:c01`.  
**Policy:** preserve source, no silent correction.

## F-01 · [Source semantics limitation] · duplicate rows with NULL keys

Duplicate solution on `p0306:c01`:
- groups by `tea, temperature`;
- joins back with `t.tea = d.tea AND t.temperature = d.temperature`.

The sample contains no NULL values in these columns.

**Finding:** the chapter does not demonstrate whether duplicate groups containing NULL can be joined back by this equality predicate. Null-key behavior is [Needs confirmation].

## F-02 · [Source semantics limitation] · max-per-group ties

`p0308:c01` selects `MAX(date)` for each employee and joins to sales on employee + date.

If an employee has multiple rows on the same maximum date, all matching rows can satisfy the join; the sample has one latest row per employee.

**Finding:** source solves the shown dataset, not deterministic single-row tie-breaking.

## F-03 · [Source wording/output-shape limitation] · ARRAY_AGG alongside string aggregators

`p0310:c01`–`p0311:c01` describes “объединить данные ... в одну строку” and then lists:
- GROUP_CONCAT,
- LISTAGG,
- ARRAY_AGG,
- STRING_AGG.

The chapter does not show PostgreSQL ARRAY_AGG output.

**Finding:** source groups these functions as alternatives for multi-row aggregation, but does not establish identical output data type/format. Preserve function names without normalizing output semantics.

## F-04 · [Needs confirmation] · “all tables” metadata scope

`p0312:c01` says the final catalog/schema/owner filter is optional and, if omitted, “будут возвращены все таблицы.”

The actual visibility of metadata may depend on RDBMS, privileges, current catalog/user and system objects.

**Finding:** interpret as source wording, not a guarantee of unrestricted global visibility.

## F-05 · [Needs confirmation] · SQLite metadata limitation

`p0312:c01` says SQLite has no table containing all column names and recommends `.tables` plus `pragma table_info(my_table)`.

This is an edition/version assertion. Current SQLite metadata capabilities are not externally verified in `rag_only`.

## F-06 · [Source semantics limitation] · Oracle UPDATE lacks match filter

Oracle source on `p0314:c01`:
```sql
UPDATE deals d
SET name = (
  SELECT p.name
  FROM products p
  WHERE d.id = p.id
);
```

There is no outer WHERE restricting target rows to ids that have a product match.

The sample `deals` rows 102/103 both have corresponding product rows, so unmatched behavior is not demonstrated.

**Finding:** generalizing this query to datasets with unmatched ids is unsafe without target verification.

## F-07 · [Source code/semantics ambiguity] · PostgreSQL/SQLite UPDATE repeats target table

Source on `p0314:c01`:
```sql
UPDATE deals
SET name = p.name
FROM deals d
     INNER JOIN products p
     ON d.id = p.id
WHERE deals.id = p.id;
```

The target table `deals` appears both as UPDATE target and again as `deals d` in FROM. The alias `d` participates in the JOIN but is not used by the final WHERE target relation except through p.

**Finding:** source intent is clear (update matching ids), but exact semantics/runnable correctness for PostgreSQL and SQLite is **[Needs confirmation]**. No silent rewrite is performed.

## F-08 · [Needs confirmation] · multi-match UPDATE semantics

All UPDATE examples assume one product row per id. The source does not discuss duplicate `products.id` values.

**Finding:** if source relation is one-to-many, dialects may differ or update may be ambiguous; uniqueness prerequisite is [Needs confirmation].

## F-09 · [Source-supported safety boundary] · rollback depends on transaction

`p0315:c01` states that UPDATE results cannot be undone, except when a transaction is started before UPDATE.

This aligns with the book's transaction framing, but exact autocommit/transaction semantics of a concrete engine remain [Needs confirmation].

Artifacts therefore require transaction verification before presenting rollback as available.

## Control

Canonical source/RAG unchanged. Findings do not adjudicate dialect correctness from external knowledge.
