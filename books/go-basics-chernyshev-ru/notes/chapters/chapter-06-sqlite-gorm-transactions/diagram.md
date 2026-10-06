# Диаграмма — глава 6: SQL → ORM → transactions → repository

~~~mermaid
flowchart TD
    A["SQLite file"] --> B["Classic database/sql"]
    B --> B1["sql.Open"]
    B --> B2["Exec: DDL / INSERT / UPDATE / DELETE"]
    B --> B3["Query + Scan: SELECT"]
    B --> B4["SQLiteRepository wraps *sql.DB"]

    A --> C["GORM"]
    C --> C1["gorm.Open"]
    C --> C2["struct tags"]
    C --> C3["AutoMigrate"]
    C --> C4["Create / Delete / Find / Where / Save"]

    C --> D["Transactions"]
    D --> D1["callback Transaction"]
    D --> D2["nested Transaction"]
    D --> D3["Begin / Commit / Rollback"]
    D --> D4["panic → deferred Rollback"]

    C --> E["DryRun"]
    E --> E1["generate SQL"]
    E --> E2["do not execute"]

    C --> F["Tic-tac-toe v.5"]
    F --> F1["IRepository"]
    F1 --> F2["SQLiteRepository"]
    F2 --> F3["Player"]
    F2 --> F4["GameSnapshot"]
    F2 --> F5["PlayerFinishGame"]
    F --> F6["Game depends on IRepository"]
    F6 --> F7["save/load by nickname"]
    F6 --> F8["finished game history"]
~~~

## Classic vs ORM

~~~text
Classic:
Go code → SQL string + args → database/sql → SQLite

GORM:
Go models/methods → ORM → generated SQL → SQLite
~~~

## Transaction state machine

~~~text
BEGIN
→ change A
→ change B
→ outcome?
   ├─ success → COMMIT
   └─ error/panic path → ROLLBACK
~~~

## Project v.5 migration

~~~text
v.4 storage package + JSON files
→ remove storage
→ database package
→ IRepository
→ SQLiteRepository
→ SQLite tables
→ structured queryable history
~~~

## Provenance

- classic SQLite: `p0308:c01–p0329:c01`
- GORM: `p0330:c01–p0334:c01`
- transactions: `p0335:c01–p0342:c01`
- DryRun: `p0343:c01`
- project v.5: `p0343:c01–p0360:c01`
