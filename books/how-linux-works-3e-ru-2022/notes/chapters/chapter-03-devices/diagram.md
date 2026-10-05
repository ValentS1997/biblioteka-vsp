# Диаграмма: устройство от hardware до user space

~~~mermaid
flowchart TB
    HW["Hardware device"] --> KD["Kernel driver / subsystem"]
    KD --> SYS["sysfs: /sys/devices"]
    KD --> DEV["devtmpfs: базовый device node"]
    KD --> UE["kernel uevent"]

    UE --> UDEVD["udevd"]
    UDEVD --> RULES["udev rules"]
    RULES --> PERM["permissions"]
    RULES --> LINKS["persistent symlinks"]
    RULES --> ACTIONS["user-space actions / notifications"]

    DEV --> NODE["/dev node"]
    LINKS --> NODE
    NODE --> APP["User-space process"]
    SYS --> APP
~~~

## Investigation flow

~~~mermaid
flowchart LR
    A["/dev node"] --> B["ls -l"]
    B --> C["type + major/minor"]
    C --> D["udevadm info"]
    D --> E["sysfs path + attributes"]
    E --> F["/dev/disk/by-id or equivalent"]
    F --> G["persistent identity"]
    G --> H["udevadm monitor / journalctl -k"]
    H --> I["subsystem / event confirmed"]
~~~

## udev event processing

~~~mermaid
sequenceDiagram
    participant H as Hardware
    participant K as Kernel
    participant D as devtmpfs
    participant U as udevd
    participant R as Rules
    participant P as User-space process

    H->>K: device add/change/remove
    K->>D: expose base device node
    K->>U: uevent
    U->>R: load attributes and evaluate rules
    R-->>U: permissions / symlinks / actions
    U-->>P: configured device becomes visible/usable
~~~

## SCSI architecture

~~~mermaid
flowchart TB
    APP["User-space process"] --> CLASS["Class device or generic SCSI node"]
    CLASS --> UPPER["SCSI upper layer"]
    UPPER --> MIDDLE["SCSI middle layer"]
    MIDDLE --> LOWER["SCSI lower layer / bridge"]
    LOWER --> USB["USB storage path"]
    LOWER --> ATA["libata / ATA-SATA path"]
    LOWER --> HOST["SCSI host adapter"]
    USB --> HW["Hardware"]
    ATA --> HW
    HOST --> HW
~~~

## Operational meaning

Один hardware device может иметь несколько представлений: короткий node в <code>/dev</code>, подробный sysfs path, persistent symlinks и иногда generic SCSI node. Поэтому state-changing operation должна начинаться не с угадывания имени, а с подтверждения identity.
