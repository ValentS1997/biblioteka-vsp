# Команды и интерфейсы — глава 8 «Процессы и использование ресурсов»

**Provenance:** `p0244:c01`–`p0269:c01`, PDF/печатные страницы 244–269. Только явно поддержанные chapter RAG команды/интерфейсы.

Классы: **RO** — read-only observation; **WG** — workload-generating / continuous / tracing; **SC** — state-changing.

## 1. Processes and open resources

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `top` | WG/RO | Live process/resource display | 245 |
| `lsof` | RO | Open files/resources and owning processes | 245–247 |
| `lsof +D /usr` | WG/RO | Recursively list open files under example directory | 247 |
| `lsof -p pid` | RO | Open files for selected PID | 247 |
| `lsof -h` | RO | Short option help | 247 |

`top` hotkeys explicitly described: Space refresh; `M` memory sort; `T` cumulative CPU; `P` current CPU; `u` user filter; `f` choose fields; `?` help; `H` thread display (§8.1, §8.4.2).

## 2. Tracing

| Команда | Класс | Назначение | Boundary |
|---|---|---|---|
| `strace cat /dev/null` | WG/RO trace | Launch and trace system calls of source example | Executes target program |
| `strace cat not_a_file` | WG/RO trace | Demonstrate failed `openat` / `ENOENT` | Executes target program |
| `strace -o crummyd_strace -ff crummyd` | WG/RO trace | Trace example daemon/children into files | Potentially large output; exact example preserved |
| `ltrace` | WG/RO trace | Trace shared-library calls | Does not work for statically linked binaries per source |

`strace -o save_file` and shell redirection `2> save_file` are described for saving trace/stderr. Exact target command and output path are environment-specific.

## 3. Threads and CPU

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `ps m` | RO | Show processes with threads | 250–251 |
| `ps m -o pid,tid,command` | RO | PID/TID view | 251 |
| `top -p pid1 [-p pid2 ...]` | WG/RO | Track selected process(es) over time | 252 |
| `time ls` | WG/RO measurement | user/system/real time for example command | 252 |
| `ps -l` | RO | Includes process priority information | 253 |
| `uptime` | RO | Kernel uptime and 1/5/15-minute load averages | 254 |
| `renice 20 pid` | SC | Raise nice value, reducing CPU preference | 254 |

The source says negative nice values as superuser can deprive system processes of CPU; it advises against doing so.

## 4. Memory and page faults

| Команда / path | Класс | Назначение | PDF |
|---|---|---|---:|
| `free` | RO | Whole-system memory state | 255 |
| `/proc/meminfo` | RO interface | Memory/cache/buffer details | 255 |
| `getconf PAGE_SIZE` | RO | System page size | 256 |
| `/usr/bin/time cal > /dev/null` | WG/RO | Example showing major/minor page faults | 257 |
| `ps -o pid,min_flt,maj_flt 20365` | RO | Per-process minor/major page faults | 258 |
| `vmstat 2` | WG/RO | Whole-system CPU/memory/swap/I/O every 2 s | 258–260 |
| `vmstat -d` | RO/WG | Detailed per-disk statistics | 260 |

The first `vmstat` data line is described as lifetime average; the chapter recommends starting interpretation with the following interval line.

## 5. I/O and per-process history

| Команда | Класс | Назначение | PDF |
|---|---|---|---:|
| `iostat` | RO | Lifetime CPU and device I/O statistics | 260–261 |
| `iostat 2` | WG/RO | Repeated report every 2 s | 261 |
| `iostat -d 2` | WG/RO | Device-only repeated report | 261 |
| `iostat -p ALL` | RO | Include partitions | 261 |
| `iotop` | WG/RO | Live per-thread I/O display | 261–262 |
| `pidstat -p 1329 1` | WG/RO | Per-process CPU history every second | 262–263 |
| `pidstat -r` | WG/RO | Memory-related process statistics | 263 |
| `pidstat -d` | WG/RO | Disk-related process statistics | 263 |
| `ionice` | RO or SC depending use | Source says it can inspect/change I/O priority | 262 |

Exact `ionice` invocation is **not supplied** in the retrieved chapter, so no executable syntax is invented.

## 6. cgroups — read-only interfaces

| Команда / file | Класс | Meaning | PDF |
|---|---|---|---:|
| `cat /proc/self/cgroup` | RO | v1/v2 membership for current shell | 264–266 |
| `/sys/fs/cgroup` | RO/interface | Usual cgroup2 filesystem mount | 266 |
| `/sys/fs/cgroup/unified` | RO/interface | Source says it may be used with mixed v1/v2 | 266 |
| `cat cgroup.procs` | RO | Processes in current cgroup | 266 |
| `cat cgroup.threads` | RO | Threads in current cgroup | 266 |
| `cat cgroup.controllers` | RO | Controllers available/active in described group context | 267 |
| `cat pids.current` | RO | Current number of processes/threads counted by pids controller context | 267 |
| `cat memory.max` | RO | Memory maximum; `max` means no explicit limit at this level | 267 |
| `cat cpu.stat` | RO | Accumulated CPU usage | 268 |
| `memory.current`, `memory.stat` | RO interfaces | Current and accumulated memory information | 268 |

## 7. cgroups — state-changing

| Source action | Класс | Effect | Verification | Rollback |
|---|---|---|---|---|
| `echo pid > cgroup.procs` | SC live kernel state | Move PID into current cgroup | `/proc/<pid>/cgroup`, `cgroup.procs` | Original cgroup must be recorded; generic rollback [Needs confirmation] |
| `echo 3000 > pids.max` | SC resource limit | Limit process count for group | `pids.current`, read target limit | Prior value must be recorded; rollback [Needs confirmation] |
| Create subdirectory in cgroup tree | SC live hierarchy | Kernel creates cgroup interface files | Inspect hierarchy/interface | Exact creation command not supplied |
| `rmdir` empty cgroup | SC live hierarchy | Remove empty group even with interface files | Group absent, processes unaffected | Recreate/configure path: [Needs confirmation] |
| Write controllers to `cgroup.subtree_control` | SC hierarchy policy | Enable controllers for child groups | Read controller files/hierarchy | Prior value required; source token ambiguity applies |

The source says to write **`+cpu +pid`** for child CPU/PID controllers on p268, while the rest of the chapter names the controller **`pids`** and files `pids.current`/`pids.max`. This mismatch is not silently corrected; see `source-findings.md`.

## 8. Additional tools named in §8.7

- `sar` — historical/continuous system activity reporting.
- `acct` — process accounting.
- quota tooling — limiting user disk usage.

No executable command forms for these are supplied in this chapter, so they are recorded as tools/topics only.

## Command discipline

- PIDs, device names, cgroup paths, controller sets and acceptable thresholds are **[Needs confirmation]**.
- Observation precedes scheduling/resource-control changes.
- Do not add external command syntax to fill chapter gaps.
- Source examples are preserved as examples, not production commands.
