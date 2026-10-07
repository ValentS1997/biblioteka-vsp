# Глава 2 — Процессы и потоки

Status: `RAG_GROUNDED`

Book: `modern-operating-systems-tanenbaum-bos-4e-ru`  
Edition: 4  
Chapter: 2 — «Процессы и потоки»

## Scope and provenance

- Source mode: `rag_only`
- Canonical source format: PDF
- Canonical source SHA-256: `57b4906fe976351be3cc7ba692bdcee069036667b5f1d042517aea04d37a3bbd`
- PDF source locator range: `111–213`
- Addressable RAG chunk range: `p0111:c01 … p0213:c01`
- Chunks in chapter range: `103`
- Printed-page range: `[Needs confirmation]`
- Boundary verification:
  - PDF page 111 begins with `Глава 2. Процессы и потоки`;
  - PDF page 214 begins with `Глава 3. Управление памятью`.
- Chapter boundary: `VERIFIED`

The chapter-end summary is present on PDF page 205. Review questions/exercises are present on PDF pages 205–213.

## Main principle

Chapter 2 separates two related abstractions:

1. **Process** — resource container and protected execution context with its own address space and OS-maintained process state.
2. **Thread** — schedulable execution stream inside a process; threads have separate execution state/stacks but share the process address space and resources.

Once multiple processes or threads interact, correctness depends on synchronization: races must be excluded in critical sections, blocking and wakeup must not lose events, and scheduling must balance fairness, throughput, latency and deadlines.

## Chapter map

| Section | Topic | PDF pages |
|---|---|---:|
| 2.1 | Processes | 111–123 |
| 2.1.1 | Process model | 112–114 |
| 2.1.2 | Process creation | 114–116 |
| 2.1.3 | Process termination | 116–117 |
| 2.1.4 | Process hierarchies | 117–118 |
| 2.1.5 | Process states | 118–120 |
| 2.1.6 | Process implementation / process table | 120–122 |
| 2.1.7 | Multiprogramming model | 122–123 |
| 2.2 | Threads | 123–146 |
| 2.2.1–2.2.3 | Uses, classical model, POSIX threads | 124–135 |
| 2.2.4–2.2.9 | User/kernel/hybrid threads, scheduler activations, pop-up threads, conversion issues | 135–146 |
| 2.3 | Interprocess communication and synchronization | 146–178 |
| 2.3.1–2.3.4 | Races, critical sections, busy waiting, sleep/wakeup | 147–158 |
| 2.3.5–2.3.10 | Semaphores, mutexes, monitors, messages, barriers, RCU | 158–178 |
| 2.4 | Scheduling | 178–198 |
| 2.4.1 | Scheduling goals and categories | 179–186 |
| 2.4.2 | Batch scheduling | 186–188 |
| 2.4.3 | Interactive scheduling | 188–195 |
| 2.4.4 | Real-time scheduling | 195–196 |
| 2.4.5 | Policy and mechanism | 196–197 |
| 2.4.6 | Thread scheduling | 197–198 |
| 2.5 | Classical IPC problems | 198–203 |
| 2.5.1 | Dining philosophers | 199–202 |
| 2.5.2 | Readers and writers | 202–203 |
| 2.6 | Research on processes and threads | 203–205 |
| 2.7 | Short conclusions | 205 |
| — | Review questions / exercises | 205–213 |

Section/page mapping is derived from the RAG table of contents on PDF pages 7–8.

## Key concepts

- **Pseudo-parallelism:** on one CPU, rapid context switching creates the model of multiple concurrent processes.
- **Process states:** running, ready, blocked.
- **Process table:** stores saved registers, program counter, scheduling state, IDs, signal/accounting data, memory pointers and file-related state.
- **Threads:** share process resources/address space while retaining per-thread program counter, registers and stack.
- **User-level threads:** cheap and flexible but a blocking kernel operation/page fault can block the whole process and there is no per-thread timer preemption unless extra machinery is added.
- **Kernel threads:** kernel knows and schedules each thread; blocking one thread need not block the others.
- **Race condition:** final result depends on execution interleaving while shared data are read/written.
- **Critical section:** code touching shared state; mutual exclusion is necessary but must also preserve progress and bounded waiting.
- Synchronization mechanisms introduced: Peterson, TSL/XCHG, sleep/wakeup, semaphores, mutexes, condition variables, monitors, message passing, barriers and RCU.
- **Scheduling:** different environments optimize different goals—batch throughput/turnaround, interactive response, or real-time deadlines/predictability.
- Scheduling algorithms include FCFS, shortest job first, shortest remaining time, round-robin, priority, multilevel queues, aging-based prediction, guaranteed, lottery and fair-share scheduling.
- Policy can be separated from scheduling mechanism so user-space components supply priorities/parameters while the kernel executes the mechanism.

## Practical interpretation

Operationally, distinguish four different causes of “a task is not progressing”:

`blocked on event/resource` ≠ `ready but not scheduled` ≠ `spinning on a lock` ≠ `deadlocked/starved`.

For concurrency incidents, identify the shared state and synchronization primitive before changing scheduling or priorities.

## Artifacts

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md)
- [review-questions.md](review-questions.md)
- [review-answers.md](review-answers.md)
- [source-findings.md](source-findings.md)

## Limitations

- Figures are referenced by extracted RAG text but are not independently encoded as multimodal RAG objects.
- Some figure-label text on PDF page 178 is mojibake in the extracted text layer.
- One Pthreads code sample on PDF page 135 contains extraction artifacts in string quoting.
- Environment-dependent experiment results remain `[Needs confirmation]`.
