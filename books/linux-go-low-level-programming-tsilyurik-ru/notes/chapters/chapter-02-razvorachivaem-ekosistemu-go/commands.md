# Commands — глава 2 «Разворачиваем экосистему Go»

Только команды и инструменты, явно присутствующие в chapter RAG.

## Discovery and verification

| Команда | Класс | Назначение |
|---|---|---|
| `aptitude search golang` | read-only | Поиск GoLang packages |
| `aptitude search gccgo` | read-only | Поиск gccgo |
| `aptitude search golang-1.` | read-only | Просмотр доступных версий |
| `which go` | read-only | Путь активного `go` |
| `go version` | read-only | Версия активного Go |
| `which gccgo` | read-only | Путь gccgo |
| `gccgo --version` | read-only | Версия gccgo |
| `gcc --version` | read-only | Версия GCC |
| `lsb_release -a` | read-only | Информация о дистрибутиве |
| `uname -a` | read-only | Kernel/platform info |
| `inxi -Cxxx` | read-only | CPU/platform info |
| `file <artifact>` | read-only | Формат бинарника/объекта |
| `ldd <artifact>` | read-only | Динамические зависимости |
| `du -hs <path>` | read-only | Размер дерева |
| `pkg-config --libs glu` | read-only | Link flags для библиотеки |

## Package management

Следующие команды **state-changing**:

```bash
sudo apt install golang
sudo apt install gccgo
sudo apt install golang-1.16
sudo apt install subversion
sudo apt install mercurial
sudo apt install git
sudo apt install bzr
sudo apt install delve
```

Effect: изменяют системный package state.

Verification: соответствующие `which`, `--version`, `go version`.

Rollback: **[Needs confirmation]**.

## Multiple Go versions

Read-only:

```bash
update-alternatives --list go
ls -l "$(which go)"
ls -ld /lib/go*
```

State-changing:

```bash
sudo update-alternatives --install /usr/bin/go go /lib/go-1.13/bin/go 60
sudo update-alternatives --install /usr/bin/go go /lib/go-1.16/bin/go 70
sudo update-alternatives --install /usr/bin/go go /home/olej/goroot/bin/go 80
sudo update-alternatives --config go
```

Verification:

```bash
go version
update-alternatives --list go
```

Rollback: выбрать предыдущую alternative; удаление записи — [Needs confirmation].

## Building Go from source

State-changing / network:

```bash
cd "$HOME"
git clone https://go.googlesource.com/go goroot
cd goroot
git fetch
cd src
time ./all.bash
```

Effect: создаёт/обновляет Git tree и выполняет тяжёлую сборку toolchain.

Source warning: build CPU-intensive.

Verification:

```bash
ls -l "$HOME/goroot/bin/"
"$HOME/goroot/bin/go" version
```

Rollback: [Needs confirmation].

## Basic application build

State-changing:

```bash
go build hello.go
gccgo -g hello.go -o hello.1
go build -o hello.2 hello.go
go build -o hello.2 -compiler gc hello.go
go build -o hello.3 -compiler gccgo hello.go
go build -o hello.4 -linkshared -compiler gc hello.c.go
```

Verification:

```bash
ls -l hello*
file hello*
ldd hello*
./hello
```

## Fast execution

Workload-generating:

```bash
go run hello.go
time go run tiny.go
```

Source framing: compile-and-run workflow used like a script.

## Built-in help

Read-only:

```bash
go help
go help mod
go help mod download
go help environment
go help get
go help tool
go tool nm -h
go doc nm
go tool fix -h
```

## Go environment

Read-only:

```bash
go env
go env GOPATH
go env GOTOOLDIR
env | grep GO
go help environment
```

Session state-changing example:

```bash
export GONOSUMDB='12345'
go env GONOSUMDB
```

Effect: меняет environment текущего shell/дочерних процессов.

Rollback: **[Needs confirmation]**; источник не показывает восстановление/удаление переменной.

## GOPATH workflow

Read-only/context:

```bash
go env GOPATH
ls "$(go env GOPATH)"
ls -l ~/go/src
pwd
```

State-changing:

```bash
go build
go clean
go build mtime
```

`go clean` в примере удаляет build product; `go build mtime` создаёт его в текущем рабочем каталоге.

## Cross-compilation

State-changing build commands:

```bash
GOOS=windows GOARCH=386 go build -o hello.32.exe
GOOS=windows GOARCH=amd64 go build -o hello.64.exe
GOARCH=arm go build -o hello.32.arm hello.go
```

Verification:

```bash
file *.exe
file hello.32.arm
```

Acceptance: запуск на целевой системе/архитектуре.

Rollback: [Needs confirmation].

## Formatting

State-changing:

```bash
go fmt hello.0.go
go fmt *.go
```

Effect: переписывает исходные Go-файлы в стиле formatter.

Verification: inspect/diff resulting source.

Rollback: [Needs confirmation].

## Network project retrieval

Potentially state-changing/network:

```bash
go get github.com/astaxie/beego
go get launchpad.net/gorun
go get github.com/golang/lint/golint
```

Effect: загружает project/package material в workflow, описанный источником.

Prerequisite in chapter: valid GOPATH for shown legacy workflow.

Rollback: [Needs confirmation].

## Tool subcommands

Read-only discovery:

```bash
go tool
go env GOTOOLDIR
go help tool
```

State-changing / build-analysis examples:

```bash
time GODEBUG=installgoroot=all go install std
go tool compile tiny.go
go tool link tiny.o
go tool objdump tiny.o
go tool compile -m tiny.go
```

Notes:

- `go install std` changes/install-populates toolchain state and is workload/network intensive in the source example.
- `compile` and `link` create artifacts.
- `objdump` and `compile -m` are used for analysis; `compile -m` may also emit compilation output/artifacts depending on invocation.

## Cgo

State-changing build/generation:

```bash
go build tiny.c.go
go build cex.go
go tool cgo hello.c.go
```

Read-only verification:

```bash
ls -l _obj
./cex
```

The source also demonstrates `#cgo CFLAGS`, `LDFLAGS` and `pkg-config` directives inside Go source.

## Delve

Read-only discovery/help:

```bash
aptitude search Delve | grep Go
which dlv
dlv --help
```

Installation:

```bash
sudo apt install delve
```

State-changing system package operation; rollback [Needs confirmation].
