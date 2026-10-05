# Шпаргалка: процессы и ресурсы по главе 8

## Symptom / problem framing

Типовые симптомы:

- система «тормозит»;
- один process потребляет много CPU;
- неизвестно, кто держит file;
- command падает из-за file/library/system-call problem;
- высокая memory pressure / swap activity;
- непонятно, какой process создаёт I/O;
- нужно понять cgroup membership или group resource limit.

## Baseline / context

Основные ресурсы главы:

```text
CPU
memory
I/O devices
kernel services / scheduling
```

Не начинать с tuning. Сначала определить измеряемый ресурс и подтвердить bottleneck.

## Read-only checks

### Processes

```bash
ps
top
top -p PID
ps m
ps m -o pid,tid,command
```

### Open files

```bash
lsof
lsof +D /usr
lsof -p PID
```

### Execution tracing

```bash
strace cat /dev/null
strace -o trace -ff command
ltrace command
```

### CPU / memory

```bash
time command
/usr/bin/time command
uptime
getconf PAGE_SIZE
ps -o pid,min_flt,maj_flt PID
vmstat 2
```

### I/O

```bash
iostat
iostat 2
iostat -d 2
iostat -p ALL
iotop
pidstat -p PID 1
```

### cgroups

```bash
cat /proc/self/cgroup
cat cgroup.controllers
cat pids.current
cat memory.max
cat cpu.stat
```

## Interpretation

### top / ps

`ps` — snapshot.  
`top` — continuously updated process view.

Useful `top` keys from source:
- `P` — current CPU;
- `M` — memory;
- `T` — cumulative CPU;
- `u` — one user;
- `f` — displayed fields;
- Space — immediate refresh.

### lsof

Use it to map:

`process ↔ file descriptor ↔ file/device/object`.

Filtering by PID or directory usually reduces noise.

### strace vs ltrace

`strace` → system calls and kernel return values.  
`ltrace` → shared-library calls.

Example diagnostic signal:
`openat(...) = -1 ENOENT` → requested file was not found.

### Threads

A thread has TID and is scheduled by the kernel similarly to a process, but threads in one process share resources.

`ps m -o pid,tid,command` separates process PID from thread TID.

### CPU time

- user — CPU time in user code;
- system — CPU time spent in kernel on behalf of process;
- real — elapsed wall-clock time, including waits.

### Nice / priority

Nice range in source: -20 to 20.

Higher nice → lower scheduling priority.

Negative nice for high priority is possible for superuser, but source advises against casual use.

### Load average

Interpret relative to available CPU cores. High load alone is not sufficient evidence of a performance problem.

### Memory / page faults

Minor fault → page is already in memory, mapping needs resolution.  
Major fault → page must be loaded from slower storage/source.

Many major faults can materially degrade performance.

### vmstat

In interval mode:
- first data row = average since boot;
- later rows = current intervals.

Useful groups:
- procs;
- memory;
- swap;
- io;
- system;
- cpu.

Watch `si/so` for active swapping and blocked processes when diagnosing memory pressure.

### iostat / iotop / pidstat

`iostat` → per-device throughput/transfer metrics.  
`iotop` → active I/O by thread/process context.  
`pidstat` → repeated per-process measurements in stream form; source notes `-r` for memory and `-d` for disk.

### cgroups v1 vs v2

v1:
- hierarchy per controller;
- process can appear in different cgroups for different controllers.

v2:
- process belongs to one cgroup;
- multiple controllers may be enabled for that group.

Further chapter discussion focuses on v2.

## Next action

1. Identify resource: CPU / memory / I/O / file / syscall / cgroup.
2. Capture read-only baseline.
3. Narrow to process or thread.
4. If process state is insufficient, use tracing.
5. If system-wide, use vmstat/iostat.
6. If grouped services/resources matter, inspect cgroup state.
7. Change priority/limit only after the bottleneck is confirmed.

## Modifying action

Source-confirmed state changes include:

```bash
renice 20 PID
echo PID > cgroup.procs
echo 3000 > pids.max
```

The chapter also describes creating/removing cgroup directories and enabling child controllers through `cgroup.subtree_control`, but exact end-to-end rollback workflow is not defined.

## Verification / acceptance checks

| Change | Verification |
|---|---|
| renice | confirm expected priority/nice in process view |
| cgroup membership | re-read process/cgroup membership |
| pids.max | re-read `pids.max` and observe intended group behavior |
| controller/accounting state | re-read controller files such as `cpu.stat`, `memory.max`, `pids.current` |

## Rollback

- `renice`: previous nice value must be known; otherwise `[Needs confirmation]`.
- cgroup membership: previous cgroup path must be known; otherwise `[Needs confirmation]`.
- cgroup limits/controller hierarchy: restore prior pseudo-file values/configuration only from a verified baseline; otherwise `[Needs confirmation]`.
