# Source findings — глава 9. Работа с несколькими таблицами и запросами

**Scope:** PDF 273–303, RAG `p0273:c01`–`p0303:c01`.  
**Policy:** preserve source, no silent correction.

## F-01 · [Source code mismatch] · self-join INNER JOIN without ON

Table 9.3 on `p0277:c01` gives a “new syntax” self join:
```sql
SELECT *
FROM states s1
INNER JOIN states s2
WHERE s1.region = s2.region;
```

The source itself elsewhere defines standard JOIN syntax as `JOIN ... ON ...`.

**Finding:** shown self-join form omits ON and moves the condition to WHERE after INNER JOIN. Runnable target syntax is [Needs confirmation]. Do not silently insert ON.

## F-02 · [Source semantics mismatch] · CTE example names SUM(order_id) as num_orders

Table 9.1 continuation on `p0274:c01` shows:
```sql
SELECT name,
       SUM(order_id) AS num_orders
FROM customers
GROUP BY name
```

Alias `num_orders` suggests a count, while expression is SUM of order_id.

**Finding:** alias and aggregation semantics are inconsistent. Preserve source; do not replace SUM with COUNT from inference.

## F-03 · [Needs confirmation] · UNION ALL performance claim

`p0291:c01` says UNION performs an additional hidden sort to detect duplicates and recommends UNION ALL for performance when duplicates are impossible.

No execution plan/benchmark is provided, and duplicate elimination implementation is optimizer-specific.

**Finding:** semantic distinction UNION vs UNION ALL is source-supported; implementation/performance mechanism is [Needs confirmation].

## F-04 · [Cross-chapter semantic risk] · MySQL EXCEPT workaround uses NOT IN

`p0293:c01` recommends:
```sql
WHERE name NOT IN (SELECT name FROM residents)
```
as a MySQL workaround for EXCEPT.

Earlier source `p0197:c01` explicitly warns that NOT IN can return no expected rows if the subquery contains NULL.

The chapter 9 sample residents.name has no NULL, so shown data can work; generalized workaround requires a NOT NULL assumption or alternative logic.

## F-05 · [Source semantics mismatch] · INTERSECT workaround compares fewer columns

Source INTERSECT on `p0293:c01`:
```sql
SELECT name, origin FROM staff
INTERSECT
SELECT name, country FROM residents;
```

MySQL workaround:
```sql
SELECT s.name, s.origin
FROM staff s
INNER JOIN residents r
  ON s.name = r.name;
```

INTERSECT compares two-column rows, while workaround only requires matching `name`.

**Finding:** these are not generally equivalent if same name has different origin/country. The sample happens to yield tahani/england.

## F-06 · [Needs confirmation] · set-operation precedence

`p0294:c01` states operations are evaluated top-to-bottom except INTERSECT has precedence over UNION and EXCEPT.

Exact precedence/parentheses support can be dialect/version-specific. Source recommends parentheses; current target semantics remain [Needs confirmation].

## F-07 · [Source portability limitation] · LIMIT replacement examples

`p0297:c01` says replace `LIMIT 1` with `ROWNUM = 1` in Oracle and `TOP 1` in SQL Server.

The source does not show complete rewritten query blocks preserving the preceding `ORDER BY avg_salary DESC`.

**Finding:** equivalence of merely replacing the token is not demonstrated. Exact top-N query per target is [Needs confirmation].

## F-08 · [Source semantics limitation] · one-step LAG fill

`p0300:c01` fills missing prices using:
```sql
COALESCE(s.price, LAG(s.price) OVER (ORDER BY d.dt))
```

The sample gaps are isolated one-day gaps, so previous source row has a price.

**Finding:** consecutive NULL gaps are not covered; LAG of the immediately previous row can itself be NULL. Source does not claim a general forward-fill algorithm, so artifacts keep scope limited to the shown sample.

## F-09 · [Needs confirmation] · JOIN support claims

`p0282:c01` says:
- SQLite does not support RIGHT JOIN;
- MySQL and SQLite do not support FULL OUTER JOIN.

These are edition/version assertions. Current support for concrete versions is [Needs confirmation].

## F-10 · [Needs confirmation] · recursive CTE syntax/support

`p0295:c01` says:
- MySQL/PostgreSQL require RECURSIVE;
- Oracle/SQL Server omit it;
- SQLite accepts either.

Tables 9.4/9.5 give product-specific recursive date/hierarchy syntax.

All current-version recursion limits, cycle behavior and exact syntax remain [Needs confirmation].

## F-11 · [Source extraction/layout risk] · recursive-date table line wrapping

Table 9.4 spans `p0300:c01`–`p0301:c01`; PostgreSQL/SQL Server expressions are line-wrapped in the text layer (e.g. date literal and CAST expressions split across lines).

**Policy:** do not reconstruct a runnable command solely from wrapped table text without target-specific verification.

## Control

Canonical source/RAG unchanged. Findings distinguish source contradiction, semantic limitation and version-sensitive behavior; no external adjudication is imported.
