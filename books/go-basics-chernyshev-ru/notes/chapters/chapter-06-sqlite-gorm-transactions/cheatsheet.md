# Шпаргалка — глава 6: SQLite, GORM и транзакции

## Fast model

~~~text
SQL / database/sql
→ explicit queries
→ SQLiteRepository

GORM
→ Go structs/tags
→ generated SQL
→ shorter CRUD

Transactions
→ atomic change set
→ commit or rollback
~~~

Scope: PDF 308–362.

## Classic SQLite

Dependencies:

~~~bash
go get github.com/mattn/go-sqlite3
go get github.com/dixonwille/wmenu
~~~

Open/create DB:

~~~go
db, err := sql.Open("sqlite3", "todo.db")
db.Exec(ProjectTabelDefinition)
db.Exec(TaskTabelDefinition)
~~~

## Schema

~~~text
projects
├─ id PK
├─ name UNIQUE
└─ description

tasks
├─ id PK
├─ name
├─ description
├─ priority
├─ is_done
└─ project_id FK → projects.id
~~~

## POD / model

Source terminology:

~~~text
entity = plain old data (POD)
model  = entity extended with more structure/behavior
~~~

## CRUD

~~~text
C → INSERT / Exec
R → SELECT / Query / Scan
U → UPDATE / Exec
D → DELETE / Exec
~~~

Parameterized values:

~~~go
db.Exec(
    "INSERT INTO projects(name, description) values(?,?)",
    name, description,
)
~~~

## GORM setup

~~~bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/sqlite
~~~

~~~go
db, err := gorm.Open(sqlite.Open(dbName), &gorm.Config{})
db.AutoMigrate(&Project{}, &ProjectTask{})
~~~

## GORM CRUD map

| Need | Method |
|---|---|
| create | `Create` |
| delete | `Delete` |
| read many | `Find` |
| filter | `Where` |
| persist update | `Save` |
| check result | `Error`, `RowsAffected` |

## Transaction callback

~~~go
db.Transaction(func(tx *gorm.DB) error {
    tx.Create(...)
    if failed {
        return err // rollback
    }
    return nil // commit
})
~~~

## Nested transaction

~~~text
outer transaction
├─ outer changes
├─ inner transaction A → rollback
├─ inner transaction B → rollback
└─ outer returns nil → outer commit
~~~

## Manual transaction

~~~go
tx := db.Begin()
if err := tx.Create(...).Error; err != nil {
    tx.Rollback()
    return err
}
return tx.Commit().Error
~~~

Panic guard from source:

~~~go
defer func() {
    if recover() != nil {
        tx.Rollback()
    }
}()
~~~

## Default transaction trade-off

~~~go
db.Session(&Session{SkipDefaultTransaction: true})
~~~

Source: performance may improve, integrity protection may decrease.

## DryRun

~~~go
db, _ := gorm.Open(
    sqlite.Open(dbName),
    &gorm.Config{DryRun: true},
)
stmt := db.Where("project_id", 1).Find(&tasks).Statement
fmt.Println(stmt.SQL.String())
~~~

No query executes; generated SQL can be inspected.

## Tic-tac-toe v.5

~~~text
v.4: JSON files / storage package
→ v.5: SQLite / database package

Game
→ IRepository
→ SQLiteRepository
→ GORM
→ SQLite file
~~~

DB models:
- Player;
- GameSnapshot;
- PlayerFinishGame.

Application models:
- model.GameSnapshot;
- model.FinishGameSnapshot.

## Acceptance

After chapter you should be able to:
- explain SQL vs ORM source framing;
- create/open SQLite DB with `database/sql`;
- create tables via DDL;
- implement parameterized CRUD;
- explain POD/entity/model distinction;
- create GORM DB and migrate models;
- map common GORM CRUD methods;
- explain commit/rollback;
- use callback and manual transactions;
- explain nested transactions;
- inspect generated SQL via DryRun;
- explain v.5 repository migration.

## Rollback / safety

Database operations are state-changing. For write examples, verify target DB and understand whether operation is inside a transaction. Source-backed rollback mechanism is transaction rollback; VCS rollback remains `[Needs confirmation]`.
