# Source-confirmed commands: глава 2

**Provenance:** Элис Жао, PDF 33–54, RAG `p0033:c01`–`p0054:c01`. **Execution:** не выполнялось. Все тестовые имена — книжные примеры, не подтверждённые объекты инфраструктуры.

## Классы воздействия

- **Read-only:** просмотр данных/каталога, проверка соединения без намеренного изменения данных.
- **State-changing:** `CREATE`/`INSERT`, создание/открытие файловой БД с возможным изменением, установка пакетов, переключение текущего подключения/завершение сессии (только локальный контекст). Эти действия разделены по риску.
- **Workload-generating:** отдельные нагрузочные тесты главой не приведены — [Not applicable].
- **Проверка:** вернуть ожидаемый вывод в разрешённой тестовой среде; результаты настоящего выполнения [Needs confirmation].
- **Rollback:** у изменяющих команд [Needs confirmation] — глава не описывает полноценный безопасный rollback. Не исполнять в production «на пробу».

`sqlite>`, `mysql>`, `SQL>`, `postgres=#`, `1>`, `2>` — **приглашения** примеров, а не части команд.

## SQLite (PDF 35–36; `p0035:c01`, `p0036:c01`)

```sh
sqlite3
sqlite3 my_new_db.db
```

- `sqlite3` запускает консоль в памяти согласно описанию книги; изменения не сохраняются после закрытия.
- `sqlite3 my_new_db.db` подключается к файловой базе (возможный **state-changing** эффект на файловой системе), не запускать на неизвестном пути без согласования.

```sql
CREATE TABLE test (id int, num int);
INSERT INTO test VALUES (1, 100), (2, 200);
SELECT * FROM test LIMIT 1;
```

- Первые две команды **state-changing (схема/данные)**, последняя **read-only**. Авторский тестовый результат `1|100`; выполнение не проверялось.
- Перед созданием требуются разрешённая тестовая БД, отсутствие конфликта имён и план отката: [Needs confirmation].

```text
.databases
.tables
.headers on
.headers off
.quit
```

- `.databases`/`.tables`: **read-only** каталог.
- `.headers on/off`: **state-changing (отображение текущей CLI-сессии)**, данные БД не изменяет.
- `.quit`: **state-changing (закрытие сессии)**.

## MySQL (PDF 37, `p0037:c01`)

```sh
brew install mysql
```

**State-changing (установка ПО)**, только если выбрана соответствующая система и менеджер пакетов. Версия/совместимость [Needs confirmation].

```sql
CREATE TABLE test (id int, num int);
INSERT INTO test VALUES (1, 100), (2, 200);
SELECT * FROM test LIMIT 1;
```

`CREATE`/`INSERT` — **state-changing**; `SELECT` — **read-only**.

```text
show databases;
connect another_db;
show tables;
quit
```

- `show databases;`, `show tables;`: **read-only**.
- `connect another_db;`: **state-changing (текущий контекст подключения)**, не утверждает создание БД.
- `quit`: завершение сессии.

## Oracle Database (PDF 37–38, `p0037:c01`, `p0038:c01`)

```sql
CREATE TABLE test (id int, num int);
INSERT INTO test VALUES (1, 100);
INSERT INTO test VALUES (2, 200);
SELECT * FROM test WHERE ROWNUM <=1;
```

Первые три оператора — **state-changing**, последний — **read-only**, синтаксис оставлен авторским.

```sql
SELECT * FROM global_name;
SELECT table_name FROM all_tables;
SELECT table_name FROM user_tables;
```

Все три — **read-only**; `quit` завершает CLI. Целевые права/доступность словаря данных [Needs confirmation].

## PostgreSQL (PDF 38–39, `p0038:c01`, `p0039:c01`)

```sh
brew install postgresql
```

**State-changing (установка ПО).**

```sql
CREATE TABLE test (id int, num int);
INSERT INTO test VALUES (1, 100),
  (2, 200);
SELECT * FROM test LIMIT 1;
```

`CREATE` и `INSERT` — **state-changing**; `SELECT` — **read-only**.

```text
\l
\c another_db
\d
\q
```

- `\l`, `\d`: **read-only** получение метаданных.
- `\c another_db`: **state-changing (смена активной БД в сессии)**.
- `\q`: выход из клиента. Не путать с SQL-кодом.
- Книга указывает на приглашение `postgres-#` при незавершённом SQL; точное состояние консоли [Needs confirmation], не нормализуется без источника.

## Microsoft SQL Server (PDF 39–40, `p0039:c01`, `p0040:c01`)

```sql
CREATE TABLE test (id int, num int);
INSERT INTO test VALUES (1, 100), (2, 200);
go
SELECT TOP 1 * FROM test;
go
```

- `CREATE`, `INSERT`: **state-changing**.
- `SELECT TOP 1`: **read-only**.
- `go` в исходном консольном примере отправляет предыдущий блок на выполнение; **эффект зависит от содержимого блока**, не запускать без проверки.
- `1>`/`2>` — не часть текста для ввода.

```sql
SELECT name FROM master.sys.databases;
go
USE another_db;
go
SELECT * FROM information_schema.tables;
go
```

- `SELECT`: **read-only**.
- `USE`: **state-changing (контекст БД)**.
- `quit` — выход из клиента.

