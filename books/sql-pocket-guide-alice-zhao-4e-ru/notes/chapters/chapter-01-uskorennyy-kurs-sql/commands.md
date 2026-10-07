# SQL-фрагменты из главы 1

**Источник:** Элис Жао, «SQL. Карманный справочник», 4-е изд., PDF 21–32; `rag/chunks/p0001-p0100/p0021-c01.md`–`p0032-c01.md`.

**Проверка:** запросы не исполнялись. Схема БД, права пользователя и версия РСУБД: [Needs confirmation]. Следующие примеры предназначены для чтения.

## Базовые SELECT

**PDF 21, `p0021:c01`** — пример из книги:

```sql
SELECT * FROM birthdays
WHERE person = 'husband';
```

**PDF 27–28, `p0027:c01`, `p0028:c01`** — получить таблицу:

```sql
SELECT * FROM my_table;
```

**PDF 28, `p0028:c01`** — отобрать строки и упорядочить результат:

```sql
SELECT *
FROM my_table
WHERE column1 > 100
ORDER BY column2;
```

Все три примера: **read-only**; реальные объекты `birthdays`, `my_table` не проверены. После разрешённого выполнения нужно сверить полученный набор строк; результат: [Needs confirmation]. Rollback: [Not applicable].

## Диалекты: получить до 10 строк (PDF 24, `p0024:c01`)

**MySQL / PostgreSQL / SQLite** — read-only:

```sql
SELECT * FROM birthdays LIMIT 10;
```

**Microsoft SQL Server** — read-only:

```sql
SELECT TOP 10 * FROM birthdays;
```

**Oracle Database** — read-only:

```sql
SELECT * FROM birthdays WHERE ROWNUM <= 10;
```

Синтаксис записан точно по книге. Проверка на конкретной версии РСУБД: [Needs confirmation]; поправки из внешней документации не вносились.

## Неисполняемые схемы

- Порядок **написания**: `SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY` (PDF 28, `p0028:c01`).
- Логический порядок **обработки** из книги: `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` (PDF 29–30, `p0029:c01`, `p0030:c01`).
- `--` начинает комментарий SQL (PDF 29, `p0029:c01`).

## Классификация отсутствующих типов

- **Workload-generating:** [Not applicable] — нагрузочных SQL-команд в этой главе нет.
- **State-changing:** [Not applicable] — CRUD обсуждается как термин, но готовые примеры модификации данных глава 1 не даёт (PDF 26–27).
- Эффект, риск, верификация и rollback гипотетических модификаций: [Needs confirmation]. Не конструировать команды, которых нет в RAG.
