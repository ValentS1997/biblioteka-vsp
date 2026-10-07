# Chapter 4 conceptual / diagnostic flow

```mermaid
flowchart TD
    A["Process supplies path"] --> B["Directory/path resolution"]
    B --> C{"Object found?"}
    C -->|no| N["Namespace/path failure"]
    C -->|yes| D["Metadata: type, attrs, links, size"]
    D --> E["Open-file descriptor / VFS object"]
    E --> F["Logical file offset"]
    F --> G{"Allocation model"}
    G --> G1["Contiguous"]
    G --> G2["Linked / FAT"]
    G --> G3["I-node / indexed"]
    G1 --> H["Physical block"]
    G2 --> H
    G3 --> H

    H --> I{"Block cached?"}
    I -->|yes| J["Serve from cache"]
    I -->|no| K["Disk read / optional read-ahead"]
    K --> J

    D --> L["Persistent metadata update"]
    L --> M{"Crash before all writes?"}
    M -->|yes| Q["Potential inconsistency"]
    Q --> R["Journal replay or consistency check"]
    R --> R1["lost blocks"]
    R --> R2["duplicate free blocks"]
    R --> R3["duplicate data refs"]
    R --> R4["link-count mismatch"]

    H --> S["Free-space accounting"]
    S --> S1["bitmap"]
    S --> S2["free list / runs"]

    E --> V["VFS"]
    V --> V1["local FS"]
    V --> V2["other local FS"]
    V --> V3["remote FS"]

    A --> BK["Backup / restore"]
    BK --> BK1["physical backup"]
    BK --> BK2["logical / incremental"]
    BK2 --> SNAP{"Source active?"}
    SNAP -->|yes| SS["stable snapshot-like view"]
```

## Operational distinction

```text
path resolution
    ≠ allocation mapping
    ≠ free-space accounting
    ≠ crash consistency
    ≠ durability of dirty cache
    ≠ backup/restore
    ≠ layout/performance optimization
```
