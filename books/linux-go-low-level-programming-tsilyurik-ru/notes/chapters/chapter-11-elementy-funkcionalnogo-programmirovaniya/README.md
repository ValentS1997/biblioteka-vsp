# Глава 11. Элементы функционального программирования

Статус: **RAG_GROUNDED**

## Scope

Глава показывает, какие приёмы функционального программирования можно применять в Go, не объявляя сам язык функциональным.

Основные темы:

1. функции как значения и функции высшего порядка;
2. функциональные замыкания;
3. сравнение closure/state techniques в Python, C++, C и Go;
4. каррирование;
5. рекурсивный обход бинарного дерева;
6. рекурсия с кэшированием / memoization;
7. чистые функции и немутабельный стиль.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Элементы функционального программирования`
- RAG chunk range: `p0233:c01` … `p0243:c01`
- Included chunks: **11**
- PDF page range: **233–243**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - TOC starts the chapter at page 233;
  - page 243 contains the chapter source list;
  - page 244 starts `Скоростные и другие сравнения языков`.

## Main principle

Глава строится вокруг функций как данных:

```text
function value
    ↓
pass / return / store
    ↓
higher-order function
    ↓
closure with state
    ↓
currying / recursion / memoization
    ↓
pure-function style
```

Источник использует comparative approach: один и тот же accumulating transform реализуется на C, GCC nested functions, C++ functor/lambda, Go closure и Python.

## Core examples

### Closure

```go
func makeAdder(x int) func(int) int {
    return func(y int) int {
        return x + y
    }
}
```

### Higher-order transform

```go
func my_transform(in []int, xform func(int) int) (out []int)
```

### Currying-style construction

```go
func mkAdd(a int) func(int) int
```

### Recursive tree traversal

```go
func (n *Node) Traverse(f func(int))
```

### Memoization

```go
func Memoize(mf Memoized) Memoized
```

### Pure-style value transformation

```go
func (p Point) Add(q Point) Point
```

## Operational boundary

State-changing local actions:

- `make` creates several C/C++/Go binaries;
- `go build curry1.go` creates a binary;
- `go fmt btree.go` and `go fmt nomut.go` rewrite source formatting.

Compile-run:

- `go run clos1.go`;
- `go run btree.go`;
- `go run nomut.go`.

Workload:

- closure comparison binaries;
- Fibonacci recursive/memoized examples.

No system configuration changes are evidenced by this chapter.

## Conditional artifacts

- explicit chapter-end summary: **not present**
- review questions/exercises: **not present**
- source findings: **present**

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
