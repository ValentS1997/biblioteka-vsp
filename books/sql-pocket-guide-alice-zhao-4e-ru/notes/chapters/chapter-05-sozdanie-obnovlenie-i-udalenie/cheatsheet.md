# Cheatsheet — глава 5. Создание, обновление и удаление

**Source:** PDF 105–154, RAG `p0105:c01`–`p0154:c01`. Никаких изменений БД не выполнялось.

## Symptom / problem framing

Нужно создать/изменить/удалить объект или данные SQL и не повредить рабочую БД. Глава показывает DDL/DML/TCL и одновременно предупреждает о необратимых операциях, правах, backup и транзакциях. Основной operational risk — выполнить правильную команду против неправильной БД/таблицы либо слишком широкого набора строк.

## Baseline / context

| Область | Read-only baseline | State-changing действия |
|---|---|---|
| Database | SHOW/SELECT current DB, `\l`, `.database` | CREATE/DROP DB, USE/\c/.open |
| Table | SHOW tables, DESCRIBE/\d/PRAGMA | CREATE, ALTER, DROP |
| Rows | SELECT | INSERT, UPDATE, DELETE |
| Constraints | metadata queries | ADD/MODIFY/DROP constraint |
| Index | запрос к таблице | CREATE/DROP INDEX |
| View | list/query views | CREATE/REPLACE/ALTER/DROP VIEW |
| Transaction | SELECT verification | BEGIN/START, DML, COMMIT/ROLLBACK |

**Target database / RDBMS / version / owner / backup / change window:** [Needs confirmation].

## Read-only checks

Перед изменением источник поддерживает следующие проверки.

**Текущая БД** (`p0108:c01`):
- MySQL: `SELECT database();`
- Oracle: `SELECT * FROM global_name;`
- PostgreSQL: `SELECT current_database();`
- SQL Server: `SELECT db_name();`
- SQLite: `.database`

**Существующие таблицы** (`p0114:c01`):
- MySQL: `SHOW tables;`
- Oracle: `SELECT table_name FROM user_tables;`
- PostgreSQL: `\dt`
- SQL Server: `SELECT table_name FROM information_schema.tables;`
- SQLite: `.tables`

**Столбцы** (`p0130:c01`): `DESCRIBE my_table;`, `\d my_table`, information_schema, `pragma table_info(my_table);`.

**Preview-before-update** (`p0137:c01`–`p0139:c01`):
```sql
SELECT LOWER(name)
FROM my_table;
```
```sql
SELECT awards + 1
FROM my_table
WHERE country = 'CA';
```
```sql
SELECT MIN(awards)
FROM my_table;
```

**Preview-before-delete** (`p0151:c01`–`p0152:c01`):
```sql
SELECT * FROM books WHERE title LIKE '% %';
```

Фактические результаты, объём строк и права: [Needs confirmation].

## Interpretation

### Объекты и ограничения

`CREATE TABLE` задаёт структуру; `INSERT` загружает строки. `NOT NULL`, `DEFAULT`, `CHECK`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY` ограничивают допустимое состояние (`p0112:c01`–`p0122:c01`).

Primary key однозначно идентифицирует строку; foreign key ссылается на key другой таблицы по описанию автора. Composite keys требуют совпадающего набора ссылочных колонок (`p0119:c01`–`p0122:c01`).

### DML blast radius

`UPDATE ... SET ... WHERE ...` изменяет выбранные строки; отсутствие WHERE расширяет действие на всю таблицу (`p0137:c01`–`p0139:c01`).

`DELETE FROM my_table WHERE id = 9;` удаляет выбранную строку; `DELETE FROM my_table;` удаляет все строки, но оставляет определение таблицы (`p0133:c01`).

### Index и view

Индекс создаётся для ускорения доступа в примере `log_date`, но требует места и обновления при изменении строк (`p0141:c01`–`p0144:c01`). Фактический выигрыш — [Needs confirmation].

View сохраняет определение запроса и используется как табличный источник; сам автор описывает его как объект, не хранящий данные (`p0145:c01`–`p0149:c01`).

### Transaction

Рабочий pattern главы:
`BEGIN/START → SELECT baseline → state-changing DML → SELECT verification → COMMIT | ROLLBACK`.

Это не универсальная гарантия для любого DDL/движка. Глава демонстрирует этот pattern на DML `DELETE`; точные transactional semantics целевой РСУБД — [Needs confirmation].

## Next action

Для реального изменения:
1. Подтвердить target DB/host/schema и версию.
2. Подтвердить owner/approval и privilege.
3. Иметь backup/restore point, если источник называет действие необратимым.
4. Сначала выполнить source-confirmed read-only baseline/preview.
5. Если действие допускает транзакцию в целевой системе, начать transaction только после проверки semantics.
6. Выполнить **одно** узкое изменение.
7. Read-back/SELECT verification.
8. При несовпадении — source-supported `ROLLBACK` только если изменение действительно находится в поддерживаемой незакоммиченной транзакции; иначе rollback [Needs confirmation].
9. `COMMIT` — только после acceptance check.

## Modifying action

Примеры из книги **не являются инструкцией для production**.

| Действие | Эффект | Риск | Verification | Rollback |
|---|---|---|---|---|
| `CREATE DATABASE/TABLE/INDEX/VIEW` | создаёт объект | конфликт имени, ресурсы, права | list/describe/query object | [Needs confirmation] |
| `INSERT` | добавляет строки | неверные данные/дубли | SELECT по ключу/условию | transaction rollback только если применимо |
| `ALTER TABLE` | меняет schema | несовместимость, loss | DESCRIBE/metadata + data check | backup/recreate; [Needs confirmation] |
| `UPDATE ... WHERE` | меняет строки | неверный predicate | тот же WHERE через SELECT | ROLLBACK до COMMIT, если поддержано |
| `DELETE ... WHERE` | удаляет строки | data loss | предварительный SELECT и post-check | ROLLBACK до COMMIT, если поддержано |
| `DELETE FROM table;` | удаляет все строки | полный data loss | row/sample check | backup/transaction; [Needs confirmation] |
| `DROP ...` | удаляет объект | необратимость по книге | проверить object/backup заранее | restore/recreate; [Needs confirmation] |
| `COMMIT` | фиксирует transaction | отмена ROLLBACK path | итоговый SELECT до COMMIT | после COMMIT источник говорит rollback невозможен |

## Verification / acceptance checks

- Target DB/schema точно идентифицированы.
- Список затрагиваемых объектов совпадает с change scope.
- Preview SELECT возвращает только ожидаемые строки.
- Для UPDATE/DELETE присутствует ожидаемый WHERE, если scope не «все строки».
- Constraints/column definitions после ALTER совпадают с ожидаемыми.
- Row count/data samples после DML соответствуют acceptance criteria.
- До COMMIT результат проверен внутри transaction.
- Backup/restore или rollback point подтверждён для необратимых операций.

В этой работе все execution checks — **[Not executed]**.

## Rollback

**Source-supported transaction rollback:** `ROLLBACK;` на `p0153:c01`–`p0154:c01`, до `COMMIT`.

**После COMMIT:** книга прямо говорит, что транзакцию уже нельзя отменить (`p0152:c01`).

**DROP DATABASE/TABLE/VIEW, ALTER и другие structural changes:** источник часто предупреждает об необратимости либо backup; универсального rollback script глава не даёт. Статус: **[Needs confirmation]**.

**Правило:** не подменять rollback обратной destructive-командой из предположений.
