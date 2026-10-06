# Cheatsheet — глава 4 «Новости от последних версий...»

## Symptom / problem framing

Два класса задач:

1. проект импортирует внешние packages, но зависимость не описана в module metadata;
2. нужно написать функцию/тип, работающий с несколькими типами без дублирования кода.

## Baseline / context

### Modules

Источник показывает:

```bash
go mod init generic
cat go.mod
grep import max.go
```

После появления внешнего импорта build сообщает о недостающем module provider.

### Generics

Базовая форма:

```go
func PrintSlice[T any](s []T) {
    for _, v := range s {
        fmt.Printf("%v ", v)
    }
}
```

Где `T` — type parameter, а `any` в источнике описан как синоним `interface{}`.

## Read-only checks

```bash
cat go.mod
ls -l go.*
go env GOPATH
ls "$(go env GOPATH)"/pkg/mod/...
tree "$(go env GOPATH)"/pkg/mod/.../constraints
grep import max.go
grep ^type "$(go env GOPATH)"/pkg/mod/.../constraints/constraints.go
```

Назначение: проверить module metadata, effective GOPATH, содержимое module cache и объявленные constraint types.

## Modules: controlled change

### Initialize

```bash
go mod init generic
```

Effect: создаёт `go.mod`.

Verification:

```bash
cat go.mod
```

Rollback: **[Needs confirmation]**.

### Add dependency explicitly

```bash
go get golang.org/x/exp/constraints
```

Effect по источнику:

- загружает module;
- изменяет `go.mod`;
- создаёт/изменяет `go.sum`;
- заполняет module cache.

Verification:

```bash
ls -l go.*
cat go.mod
go env GOPATH
```

Rollback: **[Needs confirmation]**.

### Reconcile imports

```bash
go mod tidy
```

Источник описывает команду как анализ imports и подготовку требуемых dependencies.

Verification: `go.mod`, `go.sum`, module cache, успешный `go build`.

Rollback: **[Needs confirmation]**.

## Generics

### Unconstrained-any example

```go
func PrintSlice[T any](s []T)
```

Вызов может быть explicit:

```go
PrintSlice[string](s)
```

или, если inference срабатывает:

```go
PrintSlice(s)
```

### Custom constraint

```go
type MyConstraint interface {
    int | int8 | int16 | int32 | int64
}
```

### Built-in comparable

```go
func existsInSlice[T comparable](val T, values []T) bool
```

Источник использует это для операций `==`/`!=`.

### Imported Ordered constraint

```go
func Max[T constraints.Ordered](a T, b T) T
```

Источник показывает успешные string/int/float примеры и compile error для complex value.

## Modifying actions

```bash
go fmt print_slice.0.go
go build -o print_slice print_slice.0.go

go build exist.go

go fmt max.go
go build max.go
```

Effects:

- `go fmt` переписывает source formatting;
- `go build` создаёт/заменяет build artifacts.

Verification: запуск соответствующего бинарника и проверка ожидаемого output.

Rollback: **[Needs confirmation]**.

## Verification / acceptance checks

Modules:

```bash
cat go.mod
ls -l go.*
go build max.go
```

Generics:

- `PrintSlice` работает для нескольких типов;
- type inference либо срабатывает, либо compiler требует explicit type arguments;
- `comparable` допускает equality comparison;
- `constraints.Ordered` пример компилируется для показанных ordered types;
- комплексный пример в источнике ожидаемо не проходит показанный constraint.

## Next action

После этой главы книга переходит к части 2 — конкурентности и многопроцессорности.
