# Команды и инструменты — глава 2

Source policy: `rag_only`.

## Module commands

| Command | Type | Effect | Verification | Rollback |
|---|---|---|---|---|
| `go mod init golang/first` | state-changing | создаёт module и `go.mod` | `go.mod` появился | [Needs confirmation] |
| `go mod download` | state-changing/network | скачивает dependencies; sample creates `go.sum` | dependency available | [Needs confirmation] |
| `go get github.com/google/uuid` | state-changing/network | добавляет external dependency | `go.mod` contains dependency | unused dependency → `go mod tidy` |
| `go get golang.org/x/time/rate` | state-changing/network | intentionally adds unused dependency | dependency appears in `go.mod` | `go mod tidy` |
| `go mod tidy` | state-changing/network | adds missing/removes unused requirements | unused dependency removed | [Needs confirmation] |
| `go mod vendor` | state-changing | creates/updates `vendor` | vendor tree exists | [Needs confirmation] |
| `go mod graph` | read-only | prints requirement graph | inspect stdout | N/A |
| `go mod verify` | read-only | verifies expected dependency content | inspect result | N/A |
| `go mod edit` | state-changing CLI interface | edits/formats `go.mod` | inspect file | [Needs confirmation] |
| `go mod why` | read-only | explains why package/module is needed | inspect stdout | N/A |

The `go mod` command list above is explicitly summarized in `p0150:c01`.

## External Faker dependency

~~~bash
go get github.com/jaswdr/faker
~~~

Type: state-changing/network.
Effect: adds Faker dependency.
Verification: sample imports package and generates fake data.
Rollback when unused: `go mod tidy`.

Provenance: `p0143:c01`.

## Run tests

~~~bash
go test ./test -v
~~~

Type: workload-generating.
`./test` selects test directory; `-v` adds detailed output.

Provenance: `p0134:c01`.

## Coverage

~~~bash
go test ./... -cover
go test ./... -coverprofile="coverage.out"
go tool cover -html="coverage.out"
~~~

- `-cover`: calculate package coverage.
- `-coverprofile`: create coverage profile file.
- `go tool cover -html`: visualize covered/uncovered code.

Generated `coverage.out` changes filesystem state. Exact removal command is not given by source → `[Needs confirmation]`.

Provenance: `p0139:c01–p0140:c01`.

## Benchmarks

~~~bash
go test ./... -bench=.
go test ./... -bench=Pow2
go test ./... -bench=Mul
go test ./... -bench=Pow2 -benchmem -benchtime=100000x
~~~

Type: workload-generating.

- `-bench=.` runs benchmarks.
- named value selects benchmark.
- `-benchmem` reports B/op and allocs/op.
- `-benchtime=100000x` fixes iteration count to 100000 in source example.

Provenance: `p0141:c01–p0142:c01`.

## go.mod directives shown

External dependency:

~~~text
require github.com/google/uuid v1.6.0
~~~

Local module:

~~~text
replace golang/second => ../second
require golang/second v0.0.0-00010101000000-000000000000
~~~

The RAG text contains typographic dashes in some code listings; punctuation here is normalized only where intended syntax is unambiguous.

## Go testing API

~~~go
func TestAdd(t *testing.T) { ... }
t.Errorf(...)
t.Run(name, func(t *testing.T) { ... })

func BenchmarkMul(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Mul(5, 10)
    }
}
~~~

## Code-level mechanisms

- `package main` — executable package.
- uppercase identifier — exported.
- lowercase identifier — package-private.
- `alias "module/path"` — import alias.
- `type` — named type/function-signature alias in chapter terminology.
- `return` — explicit function result.
- `defer` — deferred call.
- goroutine + channel — generator mechanism.

## Operational boundary

Dependency commands may alter `go.mod`, `go.sum`, module cache and `vendor`. Chapter does not define VCS rollback; do not invent it in RAG-only artifacts.
