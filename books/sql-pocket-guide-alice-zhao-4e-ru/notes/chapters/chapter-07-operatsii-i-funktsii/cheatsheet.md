# Cheatsheet — глава 7. Операции и функции

**Source:** PDF 190–243, RAG `p0190:c01`–`p0243:c01`. SQL не выполнялся.

## Symptom / problem framing

Нужно вычислять, сравнивать, агрегировать, обрабатывать строки/даты/NULL и учитывать dialect differences. Основной риск — перенос функции/операции между РСУБД без проверки semantics.

## Baseline / context

| Область | Примеры |
|---|---|
| Logical | AND, OR, NOT |
| Comparison | =, <>, BETWEEN, EXISTS, IN, IS NULL, LIKE |
| Arithmetic | +, -, *, /, %, MOD |
| Aggregate | COUNT, SUM, AVG, MIN, MAX |
| Numeric | ABS, SQRT, LOG, ROUND, CAST, random |
| String | LENGTH/LEN, TRIM, CONCAT, INSTR, SUBSTR, REPLACE |
| Regex | REGEXP, REGEXP_*, SIMILAR TO, ~, LIKE |
| Date/time | CURRENT_*, DATEDIFF/AGE, EXTRACT/DATEPART/strftime |
| NULL | COALESCE, IFNULL, NVL, ISNULL |

Target RDBMS/version/collation/timezone/locale: **[Needs confirmation]**.

## Read-only checks

```sql
SELECT *
FROM employees
WHERE start_date IS NOT NULL
  AND (title = 'analyst' OR pay_rate < 25);
```

```sql
SELECT e.id
FROM employees e
WHERE NOT EXISTS (
  SELECT *
  FROM vacations v
  WHERE v.emp_id = e.id
);
```

```sql
SELECT COUNT(*) AS total_rows,
       AVG(age) AS average_age
FROM my_table;
```

```sql
SELECT *
FROM my_table
WHERE CAST(str_col AS DECIMAL) > 3;
```

```sql
SELECT COALESCE(greeting, 'hi') AS greeting
FROM my_table;
```

Все примеры source-confirmed; фактический execution = [Not executed].

## Interpretation

- NULL требует отдельной проверки через `IS NULL`; `NOT IN` особенно чувствителен к NULL в подзапросе.
- Aggregate functions сворачивают строки; scalar numeric/string/date functions работают с выражениями/значениями.
- Regex/date-time/case sensitivity и integer division — dialect-sensitive.
- CAST не меняет тип столбца навсегда.

## Next action

1. Подтвердить РСУБД/версию и session settings.
2. Проверить NULL/boundary cases.
3. Выбрать source-confirmed dialect variant.
4. Тестировать read-only на representative data.
5. Проверить collation/timezone/locale.
6. Только затем использовать выражение в DML.

## Modifying action

На `p0228:c01` source создаёт и наполняет таблицу:

```sql
CREATE TABLE my_table (
  id INT,
  creation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO my_table (id)
VALUES (1), (2), (3);
```

Class: **state-changing**. Risk: schema/data/session semantics. Verification: SELECT. Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

- AND/OR precedence explicit.
- NULL cases tested.
- Target dialect supports operator/function.
- LIKE/regex case behavior verified.
- Division/rounding tested.
- Date/time unit and timezone checked.
- Aggregate output checked against NULL/row-count expectations.
- CAST treated as expression conversion only.

## Rollback

- Read-only: [Not applicable].
- CREATE/INSERT/DML reuse: **[Needs confirmation]**.
- Не считать inverse DDL/DML автоматическим rollback.
