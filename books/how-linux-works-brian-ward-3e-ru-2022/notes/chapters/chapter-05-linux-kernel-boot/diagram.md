# Mermaid — глава 5 «Загрузка ядра Linux»

Источник: **RAG `p0156:c01`–`p0175:c01`**, PDF/печатные страницы 156–175. Диаграммы синтезированы из текста главы; точные рисунки 5.1–5.2 не реконструируются.

## 1. Общая последовательность boot

```mermaid
flowchart TD
    FW["BIOS / UEFI firmware"] --> BL["Bootloader"]
    BL --> KIMG["Kernel image + parameters"]
    KIMG --> KCPU["Kernel: CPU + memory"]
    KCPU --> KBUS["Bus discovery"]
    KBUS --> KDEV["Device discovery"]
    KDEV --> KSUB["Kernel subsystems"]
    KSUB --> ROOT["Mount root filesystem"]
    ROOT --> INIT["Start init / first user-space process"]
    INIT --> USER["Further user-space startup (chapter 6)"]
```

Глава 5 покрывает firmware/bootloader/kernel и переход к первому user-space process; детальное продолжение systemd/init отложено до главы 6 (§5 intro, §5.2).

## 2. Как GRUB видит систему

```mermaid
flowchart LR
    MENU["GRUB menu"] --> EDIT["e: temporary entry editor"]
    MENU --> CLI["c: GRUB command line"]
    CLI --> DEV["ls / ls -l: GRUB devices and partitions"]
    CLI --> ROOT["echo $root"]
    ROOT --> FILES["ls ($root)/boot"]
    CLI --> VARS["set: root + prefix"]
    EDIT --> LINUX["linux → kernel image + kernel parameters"]
    EDIT --> INITRD["initrd → initial RAM filesystem image"]
    LINUX --> BOOT["boot"]
    INITRD --> BOOT
    BOOT --> KERNEL["Linux kernel starts"]
```

**Namespace boundary:** GRUB's `root`, `insmod`, `ls` and device syntax such as `(hd0,msdos1)` are not Linux shell/kernel equivalents (§5.5–5.5.1).

## 3. Persistent GRUB configuration

```mermaid
flowchart TD
    INPUT["/etc/grub.d scripts + custom files"] --> GEN["grub-mkconfig"]
    GEN --> STDOUT["Without -o: generated config on stdout"]
    GEN --> WRITE["With -o: write grub.cfg"]
    WRITE --> CFG["/boot/grub/grub.cfg"]
    CFG --> GRUB["GRUB executes menuentry / linux / initrd"]
    GRUB --> KERNEL["Kernel boot"]
    INPUT -.-> WARN["Do not edit generated grub.cfg directly"]
```

Before replacing the target configuration, the chapter instructs the reader to back up the previous configuration and confirm the destination (§5.5.2).

## 4. BIOS/MBR versus UEFI/ESP

```mermaid
flowchart TD
    START["Firmware boot"] --> MODE{"Boot model"}
    MODE --> BIOS["BIOS / MBR"]
    MODE --> UEFI["UEFI"]
    BIOS --> MBR["Small MBR boot code"]
    MBR --> STAGE["Additional staged GRUB code / BIOS boot partition"]
    STAGE --> CORE["GRUB core"]
    UEFI --> ESP["EFI System Partition (VFAT)"]
    ESP --> EFI["*.efi loader (e.g. GRUB/shim)"]
    EFI --> CORE
    CORE --> CFG["Load configuration and modules"]
    CFG --> K["Load kernel (+ optional initrd)"]
```

The chapter contrasts code outside the filesystem in traditional MBR boot with a filesystem-based ESP containing UEFI executables (§5.8.1–5.8.3).

## 5. Operational decision boundary

```mermaid
flowchart TD
    OBS["Observe: journalctl -k / cmdline / efibootmgr"] --> LOC["Identify boot mode, kernel, root, GRUB path"]
    LOC --> TEMP{"Can temporary GRUB edit test the hypothesis?"}
    TEMP -->|Yes| E["Edit menu entry only"]
    E --> B["Boot and verify /proc/cmdline + logs"]
    TEMP -->|No| PERSIST["Persistent config/install requested"]
    PERSIST --> PRE{"Backup + emergency boot path + exact target verified?"}
    PRE -->|No| STOP["[Needs confirmation] — STOP"]
    PRE -->|Yes| CHANGE["Generate config or install GRUB"]
    CHANGE --> REBOOT["Reboot / verify GRUB + kernel"]
    REBOOT --> OK{"Acceptance?"}
    OK -->|No| RB["Use verified recovery path / rollback"]
    OK -->|Yes| KEEP["Keep configuration"]
```

This safety sequence is an analytical organization of the chapter's warnings, not a complete vendor-neutral recovery procedure.

## 6. Full GRUB execution sequence from §5.8.3

```mermaid
flowchart TD
    A["Firmware initializes hardware"] --> B["Find and execute boot code"]
    B --> C["Load GRUB core"]
    C --> D["GRUB initializes disk/filesystem access"]
    D --> E["Identify boot partition / load configuration"]
    E --> F["Allow user configuration changes"]
    F --> G["Execute grub.cfg after timeout/action"]
    G --> H["Load extra GRUB modules as needed"]
    H --> I["boot → load and execute Linux kernel"]
```

For UEFI/ESP, firmware can navigate the ESP and directly execute the GRUB/other `.efi` loader; for non-UEFI paths the process can start from MBR boot code (§5.8.3).
