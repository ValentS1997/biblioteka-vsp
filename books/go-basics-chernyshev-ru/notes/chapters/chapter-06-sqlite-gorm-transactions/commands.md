# Команды и инструменты — глава 6

Source policy: `rag_only`.

## Dependencies

### SQLite driver

~~~bash
go get github.com/mattn/go-sqlite3
~~~

Type: state-changing/network.

Source note: driver requires GCC; Windows example references MinGW/TDM-GCC.

### Console menu

~~~bash
go get github.com/dixonwille/wmenu
~~~

### GORM

~~~bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/sqlite
~~~

These update module dependency state.

## Run ToDo example

~~~bash
go run .\main.go
~~~

Source example creates/opens `todo.db` and starts the terminal menu.

## Classic `database/sql` operations

### Open

~~~go
db, err := sql.Open("sqlite3", dbName)
~~~

### Execute write/DDL

~~~go
res, err := db.Exec(query, args...)
~~~

### Query rows

~~~go
rows, err := db.Query(query, args...)
defer rows.Close()
for rows.Next() {
    err := rows.Scan(&field1, &field2)
}
~~~

### Result metadata

~~~go
id, err := res.LastInsertId()
n, err := res.RowsAffected()
~~~

## SQL examples from chapter

Create tables:

~~~sql
CREATE TABLE IF NOT EXISTS projects (...);
CREATE TABLE IF NOT EXISTS tasks (...);
~~~

Insert with placeholders:

~~~sql
INSERT INTO projects(name, description) values(?,?)
~~~

Delete:

~~~sql
DELETE FROM tasks WHERE id = ?
~~~

Join-style read example from SQLite Explorer:

~~~sql
SELECT p.name, p.description, t.name, t.description, t.priority, t.is_done
FROM projects as p, tasks as t
WHERE p.id = t.project_id
ORDER BY t.priority DESC;
~~~

## GORM operations

~~~go
db, err := gorm.Open(sqlite.Open(dbName), &gorm.Config{})
db.AutoMigrate(&Project{}, &ProjectTask{})

db.Create(&value)
db.Delete(&value)
db.Find(&values)
db.Where("project_id", id).Find(&values)
db.Save(&value)
~~~

Check:
- `tx.Error`;
- `tx.RowsAffected`.

## Transactions

Callback form:

~~~go
db.Transaction(func(tx *gorm.DB) error {
    ...
    return nil
})
~~~

Manual:

~~~go
tx := db.Begin()
tx.Commit()
tx.Rollback()
~~~

Default write transactions can be disabled in source example:

~~~go
db.Session(&Session{SkipDefaultTransaction: true})
~~~

Risk: source warns about data-integrity trade-off.

## DryRun

~~~go
db, _ := gorm.Open(
    sqlite.Open(dbName),
    &gorm.Config{DryRun: true},
)
fmt.Println(stmt.SQL.String())
~~~

Effect: generates SQL without executing DB operations.

## Operational verification

| Action | Verification | Rollback |
|---|---|---|
| dependency install | inspect `go.mod` / `go.sum` | `[Needs confirmation]` |
| create DB/tables | inspect SQLite schema | transaction not applicable to initial file creation in shown example |
| insert/update/delete | inspect rows / `RowsAffected` | transaction rollback when wrapped in transaction |
| GORM migration | inspect generated tables | `[Needs confirmation]` |
| transaction | inspect state after commit/rollback | `Rollback()` before commit |
| DryRun | inspect SQL text; DB state unchanged | N/A |
