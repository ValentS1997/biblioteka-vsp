# Cheatsheet — глава 9. Работа с несколькими таблицами и запросами

**Source:** PDF 273–303, RAG `p0273:c01`–`p0303:c01`. SQL не выполнялся.

## Symptom / problem framing

Нужно объединить данные из нескольких таблиц или нескольких SELECT и выбрать подход:
- JOIN → соединить столбцы по relation;
- UNION/EXCEPT/INTERSECT → объединить/сравнить result sets по строкам;
- CTE → именовать промежуточный запрос или строить recursion.

Основные риски: неверная cardinality, accidental Cartesian product, NULL в anti-join logic, неэквивалентные workarounds и runaway recursion.

## Baseline / context

| Концепция | Source semantics |
|---|---|
| INNER JOIN | only matching rows |
| LEFT/RIGHT/FULL | preserve one/both sides + NULLs |
| USING | equijoin по одинаковому имени column |
| NATURAL JOIN | автоматически все одинаковые column names |
| CROSS JOIN | все комбинации строк |
| Self Join | таблица соединяется сама с собой |
| UNION | combine rows + remove duplicates |
| UNION ALL | combine rows + preserve duplicates |
| EXCEPT/MINUS | set difference |
| INTERSECT | set intersection |
| CTE | named temporary query result |
| Recursive CTE | anchor + recursive member |

Target RDBMS/version/cardinality/indexes/recursion limit: **[Needs confirmation]**.

## Read-only checks

INNER JOIN:
```sql
SELECT *
FROM states s
INNER JOIN pets p
  ON s.name = p.name;
```

LEFT JOIN:
```sql
SELECT *
FROM states s
LEFT JOIN pets p
  ON s.name = p.name;
```

UNION:
```sql
SELECT name, origin FROM staff
UNION
SELECT name, country FROM residents;
```

CTE:
```sql
WITH avg_dept_salary AS (
  SELECT dept, AVG(salary) AS avg_salary
  FROM employees
  GROUP BY dept
)
SELECT *
FROM avg_dept_salary
ORDER BY avg_salary DESC
LIMIT 1;
```

All read-only; execution = **[Not executed]**.

## Interpretation

### JOIN cardinality

One-to-many matches duplicate the left/right entity across result rows. Before aggregation, verify whether repeated rows are expected.

### NATURAL JOIN

Source explicitly warns it can silently change behavior if schema adds/removes same-named columns. Suitable only for quick/ad-hoc use in the source framing, not stable production query design.

### Set operations

- UNION removes duplicates.
- UNION ALL preserves duplicates.
- EXCEPT removes right-side rows from left result.
- INTERSECT keeps overlap.

Before set operations: same number of selected columns; compatible types according to target engine. Exact coercion rules [Needs confirmation].

### Recursive CTE

Pattern:
1. anchor row(s);
2. UNION ALL;
3. recursive member references the CTE;
4. termination predicate.

Missing termination / unexpected graph cycles may expand work dramatically; source does not define operational recursion guards.

## Next action

1. Confirm target RDBMS/version.
2. Identify relationship/cardinality and expected row count.
3. Preview each input query independently.
4. For JOIN, validate join keys and duplicate behavior.
5. For UNION/EXCEPT/INTERSECT, verify column count/types and NULL semantics.
6. For recursive CTE, define termination and expected depth.
7. Compare output row counts to acceptance criteria.
8. Only then consider production execution.

## Modifying action

**[Not applicable]** — chapter 9 examples are SELECT/CTE and do not persist data changes.

Potential workload effects remain significant for CROSS JOIN and recursion.

## Verification / acceptance checks

- Join predicate references intended columns.
- No unintended Cartesian product.
- Outer-join NULL rows are expected.
- NATURAL JOIN not used where schema stability matters.
- UNION duplicate behavior matches requirement.
- Anti/intersection workaround is semantically equivalent on all selected columns.
- Recursive CTE termination is explicit.
- Expected row count/depth known before execution.

## Rollback

Read-only queries: [Not applicable].  
If query causes excessive workload, cancellation/timeout procedure for target environment: **[Needs confirmation]**.
