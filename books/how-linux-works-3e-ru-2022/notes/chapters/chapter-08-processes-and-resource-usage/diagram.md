# Диаграмма: процессы и ресурсы по главе 8

## Resource troubleshooting

~~~mermaid
flowchart TD
    S["System/process symptom"] --> R{"Which resource?"}
    R --> CPU["CPU"]
    R --> MEM["Memory"]
    R --> IO["I/O"]
    R --> FILE["Open file/object"]
    R --> CALL["System/library call"]
    CPU --> TOP["ps / top / time / uptime"]
    MEM --> VM["page faults / vmstat / pidstat"]
    IO --> IOS["iostat / iotop / pidstat"]
    FILE --> LSOF["lsof"]
    CALL --> TRACE["strace / ltrace"]
    TOP --> CG["cgroup context"]
    VM --> CG
    IOS --> CG
~~~

## Process / thread

~~~mermaid
flowchart LR
    P["Process PID"] --> T1["Main thread TID"]
    P --> T2["Thread TID"]
    P --> T3["Thread TID"]
    P --> RES["Shared process resources"]
    T1 --> CPU["Kernel scheduler"]
    T2 --> CPU
    T3 --> CPU
~~~

## Memory and page faults

~~~mermaid
flowchart TD
    PROC["Process virtual address"] --> MMU["MMU + page table"]
    MMU --> Q{"Page ready?"}
    Q -->|Yes| RAM["Physical memory"]
    Q -->|Minor fault| MAP["Kernel fixes mapping"]
    MAP --> RAM
    Q -->|Major fault| LOAD["Load page from slower storage/source"]
    LOAD --> RAM
~~~

## cgroups v1 vs v2

~~~mermaid
flowchart LR
    subgraph V1["cgroups v1"]
      P1["Process"] --> C1["CPU cgroup"]
      P1 --> M1["Memory cgroup"]
    end

    subgraph V2["cgroups v2"]
      P2["Process"] --> G["One cgroup"]
      G --> C2["CPU controller"]
      G --> M2["Memory controller"]
      G --> PIDS["PIDs controller"]
    end
~~~

## cgroup v2 filesystem

~~~mermaid
flowchart TD
    PROC["/proc/PID/cgroup"] --> PATH["cgroup path"]
    PATH --> DIR["/sys/fs/cgroup/..."]
    DIR --> MEMBERS["cgroup.procs"]
    DIR --> CTRLS["cgroup.controllers"]
    DIR --> PIDS["pids.current / pids.max"]
    DIR --> MEM["memory.current / memory.max"]
    DIR --> CPU["cpu.stat"]
~~~
