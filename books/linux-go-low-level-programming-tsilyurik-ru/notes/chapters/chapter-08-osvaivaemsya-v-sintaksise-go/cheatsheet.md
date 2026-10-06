# Cheatsheet — глава 8 «Осваиваемся в синтаксисе Go»

## Goal

Закрепить синтаксис Go на небольших законченных программах и одновременно увидеть типовые области применения: CLI, вычисления, данные, сеть.

## 1. CLI / flag

Источник показывает:

```go
var omitNewLine = flag.Bool("n", false, "не печатать знак новой строки")
flag.Parse()
flag.NArg()
flag.Arg(i)
```

Проверка:

```bash
./echo повторяет то что я пишу
./echo -n 12345
./echo -z 12345
./echo 12345 -n
./echo -h
./echo --help
```

Source claim: options in this example must precede positional arguments.

## 2. Newton sqrt

Один и тот же алгоритм реализован на C и Go.

Go function returns:

```go
func sqrt(x float64) (float64, int)
```

Сравнение binaries:

```bash
./sqrt_c 10
./sqrt_cl 10
./sqrt_go 10
./sqrt_gc 10
```

Acceptance in source example: все варианты сходятся за одинаковое число итераций и дают близкие numeric results.

## 3. Arbitrary precision

### Integer π

`math/big` используется для целочисленной арифметики произвольной разрядности.

Проверка:

```bash
./pi.py 80
go run pi.go 80
```

Источник показывает совпадающую последовательность digits для двух implementations.

### High-precision float

Следующий пример вычисляет `sqrt(2)` через `big.Float`.

Проверка:

```bash
./newton
```

## 4. Streaming statistics

Идея:

```text
mean = sum(x) / N
variance = sum(x²) / N - mean²
```

Это позволяет получить mean/variance за один проход без хранения всей последовательности.

Build:

```bash
make
```

Run:

```bash
time ./sko 100000000
time ./skoc 100000000
```

Важно: источник сам предупреждает, что разница времени может быть обусловлена разными random generators, а не языком как таковым.

## 5. 2D polygon

Источник использует:

- `complex128` для точки 2D;
- методы для `point` / `shape`;
- `math/cmplx`;
- stdin parsing;
- perimeter and area calculations.

Build/run:

```bash
go build -o triangle triangle.go
./triangle
```

Input validation examples включают неверное число координат и ошибки `strconv.ParseFloat`.

## 6. TCP echo

Sequential server:

```bash
go build -o echo_serv echo_serv.go
./echo_serv
```

Test clients:

```bash
nc 127.0.0.1 51500
socat tcp4:127.0.0.1:51500 STDOUT
telnet 127.0.0.1 51500
```

Go client:

```bash
go build -o echo_cli echo_cli.go
./echo_cli
```

## 7. Concurrent TCP server

Minimal change:

```go
go func(cn net.Conn) {
    defer func() { cn.Close() }()
    // echo loop
}(conn)
```

Build:

```bash
go build -o echo_servm echo_servm.go
```

Clients connect concurrently to port `51501`.

## 8. HTTP server

Source example implements `http.Handler`:

```go
type Hello struct{}

func (h Hello) ServeHTTP(
    w http.ResponseWriter,
    r *http.Request) {
    fmt.Fprint(w, "Hello!")
}
```

Runtime:

```bash
./http
```

Endpoint shown by source:

```text
http://localhost:4000/
```

## 9. map iteration

Source experiment:

```bash
./map4rand
./map4rand
```

Observed order differs between iterations/runs.

Operational rule extracted from source:

> do not make program correctness depend on map iteration order.

Exact historical/runtime wording remains version-scoped; see `source-findings.md`.

## Acceptance pattern

For each example:

1. build succeeds;
2. expected binary exists;
3. input/output behavior matches example intent;
4. for network code, server is actually listening before client test;
5. for comparative timing, workload and implementation differences are recorded before interpreting performance.
