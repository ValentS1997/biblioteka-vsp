# Commands — глава 6 «Параллелизм и многопроцессорность»

Только shell-команды, явно подтверждённые chapter RAG.

| Команда | Класс | Назначение | Effect / risk | Verification |
|---|---|---|---|---|
| `./forks 3` | workload | Запустить fork example | Создаёт child processes | наблюдать PID/order |
| `g++ -O3 threads.cc -lpthread -o threads` | state-changing | Собрать pthread example | Создаёт binary | `./threads 3` |
| `./threads 3` | workload | Запустить pthread example | Создаёт kernel threads | наблюдать порядок |
| `./threads+ 6` | workload | Запустить std::thread example | Создаёт kernel threads | наблюдать порядок |
| `make parm` | state-changing | Собрать goroutine example | Makefile вызывает gccgo и go build | запустить `./parm` |
| `./parm` | workload | Проверить goroutine parameters | Выполняет binary | output examples |
| `make sleep` | state-changing | Собрать channel/goroutine example | Создаёт binaries | `./sleep` |
| `./sleep` | workload | Запустить channel example | Long-running/temporary workload | sequence output |
| `./result` | workload | Проверить goroutine result synchronization | Выполняет binary | transformed array output |
| `./buffer` | workload | Проверить buffered channel | Выполняет binary | `1\n2` |
| `./close` | workload | Проверить close/range | Выполняет binary | Fibonacci sequence |
| `./select` | workload | Проверить select/channel flow | Выполняет binary | sequence + `quit` |
| `./unblock` | workload | Проверить select default + timers | Выполняет timed workload | tick/BOOM output |
| `./closure1` | workload | Source closure capture example | Version-sensitive behavior | source shows repeated final value |
| `./closure2` | workload | Closure arg binding example | Executes goroutines | source shows a/b/c |
| `./closure3` | workload | Per-iteration binding example | Executes goroutines | source shows a/b/c |
| `./once` | workload | Проверить sync.Once | Executes goroutines | one output line |
| `./smp2` | workload | Channel synchronization benchmark | CPU/scheduler workload | result count + duration |
| `./smp2 2` | workload | 2 execution threads in example | CPU/sync workload | count + duration |
| `./smp2 3` | workload | 3 execution threads in example | CPU/sync workload | count may reflect integer division | count + duration |
| `./smp2 4` | workload | 4 execution threads in example | CPU/sync workload | count + duration |
| `./smp2 100` | workload | Many goroutines/execution limit example | CPU/sync workload | count + duration |
| `./smp1` | workload | Atomic synchronization benchmark | CPU workload | count + duration |

## Makefile behavior shown by source

For Go examples, chapter shows:

```make
%: %.go
        gccgo -g $< -o $@
        go build -o $@.gl -compiler gc $<
```

Therefore `make parm` / `make sleep` are state-changing build actions.

## Safety boundary

These examples intentionally exercise parallel processes, threads and goroutines.

Before scaling parameters:

- confirm host load;
- do not infer deterministic execution order;
- avoid running stress-like variants on production systems;
- verify result counts, not only elapsed time.

## Timing caveat from source

The chapter explicitly warns that timings in a multitasking OS can vary substantially. Its own recommendation is to interpret coarse order-of-magnitude differences rather than treat one sample as precise benchmarking evidence.
