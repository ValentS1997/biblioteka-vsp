# Глава 6. Параллелизм и многопроцессорность

Статус: **RAG_GROUNDED**

## Scope

Глава последовательно сравнивает несколько моделей параллельного выполнения и затем переходит к Go concurrency:

1. процессы и `fork()`;
2. POSIX threads (`pthread_t`);
3. `std::thread` в C++;
4. goroutines и M:N scheduling;
5. channels, buffered/unbuffered communication, `close`, `select`;
6. closures в goroutines;
7. `sync`: Mutex, Cond, RWMutex, Once, Pool, WaitGroup;
8. `sync/atomic`;
9. различие конкурентности и параллельности;
10. `GOMAXPROCS`, `runtime.NumCPU()` и два SMP-примера.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Параллелизм и многопроцессорность`
- RAG chunk range: `p0147:c01` … `p0173:c01`
- Included chunks: **27**
- PDF page range: **147–173**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 147 starts with `Параллелизм и многопроцессорность`;
  - pages 172–173 contain the chapter source list;
  - page 174 starts `Масштабирование`.

## Main principle

Источник проводит одну сквозную мысль: параллельные ветви не имеют гарантированного порядка выполнения, а shared state и обмен результатами требуют явной синхронизации.

Модели эволюционируют так:

```text
process + isolated address space
        ↓
kernel threads + shared process memory
        ↓
Go goroutines scheduled M:N
        ↓
channels / sync primitives
        ↓
actual SMP parallelism depends on scheduler + workload
```

## Core lessons

- `fork()` даёт изолированные адресные пространства; взаимодействие требует IPC.
- pthread/std::thread разделяют память процесса, поэтому синхронизация становится обязательной.
- порядок старта/завершения параллельных ветвей недетерминирован;
- goroutine запускается выражением `go`; вызывающая функция не ждёт её автоматически;
- channel используется и для передачи данных, и как механизм синхронизации;
- `select` ожидает несколько channel operations;
- `sync` предоставляет низкоуровневые примитивы, но источник предпочитает high-level communication через channels там, где это уместно;
- конкурентность и фактический SMP-параллелизм рассматриваются как разные понятия;
- больше goroutines/OS threads/CPU не означает автоматического ускорения.

## Benchmark interpretation

Примеры `smp1` и `smp2` намеренно показывают, что synchronization overhead может доминировать над полезной работой.

Источник сравнивает:

- atomic increment + WaitGroup;
- channel-based serialization + WaitGroup.

Результаты относятся только к конкретным примерам и окружению автора. Абсолютные времена не являются универсальным benchmark.

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
