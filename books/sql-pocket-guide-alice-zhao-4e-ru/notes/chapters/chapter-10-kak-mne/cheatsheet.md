# Cheatsheet — глава 10. Как мне?..

**Source:** PDF 304–315, RAG `p0304:c01`–`p0315:c01`. SQL не выполнялся.

## Symptom / problem framing

Нужно решить типовые SQL-задачи, комбинируя уже изученные конструкции:
- убрать/найти duplicates;
- выбрать latest/max row per group;
- concatenate fields;
- искать metadata;
- обновить одну таблицу значениями из другой.

## Baseline / context

| Задача | Pattern |
|---|---|
| Unique combinations | `SELECT DISTINCT ...` |
| Duplicate rows | CTE + GROUP BY + HAVING + JOIN |
| Latest row per entity | MAX per group + JOIN back |
| One-row concat | CONCAT / `||` |
| Multi-row aggregation | GROUP_CONCAT / LISTAGG / ARRAY_AGG / STRING_AGG |
| Find columns | information_schema / all_tab_columns / SQLite metadata commands |
| Cross-table update | dialect-specific UPDATE + transaction |

Target RDBMS/version/data shape/transaction semantics: **[Needs confirmation]**.

## Read-only checks

Unique combinations:
```sql
SELECT DISTINCT tea, temperature
FROM teas;
```

Duplicates:
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

Latest row per employee:
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

Metadata example:
```sql
SELECT table_name, column_name
FROM information_schema.columns
WHERE column_name LIKE '%city%'
  AND table_catalog = 'my_db_name';
```

Execution status: **[Not executed]**.

## Interpretation

### Duplicates

`DISTINCT` answers “what unique combinations exist?”.  
CTE + `HAVING COUNT(*) > 1` answers “which combinations are duplicated?”, and JOIN back restores row ids.

### Max-per-group

Aggregate query finds the max date; JOIN returns the complete row. If two source rows share the same maximum date, this pattern can return both; source sample contains no tie.

### Concatenation

Single-row concatenation and multi-row aggregation are different operations. Multi-row function name/output varies by RDBMS.

### Metadata

Metadata queries are read-only, but visibility can depend on catalog/user/privileges. “All tables” must be interpreted within target metadata visibility: [Needs confirmation].

## Next action

1. Confirm target RDBMS/version.
2. Validate sample data and NULL/tie cases.
3. Run only read-only SELECT variant first.
4. For cross-table UPDATE, build a preview SELECT with same join/subquery condition.
5. Confirm expected affected-row count.
6. Start transaction only if target semantics support rollback for this operation.
7. UPDATE.
8. Post-update SELECT verification.
9. COMMIT only after acceptance; otherwise ROLLBACK if still available.

## Modifying action

Source chapter includes cross-table UPDATE. Example SQL differs per product.

**Effect:** modifies `deals.name` from `products.name` for matching ids according to shown dialect.

**Risks:**
- wrong join/subquery scope;
- unmatched-row behavior;
- unexpected multi-match behavior;
- more affected rows than expected;
- COMMIT removes rollback path.

**Required pre-check:** source tables and a preview JOIN/SELECT.  
**Verification:** SELECT from `deals` after UPDATE before COMMIT.  
**Rollback:** transaction rollback only if supported and still uncommitted; otherwise **[Needs confirmation]**.

## Verification / acceptance checks

- Duplicate grouping columns match business definition.
- NULL duplicate semantics explicitly tested.
- Max-per-group ties explicitly tested.
- Concatenation output type/order checked.
- Metadata scope matches expected catalog/schema/user.
- UPDATE preview returns exactly expected ids.
- Post-update values match products.
- No COMMIT before verification.

## Rollback

Read-only tasks: [Not applicable].

Cross-table UPDATE: source explicitly says reversal is unavailable after the statement unless a transaction was started beforehand. Exact transaction/rollback behavior for target RDBMS/version: **[Needs confirmation]**.
