# Глава 7. Масштабирование

Статус: **RAG_GROUNDED**

## Scope

Глава сводит предыдущие темы CPU topology, goroutine scheduling, `GOMAXPROCS` и affinity в один практический вопрос: как один и тот же Go-код ведёт себя на системах с резко различающимся числом и производительностью процессоров.

Основные блоки:

1. рабочая модель scheduler Go и `GOMAXPROCS`;
2. испытательный стенд: Raspberry Pi, Orange Pi, desktop, multi-socket server;
3. первая экспериментальная программа `mlpar`;
4. ограничение первой методики из-за вызовов времени внутри worker loop;
5. второй эксперимент `mlpar2` с вычислительной active wait и калибровкой;
6. распределение goroutines по OS threads;
7. масштабирование при `N <= P` и `N > P`;
8. управление числом execution threads через `runtime.GOMAXPROCS` и shell variable;
9. ограничение CPU set средствами Linux `taskset`.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Масштабирование`
- RAG chunk range: `p0174:c01` … `p0195:c01`
- Included chunks: **22**
- PDF page range: **174–195**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 174 starts with `Масштабирование`;
  - page 195 contains the chapter source list;
  - page 196 starts `Часть 3. Некоторые примеры и сравнения`.

## Definition used by the source

В рамках главы масштабирование — способность программного кода переноситься между архитектурами разной производительности и эффективно использовать доступные ресурсы, прежде всего распределять вычислительную нагрузку между доступными processors.

## Main experimental model

```text
same Go workload
      ↓
different hardware
SBC → desktop → server
      ↓
vary goroutine count N
      ↓
observe available CPUs P
      ↓
observe runtime worker/thread behavior
      ↓
measure T(N)
      ↓
repeat with GOMAXPROCS / taskset constraints
```

## Main conclusions supported by the chapter

- число goroutines может существенно превышать число доступных CPU;
- при CPU-bound workload производительность определяется не только количеством goroutines, но и числом CPU, scheduler behavior и interference ОС;
- распределение goroutines по runtime/OS threads наблюдается экспериментально, а не выводится только из теории;
- первый benchmark может оказаться методологически некорректным из-за скрытых blocking/syscall points;
- изменение `GOMAXPROCS` и Linux affinity позволяет независимо исследовать runtime-level и OS-level ограничения;
- больше параллельных ветвей не означает линейное ускорение.

## Safety / operational boundary

Read-only diagnostics:

- `inxi`, `free`, `lsb_release`, `uname`, `go version`;
- `nproc`, `/proc/cpuinfo`, `lscpu`;
- `taskset -p PID`.

State-changing or environment-changing actions:

- `go build` creates/replaces binaries;
- `export GOMAXPROCS=...` changes current shell environment;
- `taskset -c ... command` constrains CPU affinity of a launched workload.

Before using `taskset` on a real workload, CPU topology must be verified first; the chapter itself relies on earlier topology analysis.

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
