# Source-confirmed SQL examples — глава 4

**Source:** Элис Жао, «SQL. Карманный справочник», 4-е изд.; PDF 70–104, RAG `p0070:c01`–`p0104:c01`. Исполнение **не проводилось**; версии РСУБД, объекты, данные, права и стоимость запросов: [Needs confirmation].

## Классификация и область применения

**Все законченные SQL-операторы главы 4 в этом документе — `SELECT`, read-only в отношении изменения хранимых данных.** При этом сканирование таблиц, JOIN, агрегация и коррелированные подзапросы могут быть **workload-generating**. Запуск на production без границ нагрузки и доступа не предусмотрен.

**State-changing:** [Not applicable] — примеров самостоятельных `CREATE/INSERT/UPDATE/DELETE` для исполнения в главе нет. **Rollback:** [Not applicable] для неисполненных read-only примеров; для реакции на нагрузку/отзыва доступа — [Needs confirmation].

## 1. SELECT: список полей, все поля и выражения

**PDF 72, `p0072:c01` — read-only:**
```sql
SELECT id, name
FROM owner;
```

**PDF 72, `p0072:c01` — read-only, потенциально большой результат:**
```sql
SELECT *
FROM owner;
```

**PDF 73, `p0073:c01` — read-only, выражение:**
```sql
SELECT name, ROUND(population * 0.9, 0)
FROM county;
```

**PDF 73, `p0073:c01` — read-only, функция без FROM (в книге указаны MySQL, PostgreSQL, SQLite):**
```sql
SELECT CURRENT_DATE;
```

Дата `2021-12-01` на странице книги — пример результата, не свидетельство о сегодняшней дате.

**PDF 75, `p0075:c01` — read-only, алиасы столбцов:**
```sql
SELECT id AS county_id, name,
       ROUND(population * 0.90, 0) AS estimated_pop
FROM county;
```

**PDF 76–77, `p0076:c01`–`p0077:c01` — read-only, квалификация и алиас таблицы:**
```sql
SELECT o.id, o.name
FROM sqlbook.owner o;
```

## 2. Подзапрос в SELECT и correlated subquery

**PDF 78, `p0078:c01` — read-only, скалярный некоррелированный подзапрос:**
```sql
SELECT id, name, population,
       (SELECT AVG(population) FROM county)
       AS average_pop
FROM county;
```

Автор требует от подзапроса в `SELECT` один столбец и не более одной строки; если строк нет, в результате `NULL` (`p0078:c01`, `p0079:c01`).

**PDF 79, `p0079:c01` — read-only, workload-generating:**
```sql
SELECT o.id, o.name,
       (SELECT COUNT(*) FROM waterfall w
        WHERE o.id = w.owner_id) AS num_waterfalls
FROM owner o;
```

**PDF 80, `p0080:c01` — альтернативный JOIN, read-only/workload-generating:**
```sql
SELECT   o.id, o.name,
         COUNT(w.id) AS num_waterfalls
FROM     owner o LEFT JOIN waterfalls w
         ON o.id = w.owner_id
GROUP BY o.id, o.name
```

**Важное несовпадение источника:** `waterfall` в первом и `waterfalls` во втором. Не исправлять молча; см. `source-findings.md`. Равенство результата и ускорение **[Needs confirmation]**.

## 3. DISTINCT и COUNT

**PDF 81, `p0081:c01` — read-only, уникальные комбинации:**
```sql
SELECT DISTINCT o.type, w.open_to_public
FROM owner o
JOIN waterfall w ON o.id = w.owner_id;
```

**PDF 81, `p0081:c01` — read-only, число уникальных типов:**
```sql
SELECT COUNT(DISTINCT type) AS unique
FROM owner;
```

**PDF 81, `p0081:c01` — read-only, несколько полей через подзапрос:**
```sql
SELECT COUNT(*) AS num_unique
FROM (SELECT DISTINCT o.type, w.open_to_public
      FROM owner o JOIN waterfall w
      ON o.id = w.owner_id) my_subquery;
```

**PDF 82, `p0082:c01`:** автор дополнительно даёт два диалектных способа для нескольких полей: MySQL `COUNT(DISTINCT o.type, w.open_to_public)` и PostgreSQL `COUNT(DISTINCT (o.type, w.open_to_public))`. Совместимость с реальными версиями не проверялась.

## 4. FROM: JOIN, производная таблица и CTE

**PDF 85, `p0085:c01` — read-only, JOIN:**
```sql
SELECT w.name AS waterfall_name,
       t.name AS tour_name
FROM waterfall w JOIN tour t
     ON w.id = t.stop;
```

`JOIN` в книге трактуется как `INNER JOIN`. Если совпадений нет, сущность не попадает в показанный результат (`p0085:c01`).

**PDF 86, `p0086:c01` — read-only, подзапрос как источник:**
```sql
SELECT w.name AS waterfall_name,
       o.name AS owner_name
FROM (SELECT * FROM owner WHERE type = 'public') o
     JOIN waterfall w
     ON o.id = w.owner_id;
```

