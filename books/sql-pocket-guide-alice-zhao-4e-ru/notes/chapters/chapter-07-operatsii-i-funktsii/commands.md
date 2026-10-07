# Source-confirmed SQL examples — глава 7

**Source:** PDF 190–243, RAG `p0190:c01`–`p0243:c01`.  
**Execution:** не выполнялось. Target RDBMS/version/data/privileges — [Needs confirmation].

## 1. Logical / comparison

```sql
SELECT *
FROM employees
WHERE start_date IS NOT NULL
      AND (title = 'analyst' OR pay_rate < 25);
```
Read-only. Source: `p0192:c01`.

```sql
SELECT *
FROM my_table
WHERE age BETWEEN 35 AND 44;
```
Read-only. Source: `p0195:c01`.

```sql
SELECT e.id, e.name
FROM employees e
WHERE EXISTS (
  SELECT *
  FROM customers c
  WHERE c.email = e.email
);
```
Read-only. Source: `p0196:c01`.

```sql
SELECT e.id
FROM employees e
WHERE NOT EXISTS (
  SELECT *
  FROM vacations v
  WHERE v.emp_id = e.id
);
```
Read-only. Source recommends this over NOT IN when subquery may contain NULL (`p0197:c01`).

## 2. LIKE

```sql
SELECT *
FROM my_table
WHERE txt LIKE '%you%';
```
Read-only. Case behavior is product/collation sensitive; source shows differing outputs (`p0198:c01`–`p0199:c01`).

```sql
SELECT *
FROM my_table
WHERE txt LIKE '%!%%' ESCAPE '!';
```
Read-only. Source: `p0199:c01`.

## 3. Arithmetic / aggregate

```sql
SELECT salary / 52 AS weekly_pay
FROM my_table;
```
Read-only. Integer-division semantics differ by product (`p0200:c01`–`p0201:c01`).

```sql
SELECT COUNT(*) AS total_rows,
       AVG(age) AS average_age
FROM my_table;
```
Read-only. Source: `p0202:c01`.

```sql
SELECT region, MIN(age), MAX(age)
FROM my_table
GROUP BY region
HAVING MIN(age) < 18;
```
Read-only/workload-generating. Source: `p0202:c01`.

## 4. Numeric

```sql
SELECT ROUND(98.7654,2);
```
Read-only. Source: `p0207:c01`.

```sql
SELECT *
FROM my_table
WHERE CAST(str_col AS DECIMAL) > 3;
```
Read-only. Source: `p0208:c01`–`p0209:c01`.

Random-source examples include `RAND()`, `RANDOM()`, Oracle DBMS_RANDOM and TABLESAMPLE/SAMPLE variants (`p0206:c01`). Do not use a generic random-row snippet across products without confirming dialect.

## 5. String

```sql
SELECT LENGTH(name)
FROM my_table;
```
Read-only. SQL Server source uses LEN instead (`p0209:c01`).

```sql
SELECT TRIM(color) AS color_clean
FROM my_table;
```
Read-only. Source: `p0211:c01`.

```sql
SELECT REPLACE(my_text, 'some', 'the') AS new_text
FROM my_table;
```
Read-only. Source: `p0217:c01`.

```sql
SELECT SUBSTR(my_text, 14, 8) AS sub_str
FROM my_table;
```
Read-only, dialect-sensitive. Source: `p0215:c01`–`p0216:c01`.

## 6. Regex

MySQL source:
```sql
SELECT *
FROM movies
WHERE title REGEXP '\\d';
```

Oracle source:
```sql
SELECT *
FROM movies
WHERE REGEXP_LIKE(title, '\d');
```

PostgreSQL source:
```sql
SELECT *
FROM movies
WHERE title ~ '\d';
```

SQL Server source:
```sql
SELECT *
FROM movies
WHERE title LIKE '%[0-9]%';
```

All read-only; regex dialect/version must be confirmed. Source: `p0220:c01`–`p0225:c01`.

## 7. Date/time

```sql
SELECT CURRENT_DATE;
SELECT CURRENT_TIME;
SELECT CURRENT_TIMESTAMP;
```
Source variants differ for Oracle/SQL Server (`p0227:c01`).

Date arithmetic examples are product-specific (`p0229:c01`).

Read-only month extraction:
```sql
SELECT EXTRACT(month FROM CURRENT_DATE);
```
MySQL/PostgreSQL source form; exact support [Needs confirmation].

## 8. NULL

```sql
SELECT COALESCE(greeting, 'hi') AS greeting
FROM my_table;
```
Read-only. Source also lists IFNULL/NVL/ISNULL variants (`p0243:c01`).

## 9. State-changing demo

```sql
CREATE TABLE my_table (
  id INT,
  creation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO my_table (id)
VALUES (1), (2), (3);
```

Source: `p0228:c01`.  
Class: **state-changing**.  
Effect: schema + rows.  
Risk: object collision/dialect/default-time semantics.  
Verification: SELECT.  
Rollback: **[Needs confirmation]**.

## Acceptance / rollback

- Read-only examples: rollback [Not applicable].
- Regex/date/math output: test representative and NULL/boundary cases.
- CREATE/INSERT: no authorization to execute; rollback [Needs confirmation].
