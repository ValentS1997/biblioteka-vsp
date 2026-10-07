# Cheatsheet — глава 8 «Процессы и использование ресурсов»

**Источник:** `how-linux-works-brian-ward-3e-ru-2022:p0244:c01`–`p0269:c01`, PDF/печатные страницы 244–269. Только `rag_only`.

## Symptom / problem framing

Глава помогает ответить на четыре вопроса:

1. какой процесс/поток потребляет CPU, memory или I/O;
2. какой файл/ресурс держит процесс;
3. какой системный вызов или библиотечный вызов приводит к ошибке/ожиданию;
4. ограничивает ли cgroup ресурсы процесса/службы.

Источник прямо предупреждает: сначала измерение и интерпретация, а не «оптимизация ради оптимизации».

## Baseline / context

| Область | Базовая модель главы | PDF |
|---|---|---:|
| Processes | `ps` — snapshot, `top` — обновляемое состояние | 244–245 |
| Open files | `lsof` связывает PID с files/sockets/libs/pipes | 245–247 |
| Tracing | `strace` → syscalls; `ltrace` → shared-library calls | 247–249 |
| Threads | TID, shared process resources, kernel schedules threads | 250–251 |
| CPU | user/system/real time, nice, load average | 252–255 |
| Memory | demand paging, minor/major faults, swap/cache | 255–260 |
| I/O | `iostat`, `iotop`, device/process views | 260–262 |
| History | `pidstat` samples per-process CPU/memory/disk | 262–263 |
| cgroups | v1/v2 hierarchy, controllers, interface files | 263–268 |

## Read-only checks

```sh
top
lsof
lsof -p pid
lsof -h
strace cat /dev/null
ltrace command
ps m
ps m -o pid,tid,command
top -p pid
time ls
ps -l
uptime
free
cat /proc/meminfo
getconf PAGE_SIZE
/usr/bin/time cal
ps -o pid,min_flt,maj_flt pid
vmstat 2
vmstat -d
iostat
iostat 2
iostat -d 2
iostat -p ALL
iotop
pidstat -p pid 1
pidstat -r -p pid 1
pidstat -d -p pid 1
cat /proc/self/cgroup
cat cgroup.controllers
cat cgroup.procs
cat cgroup.threads
cat pids.current
cat memory.max
cat cpu.stat
cat memory.current
cat memory.stat
```

Дополнительно:
- `lsof +D /usr` — read-only, но рекурсивный обход может быть тяжёлым.
- `strace`, `ltrace`, `iotop`, `top`, `vmstat`, `iostat`, `pidstat` — наблюдение с runtime overhead/output.
- В `top`: `M`, `T`, `P`, `u`, `f`, `H`, пробел и `?` — интерактивные controls из главы.

## Interpretation

| Наблюдение | Интерпретация по источнику | Что ещё проверить |
|---|---|---|
| High CPU in `top` | Process активно получает CPU time | Is this expected workload? user/sys split? |
| High load average | Много runnable work | CPU count, responsiveness, memory pressure |
| `real` ≫ `user+sys` | Process spends time waiting on system/external resources | I/O/network/external wait [Needs confirmation] |
| Major page faults grow | Pages must be fetched from disk/slow storage | Memory pressure vs normal cold-start |
| `vmstat so` grows | Kernel is swapping pages out | Free/cache/buffers, blocked processes, I/O |
| `vmstat b` grows | Processes blocked waiting for resources | Correlate with si/so, bi/bo, wa |
| High `wa` | CPU time waiting for I/O | Device/process I/O with iostat/iotop |
| `iostat` busy device | Device-level I/O activity | Which process? use iotop/pidstat |
| `lsof -p pid` shows target file | Process holds that file/resource | Exact FD/type and intended behavior |
| `strace` returns `ENOENT` | Program tried to open a missing path | Whether path should exist |
| cgroup `memory.max=max` | No explicit memory limit at that cgroup level | Parent cgroup may still constrain it |
| cgroup v1 entries + v2 entry | Hybrid layout | Which controller/version owns target resource |

## Next action

1. Define scope: process, thread, whole system, device, or cgroup.
2. Capture time-series evidence rather than relying on one snapshot.
3. Correlate CPU, memory/page faults and I/O before changing priorities.
4. If a program fails immediately, inspect open paths/system calls rather than guessing.
5. Before changing cgroups, determine v1/v2, exact group path, parent limits and active controllers.
6. Unknown workload intent or target cgroup → **[Needs confirmation]**.

## Modifying action

| Action from chapter | Effect | Risk |
|---|---|---|
| `renice 20 pid` | Increases nice value; process receives lower CPU scheduling preference | Can slow important workload; negative nice as root may starve others |
| `ionice` | Can inspect/change I/O priority | Exact source syntax not provided; change behavior [Needs confirmation] |
| Write PID to `cgroup.procs` | Moves process into a cgroup | Live resource policy changes immediately |
| Write value to `pids.max` | Limits total PIDs in group | New processes/threads may fail once limit reached |
| Configure `cgroup.subtree_control` | Enables controllers for child cgroups | Hierarchy-wide behavior; source token ambiguity recorded |
| Create cgroup directory | Creates cgroup interface via cgroup filesystem | Must obey hierarchy/controller rules |
| `rmdir` empty cgroup | Removes empty cgroup | Only safe when no processes/required hierarchy remain |

## Verification / acceptance checks

| Change | Source-grounded verification | Acceptance |
|---|---|---|
| renice | `top` / `ps -l` | NI/priority reflects intended change; workload remains healthy |
| I/O priority | `iotop` displays PRIO | Expected class/priority visible |
| Process moved to cgroup | `cat /proc/<pid>/cgroup`, target `cgroup.procs` | PID appears in intended hierarchy |
| PID limit | `cat pids.current`, target limit file | Current count below intended limit; no unexpected failures |
| Memory accounting | `memory.current`, `memory.stat` | Usage readable and consistent with target group |
| CPU accounting | `cpu.stat` | Usage counters increase for group workload |
| Performance diagnosis | Repeat same monitor after any change | Symptom improves without new contention |

## Rollback

- **Read-only monitoring/tracing:** [Not applicable], apart from stopping interactive/continuous tools.
- `renice`: previous nice value must be captured before change; exact inverse command is not prescribed in chapter → **[Needs confirmation]**.
- `ionice`: prior class/priority must be captured; rollback syntax not supplied → **[Needs confirmation]**.
- cgroup membership/limits: source does not provide a generic transactional rollback workflow. Record original cgroup path and controller values before modification; otherwise **[Needs confirmation]**.
- cgroup deletion is only discussed for empty groups; restoring a removed hierarchy/configuration is **[Needs confirmation]**.

## Guardrails

- High load is not automatically a fault.
- Free RAM alone is not enough to diagnose memory pressure.
- Major faults are not automatically pathological; cold-start faults are expected.
- Avoid tuning scheduler/cgroup controls until the measured bottleneck is identified.
- Current PID, device, cgroup path, controller set and acceptable resource threshold remain **[Needs confirmation]** on any real host.