**PDF 87, `p0087:c01` — read-only, CTE:**
```sql
WITH o AS (SELECT * FROM owner
           WHERE type = 'public')
SELECT w.name AS waterfall_name,
       o.name AS owner_name
FROM o JOIN waterfall w
     ON o.id = w.owner_id;
```

**PDF 88, `p0088:c01` — read-only, два шага через вложенный запрос:**
```sql
SELECT AVG(num_stops) FROM
(SELECT name, MAX(stop) as num_stops
 FROM tour
 GROUP BY name) tour_stops;
```

Автор описывает `MAX(stop)` как «число остановок». Корректность этого вывода зависит от смысла поля `stop`; `p0083:c01` использует его как ссылку на `waterfall.id`. **[Source code mismatch]**, см. findings.

## 5. WHERE: фильтры и IN-подзапрос

**PDF 90, `p0090:c01` — read-only, поиск названий без «Falls»:**
```sql
SELECT id, name
FROM waterfall
WHERE name NOT LIKE '%Falls%';
```

**PDF 91, `p0091:c01` — read-only, составной предикат:**
```sql
SELECT id, name
FROM waterfall
WHERE name NOT LIKE '%Falls%'
      AND owner_id IS NULL;
```

**PDF 92, `p0092:c01` — read-only, фильтр подзапросом:**
```sql
SELECT w.name
FROM   waterfall w
WHERE  w.open_to_public = 'y'
       AND w.county_id IN (
           SELECT c.id FROM county c
           WHERE c.name = 'Alger');
```

Результат подзапроса `IN` не требует алиаса в контексте WHERE по книге (`p0092:c01`); автор показывает альтернативу с `INNER JOIN county` (`p0093:c01`). Утверждение о выигрыше производительности — не измеренный benchmark.

## 6. GROUP BY и HAVING

**PDF 94, `p0094:c01`, и PDF 99, `p0099:c01` — read-only, потенциально ресурсоёмкое агрегирование:**
```sql
SELECT   t.name AS tour_name,
         COUNT(*) AS num_waterfalls
FROM     waterfall w INNER JOIN tour t
         ON w.id = t.stop
GROUP BY t.name
HAVING COUNT(*) = 6;
```

**По книге:** `GROUP BY` формирует группы, `COUNT(*)` считает **строки**; если сущность повторяется в нескольких строках, это не количество уникальных сущностей (`p0095:c01`–`p0098:c01`).

**PDF 100, `p0100:c01`:** `HAVING num_waterfalls = 6` приведён как неверный для общего случая; отдельно оговорено исключение MySQL/SQLite, поддерживающих алиас. В source-примере строка с `#` — авторская пометка «код не будет выполняться», **не** безопасный runnable SQL.

## 7. ORDER BY и LIMIT

**PDF 101, `p0101:c01` — read-only, сортировка:**
```sql
SELECT   COALESCE(o.name, 'Unknown') AS owner,
         w.name AS waterfall_name
FROM     waterfall w
         LEFT JOIN owner o ON w.owner_id = o.id
ORDER BY owner, waterfall_name;
```

**PDF 102, `p0102:c01` — read-only, сортировка по полям, которых нет в SELECT:**
```sql
SELECT   COALESCE(o.name, 'Unknown') AS owner,
         w.name AS waterfall_name
FROM     waterfall w
         LEFT JOIN owner o ON w.owner_id = o.id
ORDER BY o.id DESC, w.id;
```

О вариантах `DESC`/`ASC` и `ORDER BY 1 DESC, 2 ASC` говорится на `p0102:c01`–`p0103:c01`; ссылки на позицию столбца зависят от состава SELECT. Если `ORDER BY` нет, стабильная последовательность строк не гарантируется (`p0103:c01`).

**PDF 103, `p0103:c01` — MySQL/PostgreSQL/SQLite, read-only:**
```sql
SELECT *
FROM owner
LIMIT 3;
```

**PDF 103, `p0103:c01` — Oracle, read-only:**
```sql
SELECT *
FROM owner
WHERE ROWNUM <= 3;
```

**PDF 104, `p0104:c01` — SQL Server, read-only:**
```sql
SELECT TOP 3 *
FROM owner;
```

Для определённого набора «первых N» порядок требуется задавать явно, если это поддерживается целевым контекстом; глава предупреждает о непредсказуемости сортировки без `ORDER BY`. Любые фактические результаты **[Needs confirmation]**.

## Verification / acceptance / rollback

1. До выполнения: подтвердить target DB, привилегии, объём данных и допустимый workload — [Needs confirmation].
2. После read-only выполнения: сверить результат с ожидаемой схемой, проверить отсутствие нежелательных дублей и групп; фактические результаты [Needs confirmation].
3. Нагрузочные характеристики JOIN/подзапросов — только после отдельных измерений; в главе benchmark не дан.
4. Rollback изменения данных [Not applicable] (команд записи не выполнялось). Механизм отмены перегружающего запроса в конкретной среде — [Needs confirmation].
