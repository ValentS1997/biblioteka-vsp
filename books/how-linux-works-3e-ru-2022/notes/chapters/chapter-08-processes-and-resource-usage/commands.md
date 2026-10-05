# Команды и интерфейсы главы 8

Только элементы, явно подтверждённые RAG главы 8.

| Команда / интерфейс | Назначение | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|---|
| `ps` | Snapshot процессов | read-only | Не меняет state | Нет | Сопоставить PID/state | N/A |
| `top` | Интерактивный process/resource view | read-only/workload-generating | Обновляет display | Небольшой monitoring overhead | Найти active process/resource | N/A |
| `top -p PID` | Следить за конкретным process | read-only | Не меняет state | Нет | Проверить selected PID | N/A |
| `lsof` | Open files/processes | read-only | Не меняет state | Большой output | Фильтровать по object/PID | N/A |
| `lsof +D /usr` | Open files under directory tree | read-only | Traversal/search | Может быть медленным на большом tree | Проверить matching rows | N/A |
| `lsof -p PID` | Files конкретного process | read-only | Не меняет state | Нет | Сопоставить FD/object | N/A |
| `strace command` | System-call trace | workload-generating | Запускает command under tracer | Timing/output меняются; verbose | Читать syscalls/return codes | N/A |
| `strace -o FILE -ff command` | Trace child processes to files | workload-generating | Создаёт trace files | Disk/output volume | Проверить generated per-PID traces | Удаление trace files вне scope главы |
| `ltrace command` | Shared-library call trace | workload-generating | Запускает command under tracer | Не работает со static binaries | Сопоставить library calls | N/A |
| `ps m` | Показать threads | read-only | Не меняет state | Нет | Отличить process/thread rows | N/A |
| `ps m -o pid,tid,command` | PID/TID mapping | read-only | Не меняет state | Нет | Проверить TID list | N/A |
| `time command` | User/system/real time | read-only/workload-generating | Измеряет command run | Shell builtin может давать меньше stats | Сравнить three time values | N/A |
| `/usr/bin/time command` | Расширенная process resource statistics | read-only/workload-generating | Измеряет command run | Нет state change | Читать faults/swaps/etc. | N/A |
| `ps -l` | Process priority view | read-only | Не меняет state | Нет | Проверить priority/nice | N/A |
| `renice 20 PID` | Изменить nice process | state-changing | Меняет scheduling priority | Может ухудшить/изменить scheduling behavior | Проверить NI/PR | Вернуть previous nice, если baseline известен |
| `uptime` | Load averages | read-only | Не меняет state | Нет | Интерпретировать относительно CPU count | N/A |
| `getconf PAGE_SIZE` | Page size | read-only | Не меняет state | Нет | Проверить output | N/A |
| `ps -o pid,min_flt,maj_flt PID` | Page-fault counters | read-only | Не меняет state | Counters cumulative | Сравнить MINFL/MAJFL | N/A |
| `vmstat 2` | CPU/memory/swap/I/O summary | read-only/workload-generating | Periodic output | Первая строка — since-boot average | Читать subsequent rows | N/A |
| `iostat` | CPU + device I/O summary | read-only | Не меняет state | First report cumulative-like context | Сопоставить device metrics | N/A |
| `iostat 2` | Periodic iostat | read-only/workload-generating | Periodic output | Нет state change | Сравнить intervals | N/A |
| `iostat -d 2` | Device-only periodic I/O | read-only/workload-generating | Periodic output | Нет | Проверить device activity | N/A |
| `iostat -p ALL` | Include partitions | read-only | Больше output | Output volume | Найти target partition/device | N/A |
| `iotop` | Per-thread/process I/O activity | read-only/workload-generating | Interactive monitoring | Может требовать elevated access | Найти active TID/process | N/A |
| `pidstat -p PID 1` | Per-process periodic stats | read-only/workload-generating | Periodic text output | Нет state change | Сравнить intervals | N/A |
| `pidstat -r` | Memory monitoring | read-only/workload-generating | Periodic process memory stats | Нет | Сопоставить process | N/A |
| `pidstat -d` | Disk monitoring | read-only/workload-generating | Periodic process disk stats | Нет | Сопоставить process | N/A |
| `cat /proc/self/cgroup` | Current process cgroup membership | read-only | Не меняет state | v1/v2 format differs | Определить hierarchy/version | N/A |
| `cat cgroup.controllers` | Enabled/available controllers file | read-only | Не меняет state | Context depends on current cgroup | Проверить list | N/A |
| `cat pids.current` | Current thread/process count in group | read-only | Не меняет state | Нет | Проверить value | N/A |
| `cat memory.max` | Memory limit | read-only | Не меняет state | Hierarchical parent may impose lower bound | Проверить value/parent context | N/A |
| `cat cpu.stat` | Accumulated CPU accounting | read-only | Не меняет state | Cumulative counter | Compare over time | N/A |
| `echo PID > cgroup.procs` | Move process into cgroup | state-changing | Changes cgroup membership | Resource policy may change immediately | Re-read membership | Restore previous group only if known |
| `echo 3000 > pids.max` | Set PID limit | state-changing | Changes process/thread limit | Can prevent new tasks | Re-read `pids.max`/behavior | Restore previous value only if known |

## top hotkeys from source

- Space — refresh;
- `M` — sort current memory usage;
- `T` — cumulative CPU;
- `P` — current CPU;
- `u` — one user;
- `f` — choose fields;
- `?` — help.

Hotkeys are case-sensitive.

## cgroup v2 interface notes

Typical mount: `/sys/fs/cgroup`.

Important pseudo-files named in source:
- `cgroup.procs`;
- `cgroup.threads`;
- `cgroup.controllers`;
- `cgroup.subtree_control`;
- `pids.current`;
- `pids.max`;
- `memory.max`;
- `memory.current`;
- `memory.stat`;
- `cpu.stat`.

## Safety notes

1. Не менять nice только из-за высокого load average.
2. Отрицательный nice источник не рекомендует использовать casually.
3. Не вводить cgroup limits без baseline: они могут немедленно изменить scheduling/resource availability.
4. Для rollback cgroup state требуется знать previous membership/values; иначе `[Needs confirmation]`.
