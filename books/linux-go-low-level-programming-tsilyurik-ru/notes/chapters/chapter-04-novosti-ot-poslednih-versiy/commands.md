# Commands — глава 4 «Новости от последних версий...»

Только команды, подтверждённые RAG главы.

| Команда | Класс | Назначение | Effect / risk | Verification | Rollback |
|---|---|---|---|---|---|
| `go mod init generic` | state-changing | Создать module metadata | Создаёт `go.mod` | `cat go.mod` | [Needs confirmation] |
| `cat go.mod` | read-only | Просмотреть module metadata | Нет изменения | stdout | [Not applicable] |
| `grep import max.go` | read-only | Проверить imports | Нет изменения | строки import | [Not applicable] |
| `go build max.go` | state-changing | Собрать пример | Создаёт/заменяет binary | `ls -l max`, `./max` | [Needs confirmation] |
| `go get golang.org/x/exp/constraints` | network + state-changing | Добавить dependency | Изменяет module metadata/cache | `cat go.mod`, `ls -l go.*` | [Needs confirmation] |
| `go mod tidy` | network + state-changing | Согласовать dependencies с imports | Изменяет `go.mod/go.sum`, cache | inspect files + build | [Needs confirmation] |
| `ls -l go.*` | read-only | Проверить module files | Нет изменения | file listing | [Not applicable] |
| `go env GOPATH` | read-only | Получить effective GOPATH | Нет изменения | path in stdout | [Not applicable] |
| `ls $(go env GOPATH)/pkg/mod/...` | read-only | Осмотреть module cache | Нет изменения | listing | [Not applicable] |
| `tree $(go env GOPATH)/pkg/mod/.../constraints` | read-only | Осмотреть constraint package | Нет изменения | tree output | [Not applicable] |
| `go fmt print_slice.0.go` | state-changing | Отформатировать source | Переписывает файл | inspect/diff | [Needs confirmation] |
| `go build -o print_slice print_slice.0.go` | state-changing | Собрать generic example | Создаёт binary `print_slice` | [source mismatch: запуск показан иначе] | [Needs confirmation] |
| `go build exist.go` | state-changing | Собрать comparable example | Создаёт binary | `./exist` | [Needs confirmation] |
| `./exist` | workload | Запустить example | Выполняет binary | expected booleans | [Not applicable] |
| `go fmt max.go` | state-changing | Форматировать source | Переписывает файл | inspect/diff | [Needs confirmation] |
| `./max` | workload | Запустить Ordered example | Выполняет binary | `world / 9 / 5.4` | [Not applicable] |
| `grep ^type .../constraints.go` | read-only | Показать constraint declarations | Нет изменения | список types | [Not applicable] |

## Important network boundary

`go get` и `go mod tidy` могут обращаться к сети и изменять локальный module cache. В source artifacts они поэтому не классифицируются как read-only.

## Source-specific paths

Путь вида:

```text
$GOPATH/pkg/mod/golang.org/x/exp@v0.0.0-20230310171629-522b1b587ee0/
```

относится к конкретной версии из окружения автора и не является универсальным текущим путём.
