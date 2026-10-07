# Commands and source-confirmed examples — глава 3

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е издание.  
**Прямой источник:** RAG chunks `p0055:c01`–`p0069:c01` (PDF 55–69).  
**Исполнение:** ни один пример не запускался. БД, версии, схемы и права — [Needs confirmation].

## Классификация

- **Read-only SQL:** в учебных примерах `SELECT` предназначен для чтения/вычисления; на БД может создавать нагрузку — фактический план/ресурсы [Needs confirmation].
- **Non-SQL illustrative code:** Python-цикл используется для пояснения императивного подхода; БД не изменяет.
- **State-changing:** `CREATE`, `ALTER`, `DROP`, `INSERT`, `UPDATE`, `DELETE`, `GRANT`, `REVOKE`, `COMMIT`, `ROLLBACK` приведены только как **имена операторов в классификации** (PDF 68); здесь **нет** готовых инструкций на запись.
- **Workload-generating:** отдельных команд тестирования нагрузки в главе нет — [Not applicable].
- Для изменяющих операций: эффект указан по категории; риск изменения объектов/данных/прав/транзакции. Конкретные параметры, проверка и rollback — **[Needs confirmation]**, примеры не исполнять.

## 1. Python versus SQL: что и как

**PDF 56, `p0056:c01` — Python, иллюстрация (локальное вычисление):**

```python
calories = [90, 240, 165]
total = 0
for c in calories:
    total += c
print(total)
```

Класс: **read-only по отношению к БД**, локальный вычислительный пример; наличие установленного Python/вывод не проверялись.

**PDF 56, `p0056:c01` — SQL, запрос чтения/агрегации:**

```sql
SELECT SUM(calories)
FROM workouts;
```

Класс: **read-only** (SQL `SELECT`). Таблица `workouts` и поле `calories`: [Needs confirmation]. Автор сопоставляет императивный цикл и декларативное вычисление суммы.

## 2. Два варианта SQL по книге: DECODE / CASE

**PDF 58, `p0058:c01`: Oracle-специфичный пример (read-only):**

```sql
-- код, характерный для Oracle
SELECT item, DECODE (flag, 0, 'No', 1, 'Yes')
             AS Yes_or_No
FROM items;
```

**PDF 58, `p0058:c01`: вариант CASE, названный автором стандартным (read-only):**

```sql
-- Код, работающий в любой РСУБД
SELECT item, CASE WHEN flag = 0 THEN 'No'
             ELSE 'Yes' END AS Yes_or_No
FROM items;
```

**Важно:** в тексте эти конструкции названы обладающими одинаковой логикой. Однако для `flag` вне `0/1` полная эквивалентность **не доказана предоставленной главой**; отдельное замечание — `source-findings.md`. Не нормализовать SQL и не делать вид, что код прошёл тесты.

## 3. Два стиля соединения по книге

**PDF 59, `p0059:c01`: ANSI-89 (read-only):**

```sql
-- ANSI-89
SELECT c.id, c.name, o.date
FROM customer c, order o
WHERE c.id = o.id;
```

**PDF 59, `p0059:c01`: ANSI-92 (read-only):**

```sql
-- ANSI-92
SELECT c.id, c.name, o.date
FROM customer c INNER JOIN order o
ON c.id = o.id;
```

Схемы `customer`, `order`, полей `id/name/date` нет в RAG; выполнение: [Needs confirmation]. Идентификатор `order` совпадает с частью ключевого слова `ORDER BY` и требует проверки правил конкретной РСУБД: [Needs confirmation]. Авторский текст не исправлен.

## 4. Учебный оператор с функциями, псевдонимами и предложениями

**PDF 59–65, `p0059:c01`–`p0065:c01` (read-only SELECT):**

```sql
-- Продажи, выполненные в 2021 году
SELECT e.name, COUNT(s.sale_id) AS num_sales
FROM employee e
  LEFT JOIN sales s ON e.emp_id = s.emp_id
WHERE YEAR(s.sale_date) = 2021
  AND s.closed IS NOT NULL
GROUP BY e.name;
```

- Функции: `COUNT()`, `YEAR()` (`p0060:c01`, `p0061:c01`).
- Алиасы: `e`, `s`, `num_sales` (`p0062:c01`).
- Предложения: `SELECT`, `FROM`, `WHERE`, `GROUP BY` (`p0063:c01`, `p0064:c01`).
- Выражение: `COUNT(s.sale_id)`; предикаты из `WHERE` (`p0065:c01`).
- Поддержка функции `YEAR()` и результат на целевой РСУБД: [Needs confirmation]. Данные не изменяются намеренно, но нагрузка выполнения неизвестна.

## 5. Выражения и предикаты — не самостоятельные команды

**PDF 65–66, `p0065:c01`–`p0066:c01`:**

```sql
COUNT(s.sale_id)
s.sale_id + 10
CURRENT_DATE
```

Это **фрагменты/выражения**, не готовые запросы: как отдельные команды **[Not applicable]**. Предикат может дать `TRUE`, `FALSE` или `UNKNOWN`; для отсутствия значения автор показывает `IS NULL` вместо `= NULL`.

## 6. Комментарии, кавычки, форматирование

**PDF 66–67, `p0066:c01`–`p0067:c01`:**

```sql
-- Это мои комментарии
/* Это
мои комментарии */
```

Некомандные синтаксические примеры, исполнение БД: [Not applicable].

```sql
SELECT "This column"
FROM my_table
WHERE name = 'Bob';
```

Класс: **read-only**. `'Bob'` — строковый литерал, `"This column"` — quoted identifier в описании книги; для MySQL автор отдельно указывает иной стиль quoting (`p0067:c01`). Реальная совместимость с целевой РСУБД: [Needs confirmation].

```sql
SELECT * FROM my_table;
SELECT *
  FROM my_table;
```

Оба образца — **read-only**. По автору, разное форматирование пробелов и переводов строк не меняет смысл (`p0067:c01`). Здесь две **альтернативные** формы, не единая операция.

## 7. Подъязыки — имена ключевых слов, не исполняемые инструкции

**PDF 68, `p0068:c01`:**

| Подъязык | Операторы в таблице автора | Влияние |
|---|---|---|
| DQL | `SELECT` | Read-only получение данных |
| DDL | `CREATE`, `ALTER`, `DROP` | State-changing: объекты/схема |
| DML | `INSERT`, `UPDATE`, `DELETE` | State-changing: строки/данные |
| DCL | `GRANT`, `REVOKE` | State-changing: привилегии |
| TCL | `COMMIT`, `ROLLBACK` | State-changing: транзакция |

**Мера безопасности:** эти отдельные ключевые слова не образуют готовую команду изменения/восстановления БД, не исполнять «для проверки».

## Verification / rollback

**Только статическая сверка с RAG:** примеры и классификация подтверждены указанными PDF/chunk provenance; реальные результаты отсутствуют. Для SELECT-образцов rollback [Not applicable]; для любых модифицирующих операций необходим отдельный контекст, критерий успеха и безопасный rollback — **[Needs confirmation]**. 
