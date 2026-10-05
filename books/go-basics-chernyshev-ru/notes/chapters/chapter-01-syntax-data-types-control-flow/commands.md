# Команды и инструменты — глава 1

Source policy: `rag_only`.

Включены только команды и инструменты, которые явно присутствуют в RAG главы 1.

## Shell / Go CLI

| Command | Type | Effect | Verification | Risk / rollback |
|---|---|---|---|---|
| `go version` | read-only | выводит установленную версию Go и используется для проверки установки | команда должна вернуть информацию о Go version | state не изменяет |
| `go mod init hello-go` | state-changing | инициализирует Go module и создаёт `go.mod` | `go.mod` появляется в project directory | rollback: `[Needs confirmation]` |
| `go run main.go` | workload-generating | собирает и запускает `main.go` | Hello World example печатает `Hello World!`; stdin example ожидает ввод | способ остановки/rollback отдельно не документирован |

### Extraction normalization note

В RAG команда и имя каталога отображаются как `hello–go` с типографским dash.
Для runnable command использован ASCII `hello-go`; намерение однозначно из контекста создания директории/module.

Provenance:
- `go version`: `p0019:c01`;
- `go mod init`: `p0021:c01`;
- `go run main.go`: `p0022:c01`, повторно `p0067:c01`.

## IDE actions

Это не shell commands.

| Action | Type | Source purpose |
|---|---|---|
| `F5` | workload-generating UI action | запуск в debug mode |
| `Ctrl+F5` | workload-generating UI action | запуск без debug mode |
| `Ctrl+Shift+X` | read-only/navigation UI action | открыть Extensions в VS Code |
| `Ctrl+Shift+P` / `F1` | read-only/navigation UI action | открыть command palette |
| `Go: Install/Update tools` | state-changing IDE action | установить/обновить tools расширения Go |

Точный rollback для установки/обновления IDE tools: `[Needs confirmation]`.

## Go language operators / built-ins used as tools

### Allocation and collection operations

| Item | Purpose | Boundary |
|---|---|---|
| `make` | создать initialized slice/map в примерах | не shell command |
| `new` | выделить zeroed object и вернуть pointer | reference types всё равно могут содержать `nil` |
| `copy` | скопировать элементы slice | destination length ограничивает число скопированных элементов |
| `append` | добавить элементы в slice | may change backing array |
| `delete` | удалить key из map | state-changing в памяти процесса |
| `len` | получить длину string/array/slice/map | read-only |
| `cap` | получить capacity slice | read-only |

## fmt

Source-confirmed functions:
- `fmt.Print`;
- `fmt.Println`;
- `fmt.Printf`;
- `fmt.Sprintf`;
- `fmt.Fscan`.

Formatting inventory:

### Integers

- `%b`
- `%c`
- `%d`
- `%o`
- `%O`
- `%x`
- `%X`
- `%U`

### Floats

- `%b`
- `%e` / `%E`
- `%f` / `%F`
- `%x` / `%X`

### Strings / byte slices

- `%s`
- `%q`
- `%x` / `%X`

### Generic

- `%v`
- `%+v`
- `%T`
- `%%`

### Other

- `%p` — pointer address;
- `%t` — bool.

Provenance: `p0076:c01–p0078:c01`.

## strconv

Explicit conversions shown:
- `strconv.Itoa(int) string`;
- `strconv.Atoi(string) (int, error)`;
- `strconv.FormatFloat`;
- `strconv.ParseFloat`.

Provenance: `p0066:c01`.

## strings

Functions explicitly demonstrated include:

- `TrimSpace`;
- `Trim`;
- `TrimLeft`;
- `TrimRight`;
- `TrimPrefix`;
- `TrimSuffix`;
- `ToUpper`;
- `ToLower`;
- `ToTitle`;
- `Split`;
- `SplitAfter`;
- `SplitN`;
- `Fields`;
- `FieldsFunc`;
- `Builder.Write`;
- `Builder.WriteString`;
- `Builder.WriteByte`;
- `Builder.WriteRune`;
- `Builder.Len`;
- `Builder.Cap`;
- `Builder.Grow`;
- `Builder.Reset`.

Provenance: `p0079:c01–p0086:c01`.

## slices

Functions explicitly demonstrated include:

- iteration: `All`, `Backward`, `Chunk`;
- mutation/copy: `Insert`, `Clone`, `Concat`, `Delete`, `DeleteFunc`, `Repeat`, `Replace`, `Reverse`;
- sorting: `Sort`, `SortFunc`, `IsSorted`;
- search: `BinarySearch`, `Index`, `Contains`;
- comparison: `Compare`, `Equal`;
- cleanup/statistics: `Compact`, `Max`, `Min`.

Provenance: `p0087:c01–p0091:c01`.

## maps

Functions explicitly demonstrated:

- `maps.Clone`;
- `maps.Copy`;
- `maps.DeleteFunc`;
- `maps.Equal`;
- `maps.Keys`;
- `maps.Values`.

Provenance: `p0091:c01–p0092:c01`.

## State-changing boundary

The chapter contains code that changes process memory, files created by Go tooling, and project source code, but does not define a general rollback/VCS workflow.

Therefore:
- shell/project rollback not supplied by chapter → `[Needs confirmation]`;
- in-memory examples are reset by restarting/re-running the program;
- do not invent Git commands or cleanup commands from model memory.