## GUI и подключение (PDF 40–43)

```sql
CREATE DATABASE my_new_db;
```

**State-changing:** создаёт БД, требует разрешения и rollback [Needs confirmation] (`p0042:c01`).

Другие варианты по книге: открыть существующий `.db` файл или подключиться к удалённой/локальной БД через поля `Host / Port / Database / Username / Password`. Учебные дефолты: MySQL `3306`, Oracle `1521`, PostgreSQL `5432`, SQL Server `1433` (`p0043:c01`). Для SQLite нужен путь к файлу. Книжный пример удалённого IP в `p0043:c01` непригоден как реальный адрес (см. `source-findings.md`).

## Python: установка (PDF 45–46)

Следующие команды — **state-changing (изменение окружения пакетов)**, не выполнять без выбора драйвера и версии:

```sh
pip install mysql-connector-python
pip install cx_Oracle
pip install psycopg2
pip install pyodbc
```

Книга даёт альтернативы `conda install -c conda-forge` для тех же пакетов; **не требуется запускать одновременно pip и conda**. Для SQLite в Python 3 автор использует встроенный модуль `sqlite3`; отдельную установочную команду не приводит (`p0045:c01`). Произвольные новые библиотеки не добавляются.

## Python: подключение/запрос/закрытие (PDF 46–49)

Вариант **SQLite** — может создать/изменить файл БД при соединении; не считать полностью read-only:

```python
import sqlite3
conn = sqlite3.connect('my_new_db.db')
```

Вариант **MySQL** — пароль **заменён placeholder**, остальные поля отражают книжный пример (`p0046:c01`):

```python
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    database='my_new_db',
    user='<DB_USER>',
    password='<DB_PASSWORD>')
```

Создание соединения: **state-changing (сессия/возможная активность сервера)**, не равняется `INSERT`; сетевой доступ, привилегии и конфигурация [Needs confirmation]. В главе также приведены `cx_Oracle`, `psycopg2`, `pyodbc` (`p0046:c01`–`p0047:c01`); не смешивать их параметры подключения.

**Read-only SQL, выполняемый через драйвер**, пример `p0048:c01`:

```python
cursor = conn.cursor()
cursor.execute('SELECT * FROM test;')
result = cursor.fetchall()
print(result)
```

Для `cx_Oracle` автор отдельно требует убрать конечный `;` внутри SQL-строки (`p0048:c01`). Схема `test` [Needs confirmation].

```python
import pandas as pd
df = pd.read_sql('''SELECT * FROM test;''', conn)
print(df)
print(type(df))
```

**Read-only запрос**, `p0049:c01`; установка pandas отдельно в этой главе не показана.

```python
cursor.close()
conn.close()
```

**State-changing (закрытие локального ресурса/соединения)**, без изменения строк БД (`p0049:c01`).

**SQLAlchemy**, `p0049:c01`–`p0050:c01`: автор приводит `conn.table_names()` и установку `pip install sqlalchemy` или `conda install -c conda-forge sqlalchemy`. Совместимость конкретного Python API с текущей версией SQLAlchemy **[Needs confirmation]**. Пример URL подключения содержит пароль; буквальные реквизиты в артефакты не переносим.

## R: установка, DBI и запрос (PDF 51–54)

**State-changing (установка R-пакетов), только при согласованном окружении:**

```r
install.packages("RSQLite")
install.packages("RMySQL")
install.packages("RPostgres")
install.packages("odbc")
```

В книге для Oracle дополнительно приведён `ROracle_1.3-2.zip` (зависит от локального файла и версии; [Needs confirmation]). Для SQL Server приведён драйвер ODBC (платформа-зависимый пример, `p0051:c01`).

**SQLite-соединение по книге (`p0052:c01`)** — может создать файл, если указанный путь не существует:

```r
library(DBI)
con <- dbConnect(RSQLite::SQLite(), "my_new_db.db")
```

**Read-only** (`p0053:c01`–`p0054:c01`):

```r
dbListTables(con)
dbReadTable(con, "test")
df <- dbGetQuery(con, "SELECT * FROM test WHERE id = 2")
print(df); class(df)
```

Oracle-специфическая заметка о `TEST` и разрыве `dbRead Table` в тексте RAG вынесена в `source-findings.md`; в блоке выше только непротиворечивая запись `dbReadTable` из самой страницы 54. Наличие таблицы `test` [Needs confirmation].

```r
dbDisconnect(con)
```

**State-changing (закрывает сеанс, не изменяет данные)**, `p0054:c01`.

**Безопасность:** учебник (`p0053:c01`) предлагает `rstudioapi::askForPassword("Password?")` для интерактивного запроса пароля. Это способ ввода, а не достаточное описание полной защиты учётных данных. Не публиковать значения из исходных примеров.

## Финальная верификация

1. До любого запуска подтвердить тип БД, целевую среду, владельца, учётные данные и права: [Needs confirmation].
2. Первой разрешённой операцией выбрать read-only получение метаданных или `SELECT`.
3. Изменяющие команды выполнять только отдельно, на явной test-DB, с независимыми rollback/acceptance: [Needs confirmation].
4. После работы закрыть курсор/соединение (`p0049:c01`, `p0054:c01`).
5. Авторские фрагменты сохранены без скрытой модернизации версий; все подстановки секретов помечены.
