# Cheatsheet — глава 2 «Разворачиваем экосистему Go»

## Symptom / problem framing

Нужно получить рабочую и проверяемую Go-среду в Linux, понимать какая версия и реализация реально используется, уметь собирать и запускать приложение, исследовать effective environment и использовать toolchain для обычной и кросс-компиляции.

## Baseline / context

Перед изменениями источник использует read-only диагностику:

```bash
aptitude search golang
aptitude search gccgo
which go
go version
which gccgo
gccgo --version
gcc --version
lsb_release -a
ls -l "$(which go)"
ls -ld /lib/go*
update-alternatives --list go
```

Версии в книге — примеры конкретных систем автора, не acceptance criteria.

## Read-only checks

### Toolchain

```bash
which go
go version
which gccgo
gccgo --version
gcc --version
```

### Built-in documentation

```bash
go help
go help mod
go help mod download
go help environment
go help get
go help tool
go doc nm
```

### Environment

```bash
go env
go env GOPATH
go env GOTOOLDIR
env | grep GO
```

### Build artifacts

```bash
ls -l <artifact>
file <artifact>
ldd <artifact>
```

### Platform

```bash
lsb_release -a
uname -a
inxi -Cxxx
```

## Interpretation

### Which Go is active?

`which go` показывает фактический executable path, `go version` — активную версию. Если установлено несколько версий, источник использует `update-alternatives --list/config`.

### What environment does Go see?

`go env` показывает effective Go environment. Источник отдельно различает Go environment settings и обычные переменные окружения Linux, хотя системная переменная может переопределить поведение команды Go.

### Static vs dynamic result

Источник проверяет результат через:

```bash
file hello.*
ldd hello.*
```

и сравнивает сборки gc/gccgo/`-linkshared`.

### Cross-compilation

`GOOS` и `GOARCH` задаются для отдельной команды build. Результат проверяется `file`, затем запускается на целевой платформе.

## Next action

Нормальный workflow главы:

1. проверить доступные пакеты;
2. установить выбранный toolchain;
3. подтвердить `which` + `version`;
4. при нескольких версиях — зарегистрировать/выбрать alternative;
5. собрать тестовую программу;
6. проверить результат `file`/`ldd` и запуском;
7. изучить `go help` и `go env`;
8. только затем переходить к GOPATH, cross-build, tool и Cgo.

## Modifying action

### Package installation

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

Effect: устанавливает/изменяет системные пакеты.

Verification: `which`, `--version`, `go version`.

Rollback: [Needs confirmation] — источник не приводит команды удаления.

### Alternatives

```bash
sudo update-alternatives --install /usr/bin/go go /lib/go-1.13/bin/go 60
sudo update-alternatives --install /usr/bin/go go /lib/go-1.16/bin/go 70
sudo update-alternatives --config go
```

Effect: регистрирует и/или меняет активную реализацию `/usr/bin/go`.

Verification:

```bash
update-alternatives --list go
go version
```

Rollback: выбрать прежнюю alternative через `update-alternatives --config go`; удаление alternative в источнике не показано.

### Formatting

```bash
go fmt hello.0.go
go fmt *.go
```

Effect: изменяет исходные файлы.

Verification: проверить diff/размер/содержимое файла.

Rollback: [Needs confirmation].

### Build / clean

```bash
go build
go build hello.go
go clean
```

Effect: build создаёт артефакт, clean удаляет результаты сборки.

Verification: `ls -l`, запуск, `file`/`ldd`.

## Verification / acceptance checks

Минимальная проверка Go-среды по главе:

```bash
which go
go version
go env
go help
```

Минимальная проверка сборки:

```bash
go build hello.go
ls -l hello
file hello
./hello
```

Для cross-build:

```bash
GOOS=windows GOARCH=amd64 go build -o hello.64.exe
file hello.64.exe
```

Фактическая работоспособность подтверждается запуском на целевой ОС/архитектуре.

## Rollback

Rollback определён источником частично:

- build artifact: `go clean` в GOPATH/project workflow;
- active version: повторный `update-alternatives --config go`;
- остальные установки/изменения: **[Needs confirmation]**.
