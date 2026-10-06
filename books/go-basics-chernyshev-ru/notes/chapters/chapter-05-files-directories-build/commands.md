# Команды и инструменты — глава 5

Source policy: `rag_only`.

## Go CLI / shell commands explicitly present

### Initialize module

~~~bash
go mod init my_app
~~~

Type: state-changing.
Effect: creates `go.mod`.
Verification: module file appears.
Rollback: `[Needs confirmation]`.

### Build

~~~bash
go build
go build -o new-app.exe
go build -o .\my_app\new-app.exe .\my_app\main.go
go build -v -x
go build -race
~~~

Effects:
- produces executable;
- `-o` controls output path/name;
- `-v` prints build details;
- `-x` prints internal commands;
- `-race` enables race detector during build in source description.

### Run with runtime flags

~~~bash
go run main.go
go run main.go -int=33 -bool
go run main.go -h
~~~

`-h` is provided by package `flag` in chapter example.

### Compile-time variable injection

~~~bash
go build -ldflags "-X main.Version=1.2.3 -X main.VersionType=test"
go build -ldflags "-X main.Version=1.2.3 -X main.VersionType=test" -o my_app.exe
go build -ldflags="-s -w"
~~~

`-X` sets package variables during linking in source example.

`-s -w` removes symbol/debug information and is presented as reducing binary size.

## File APIs

| API | Changes state? | Purpose |
|---|---:|---|
| `os.Create` | yes | create/truncate file |
| `os.Open` | no | open for reading |
| `os.OpenFile` | depends on flags | flexible open/create/read/write/append |
| `os.Stat` | no | file/dir metadata |
| `os.Rename` | yes | rename/move |
| `os.Remove` | yes | remove file/empty dir in examples |
| `os.ReadFile` | no | read complete file |
| `os.WriteFile` | yes | write complete data |
| `io.ReadAll` | no | read reader fully |
| `io.Copy` | yes for destination | copy stream |
| `File.Sync` | yes/flush | sync file content |

## `os.OpenFile` flags

~~~text
O_RDONLY
O_WRONLY
O_RDWR
O_APPEND
O_CREATE
O_EXCL
O_SYNC
O_TRUNC
~~~

## Directory APIs

~~~go
os.Mkdir(path, perm)
os.MkdirTemp(dir, pattern)
os.MkdirAll(path, perm)
os.ReadDir(path)
os.Rename(oldPath, newPath)
os.Stat(path)
os.IsNotExist(err)
filepath.Join(parts...)
~~~

## Formatted file I/O

~~~go
fmt.Fprint(writer, ...)
fmt.Fprintf(writer, format, ...)
fmt.Fprintln(writer, ...)
fmt.Fscan(reader, ...)
fmt.Fscanf(reader, format, ...)
fmt.Fscanln(reader, ...)
~~~

## JSON APIs

~~~go
json.Marshal(value)
json.MarshalIndent(value, "", "  ")
json.Unmarshal(data, &target)
~~~

## Build/config mechanisms

### Package `flag`

~~~go
flag.String(...)
flag.Int(...)
flag.Bool(...)
flag.Parse()
~~~

### `go:embed`

~~~go
//go:embed embed_config.json
var configData []byte
~~~

### `.env`

No external dotenv package is used in the source example; chapter implements its own loader around `os.Open`, `bufio.Scanner`, `os.Environ`, regex parsing and typed getters.

## Risk / verification matrix

| Action | Risk | Verify |
|---|---|---|
| `os.Create` | truncates existing file | inspect path/content before/after |
| `os.Remove` | deletes target | confirm exact path first |
| `os.Rename` | moves/renames | verify source/destination |
| `O_WRONLY` without append | overwrites from beginning | choose flags deliberately |
| permissive mode like `0777` | broad access | use only when required |
| `go build` | creates artifact | verify output file/path |
| `.env` with secrets | repository disclosure | keep out of remote repo as source instructs |
