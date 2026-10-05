# Шпаргалка — глава 2: функции, модули, пакеты и тестирование

## Symptom / problem framing

| Problem | Source-grounded direction |
|---|---|
| повторяющийся код | вынести reusable logic в function |
| function должна менять caller state | передать pointer, если это действительно требуется |
| сложная сигнатура | объявить named type через `type` |
| длинный `main` | декомпозировать на functions/packages |
| package function не видна | проверить uppercase exported identifier |
| dependency не используется | `go mod tidy` |
| local module dependency | `replace ... => ../path` |
| одна функция должна пройти много комбинаций | table-driven tests |
| непонятно, что не покрыто тестами | coverage profile + `go tool cover` |
| нужно сравнить performance | benchmark |

## Baseline / context

~~~text
functions
→ abstraction/reuse
→ packages/modules
→ dependency management
→ tests
→ refactored project
~~~

Scope: PDF 101–152.

## Read-only checks

~~~bash
go mod graph
go mod verify
go mod why
go test ./... -cover
~~~

- `go mod graph` — dependency graph.
- `go mod verify` — проверка ожидаемого содержимого dependencies.
- `go mod why` — объяснение, зачем нужен package/module.
- `go test ./... -cover` — tests + coverage.

## Function forms

~~~go
func hello() { ... }

func add(a, b int) int {
    return a + b
}

func add2(a, b int) (int, bool) {
    return a + b, a > b
}

func named(a, b int) (sum int) {
    sum = a + b
    return
}

func variadic(values ...int) int { ... }
~~~

Multi-return нужно полностью распаковать; ненужное значение принимается в `_`.

## Value vs pointer

~~~text
value argument
→ copy
→ source variable unchanged

pointer argument
→ address copied
→ dereference can change source value
~~~

Chapter comparison `find1` vs `find2` показывает: явный return обычно делает contract понятнее, чем скрытый result через pointer argument.

## Function values / higher-order

~~~go
myFunc := add
fmt.Println(myFunc(3, 5))
~~~

Function signature становится type переменной.

~~~go
func sub(c, a, b int, addFunc func(int, int) int) int {
    return c - addFunc(a, b)
}
~~~

## Anonymous functions / closures

Anonymous function не имеет имени и может быть assigned, passed, returned или invoked inline.

Closure сохраняет доступ к enclosing lexical scope:

~~~text
outer values
→ nested function captures them
→ returned function keeps using them
~~~

## Recursion

~~~text
direct:   f → f
indirect: f → g → f
~~~

Всегда нужен exit condition.

## Generator

Generator example:

~~~text
request next value
→ goroutine produces
→ channel transfers
→ no need to materialize full sequence
~~~

## defer

`defer` выполняет call при выходе из function. Несколько deferred calls выполняются LIFO.

Source use cases:
- file/socket close;
- mutex unlock;
- guaranteed resource release.

## Modules vs packages

| Concept | Meaning in chapter |
|---|---|
| executable package | `package main` + `main` |
| utility package | reusable code |
| executable module | contains executable package |
| service module | dependency-only, no executable package |

## go.mod / go.sum

`go.mod`: module path, Go version, requirements.

`go.sum`: integrity-related dependency records.

## Dependency workflow

~~~bash
go mod init golang/first
go mod download
go get github.com/google/uuid
go mod tidy
go mod vendor
~~~

Semantic version:

~~~text
vMAJOR.MINOR.PATCH
major → incompatible API change
minor → compatible feature
patch → compatible fix
~~~

## Package visibility

~~~text
func replaceSymbols(...) → private to package
func ReplaceSymbols(...) → exported
~~~

## Import alias

~~~go
import (
    f "fmt"
    u "golang/first/utils"
)
~~~

Use cases in chapter: directory/package mismatch, collisions, overly long names.

## Local module

~~~text
replace golang/second => ../second
require golang/second <version>
~~~

## Unit test

~~~go
func TestAdd(t *testing.T) {
    result := Add(2, 5)
    expected := 7
    if result != expected {
        t.Errorf("result %d, expected %d", result, expected)
    }
}
~~~

Test function starts with `Test` and accepts `*testing.T`.

## Table-driven test

~~~text
cases[]
→ loop
→ execute function
→ compare actual vs expected
~~~

Useful when one behavior must be checked against many inputs and edge cases.

## Subtests

~~~go
t.Run(name, func(t *testing.T) {
    ...
})
~~~

## Coverage

~~~bash
go test ./... -cover
go test ./... -coverprofile="coverage.out"
go tool cover -html="coverage.out"
~~~

## Benchmark

~~~go
func BenchmarkMul(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Mul(5, 10)
    }
}
~~~

~~~bash
go test ./... -bench=.
go test ./... -bench=Pow2
go test ./... -bench=Pow2 -benchmem -benchtime=100000x
~~~

## Next action

1. Вынести повторяющийся код в functions.
2. Разделить reusable code на package.
3. Проверить exported/private boundary.
4. Инициализировать module.
5. Добавить dependency и выполнить tidy.
6. Написать table-driven tests.
7. Проверить coverage.
8. Добавить benchmark для performance-sensitive function.
9. Разобрать tic-tac-toe v.1.

## Modifying action

### `go mod init`
Effect: создаёт `go.mod`.
Verification: `go.mod` существует.
Rollback: `[Needs confirmation]`.

### `go get <module>`
Effect: добавляет external dependency и меняет module metadata.
Verification: dependency появляется в `go.mod`; sample uses package.
Rollback when dependency becomes unused: chapter-supported cleanup is `go mod tidy`.

### `go mod tidy`
Effect: добавляет missing и удаляет unused module requirements.
Verification: unused dependency исчезает из `go.mod`.
Rollback: `[Needs confirmation]`.

### `go mod vendor`
Effect: создаёт/обновляет `vendor`.
Verification: каталог существует при наличии dependencies.
Rollback: `[Needs confirmation]`.

## Verification / acceptance checks

После главы читатель должен уметь:
- объяснить function signature и multi-return;
- отличить value from pointer argument;
- передать function as value/argument;
- объяснить closure;
- отличить direct/indirect recursion;
- объяснить generator and `defer`;
- различить module/package;
- объяснить `go.mod`, `go.sum`, `vendor`, `replace`;
- экспортировать identifier через uppercase;
- написать unit/table-driven/subtest;
- измерить coverage;
- написать benchmark;
- объяснить decomposition tic-tac-toe v.1.

## Rollback

Глава не задаёт Git/VCS rollback workflow. Для state-changing module commands точные undo procedures, кроме cleanup unused dependency через `go mod tidy`, остаются `[Needs confirmation]`.
