# Глава 12. Скоростные и другие сравнения языков

Статус: **RAG_GROUNDED**

## Scope

Глава сравнивает эквивалентные вычислительные задачи на C, C++ и Go с разными компиляторами и подчёркивает ограничения таких сравнений.

Основные блоки:

1. методика хронометража и повторяемость измерений;
2. рекурсивные числа Фибоначчи;
3. пузырьковая сортировка;
4. Ханойская башня;
5. решето Эратосфена;
6. сравнение GCC, Clang, gccgo и GoLang gc;
7. влияние структуры кода и уровня оптимизации на результат.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Скоростные и другие сравнения языков`
- RAG chunk range: `p0244:c01` … `p0257:c01`
- Included chunks: **14**
- PDF page range: **244–257**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - TOC starts the chapter at page 244;
  - page 257 ends the sieve comparison;
  - page 258 starts separate chapter `Многопроцессорные параллельные вычисления`.

## Main principle

Источник сам предупреждает: performance comparison зависит от algorithm class, source structure, compiler, optimization level, host load, cache state and measurement method.

Поэтому chapter workflow:

```text
same problem
    ↓
equivalent-ish implementations
    ↓
same input size
    ↓
same correctness signal
    ↓
repeat timings
    ↓
compare orders / broad differences
    ↓
do not generalize one result to a language as a whole
```

## Test matrix

### Fibonacci

- C via GCC
- C++ via GCC
- C++ via Clang
- Go via gccgo
- Go via GoLang gc

All variants intentionally use inefficient recursive calculation.

### Bubble sort

Worst-case descending input; result is swap count.

Important: source explicitly admits that the C++ variant using `vector<long long>` and iterators is not a fair apples-to-apples comparison with direct array/slice indexing.

### Tower of Hanoi

Recursive workload with operation count as correctness signal.

### Sieve of Eratosthenes

Array/slice scanning workload; result is count of prime numbers.

## Benchmark discipline extracted from source

- use input size large enough to avoid sub-millisecond noise;
- repeat runs;
- do not trust first run in a series;
- preserve identical input and correctness result;
- record compiler and optimization level;
- compare elapsed time only after semantic equivalence is checked;
- do not compare results across tasks that used different optimization policies as one unified benchmark.

## Operational boundary

Read-only:

- `gcc --version`
- `clang --version`
- `go version`
- `ls -l`
- `file`
- `ldd`

State-changing:

- `sudo apt install clang`
- `make`
- compiler/build commands creating binaries

Workload / measurement:

- `time ...`
- local benchmark binaries

Priority-affecting:

- `nice -9` changes scheduling priority for the launched command; source assumes privilege for negative nice values.

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
