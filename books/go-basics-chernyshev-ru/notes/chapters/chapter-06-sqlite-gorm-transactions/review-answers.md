# Ответы на вопросы для самопроверки — глава 6

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Что такое SQL и для чего он используется?

По материалу главы SQL используется для описания структуры реляционной БД и выполнения запросов к данным.

Chapter examples используют:
- DDL `CREATE TABLE` для структуры;
- `INSERT` для добавления;
- `SELECT` для чтения;
- `UPDATE` для изменения;
- `DELETE` для удаления.

Отдельного теоретического определения SQL source не разворачивает; ответ основан на применении языка в chapter examples.

Provenance: `p0309:c01–p0315:c01`, `p0329:c01`.

## 2. Что такое ORM и какие преимущества дает?

ORM — Object-Relational Mapping. Source описывает его как способ работать с БД через object-oriented representation вместо ручного написания большей части SQL.

Преимущества по chapter:
- меньше application code;
- быстрее разработка;
- меньше ошибок при ручном формировании запросов.

Ограничение: сложные generated queries могут быть менее оптимальными, чем ручной SQL.

Provenance: `p0330:c01`, `p0361:c01`.

## 3. Создание БД через go-sqlite3

Chapter открывает/создаёт SQLite file через `database/sql`:

~~~go
db, err := sql.Open("sqlite3", pathToDB)
if err != nil {
    log.Fatal(err)
}
~~~

Если file базы отсутствует, source затем выполняет DDL создания tables.

Provenance: `p0311:c01`.

## 4. Создание table через go-sqlite3

DDL хранится как SQL string:

~~~sql
CREATE TABLE IF NOT EXISTS projects(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT UNIQUE,
    description TEXT
);
~~~

И выполняется:

~~~go
db.Exec(ProjectTabelDefinition)
~~~

Provenance: `p0310:c01–p0311:c01`.

## 5. Что такое POD?

Source раскрывает POD как `plain old data` — простую структуру данных без расширяющего поведения.

Глава называет такие structures сущностями (entity). Model может расширять entity.

Provenance: `p0312:c01`.

## 6. Запросы через go-sqlite3

Write/DDL запросы выполняются через `Exec`; multi-row read — через `Query`, далее rows читаются через `Next` и `Scan`.

Example insert:

~~~go
res, err := s.db.Exec(
    "INSERT INTO projects(name, description) values(?,?)",
    project.Name, project.Description,
)
~~~

Chapter explicitly uses `?` placeholders for variable data.

Example read:

~~~go
rows, err := s.db.Query("SELECT * FROM tasks")
defer rows.Close()
for rows.Next() {
    rows.Scan(&task.ID, &task.Name, ...)
}
~~~

Provenance: `p0313:c01–p0315:c01`.

## 7. Что такое CRUD?

CRUD — acronym:
- Create;
- Read;
- Update;
- Delete.

Source связывает его с базовыми операциями над database records.

Provenance: `p0312:c01`.

## 8. Как удалить запись?

Classic example:

~~~go
res, err := s.db.Exec(
    "DELETE FROM tasks WHERE id = ?",
    taskID,
)
~~~

После этого source проверяет `RowsAffected`, чтобы убедиться, что запись действительно была удалена.

Provenance: `p0315:c01`.

## 9. Создание БД через GORM

Chapter uses:

~~~go
db, err := gorm.Open(sqlite.Open(dbName), &gorm.Config{})
~~~

Если database file отсутствует, он создаётся через SQLite driver при открытии; затем выполняется migration.

Provenance: `p0331:c01–p0332:c01`.

## 10. Создание table через GORM

Chapter uses model structures + migration:

~~~go
db.AutoMigrate(&Project{}, &ProjectTask{})
~~~

Column properties/relations задаются `gorm` struct tags.

Provenance: `p0330:c01–p0332:c01`.

## 11. Запросы через GORM

Source maps common operations to ORM methods.

Examples:

~~~go
r.db.Create(&project)
r.db.Delete(&Project{ID: projectID})
r.db.Find(&projects)
r.db.Where("project_id", projectID).Find(&tasks)
r.db.Save(&task)
~~~

Result inspection:

~~~go
tx.Error
tx.RowsAffected
~~~

Provenance: `p0332:c01–p0334:c01`.

## 12. Что такое transaction и зачем она нужна?

Transaction объединяет несколько DB operations в atomic action.

По source:
- изменения становятся согласованным набором;
- при успешном завершении фиксируются commit;
- при error откатываются rollback;
- до фиксации изменения не должны считаться окончательно записанными.

Transactions нужны для сохранения целостности данных при multi-step changes.

Provenance: `p0335:c01`.

## 13. Как откатить изменения?

В callback form GORM source возвращает error:

~~~go
db.Transaction(func(tx *gorm.DB) error {
    tx.Create(...)
    return errors.New("RollBack")
})
~~~

Это вызывает rollback.

При ручном управлении:

~~~go
tx := db.Begin()
...
tx.Rollback()
~~~

Chapter также показывает deferred rollback при panic.

Provenance: `p0338:c01–p0342:c01`.

## 14. DryRun

GORM connection/session в DryRun generates SQL statements without executing them.

Example:

~~~go
db, _ := gorm.Open(
    sqlite.Open(dbName),
    &gorm.Config{DryRun: true},
)
stmt := db.Where("project_id", 1).Find(&tasks).Statement
fmt.Println(stmt.SQL.String())
~~~

Use cases from source:
- inspect ORM-generated SQL;
- decide whether query needs optimization;
- study an alternative SQL formulation;
- do so without changing database state.

Provenance: `p0343:c01`.
