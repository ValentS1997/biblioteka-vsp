# Source-confirmed SQL examples — глава 8

**Source:** PDF 244–272, RAG `p0244:c01`–`p0272:c01`.  
**Execution:** не выполнялось. Target RDBMS/version/data volume — [Needs confirmation].

## 1. CASE

**Simple CASE, PDF 246:**
```sql
SELECT name, flag,
   CASE flag WHEN 1 THEN 'vip'
   WHEN 0 THEN 'reserved seating'
   ELSE 'general admission' END AS ticket
FROM concert;
```

**Searched CASE, PDF 248:**
```sql
SELECT name, flag,
   CASE WHEN name = 'anton' THEN 'vip'
   WHEN flag IN (0,1) THEN 'reserved seating'
   ELSE 'general admission' END AS ticket
FROM concert;
```

Class: **read-only**.  
Source semantics: first matching WHEN wins; absent ELSE with no match returns NULL.

## 2. GROUP BY / list aggregation

```sql
SELECT name,
       SUM(calories) AS total_calories
FROM workouts
GROUP BY name;
```

```sql
SELECT id, name,
       COUNT(date) AS workouts,
       SUM(calories) AS calories
FROM daily_workouts
GROUP BY id, name;
```

Read-only/workload-generating. Source: `p0250:c01`–`p0251:c01`.

MySQL list example:
```sql
SELECT name,
       GROUP_CONCAT(calories) AS calories_list
FROM workouts
GROUP BY name;
```

Other source variants: Oracle LISTAGG, PostgreSQL ARRAY_AGG, SQL Server STRING_AGG, SQLite GROUP_CONCAT (`p0252:c01`–`p0253:c01`). Exact ordering/distinct syntax is dialect/version-sensitive.

## 3. ROLLUP / CUBE / GROUPING SETS

```sql
SELECT year, month,
       SUM(amount) AS total
FROM spendings
GROUP BY ROLLUP(year, month)
ORDER BY year, month;
```

```sql
SELECT year, month,
       SUM(amount) AS total
FROM spendings
GROUP BY CUBE(year, month)
ORDER BY year, month;
```

```sql
SELECT year, month,
       SUM(amount) AS total
FROM spendings
GROUP BY GROUPING SETS(year, month)
ORDER BY year, month;
```

Class: **read-only / potentially workload-generating**.  
Source: `p0254:c01`–`p0256:c01`. Input/output inconsistencies are documented in `source-findings.md`; do not use displayed totals as verified execution results.

## 4. Window basics / ranking

```sql
SELECT name,
       ROW_NUMBER() OVER (
         PARTITION BY name
         ORDER BY month
       ) AS sale_month
FROM sales;
```

```sql
SELECT gender, name,
       ROW_NUMBER() OVER (
         PARTITION BY gender
         ORDER BY babies DESC
       ) AS popularity
FROM baby_names;
```

Read-only. Source: `p0257:c01`–`p0260:c01`.

Source comparison:
- ROW_NUMBER: ties get distinct sequence numbers.
- RANK: ties share rank and later ranks may skip.
- DENSE_RANK: ties share rank without gaps.

## 5. FIRST_VALUE / NTH_VALUE

```sql
SELECT gender, name, babies,
       FIRST_VALUE(name) OVER (
         PARTITION BY gender
         ORDER BY babies DESC
       ) AS top_name
FROM baby_names;
```

```sql
SELECT gender, name, babies,
       NTH_VALUE(name, 2) OVER (
         PARTITION BY gender
         ORDER BY babies DESC
       ) AS second_name
FROM baby_names;
```

Read-only. Source: `p0261:c01`–`p0263:c01`. Window-frame defaults/support can alter behavior and remain [Needs confirmation].

## 6. Filtering window results through derived table

