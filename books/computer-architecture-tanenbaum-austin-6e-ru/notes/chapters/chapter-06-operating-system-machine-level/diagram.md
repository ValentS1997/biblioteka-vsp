# Mermaid — глава 6 «Уровень операционной системы»

Источник: RAG `p0475:c01`–`p0554:c01`.

## 1. OS-machine layer

```mermaid
flowchart TD
  APP["Application"] --> SYS["System calls / virtual commands"]
  SYS --> OS["Operating system"]
  OS --> ISA["ISA / hardware"]
  OS --> VM["Virtual memory"]
  OS --> FS["Files / directories"]
  OS --> PROC["Processes / synchronization"]
```

## 2. Page translation

```mermaid
flowchart LR
  VA["virtual page + offset"] --> PTE["page table entry"]
  PTE -->|present| PA["frame + same offset"]
  PTE -->|absent| PF["page fault"]
  PF --> OS2["OS loads page / updates mapping"]
  OS2 --> PA
```

## 3. Working set

```mermaid
flowchart TD
  LOC["locality"] --> WS["working set"]
  WS -->|fits RAM| FEW["few page faults"]
  WS -->|exceeds frames| THR["thrashing"]
```

## 4. Segmentation vs paging

```mermaid
flowchart LR
  PAG["paging"] --> FIX["fixed pages"]
  PAG --> TRANS["transparent virtual memory"]
  SEG["segmentation"] --> VAR["variable logical regions"]
  SEG --> PROT["per-segment protection"]
  VAR --> EXT["external fragmentation"]
```

## 5. Core i7 translation

```mermaid
flowchart LR
  SEL["selector"] --> DESC["LDT/GDT descriptor"]
  DESC --> LIN["BASE + offset"]
  LIN --> DIR["page directory"]
  DIR --> PT["page table"]
  PT --> FRAME["physical frame"]
```

## 6. Hardware virtualization

```mermaid
flowchart TD
  VM1["Guest OS A"] --> H["Hypervisor"]
  VM2["Guest OS B"] --> H
  H --> CPU["CPU"]
  H --> MEM["Physical memory"]
  H --> IO["I/O devices"]
```

## 7. File abstraction

```mermaid
flowchart LR
  API["open/read/write/close"] --> FD["descriptor / handle"]
  FD --> META["filesystem metadata"]
  META --> BLK["file blocks / extents"]
  BLK --> DEV["storage device"]
```

## 8. Race condition

```mermaid
sequenceDiagram
  participant P as Producer
  participant S as Shared state
  participant C as Consumer
  P->>S: check/update
  C->>S: interleaving check/update
  Note over P,C: non-atomic check + action can lose wakeup
```

## 9. Semaphore producer/consumer

```mermaid
flowchart LR
  P["producer"] --> DA["down(available)"]
  DA --> PUT["put item"]
  PUT --> UF["up(filled)"]
  C["consumer"] --> DF["down(filled)"]
  DF --> GET["get item"]
  GET --> UA["up(available)"]
```
