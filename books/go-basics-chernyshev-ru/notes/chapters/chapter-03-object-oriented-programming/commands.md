# Команды и инструменты — глава 3

Source policy: `rag_only`.

## Shell / Go CLI explicitly present

### Initialize car-factory module

~~~bash
go mod init golang/car_factory
~~~

Type: state-changing.

Effect:
- initializes module for interface-as-field example;
- creates module metadata (`go.mod`).

Verification:
- project contains `go.mod`;
- package paths use `golang/car_factory/...` in shown imports.

Rollback:
- `[Needs confirmation]` — chapter does not provide an undo procedure.

Provenance: `p0175:c01`.

## No additional shell-command inventory

В извлечённых RAG chunks главы 3 не подтверждён отдельный набор operational CLI-команд, сопоставимый с главой 2. Поэтому artifact не добавляет `go run`, `go test`, Git или другие commands из model memory.

## Code-level mechanisms used as operational primitives

### Struct creation

~~~go
v := Type{}
v := Type{Field: value}
p := &v
p2 := new(Type)
~~~

### Method receiver

~~~go
func (v Type) ReadOnlyStyle() { ... }
func (v *Type) MutatingStyle() { ... }
~~~

### Constructor functions

~~~go
func NewType(...) *Type {
    return &Type{...}
}
~~~

### Interface conversion / assignment

Chapter shows explicit and implicit movement of concrete values to interface types when method sets match.

### Type assertion

~~~go
value, ok := i.(TargetType)
~~~

Use checked form to avoid runtime failure on unsupported assertion.

### Type switch

~~~go
switch i.(type) {
case TypeA:
case TypeB:
default:
}
~~~

### Generic constraints

~~~go
func Sum[T int | float64 | string](a, b T) T
func Sum[T ~int | float64 | string](a, b T) T
func GetMapKeys[K comparable, V any](m map[K]V) []K
~~~

## State-changing boundary

Most chapter operations change in-memory object state or source code structure, not system configuration.

Examples:
- pointer receiver mutates instance state;
- setter methods change private fields;
- `ChangeMotor` swaps interface-backed implementation;
- `Board.setSymbol` changes game board.

The chapter does not define a source-control rollback procedure → `[Needs confirmation]`.