```sql
SELECT *
FROM (
  SELECT gender, name, babies,
         ROW_NUMBER() OVER (
           PARTITION BY gender
           ORDER BY babies DESC
         ) AS popularity
  FROM baby_names
) AS popularity_table
WHERE popularity IN (1,2);
```

Read-only. Source: `p0263:c01`–`p0264:c01`. Source notes Oracle omits `AS` for derived-table alias.

## 7. LAG

```sql
SELECT gender, name, babies,
       LAG(name, 2, 'No name')
       OVER (
         PARTITION BY gender
         ORDER BY babies DESC
       ) AS prior_name_2
FROM baby_names;
```

Read-only. Source: `p0264:c01`–`p0265:c01`.

## 8. Moving average / running total

```sql
SELECT name, month, sales,
       AVG(sales) OVER (
         PARTITION BY name
         ORDER BY month
         ROWS BETWEEN 2 PRECEDING
                  AND CURRENT ROW
       ) AS three_month_ma
FROM sales;
```

```sql
SELECT name, month, sales,
       SUM(sales) OVER (
         PARTITION BY name
         ORDER BY month
         ROWS BETWEEN UNBOUNDED PRECEDING
                  AND CURRENT ROW
       ) AS running_total
FROM sales;
```

Read-only/workload-generating. Source: `p0266:c01`–`p0268:c01`.

## 9. PIVOT

Oracle:
```sql
SELECT *
FROM fruits
PIVOT (
  COUNT(id) FOR fruit IN (
    'strawberries', 'grapefruit', 'watermelon'
  )
);
```

SQL Server:
```sql
SELECT *
FROM fruits
PIVOT (
  COUNT(id) FOR fruit IN (
    [strawberries], [grapefruit], [watermelon]
  )
) AS fruits_pivot;
```

Manual CASE alternative from source:
```sql
SELECT name,
       SUM(CASE WHEN fruit = 'strawberries'
           THEN 1 ELSE 0 END) AS strawberries,
       SUM(CASE WHEN fruit = 'grapefruit'
           THEN 1 ELSE 0 END) AS grapefruit,
       SUM(CASE WHEN fruit = 'watermelon'
           THEN 1 ELSE 0 END) AS watermelon
FROM fruits
GROUP BY name
ORDER BY name;
```

All read-only. Source: `p0269:c01`–`p0270:c01`.

## 10. UNPIVOT

Oracle source:
```sql
SELECT *
FROM favorite_fruits
UNPIVOT (
  fruit FOR rank IN (
    fruit_one AS 1,
    fruit_two AS 2,
    fruit_thr AS 3
  )
);
```

SQL Server source:
```sql
SELECT *
FROM favorite_fruits
UNPIVOT (
  fruit FOR rank IN (
    fruit_one,
    fruit_two,
    fruit_thr
  )
) AS fruit_unpivot
WHERE fruit <> '';
```

Read-only. Source: `p0271:c01`. SQL Server output-shape mismatch with numeric rank is registered separately.

## 11. Manual UNPIVOT with UNION ALL

Source `p0272:c01`:
```sql
WITH all_fruits AS (
  SELECT id, name,
         fruit_one AS fruit,
         1 AS rank
  FROM favorite_fruits
  UNION ALL
  SELECT id, name,
         fruit_two AS fruit,
         2 AS rank
  FROM favorite_fruits
  UNION ALL
  SELECT id, name,
         fruit_three AS fruit,
         3 AS rank
  FROM favorite_fruits
)
SELECT *
FROM all_fruits
WHERE fruit <> ''
ORDER BY id, name, fruit;
```

Read-only. **Source mismatch:** table column is `fruit_thr`, but manual version uses `fruit_three`. Do not correct silently.

## Modifying actions / rollback

No completed state-changing statement is required by chapter 8 examples. The prose says CASE logic may be persisted using UPDATE, but no UPDATE procedure is supplied.

- Read-only examples: rollback [Not applicable].
- Any later DML reuse: **[Needs confirmation]** with separate preview/verification/rollback.
