# Mermaid — глава 3 «Цифровой логический уровень»

Источник: RAG `p0172:c01`–`p0269:c01`.

## 1. From Boolean function to system interface

```mermaid
flowchart TD
  F["Boolean function"] --> G["Gates"]
  G --> C["Combinational blocks"]
  C --> S["State elements"]
  S --> M["Registers / memory"]
  M --> B["Bus interface"]
  B --> SYS["CPU • memory • I/O system"]
```

## 2. Combinational versus stateful

```mermaid
flowchart LR
  IN["Current inputs"] --> COMB["Combinational circuit"]
  COMB --> OUT["Current output"]
  IN --> STATE["Latch / flip-flop"]
  OLD["Stored state"] --> STATE
  STATE --> NEW["Output + new state"]
```

## 3. Adder hierarchy

```mermaid
flowchart LR
  HA["Half adder"] --> FA["Full adder"]
  FA --> RIP["Ripple-carry word adder"]
  RIP --> FAST["Carry-select / faster carry strategy"]
```

## 4. Memory organization

```mermaid
flowchart TD
  ADDR["Address lines"] --> DEC["Decoder / word select"]
  DEC --> CELL["Selected word cells"]
  DATA["Shared data lines"] <--> CELL
  CTRL["CS • RD • OE"] --> CELL
```

## 5. Stateful timing

```mermaid
flowchart LR
  CLK["Clock"] --> L["Latch: level-sensitive"]
  CLK --> F["Flip-flop: edge-sensitive"]
  F --> REG["Register"]
  REG --> MEM["Memory structures"]
```

## 6. Synchronous bus

```mermaid
sequenceDiagram
  participant CPU as Master
  participant MEM as Slave
  CPU->>MEM: address + MREQ + RD
  MEM-->>CPU: WAIT if not ready
  MEM-->>CPU: data
  CPU->>CPU: sample on defined clock edge
```

## 7. Asynchronous full handshake

```mermaid
sequenceDiagram
  participant M as Master
  participant S as Slave
  M->>S: address/control + MSYN
  S-->>M: data + SSYN
  M->>S: drop MSYN
  S-->>M: drop SSYN
```

## 8. Bus arbitration

```mermaid
flowchart TD
  R1["Master A request"] --> A["Arbitration"]
  R2["Master B request"] --> A
  R3["DMA / I/O request"] --> A
  A --> G["One current bus owner"]
```

## 9. FPGA

```mermaid
flowchart LR
  HDL["Hardware description"] --> SYN["Synthesis"]
  SYN --> LUT["LUTs"]
  SYN --> ROUTE["Programmable interconnect"]
  LUT --> FPGA["Configured FPGA circuit"]
  ROUTE --> FPGA
```

## 10. PCI versus PCIe

```mermaid
flowchart LR
  PCI["PCI: shared parallel bus"] --> PRESS["bandwidth / skew / scaling pressure"]
  PRESS --> PCIE["PCIe: switch + point-to-point serial lanes"]
  PCIE --> STACK["physical → data link → transaction → software"]
```

## 11. Address decoding

```mermaid
flowchart TD
  A["CPU address"] --> FULL["Full decode"]
  A --> PART["Partial decode"]
  FULL --> ONE["Unique intended device/range"]
  PART --> ALIAS["Aliases / repeated mappings"]
```
