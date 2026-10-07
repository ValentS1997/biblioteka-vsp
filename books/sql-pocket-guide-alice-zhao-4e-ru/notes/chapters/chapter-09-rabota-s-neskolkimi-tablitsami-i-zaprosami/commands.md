# Source-confirmed SQL examples — глава 9

**Source:** PDF 273–303, RAG `p0273:c01`–`p0303:c01`.  
**Execution:** не выполнялось. Target RDBMS/version/cardinality/recursion limits — [Needs confirmation].

## 1. INNER JOIN

```sql
SELECT *
FROM states s
INNER JOIN pets p
  ON s.name = p.name;
```

Class: **read-only**. Source: `p0274:c01`–`p0280:c01`.

Multiple tables:
```sql
SELECT *
FROM states s
INNER JOIN pets p
  ON s.name = p.name
INNER JOIN lunch l
  ON s.name = l.name;
```

Multiple-key join:
```sql
SELECT *
FROM states_ages s
INNER JOIN pets_ages p
  ON s.name = p.name
 AND s.age = p.age;
```

Risk: row multiplication from one-to-many matches. Verify cardinality before aggregating.

## 2. Outer joins

```sql
SELECT *
FROM states s
LEFT JOIN pets p
  ON s.name = p.name;
```

```sql
SELECT *
FROM states s
RIGHT JOIN pets p
  ON s.name = p.name;
```

```sql
SELECT *
FROM states s
FULL OUTER JOIN pets p
  ON s.name = p.name;
```

Read-only. Source: `p0281:c01`–`p0282:c01`.

Product support claims are edition/version-sensitive. Source says SQLite lacks RIGHT JOIN and MySQL/SQLite lack FULL OUTER JOIN; current behavior [Needs confirmation].

## 3. USING / NATURAL JOIN

```sql
SELECT *
FROM states
INNER JOIN pets
USING (name);
```

```sql
SELECT *
FROM states_ages
NATURAL JOIN pets_ages;
```

Read-only. Source: `p0283:c01`–`p0284:c01`.

Source warning: NATURAL JOIN can change unexpectedly when schema gains/loses same-named columns. Do not treat as stable production pattern without explicit schema control.

## 4. CROSS JOIN / old join syntax

```sql
SELECT *
FROM states
CROSS JOIN pets;
```

Equivalent conceptual source form:
```sql
SELECT *
FROM states, pets;
```

Read-only but **potentially workload-generating**. Row count can approach product of input row counts.

## 5. Self join

Source example:
```sql
SELECT e1.emp_name, e2.emp_name AS mgr_name
FROM employee e1, employee e2
WHERE e1.mgr_id = e2.emp_id;
```

Read-only. Source: `p0286:c01`.

Pairing within department:
```sql
SELECT e.dept, e.emp_name, matching_emp.emp_name
FROM employee e, employee matching_emp
WHERE e.dept = matching_emp.dept
  AND e.emp_name <> matching_emp.emp_name;
```

Source removes mirrored pairs by adding:
```sql
AND e.emp_name < matching_emp.emp_name
```

Exact ordering/collation semantics [Needs confirmation].

## 6. UNION / UNION ALL

```sql
SELECT name, origin FROM staff
UNION
SELECT name, country FROM residents;
```

UNION removes duplicate result rows.

```sql
SELECT name, origin FROM staff
UNION ALL
SELECT name, country FROM residents;
```

UNION ALL preserves duplicates.

Source requirements:
- same number of output columns;
- output names from first SELECT;
- source says data types should match, with CAST as workaround.

Actual coercion rules are target-specific.

## 7. EXCEPT / MINUS

```sql
SELECT name FROM staff
EXCEPT
SELECT name FROM residents;
```

Source: read-only set difference.

Oracle source uses MINUS. MySQL workaround shown:
```sql
SELECT name
FROM staff
WHERE name NOT IN (
  SELECT name FROM residents
);
```

**Caution:** chapter 7 warns NOT IN can behave unexpectedly if subquery contains NULL. This workaround is safe only under additional NULL assumptions; see source findings.

## 8. INTERSECT

```sql
SELECT name, origin FROM staff
INTERSECT
SELECT name, country FROM residents;
```

Source MySQL workaround:
```sql
SELECT s.name, s.origin
FROM staff s
INNER JOIN residents r
  ON s.name = r.name;
```

**Caution:** INTERSECT compares both selected columns in the source query, while workaround joins only on name. Not generally equivalent; see source findings.

## 9. Non-recursive CTE

```sql
WITH my_cte AS (
  SELECT name, AVG(grade) AS avg_grade
  FROM my_table
  GROUP BY name
)
SELECT *
FROM my_cte
WHERE avg_grade < 70;
```

Read-only. Source: `p0295:c01`.

CTE vs subquery example:
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

Dialect-specific top-N form [Needs confirmation].

## 10. Recursive CTE: sequence

```sql
WITH RECURSIVE my_cte(n) AS (
  SELECT 1
  UNION ALL
  SELECT n + 1
  FROM my_cte
  WHERE n < 10
)
SELECT * FROM my_cte;
```

Read-only / **workload-generating**. Source: `p0295:c01`.

Termination predicate is mandatory operationally; actual recursion depth/limit differs by RDBMS.

## 11. Recursive dates

MySQL source:
```sql
WITH RECURSIVE my_dates(dt) AS (
  SELECT '2021-03-01'
  UNION ALL
  SELECT dt + INTERVAL 1 DAY
  FROM my_dates
  WHERE dt < '2021-03-06'
)
SELECT * FROM my_dates;
```

Then:
```sql
SELECT d.dt, s.price
FROM my_dates d
LEFT JOIN stock_prices s
  ON d.dt = s.date;
```

Optional fill:
```sql
SELECT d.dt,
       COALESCE(
         s.price,
         LAG(s.price) OVER (ORDER BY d.dt)
       ) AS price
...
```

Read-only. Source: `p0298:c01`–`p0301:c01`.

The LAG fallback is demonstrated only for isolated one-row gaps. Consecutive missing rows are not validated.

## 12. Recursive hierarchy

MySQL source:
```sql
WITH RECURSIVE my_cte (id, name, lineage) AS (
  SELECT id, name, name AS lineage
  FROM family_tree
  WHERE parent_id IS NULL

  UNION ALL

  SELECT ft.id, ft.name,
         CONCAT(mc.lineage, ' > ', ft.name)
  FROM family_tree ft
  INNER JOIN my_cte mc
    ON ft.parent_id = mc.id
)
SELECT *
FROM my_cte
ORDER BY id;
```

Read-only / workload-generating. Source: `p0301:c01`–`p0303:c01`.

Graph cycles, depth and duplicate paths are not operationally bounded by this example.

## Modifying actions / rollback

No state-changing SQL is required in chapter 9 examples.

- Data rollback: [Not applicable].
- Query cancellation / timeout for accidental CROSS JOIN or runaway recursion: **[Needs confirmation]** for target environment.
