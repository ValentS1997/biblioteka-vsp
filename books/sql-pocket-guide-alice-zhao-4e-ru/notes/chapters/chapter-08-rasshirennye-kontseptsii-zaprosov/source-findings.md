# Source findings — глава 8. Расширенные концепции запросов

**Scope:** PDF 244–272, RAG `p0244:c01`–`p0272:c01`.  
**Policy:** preserve source, no silent correction.

## F-01 · [Source data mismatch] · spendings input versus GROUP BY result

`p0254:c01` shows source rows:
```text
2019 1 20
2019 1 30
2019 1 42
2020 2 37
2020 2 100
```

Immediately below, GROUP BY result is:
```text
2019 1  50
2020 1  42
2020 2 137
```

The third input row is labeled 2019, but the aggregate output treats the 42 as 2020/month 1.

**Finding:** example data and aggregate result are inconsistent. Do not alter either variant in source-grounded artifacts.

## F-02 · [Source contradiction] · MySQL WITH ROLLUP wording

`p0255:c01` says:
- standard `GROUP BY ROLLUP(year, month)` works in Oracle/PostgreSQL/SQL Server;
- “Синтаксис в MySQL выглядит так: GROUP BY year, month WITH ROLLUP — и работает в SQL Server.”

The final product reference conflicts with the sentence's MySQL framing and the preceding statement.

**Status:** exact intended product label [Needs confirmation].

## F-03 · [Source data mismatch] · GROUPING SETS output year

`p0256:c01` output contains:
```text
2019  50
2019 179
     1 92
     2 137
```

Earlier totals on `p0255:c01` show 2019 total 50 and 2020 total 179.

**Finding:** the second annual row appears inconsistent with the preceding example. No correction applied.

## F-04 · [Needs confirmation] · GROUP BY “more efficient” optimization claim

`p0251:c01` recommends grouping only by `id` and using `MAX(name)` when each id has exactly one name, and states this is more efficient because GROUP BY uses one column.

The functional-dependency precondition is explicit, but no execution plan/benchmark is shown. Performance gain is therefore **[Needs confirmation]**.

## F-05 · [Needs confirmation] · list aggregation product/version syntax

`p0253:c01` gives GROUP_CONCAT/LISTAGG/ARRAY_AGG/STRING_AGG syntax, ordering and DISTINCT support by product. These are source assertions tied to the edition, not current-version verification.

Specially, the table labels a “separator” for PostgreSQL ARRAY_AGG although ARRAY_AGG returns an array rather than the same string form used by the neighboring functions. Preserve source wording; exact output representation [Needs confirmation].

## F-06 · [Source output mismatch] · SQL Server UNPIVOT rank

Expected result on `p0271:c01` has numeric `rank` values 1/2/3.

SQL Server source:
```sql
UNPIVOT (
  fruit FOR rank IN (
    fruit_one,
    fruit_two,
    fruit_thr
  )
)
```

The source does not show a mapping from the input column names to numeric 1/2/3 as the Oracle example does with `AS 1/2/3`.

**Finding:** expected numeric rank is not explained by the shown SQL Server query. Actual output [Needs confirmation].

## F-07 · [Source code mismatch] · fruit_thr versus fruit_three

Input table and Oracle/SQL Server UNPIVOT use column `fruit_thr` (`p0271:c01`).

Manual UNION ALL alternative on `p0272:c01` uses:
```sql
fruit_three AS fruit
```

**Finding:** identifier mismatch. Do not silently normalize.

## F-08 · [Needs confirmation] · MySQL constant-column assertion

`p0272:c01` says MySQL does not support inserting constants into a result column such as:
`1 AS rank`, `2 AS rank`, `3 AS rank`,
and instructs removal of those lines.

This claim is not supported by another demonstration in the chapter and is not externally verified in `rag_only`. Treat as source assertion requiring version-specific confirmation.

## F-09 · [Needs confirmation] · window ORDER BY/support/default frame claims

`p0258:c01` says ORDER BY inside the window is optional in MySQL/PostgreSQL/SQLite and required in Oracle/SQL Server for the shown discussion.

`NTH_VALUE`, FIRST/LAST, ROWS/RANGE and derived-table alias behavior may differ by product/version/default frame. Current behavior is **[Needs confirmation]**.

## F-10 · [Source semantics limitation] · filtering FIRST_VALUE by name

`p0261:c01` filters:
```sql
WHERE name = top_name
```
to return “only two rows” in the sample.

This works for the provided data because top names are unique. With ties or repeated names, cardinality may differ; the chapter does not address this case.

**Status:** not an error for the shown dataset, but a scope limitation.

## Control

Canonical source/RAG unchanged. Findings record contradictions, mismatches and unverified product claims only; no corrected SQL is written back into source.
