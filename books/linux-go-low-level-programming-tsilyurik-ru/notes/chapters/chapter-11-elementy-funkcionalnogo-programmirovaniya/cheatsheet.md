# Cheatsheet — глава 11 «Элементы функционального программирования»

## Goal

Использовать функции как значения и явно управлять состоянием, зависимостями и побочными эффектами.

## 1. First-class / higher-order functions

Source framing:

- функцию можно передать аргументом;
- вернуть как результат;
- присвоить переменной;
- использовать как functional value.

Пример:

```go
func my_transform(in []int, xform func(int) int) (out []int) {
    out = make([]int, len(in))
    for idx, val := range in {
        out[idx] = xform(val)
    }
    return
}
```

## 2. Closure

```go
func makeAdder(x int) func(int) int {
    return func(y int) int {
        return x + y
    }
}
```

```go
add5 := makeAdder(5)
add10 := makeAdder(10)
```

Verification:

```bash
go run clos1.go
```

Expected source output:

```text
7 12
```

Важно: source wording about context being “frozen at definition” is broader than these examples. См. `source-findings.md`.

## 3. Same stateful transform across languages

Target result:

```text
8 14 21 26 29 29 38
```

Variants:

- C: `static int total`;
- GCC C: nested function capturing outer local;
- C++: functor;
- C++11: lambda capture;
- Go: anonymous function referencing `total`;
- Python: nested function/global state in shown comparison.

The engineering point is not syntax parity but explicit representation of hidden/stateful accumulation.

## 4. Currying

Source definition:

```text
func(a,b,c) → func(a)(b)(c)
```

Go example:

```go
func mkAdd(a int) func(int) int {
    return func(b int) int {
        return a + b
    }
}
```

Verification:

```bash
go build curry1.go
./curry1
```

Expected:

```text
7 9
```

## 5. Recursive tree traversal

```go
func (n *Node) Traverse(f func(int)) {
    if n == nil {
        return
    }
    n.left.Traverse(f)
    f(n.value)
    n.right.Traverse(f)
}
```

Source result:

```text
[1 2 3 4 5 6]
```

This combines:

- recursion;
- nil termination;
- function callback;
- append into caller-owned slice.

## 6. Memoized recursion

Type:

```go
type Memoized func(int) int
```

Cache:

```go
cache := make(map[int]int)
```

Pattern:

```go
if val, found := cache[key]; found {
    return val
}
temp := mf(key)
cache[key] = temp
return temp
```

Source comparison shows naive Fibonacci time growing rapidly while cached version remains much lower for the tested inputs.

Important interpretation:

```text
speedup comes from algorithm/data reuse,
not from parallelism
```

Exact timings are environment-specific.

## 7. Pure-function style

Source example:

```go
func (p Point) Add(q Point) Point {
    return Point{p.x + q.x, p.y + q.y}
}
```

Chaining:

```go
r := p.Add(p).Add(q).Add(p)
```

Source emphasis: input/intermediate Point values are not modified by the method; a result value is returned.

## Verification discipline

For functional examples verify:

1. same input;
2. same result sequence;
3. where state lives;
4. whether state is shared or local to closure;
5. whether callback mutates external state;
6. whether memoization cache lifetime matches intended scope;
7. timing only after correctness is confirmed.

## Next action

Следующая глава — `Скоростные и другие сравнения языков`.
