# Шпаргалка — глава 5: файлы, JSON, сборка и конфигурация

## Fast map

~~~text
os / io / bufio
→ file + directory operations
→ JSON serialization
→ persistent stores
→ go build + runtime/compile config
→ game save/load
→ package refactor + storage interfaces
~~~

Scope: PDF 213–307.

## File operations

| Need | Source API |
|---|---|
| create/truncate file | `os.Create` |
| open existing file | `os.Open` |
| inspect file | `os.Stat` |
| rename/move | `os.Rename` |
| remove | `os.Remove` |
| flexible open | `os.OpenFile` |
| copy | `io.Copy` |
| sync buffered file state | `File.Sync` |
| line/word scanning | `bufio.Scanner` |

## `OpenFile` flags

~~~text
O_RDONLY / O_WRONLY / O_RDWR
O_APPEND
O_CREATE
O_EXCL
O_SYNC
O_TRUNC
~~~

Write without `O_APPEND` starts from beginning of file in chapter example.

## Permission examples

~~~text
0644 → owner rw, others r
0666 → rw for everyone
0755 → owner rwx, others rx
0777 → rwx for everyone
~~~

Use only permissions justified by required access.

## Formatted file I/O

Write:
- `fmt.Fprint`;
- `fmt.Fprintf`;
- `fmt.Fprintln`.

Read:
- `fmt.Fscan`;
- `fmt.Fscanf`;
- `fmt.Fscanln`.

For `Fprintf` / `Fscanf`, keep the same format structure.

## Directories

~~~go
os.Mkdir(path, perm)
os.MkdirTemp(dir, pattern)
os.MkdirAll(path, perm)
os.ReadDir(path)
os.Rename(old, new)
os.Stat(path)
os.IsNotExist(err)
filepath.Join(parts...)
~~~

## JSON

~~~go
data, err := json.Marshal(value)
data, err := json.MarshalIndent(value, "", "  ")
err = json.Unmarshal(data, &target)
~~~

### Tags

~~~go
Field string `json:"field"`
Field string `json:"-"`
Field string `json:"field,omitempty"`
~~~

### null / missing

Need to distinguish missing/null from zero value?

~~~text
plain field → zero value may hide absence
pointer field → nil can represent absence/null
~~~

### Unknown schema

`map[string]any` is shown for unknown structure; source prefers typed structs when shape is known.

## Persistence examples

### File-backed linked-list DB

~~~text
IAttribute
→ Node[T]
→ Table[T]
→ Database
→ text files
~~~

### JSON key:value store

~~~text
JSONFile
→ JSONStore
→ SetValue/GetValue
→ typed getters
→ store.json
~~~

## Build

~~~bash
go build
go build -o new-app.exe
go build -v -x
go build -race
~~~

## Runtime config

~~~bash
go run main.go -int=33 -bool
go run main.go -h
~~~

Package `flag` supports string/int/bool examples in chapter.

## Compile-time config

~~~bash
go build -ldflags "-X main.Version=1.2.3 -X main.VersionType=test"
go build -ldflags="-s -w"
~~~

## Embedded config

~~~go
//go:embed embed_config.json
var configData []byte
~~~

Deserialize embedded bytes with `encoding/json`.

## `.env`

Source implementation:
- load one or more files;
- merge OS environment;
- parse int/bool/string;
- typed getters.

Source security boundary:
- do not treat `.env` as strongest secret storage;
- exclude it from remote repository via `.gitignore`.

## Tic-tac-toe v.3

~~~text
IGameLoader
IGameSaver
   └─ IGameStorage
        ↓
JsonGameStorage
        ↓
JSON save/load
~~~

## Tic-tac-toe v.4

~~~text
board   player   game
   \      |      /
      model
        |
     storage
~~~

`GameSnapshot` breaks circular dependency pressure.

Computer levels:
- easy → random;
- medium → block threat;
- hard → minimax.

## Acceptance

After chapter you should be able to:
- choose file open flags and permissions;
- stream or fully read file deliberately;
- create/traverse directories;
- serialize/deserialize typed JSON;
- use tags and pointers for null/missing semantics;
- explain file-backed persistence examples;
- build application with main flags;
- configure via CLI, `-ldflags`, `go:embed`, `.env`;
- explain v.3 persistence interfaces;
- explain v.4 package boundaries and import-cycle avoidance.

## Rollback / risk

Filesystem examples are state-changing. Before running destructive examples, verify target path and whether overwrite/removal is intended. Exact VCS rollback procedure is not defined by source → `[Needs confirmation]`.
