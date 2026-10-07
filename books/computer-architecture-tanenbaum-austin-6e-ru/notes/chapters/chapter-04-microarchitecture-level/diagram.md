# Mermaid — глава 4 «Уровень микроархитектуры»

Источник: RAG `p0270:c01`–`p0376:c01`.

## 1. ISA to datapath

```mermaid
flowchart TD
  ISA["IJVM opcode"] --> DEC["decode / microcode dispatch"]
  DEC --> MI["microinstruction"]
  MI --> SRC["select register source"]
  SRC --> ALU["ALU / shifter"]
  ALU --> WB["C bus / write-back"]
  WB --> NEXT["next microinstruction"]
```

## 2. Mic-1 datapath

```mermaid
flowchart LR
  H["H register"] --> A["ALU input A"]
  BREG["selected register"] --> B["B bus / ALU input B"]
  A --> ALU["ALU"]
  B --> ALU
  ALU --> SHIFT["shifter"]
  SHIFT --> C["C bus"]
  C --> REGS["one or more registers"]
```

## 3. Memory paths

```mermaid
flowchart TD
  PC["PC"] --> MBR["MBR: byte fetch"]
  MAR["MAR"] --> MDR["MDR: word read/write"]
  MBR --> CTRL["microcode / operand bytes"]
  MDR --> DATA["stack / local data"]
```

## 4. Mic-1 → Mic-4

```mermaid
flowchart LR
  M1["Mic-1: sequential microcode"] --> M2["Mic-2: IFU / prefetch"]
  M2 --> M3["Mic-3: datapath pipeline"]
  M3 --> M4["Mic-4: decode + micro-op queue + deeper pipeline"]
```

## 5. Pipeline throughput

```mermaid
flowchart LR
  F["fetch"] --> R["read operands"] --> E["execute"] --> W["write-back"]
```

Different operations may occupy different stages in the same cycle.

## 6. Cache hierarchy

```mermaid
flowchart TD
  CPU["core"] --> L1I["L1-I"]
  CPU --> L1D["L1-D"]
  L1I --> L2["L2"]
  L1D --> L2
  L2 --> L3["L3"]
  L3 --> MEM["main memory"]
```

## 7. Branch prediction

```mermaid
flowchart TD
  BR["conditional branch"] --> PRED["predict taken/not taken + target"]
  PRED --> FETCH["fetch predicted path"]
  FETCH --> RESOLVE["resolve branch"]
  RESOLVE -->|correct| KEEP["keep pipeline work"]
  RESOLVE -->|wrong| FLUSH["discard / recover state"]
```

## 8. Out-of-order execution

```mermaid
flowchart TD
  D["decode"] --> RENAME["rename architectural registers"]
  RENAME --> Q["issue queue"]
  Q --> READY{"operands + unit ready?"}
  READY -->|yes| EX["execute"]
  READY -->|no| Q
  EX --> ROB["reorder / commit"]
```

## 9. Dependency types

```mermaid
flowchart TD
  DEP["dependencies"] --> RAW["RAW: true dependency"]
  DEP --> WAR["WAR: name dependency"]
  DEP --> WAW["WAW: name dependency"]
  WAR --> REN["register renaming"]
  WAW --> REN
```

## 10. Speculation

```mermaid
flowchart LR
  EARLY["execute before path is certain"] --> TEMP["temporary / rename state"]
  TEMP --> DECIDE{"path valid?"}
  DECIDE -->|yes| COMMIT["commit"]
  DECIDE -->|no| DROP["discard / recover"]
```
