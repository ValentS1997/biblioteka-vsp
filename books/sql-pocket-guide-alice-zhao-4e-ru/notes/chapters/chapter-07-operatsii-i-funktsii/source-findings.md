# Source findings — глава 7. Операции и функции

**Scope:** PDF 190–243, RAG `p0190:c01`–`p0243:c01`.  
**Policy:** preserve source; no silent correction.

## F-01 · [Source code mismatch] · undefined alias in IN example

`p0197:c01`:
```sql
SELECT *
FROM employees
WHERE e.id IN (10001, 10032, 10057);
```
The query refers to `e.id`, but `FROM employees` does not declare alias `e`.

**Status:** runnable form [Needs confirmation]. Do not silently add `e` or remove it.

## F-02 · [Needs confirmation] · LIKE case-sensitivity generalized by product

`p0198:c01`–`p0199:c01` states MySQL/SQL Server/SQLite are case-insensitive for the shown LIKE pattern, while Oracle/PostgreSQL are case-sensitive.

Actual behavior can depend on collation/settings/version; chapter does not encode these prerequisites. Treat as source assertion, not universal guarantee.

## F-03 · [Source code mismatch] · generic RANDOM() row sampling

`p0206:c01` first lists:
- MySQL/SQL Server: `RAND()`
- PostgreSQL/SQLite: `RANDOM()`
- Oracle: DBMS_RANDOM

Immediately after, a generic example uses:
```sql
ORDER BY RANDOM()
LIMIT 5;
```

**Finding:** generic snippet is not explicitly scoped and conflicts with the preceding product-specific function table for MySQL/SQL Server. Runnable target [Needs confirmation].

## F-04 · [Source extraction issue] · CONCAT line

`p0213:c01` text-layer contains:
`Server SELECT CONCAT(id, '_', name)...`
after a comment “MySQL, PostgreSQL и SQL Server”.

The extra word `Server` before SELECT is an extraction/layout artifact candidate. Do not treat it as executable SQL.

## F-05 · [Source wording/code mismatch] · PostgreSQL “days between dates”

Table 7.16 (`p0230:c01`) is titled as **number of days**, but PostgreSQL code uses:
```sql
SELECT AGE(end_date, start_date) AS day_diff
```
and displayed output on `p0231:c01` is an interval such as `4 years 1 mon 1 day`, not a numeric day count.

**Finding:** heading/alias and output semantics do not match.

## F-06 · [Source code mismatch] · missing operator in PostgreSQL time difference

`p0231:c01` is extracted as:
```sql
SELECT EXTRACT(epoch from end_time
start_time) AS time_diff
```

No operator appears between `end_time` and `start_time`. Exact intended code [Needs confirmation].

## F-07 · [Source code mismatch] · missing operator in SQLite time difference

`p0232:c01` is extracted as:
```sql
SELECT (strftime('%s',end_time)
strftime('%s',start_time)) AS time_diff
```

Again, the connecting operator is missing in text-layer extraction. Do not reconstruct it from model knowledge.

## F-08 · [Source wording/code mismatch] · “hours between datetimes”

Table 7.18 (`p0233:c01`) describes number of hours. MySQL/SQL Server/SQLite show numeric-looking hour calculations, but:
- Oracle uses `end_dt - start_dt` and displayed interval;
- PostgreSQL uses `AGE(...)` and displayed years/months/days/time.

**Finding:** heading/alias “hour_diff” does not match displayed output for Oracle/PostgreSQL.

## F-09 · [Source extraction/typo candidate] · POSIX digit token

`p0225:c01` says `\d` is equivalent to `[0-9]` and `[[:digit::]]`.

The double colon before closing bracket is suspicious, but canonical RAG does not establish the intended token. Preserve as source defect.

## F-10 · [Source wording/code mismatch] · SQL Server CONVERT target type

`p0240:c01` says SQL Server uses CONVERT to transform a string into DATETIME, but shown code is:
```sql
SELECT CONVERT(VARCHAR, '10-15-22', 105);
```
The target type in the displayed code is `VARCHAR`.

**Finding:** prose and code disagree; no correction applied.

## F-11 · [Source contradiction] · SQLite date functions

`p0242:c01` says “В SQLite нет функций для работы с датами” and suggests SUBSTR.

But the same chapter/source earlier gives SQLite:
- `CURRENT_DATE` / `CURRENT_TIME` / `CURRENT_TIMESTAMP` (`p0227:c01`);
- `DATE(...)` / `DATETIME(...)` (`p0229:c01`);
- `julianday()` / `strftime()` (`p0230:c01`–`p0236:c01`);
- `DATE(...)`, `TIME(...)`, `DATETIME(...)` conversion examples (`p0238:c01`–`p0239:c01`).

This is a direct internal contradiction. Artifacts do not resolve it externally.

## F-12 · [Needs confirmation] · version/collation dependent assertions

Claims about:
- SQLite math support,
- trailing-space LENGTH,
- regex support/case,
- integer division,
- day-of-week numbering,
- date/time formats,
are source/version-specific and not current-version verification.

## Control

Canonical source/RAG unchanged. Any external adjudication requires a separate verification task.
