# Диаграмма: storage stack и безопасный change flow

~~~mermaid
flowchart TD
    A["Need new/changed storage"] --> B["Read-only discovery"]
    B --> B1["lsblk / MODEL+SERIAL"]
    B --> B2["geom disk list"]
    B --> B3["hdparm -I / camcontrol devlist"]
    B --> C{"Exact device verified?"}
    C -->|No| D["Stop: resolve identity"]
    C -->|Yes| E{"Operation type"}

    E -->|Simple disk| F["GPT partition"]
    F --> G["Filesystem mkfs/newfs"]
    G --> H["Mount by LABEL/UUID"]
    H --> I["fstab with stable identity"]

    E -->|LVM| J["PV → VG → LV"]
    J --> J1["Snapshot / resize if needed"]
    J1 --> G

    E -->|RAID| K["mdadm array"]
    K --> K1["/proc/mdstat + monitor"]
    K1 --> G

    E -->|ZFS| L["zpool → vdevs"]
    L --> L1["zfs datasets / properties"]
    L1 --> L2["snapshots / clones"]

    E -->|Btrfs| M["mkfs.btrfs pool"]
    M --> M1["device add / balance"]
    M1 --> M2["subvolumes / snapshots"]

    N["Traditional FS"] --> N1["journaling"]
    N --> N2["fsck"]
    N --> N3["mount / fstab"]
    N --> N4["swap"]

    O["Failure protection"] --> O1["RAID / mirrors / parity"]
    O --> O2["SMART / health monitoring"]
    O --> O3["checksums / COW"]

    P["Backup"] --> P1["Separate copy"]
    P1 --> P2["Retention + encryption"]
    P2 --> P3["Restore test"]

    Q["High-risk boundary"] --> Q1["partition / mkfs"]
    Q --> Q2["secure erase"]
    Q --> Q3["zpool/zfs destroy"]
    Q --> Q4["RAID/Btrfs rebalance workload"]
    Q --> Q5["Rollback may be [Needs confirmation]"]
~~~

## Смысл диаграммы

Глава строит storage management как последовательность слоев. Безопасный change начинается с идентификации физического/виртуального device, затем изменяется ровно один слой и проверяется его результат. RAID, checksums и snapshots повышают надежность, но не заменяют независимый backup и тест восстановления.
