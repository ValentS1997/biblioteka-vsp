# Диаграмма: загрузка Linux по главе 5

## Основная последовательность

```mermaid
flowchart TB
    FW["Firmware: BIOS / UEFI"] --> BL["Bootloader"]
    BL --> KI["Kernel image + command line"]
    KI --> CPU["CPU / memory checks"]
    CPU --> BUS["Bus discovery"]
    BUS --> DEV["Device discovery / drivers"]
    DEV --> SUB["Kernel subsystems"]
    SUB --> ROOT["Mount root filesystem"]
    ROOT --> INIT["Start init as PID 1"]
    INIT --> US["User space — chapter 6"]
```

## Boot troubleshooting boundary

```mermaid
flowchart TD
    A["System does not boot normally"] --> B{"Kernel messages exist?"}
    B -->|No| C["Firmware / bootloader layer"]
    B -->|Yes| D["Inspect journalctl -k / cmdline"]
    D --> E{"Root filesystem mounted?"}
    E -->|No| F["root= / early driver / storage path"]
    E -->|Yes| G{"PID 1 started?"}
    G -->|No| H["Kernel → init boundary"]
    G -->|Yes| I["Continue with chapter 6 user-space startup"]
```

## GRUB environment

```mermaid
flowchart LR
    D["GRUB device namespace"] --> R["GRUB root"]
    R --> P["prefix /boot/grub"]
    R --> K["kernel image"]
    R --> I["initrd image"]
    K --> CMD["linux directive + kernel parameters"]
    I --> CMD
    CMD --> BOOT["boot"]
    BOOT --> LK["Linux kernel"]
    LK --> LROOT["Linux root= filesystem"]
```

GRUB root и Linux root filesystem разделены намеренно.

## BIOS/MBR vs UEFI

```mermaid
flowchart TB
    BIOS["BIOS"] --> MBR["MBR boot code"]
    MBR --> CORE["additional GRUB stage/core"]
    CORE --> CFG1["grub.cfg"]
    CFG1 --> K1["kernel"]

    UEFI["UEFI"] --> ESP["EFI System Partition"]
    ESP --> EFI["EFI/<vendor>/*.efi"]
    EFI --> CFG2["GRUB / loader configuration"]
    CFG2 --> K2["kernel"]
```

## Secure Boot chain

```mermaid
flowchart LR
    U["UEFI firmware"] --> V["signature verification"]
    V --> S["signed shim/loader"]
    S --> G["GRUB"]
    G --> K["kernel / further verified chain"]
```
