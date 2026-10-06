# Cheatsheet — глава 12 «Скоростные и другие сравнения языков»

## Goal

Сравнивать не «языки вообще», а конкретные реализации одной задачи при известных условиях.

## Baseline

Зафиксировать:

```bash
gcc --version
clang --version
go version
```

При необходимости проверить binary format/linkage:

```bash
file <binary>
ldd <binary>
```

## Measurement pattern

Source template:

```bash
time <command> <size>
```

Optional source variant:

```bash
time nice -9 <command> <size>
```

Перед использованием negative nice:

- понимать, что это меняет process priority;
- source assumes privilege/root;
- не применять как нейтральный read-only measurement.

## Fibonacci

Build source shows:

```text
GCC C
GCC C++
Clang C++
gccgo Go
GoLang gc Go
```

Correctness signal for input `42`:

```text
433494437
```

Interpretation:

- all implementations use the same intentionally inefficient recursive structure;
- source timings are host/version-specific;
- binary size/linkage differs significantly between gccgo and gc examples.

## Bubble sort

Worst-case descending sequence.

Debug mode:

```bash
./sort_go -20
```

Expected high-level result:

- input descending;
- swap count `190`;
- output ascending.

Performance run:

```bash
time ./sort_* 20000
```

Correctness signal:

```text
199990000
```

Critical caveat: the C++ version uses STL `vector` and iterators while other variants use more direct indexing. Source explicitly calls the comparison unfair.

## Tower of Hanoi

Debug:

```bash
./hanoy_c -3
```

Correctness signal:

```text
7 moves
```

Performance source input:

```bash
time ./hanoy_* 30
```

Correctness signal:

```text
1073741823 moves
```

## Sieve of Eratosthenes

Source input:

```bash
time ./erastof_* 50000000
```

Correctness signal:

```text
3001134 primes
```

Source uses `-O3` here, unlike earlier `-O0` Fibonacci/sort comparisons.

## Interpretation rules

Do:

1. verify result first;
2. compare same algorithm and same size;
3. record compiler/version;
4. record optimization level;
5. repeat runs;
6. compare broad order-of-magnitude trends.

Do not:

- generalize one microbenchmark to a language;
- compare binaries built with different semantics and call the result a pure compiler test;
- merge `-O0` and `-O3` experiments into one ranking;
- trust a single timing sample.

## Source anomalies

- `type data_t int 64` in Go bubble-sort listing;
- missing semicolon after C sieve `printf(...)`;
- complexity wording on page 244;
- optimization policy varies across subsections.

See `source-findings.md`.

## Next action

Next chapter: `Многопроцессорные параллельные вычисления`.
