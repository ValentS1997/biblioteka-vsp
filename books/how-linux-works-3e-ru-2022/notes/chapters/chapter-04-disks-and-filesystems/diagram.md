# Диаграмма: storage stack по главе 4

## От устройства до файла

```mermaid
flowchart TB
    HW["Physical / virtual block device"] --> PT["Partition table: MBR / GPT"]
    PT --> PART["Partition"]
    PART --> PV["LVM Physical Volume (optional)"]
    PV --> VG["Volume Group"]
    VG --> LV["Logical Volume"]
    PART --> FS["Filesystem / Swap"]
    LV --> FS
    FS --> MP["Mount point"]
    MP --> VFS["VFS / kernel syscalls"]
    VFS --> APP["User-space files and processes"]
```

## Safe change workflow

```mermaid
flowchart TD
    A["Нужно изменить storage"] --> B["Read-only inventory"]
    B --> C["device / partition / UUID / mount / LVM state"]
    C --> D{"Какой слой меняется?"}
    D --> P["Partition table"]
    D --> L["LVM"]
    D --> F["Filesystem / mount"]
    D --> S["Swap"]
    P --> R["Backup + target unused"]
    L --> R
    F --> R
    S --> R
    R --> X["Минимальное изменение"]
    X --> V["Verification теми же read-only views"]
    V --> Q{"Expected state?"}
    Q -->|Да| Z["Готово"]
    Q -->|Нет| RB["Rollback / recovery point"]
```

## LVM

```mermaid
flowchart LR
    PV1["PV1"] --> VG["Volume Group"]
    PV2["PV2"] --> VG
    VG --> LV1["LV1"]
    VG --> LV2["LV2"]
    LV1 --> DM1["device mapper"]
    LV2 --> DM2["device mapper"]
    DM1 --> FS1["filesystem"]
    DM2 --> FS2["filesystem / swap"]
```

## Filesystem internals

```mermaid
flowchart LR
    NAME1["directory entry: file_A"] --> INODE["inode N"]
    NAME2["hard link: file_B"] --> INODE
    INODE --> META["type / mode / metadata / link count"]
    INODE --> DATA["data blocks"]
    BITMAP["block bitmap"] --> DATA
```

Link count показывает количество directory entries, указывающих на inode. Когда оно становится нулём, inode и связанные data blocks могут быть освобождены.

## fsck consistency model

```mermaid
flowchart TD
    DIR["Directory structure"] --> REBUILD["Reconstruct expected state"]
    INODES["Inode table"] --> REBUILD
    REBUILD --> LINKS["Expected link counts"]
    REBUILD --> MAP["Expected block allocation"]
    LINKS --> CMP["Compare with on-disk metadata"]
    MAP --> CMP
    CMP --> FIX["Repair / lost+found when required"]
```
