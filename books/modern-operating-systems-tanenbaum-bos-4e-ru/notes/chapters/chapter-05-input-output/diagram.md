# Chapter 5 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Application I/O request"] --> B["User I/O library / spooler"]
    B --> C["Device-independent I/O layer"]
    C --> D["Device driver"]
    D --> E{"Transfer method"}
    E --> E1["Programmed I/O / polling"]
    E --> E2["Interrupt-driven I/O"]
    E --> E3["DMA"]
    E1 --> F["Controller registers / buffer"]
    E2 --> F
    E3 --> F
    F --> G["Physical device"]

    G --> H{"Completion / error"}
    H -->|interrupt| I["Interrupt handler"]
    H -->|DMA completion| I
    H -->|recoverable error| D
    H -->|unrecoverable| C
    I --> D
    D --> C
    C --> B
    B --> A

    C --> J["Buffering"]
    J --> J1["kernel buffer"]
    J --> J2["double buffer"]
    J --> J3["ring buffer"]

    G --> K["Disk path"]
    K --> K1["FCFS / SSF / elevator"]
    K --> K2["RAID"]
    K --> K3["bad-sector handling"]
    K --> K4["stable storage"]

    I --> L["Clock/timer path"]
    L --> L1["time of day"]
    L --> L2["process quantum"]
    L --> L3["alarms/watchdogs"]
    L --> L4["profiling"]

    B --> M["Terminal / GUI"]
    M --> M1["canonical / noncanonical input"]
    M --> M2["ANSI escape output"]
    M --> M3["X events / Windows messages"]

    C --> P["Power management"]
    P --> P1["device sleep"]
    P --> P2["CPU voltage/frequency"]
    P --> P3["application quality trade-off"]
```

## Diagnostic boundary

```text
application semantics
    ≠ buffering/spooling
    ≠ device-independent policy
    ≠ driver logic
    ≠ interrupt/DMA transport
    ≠ controller/bus
    ≠ physical device/media
```
