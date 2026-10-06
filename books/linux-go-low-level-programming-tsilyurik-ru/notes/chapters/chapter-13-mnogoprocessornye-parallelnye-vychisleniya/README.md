# Глава 13. Многопроцессорные параллельные вычисления

Статус: **RAG_GROUNDED**

## Scope

Глава сводит практические аспекты многопроцессорного Go-кода в одну последовательность: стоимость запуска параллельных ветвей, гонки, диагностика, синхронизация, масштабирование CPU-bound задачи, каналы, timers/tickers и случай, когда параллелизм делает программу медленнее.

Основные блоки:

1. сравнение стоимости активации `fork()`, `pthread_t` и goroutines;
2. Linux resource limits для процессов/threads;
3. data race на общем counter;
4. Go race detector;
5. защита shared state через `sync/atomic`, `sync.Mutex` и channel-based patterns;
6. toy local MD5 brute-force как scaling example;
7. цепочка goroutines через channels;
8. timers и tickers;
9. Basel-series experiment как контрпример механического распараллеливания;
10. итоговые выводы о synchronization overhead.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Многопроцессорные параллельные вычисления`
- RAG chunk range: `p0258:c01` … `p0279:c01`
- Included chunks: **22**
- PDF page range: **258–279**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - TOC starts the chapter at page 258;
  - page 279 contains `Выводы` and chapter sources;
  - page 280 starts `Заключение`.

## Main principle

Сквозная мысль главы:

```text
parallelism
    ↓
shared state / coordination
    ↓
synchronization
    ↓
overhead + contention
    ↓
speedup only when useful work dominates coordination cost
```

Параллелизм оценивается не по числу goroutines, а по:

- correctness;
- synchronization cost;
- contention;
- useful work per critical section;
- actual elapsed time.

## Experimental progression

### Activation cost

Source compares:

```text
fork()
pthread_create()
goroutines
```

and observes much lower activation cost for goroutines in the shown environment.

### Race

Unsynchronized `counter++` gives nondeterministic under-counting.

### Diagnostics

```bash
go build -race race.go
```

Source shows race detector output pointing to conflicting accesses.

### Synchronization

The chapter then compares:

- atomic increment;
- mutex-protected critical section;
- channel-based synchronization analogy.

Correctness improves, but elapsed time increases.

### Scaling example

A toy local MD5 search is used only as a CPU-parallelism demonstration. The artifact preserves it as a source example and does not generalize it to real credential attacks.

### Counterexample: Basel series

The source's parallel version creates many goroutines doing extremely small units of work while serializing accumulation through a mutex.

Observed result: synchronization overhead dominates and the parallel version is much slower than the sequential implementation.

## Operational boundary

Read-only:

- `ulimit -u`, `ulimit -i`, `ulimit -s`;
- `cat /proc/sys/kernel/threads-max`;
- `ls -l race`.

State-changing local:

- `make`;
- `go build`;
- `go build -race`.

High-risk host/session tuning:

- changing `ulimit` values;
- writing `/proc/sys/kernel/threads-max`.

These controls affect resource/scheduler boundaries and must not be copied casually to production/shared systems.

CPU-intensive workloads:

- large goroutine activation tests;
- race/synchronization benchmarks;
- Basel-series experiments;
- toy local brute-force example.

## Conditional artifacts

- explicit chapter-end summary: **present**
- review questions/exercises: **not present**
- source findings: **present**

## Artifacts

- [summary.md](./summary.md)
- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
