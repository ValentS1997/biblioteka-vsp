# Commands — глава 3 «Неформально о синтаксисе Go»

Только команды/инструменты, подтверждённые RAG главы.

## Formatter/help

| Команда | Класс | Назначение | Effect / risk | Verification | Rollback |
|---|---|---|---|---|---|
| `which gofmt` | read-only | Найти formatter | Нет изменения | путь в stdout | [Not applicable] |
| `gofmt --help` | read-only | Показать options | Нет изменения | help output | [Not applicable] |
| `go help fmt` | read-only | Справка по `go fmt` | Нет изменения | help output | [Not applicable] |

В help source показывает, что `gofmt -w` переписывает source file, а `go fmt` запускает formatter для указанных packages. Это **state-changing** поведение при фактическом применении режима записи.

## Example execution

Workload-generating commands, показанные в главе:

```bash
./circle
./object3
./panic
./string3
./string2
./bigint
```

Назначение: проверка поведения соответствующих примеров.

Rollback: [Not applicable] для самого запуска; возможные application-specific side effects в главе не описаны.

## Build commands

State-changing в текущем каталоге:

```bash
go build panic.go
go build -o string3 string3.go
go build -o string2 string2.go
go build -o bigint bigint.go
```

Effect: создают build artifact.

Verification:

```bash
./panic
./string3
./string2
ls -l bigint
./bigint
```

Rollback: **[Needs confirmation]**.

## Testing

Source-confirmed command:

```bash
go test
```

Класс: workload-generating / test build-and-run.

По тексту главы команда:

1. находит test functions в `*_test.go`;
2. создаёт test binary;
3. запускает его.

Source prerequisites:

```go
import "testing"

func TestFoo(t *testing.T) {
    // ...
}
```

Рассмотрение детальной технологии тестирования в главу не входит.

## Source examples that are code, not shell commands

Следующие конструкции важны, но не являются командами shell:

```go
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)

type position float64
type velocity float64

b := make([]int, 10, 100)

elem, ok = m[key]
delete(m, key)

func f(a, b int) (int, string) {
    return a + b, "сложение"
}

type Abser interface {
    Abs() float64
}
```

Они перечислены здесь отдельно, чтобы не смешивать language syntax с операционными командами.
