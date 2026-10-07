# Cheatsheet — глава 8. Расширенные концепции запросов

**Source:** PDF 244–272, RAG `p0244:c01`–`p0272:c01`. SQL не выполнялся.

## Symptom / problem framing

Нужно:
- условно отображать значения;
- агрегировать группы и subtotals;
- считать rank/running/moving metrics без схлопывания строк;
- преобразовать rows↔columns.

Основной риск — переносить advanced syntax между РСУБД без проверки frames/support/aliases/output semantics.

## Baseline / context

| Концепция | Source pattern |
|---|---|
| CASE | `CASE ... WHEN ... THEN ... ELSE ... END` |
| Group/list aggregate | `GROUP BY` + SUM/COUNT/GROUP_CONCAT/LISTAGG/... |
| Advanced grouping | ROLLUP / CUBE / GROUPING SETS |
| Window | `func() OVER (PARTITION BY ... ORDER BY ...)` |
| Ranking | ROW_NUMBER / RANK / DENSE_RANK |
| Position/window navigation | FIRST_VALUE / NTH_VALUE / LAG / LEAD |
| Frames | ROWS BETWEEN / RANGE BETWEEN |
| Shape transform | PIVOT / UNPIVOT, CASE / UNION ALL alternatives |

RDBMS/version/data volume/tie semantics: **[Needs confirmation]**.

## Read-only checks

Simple CASE:
```sql
SELECT name, flag,
  CASE flag
    WHEN 1 THEN 'vip'
    WHEN 0 THEN 'reserved seating'
    ELSE 'general admission'
  END AS ticket
FROM concert;
```

Searched CASE:
```sql
SELECT name, flag,
  CASE
    WHEN name = 'anton' THEN 'vip'
    WHEN flag IN (0,1) THEN 'reserved seating'
    ELSE 'general admission'
  END AS ticket
FROM concert;
```

Window:
```sql
SELECT gender, name,
       ROW_NUMBER() OVER (
         PARTITION BY gender
         ORDER BY babies DESC
       ) AS popularity
FROM baby_names;
```

Running total:
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

Actual execution: **[Not executed]**.

## Interpretation

- CASE does not persist changes in SELECT; UPDATE would be separate DML.
- GROUP BY collapses each group; window function preserves each row.
- PARTITION BY defines windows; ORDER BY controls order inside window.
- ROW_NUMBER/RANK/DENSE_RANK differ specifically on ties.
- Default frame behavior matters for FIRST_VALUE/NTH_VALUE and aggregate windows.
- ROWS counts physical rows; RANGE groups peer ORDER BY values in the source example.
- PIVOT/UNPIVOT syntax is product-specific; manual alternatives are ordinary SELECT patterns.

## Next action

1. Confirm target RDBMS/version.
2. Confirm tie behavior and required output cardinality.
3. For windows, define PARTITION, ORDER BY, and frame explicitly when semantics matter.
4. Test with duplicate ORDER BY values and NULLs.
5. For PIVOT/UNPIVOT, compare expected column names/types to actual output.
6. Validate totals against a simple GROUP BY baseline.
7. Only after read-only validation reuse logic in DML.

## Modifying action

Chapter 8 examples themselves are read-only SELECTs.

Source notes CASE can be used with UPDATE to persist values, but no UPDATE command/procedure is provided in this chapter. Therefore state-changing action here is **[Not applicable]**; any DML reuse requires separate change control.

## Verification / acceptance checks

- CASE branches tested including ELSE/NULL.
- GROUP totals reconcile to source rows.
- Tie behavior of ranking matches requirement.
- Window frame explicit where needed.
- FIRST/NTH/LAG outputs validated at window boundaries.
- PIVOT/UNPIVOT output columns/rank labels checked.
- Manual CASE/UNION alternatives produce equivalent logical shape.
- Performance not inferred from syntax alone.

## Rollback

Read-only SELECT examples: [Not applicable].  
Any future UPDATE based on CASE/window-derived logic: **[Needs confirmation]**.
