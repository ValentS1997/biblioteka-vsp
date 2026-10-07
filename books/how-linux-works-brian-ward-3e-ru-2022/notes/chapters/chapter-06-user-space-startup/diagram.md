# Mermaid — глава 6 «Запуск пользовательского пространства»

Источник: `p0176:c01`–`p0207:c01`, PDF/печатные страницы 176–207. Диаграммы реконструируют только текстово подтверждённые связи; рис. 6.1–6.3 не копируются.

## 1. Переход kernel → user space

```mermaid
flowchart TD
  K["Kernel ready"] --> INIT["PID 1 / init"]
  INIT --> LOW["Low-level services: udevd, logging"]
  LOW --> NET["Network configuration"]
  NET --> MID["Middle/high-level services"]
  MID --> LOGIN["Login prompts / GUI / applications"]
```

Глава начинает именно с этой последовательности (§6 intro).

## 2. systemd boot graph

```mermaid
flowchart TD
  DEF["default.target"] --> T1["target units"]
  DEF --> S1["service units"]
  DEF --> M1["mount units"]
  DEF --> SO1["socket units"]
  T1 --> S2["other services"]
  S1 --> R["dependencies"]
  M1 --> R
  SO1 --> R
  R --> READY["Units activate when ready"]
```

Зависимости формируют **граф**, а не простое дерево; systemd не обязана запускать всё строго последовательно (§6.3.1–6.3.2).

## 3. Dependency semantics

```mermaid
flowchart LR
  U["Current unit"] --> REQ["Requires: activate + failure propagates"]
  U --> WAN["Wants: activate, but failure does not propagate"]
  U --> REQ2["Requisite: dependency must already be active"]
  U --> CON["Conflicts: cannot remain active together"]
  U --> ORD["Before / After: ordering only"]
  U --> COND["Condition*: OS state checks"]
```

Dependency **strength** and **ordering** are separate concepts (§6.3.6).

## 4. Service readiness / tracking

```mermaid
flowchart TD
  START["systemd starts service"] --> TYPE{"Type="}
  TYPE --> SIMPLE["simple: main process stays"]
  TYPE --> FORK["forking: parent exits"]
  TYPE --> NOTIFY["notify: service signals readiness"]
  TYPE --> DBUS["dbus: registration signals readiness"]
  TYPE --> ONE["oneshot: process completes"]
  TYPE --> IDLE["idle: wait for active jobs to finish"]
  SIMPLE --> CG["Processes tracked in cgroup"]
  FORK --> CG
  NOTIFY --> CG
  DBUS --> CG
  ONE --> CG
  IDLE --> CG
```

§6.3.5 explains that cgroups give systemd a reliable process hierarchy.

## 5. Socket/resource activation

```mermaid
flowchart TD
  R["Resource unit: socket/path/device"] --> MON["systemd monitors resource"]
  MON --> ACCESS["Client accesses resource"]
  ACCESS --> BUF["Input is held/buffered"]
  BUF --> ACT["systemd activates service unit"]
  ACT --> READY["Service becomes ready"]
  READY --> HAND["Service takes over resource"]
```

The echo.socket / echo@.service example shows one concrete socket-activation path (§6.3.7).

## 6. Safe unit-change workflow

```mermaid
flowchart TD
  OBS["status / list-jobs / journal / UnitPath"] --> LOC["Identify effective unit and dependencies"]
  LOC --> CFG{"Need config change?"}
  CFG -->|No| RUN["Runtime action only"]
  CFG -->|Yes| ETC["Place local definition under /etc/systemd/system"]
  ETC --> RELOAD["daemon-reload / reload as appropriate"]
  RUN --> ACTION["start / stop / restart"]
  RELOAD --> ACTION
  ACTION --> VERIFY["status + jobs + journal"]
  VERIFY --> OK{"Acceptance?"}
  OK -->|Yes| KEEP["Keep"]
  OK -->|No| RB["Restore prior state/config; [Needs confirmation] if not captured"]
```

This is an operational synthesis of the chapter's rules and commands, not a universal service-management procedure.

## 7. System V init model

```mermaid
flowchart TD
  INITTAB["/etc/inittab"] --> RL["Runlevel N"]
  RL --> RC["/etc/rcN.d"]
  RC --> S["Sxx links → init.d script start"]
  RC --> K["Kxx links → init.d script stop"]
  S --> SERVICE["Service process"]
  K --> SERVICE
  TEL["telinit"] --> RL
```

System V startup is sequential and link-order driven (§6.4–6.5.4). systemd can wrap legacy scripts for compatibility (§6.5.5).

## 8. Ordered shutdown

```mermaid
flowchart TD
  SH["shutdown"] --> TERM["Ask processes to exit"]
  TERM --> KILL["TERM, then KILL if needed"]
  KILL --> UM["Unmount filesystems"]
  UM --> RO["Remount root read-only"]
  RO --> SYNC["sync buffered data"]
  SYNC --> REBOOT["Kernel reboot(2): halt/reboot"]
```

§6.6 explicitly warns against power/reset during orderly shutdown.

## 9. initramfs handoff

```mermaid
flowchart TD
  BL["Bootloader"] --> K["Kernel"]
  BL --> IR["initramfs archive in memory"]
  K --> RAM["Temporary RAM filesystem mounted as /"]
  RAM --> EINIT["Early init / udev / tools"]
  EINIT --> MOD["Load storage/root drivers/modules"]
  MOD --> REAL["Mount real root filesystem"]
  REAL --> SWITCH["Switch to real root"]
  SWITCH --> INIT["Run full init / systemd"]
```

The purpose is to solve the chicken-and-egg problem where drivers needed for the real root filesystem are themselves stored as files (§6.7).
