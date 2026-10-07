# Mermaid — глава 2 «Организация компьютерных систем»

Источник: RAG `p0076:c01`–`p0171:c01`.

## 1. System organization

```mermaid
flowchart LR
  CPU["CPU"] <--> BUS["Interconnect / bus"]
  MEM["Main memory"] <--> BUS
  CTL["I/O controller"] <--> BUS
  CTL <--> DEV["I/O device"]
```

## 2. Fetch–decode–execute

```mermaid
flowchart TD
  F["Fetch instruction"] --> PC["Advance PC"]
  PC --> D["Decode"]
  D --> A{"Memory operand?"}
  A -->|yes| L["Locate / load operand"]
  A -->|no| E["Execute"]
  L --> E
  E --> F
```

## 3. Pipeline

```mermaid
flowchart LR
  S1["Fetch"] --> S2["Decode"] --> S3["Get operands"] --> S4["Execute"] --> S5["Write back"]
```

Different instructions may occupy different stages simultaneously.

## 4. Processor-level parallelism

```mermaid
flowchart TD
  P["Parallel processing"] --> SIMD["SIMD / data parallel"]
  P --> VECTOR["Vector processor"]
  P --> MP["Multiprocessor: shared memory"]
  P --> MC["Multicomputer: private memory + messages"]
```

## 5. Memory hierarchy

```mermaid
flowchart TD
  R["Registers"] --> C["Cache"]
  C --> M["Main memory"]
  M --> SSD["SSD / magnetic disk"]
  SSD --> ARCH["Tape / optical archive"]
```

## 6. Cache path

```mermaid
flowchart LR
  CPU2["CPU request"] --> CACHE{"Cache hit?"}
  CACHE -->|yes| HIT["Return data"]
  CACHE -->|no| RAM["Read main memory"]
  RAM --> FILL["Fill cache line"]
  FILL --> HIT
```

## 7. Disk latency

```mermaid
flowchart LR
  REQ["Disk request"] --> SEEK["Seek track"]
  SEEK --> ROT["Wait for sector"]
  ROT --> XFER["Transfer data"]
```

## 8. RAID trade-off

```mermaid
flowchart TD
  RAID["RAID layouts"] --> R0["0: striping / no redundancy"]
  RAID --> R1["1: mirroring"]
  RAID --> R23["2/3: error/parity"]
  RAID --> R4["4: dedicated parity"]
  RAID --> R5["5: distributed parity"]
```

## 9. DMA + interrupt

```mermaid
sequenceDiagram
  participant CPU
  participant C as Controller
  participant D as Device
  participant M as Memory
  CPU->>C: start I/O
  C->>D: device command
  D-->>C: data stream
  C->>M: DMA transfer
  C-->>CPU: interrupt
```

## 10. Shared bus versus PCIe

```mermaid
flowchart LR
  subgraph Shared["Shared-bus model"]
    C1["CPU"] --- B["PCI-style shared bus"]
    D1["Device A"] --- B
    D2["Device B"] --- B
  end
  subgraph Switched["PCIe model"]
    RC["Root complex"] --> SW["Switch"]
    SW --> E1["Endpoint A"]
    SW --> E2["Endpoint B"]
  end
```

## 11. Display bandwidth

```mermaid
flowchart LR
  RES["resolution"] --> BW["bandwidth"]
  BPP["bytes / pixel"] --> BW
  FPS["frames / second"] --> BW
  BW --> VRAM["video-memory traffic"]
```
