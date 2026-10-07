# Chapter 3 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Program generates virtual address"] --> B["MMU: page number + offset"]
    B --> T{"TLB hit?"}
    T -->|yes| P["Physical frame + offset"]
    T -->|no| PT["Page-table lookup"]
    PT --> V{"Present / valid?"}
    V -->|yes| F["Fill/refresh TLB"]
    F --> P
    V -->|no| PF["Page fault"]
    PF --> RES{"Page already resident elsewhere?"}
    RES -->|yes| MIN["Minor fault: install mapping"]
    RES -->|no| VIC["Need frame / choose victim"]
    VIC --> RM{"Victim modified?"}
    RM -->|yes| WB["Write victim to backing store"]
    RM -->|no| LOAD["Read demanded page"]
    WB --> LOAD
    LOAD --> MAP["Update PTE/TLB"]
    MIN --> MAP
    MAP --> RE["Restart faulting instruction"]

    VIC --> ALG["Replacement policy"]
    ALG --> A1["NRU / FIFO / second chance / clock"]
    ALG --> A2["LRU / NFU / aging"]
    ALG --> A3["Working set / WSClock"]

    A3 --> WS{"Working set fits?"}
    WS -->|no| TH["Thrashing"]
    TH --> LC["Load control: reduce competing processes"]

    B --> SHARE["Sharing / protection"]
    SHARE --> COW["Copy on write"]
    SHARE --> MF["Mapped files"]
    SHARE --> PIN["Pin I/O pages"]

    A --> SEG["Alternative logical model: segmentation"]
    SEG --> EXT["Variable-size segments → external fragmentation"]
    SEG --> COMB["Segmentation may be combined with paging"]
```

## Diagnostic distinction

```text
memory access problem
  ├─ invalid/protection → protection/addressing path
  ├─ TLB miss          → translation-cache path
  ├─ minor fault       → mapping path; no disk read required
  ├─ major fault       → backing-store I/O path
  ├─ repeated faults   → replacement/locality/working-set analysis
  └─ system-wide storm → load control / thrashing analysis
```
