# Mermaid — глава 8 «Процессы и использование ресурсов»

Источник: **RAG `p0244:c01`–`p0269:c01`**, PDF/печатные страницы 244–269. Диаграммы синтезированы из текста главы; исходные рисунки 8.1–8.2 не реконструируются.

## 1. Диагностический выбор инструмента

```mermaid
flowchart TD
  S["Симптом: slow / busy / blocked"] --> Q{"Что наблюдаем?"}
  Q -->|Process activity| TOP["top / pidstat"]
  Q -->|Open resource| LSOF["lsof"]
  Q -->|Immediate failure| STR["strace / ltrace"]
  Q -->|Memory pressure| MEM["free / page faults / vmstat"]
  Q -->|Disk I/O| IO["iostat / iotop"]
  Q -->|Resource policy| CG["cgroup files/controllers"]
  TOP --> C["Correlate over time"]
  LSOF --> C
  STR --> C
  MEM --> C
  IO --> C
  CG --> C
  C --> A{"Evidence sufficient?"}
  A -->|No| MORE["Narrow scope / collect another interval"]
  A -->|Yes| ACT["Only then consider controlled change"]
```

Глава прямо отговаривает от настройки производительности без измеренного bottleneck.

## 2. Process / thread model

```mermaid
flowchart TD
  P["Process PID"] --> MAIN["Main thread TID = PID"]
  P --> T2["Additional thread TID"]
  P --> T3["Additional thread TID"]
  P --> SHARED["Shared memory / files / I/O resources"]
  MAIN --> CPU["Kernel scheduler"]
  T2 --> CPU
  T3 --> CPU
```

Потоки внутри процесса разделяют ресурсы, но kernel schedules threads as runnable entities (§8.4).

## 3. CPU time and load

```mermaid
flowchart LR
  CMD["Command execution"] --> U["user time"]
  CMD --> S["system time"]
  CMD --> W["waiting / elapsed remainder"]
  U --> REAL["real elapsed time"]
  S --> REAL
  W --> REAL
  RUN["Runnable processes"] --> LOAD["load average: 1 / 5 / 15 min"]
  CORES["CPU/core count"] --> LOAD
```

`time` и load average измеряют разные аспекты работы; high load сам по себе не доказывает проблему (§8.5.1–8.5.3).

## 4. Demand paging and memory pressure

```mermaid
flowchart TD
  PROC["Process accesses virtual page"] --> PRESENT{"Page ready in main memory?"}
  PRESENT -->|Yes, mapping known| RUN["Continue"]
  PRESENT -->|Yes, MMU mapping missing| MIN["Minor page fault"]
  MIN --> MAP["Kernel updates mapping"]
  MAP --> RUN
  PRESENT -->|No| MAJ["Major page fault"]
  MAJ --> READ["Load from disk / slower storage"]
  READ --> RUN
  PRESS["Memory pressure"] --> SWAP["Swap-out / swap-in"]
  SWAP --> BLOCK["More blocked work + I/O"]
  BLOCK --> SLOW["System slowdown"]
```

The source treats some major faults as normal cold-start behavior and warns against diagnosing from free-memory number alone.

## 5. vmstat correlation

```mermaid
flowchart LR
  V["vmstat interval"] --> P["procs: r / b"]
  V --> M["memory: free / buff / cache"]
  V --> SW["swap: si / so"]
  V --> IO["I/O: bi / bo"]
  V --> SYS["system: in / cs"]
  V --> CPU["CPU: us / sy / id / wa"]
  SW --> COR["Correlate, not one-column diagnosis"]
  IO --> COR
  CPU --> COR
  P --> COR
  M --> COR
```

The chapter uses `vmstat` to correlate memory pressure, blocked processes, swap and disk activity (§8.5.5).

## 6. I/O localization

```mermaid
flowchart TD
  WHOLE["vmstat: aggregate I/O"] --> DEV["iostat: device / partition"]
  DEV --> PROC["iotop: active thread/process I/O"]
  PROC --> HIST["pidstat -d: time series by process"]
  HIST --> TARGET["Target workload identified"]
```

Device totals and partition totals need not sum exactly because the whole disk can be accessed directly (§8.5.6).

## 7. cgroup v1 vs v2

```mermaid
flowchart LR
  V1["cgroups v1"] --> V1CPU["CPU hierarchy"]
  V1 --> V1MEM["Memory hierarchy"]
  V1 --> V1OTHER["Other controller hierarchies"]
  PROC1["One process"] --> V1CPU
  PROC1 --> V1MEM
  V2["cgroups v2"] --> ONE["Single cgroup hierarchy"]
  PROC2["One process"] --> ONE
  ONE --> CTRL["Multiple controllers can be enabled"]
```

The chapter then focuses on v2 because v1 is being phased out (§8.6.1).

## 8. cgroup v2 control flow

```mermaid
flowchart TD
  PROC["Process"] --> PATH["/proc/<pid>/cgroup"]
  PATH --> DIR["cgroup directory under /sys/fs/cgroup"]
  DIR --> PROCS["cgroup.procs / cgroup.threads"]
  DIR --> CONT["cgroup.controllers"]
  CONT --> PID["pids.current / pids.max"]
  CONT --> MEM["memory.current / memory.max / memory.stat"]
  CONT --> CPU["cpu.stat"]
  CHANGE["Write membership / limit / subtree controls"] --> DIR
  DIR --> VERIFY["Read back membership + counters + limits"]
```

Writes to cgroup interface files are live state changes; exact controller names/paths must be confirmed from the target host.

## 9. Monitoring-before-tuning boundary

```mermaid
flowchart TD
  BASE["Baseline: process + system metrics"] --> LOC["Localize resource bottleneck"]
  LOC --> HYP["Form narrow hypothesis"]
  HYP --> CHANGE{"Need scheduler/cgroup change?"}
  CHANGE -->|No| OBS["Continue observation"]
  CHANGE -->|Yes| SNAP["Capture current priority/group/limit"]
  SNAP --> APPLY["Apply one controlled change"]
  APPLY --> RE["Repeat same measurement"]
  RE --> OK{"Improved without new contention?"}
  OK -->|Yes| KEEP["Keep"]
  OK -->|No| RB["Restore prior state if known; otherwise [Needs confirmation]"]
```

This final flow is an operational synthesis of the chapter's “measure before tuning” guidance.
