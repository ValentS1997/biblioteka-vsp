# Mermaid — глава 4 «Диски и файловые системы»

**Source RAG:** `p0102:c01`–`p0155:c01`, PDF/печатные с. 102–155. Диаграммы — аналитическая схема по тексту; исходные рис. 4.1–4.10 из мультимодального PDF не восстановлены.

## 1. Storage stack и доступ к файлу (§4, 4.1, 4.2, 4.4)

```mermaid
flowchart TB
    USER["Процесс пользователя: файл и каталог"] --> VFS["VFS — единый интерфейс к FS"]
    VFS --> FS["Файловая система: метаданные + блоки данных"]
    FS --> LV{"Есть LVM?"}
    LV -->|Нет| PART["Раздел блочного устройства (MBR/GPT)"]
    LV -->|Да| LOG["Logical Volume (LV)"]
    LOG --> DM["Device mapper: перевод логических блоков"]
    DM --> PV["Physical Volumes (PV)"]
    PV --> PART
    PART --> RAW["Block layer / storage hardware"]
    USER -.->|инструменты raw I/O, большой риск| RAW
```

`parted/fdisk` меняют границы разделов; `mkfs` создаёт структуру файловой системы; `mount` подключает её к общей иерархии. LVM добавляет mapping **между** FS и физическими блоками (PDF 102–104, 114, 132–146).

## 2. Change boundary: partition и filesystem (4.1–4.2)

```mermaid
flowchart TD
    A["Read-only: lsblk / parted -l / fdisk -l"] --> B["Сопоставить диск, таблицу и раздел"]
    B --> C{"Есть точный target, verified backup и неиспользуемый раздел?"}
    C -->|Нет| STOP["[Needs confirmation] — не изменять"]
    C -->|Да| PLAN["Отдельный change plan: MBR/GPT и ожидаемые границы"]
    PLAN --> EDIT["fdisk: правки в памяти / parted: немедленные"]
    EDIT --> FINAL{"Предварительный план принят?"}
    FINAL -->|Нет| CANCEL["fdisk q до w — выйти без записи"]
    FINAL -->|Да| WRITE["fdisk w / parted — изменяет диск"]
    WRITE --> CHECK["Readback: таблица, /proc/partitions, сообщения ядра"]
    CHECK --> MKFS["mkfs только для новой/разрешённой к перезаписи FS"]
    MKFS --> MOUNT["mount к проверенной точке"]
    MOUNT --> VERIFY["mount / blkid / df"]
```

**Неприведённый rollback:** после изменения таблицы или повторного `mkfs` общий способ возврата **[Needs confirmation]** (PDF 108–111, 116–119).

## 3. Перепроверка файловой системы (4.2.11)

```mermaid
flowchart TD
    X["Подозрение на повреждение FS"] --> Y["Установить device + mount state"]
    Y --> Z{"Файловая система смонтирована?"}
    Z -->|Да, rw| NOGO["STOP: fsck на mounted FS запрещён"]
    Z -->|Нет| SAFETY["Оценить backup и серьёзность повреждения"]
    SAFETY --> DRY["fsck -n: без изменения"]
    DRY --> ISSUE{"Обнаружены проблемы?"}
    ISSUE -->|Нет| DONE["Зафиксировать отчёт"]
    ISSUE -->|Да| ESC["[Needs confirmation]: тип FS, причина, backup, сценарий исправления"]
    ESC --> REPAIR["Исправление fsck / backup superblock по отдельному решению"]
    REPAIR --> VERIFY["Проверить целостность / восстановленные данные"]
```

Исключение книги: root, смонтированный read-only в single-user mode; оно не превращает диагностику рабочей RW FS в безопасную процедуру (PDF 127–129).

## 4. LVM: user space и kernel mapper (4.4)

```mermaid
flowchart LR
    A["PV: блочные устройства + metadata"] --> VG["VG: пул физических экстентов"]
    B["PV2"] --> VG
    VG --> LV1["LV1: виртуальный block device"]
    VG --> LV2["LV2"]
    LVM["LVM user space: pvs/vgs/lvs, vgcreate/lvresize"] --> META["Метаданные PV/VG/LV"]
    META --> DM["ioctl → /dev/mapper/control"]
    DM --> K["Kernel device mapper: таблица сегментов"]
    K --> LV1
    K --> LV2
    LV1 --> FS["Filesystem или swap"]
```

`lvresize` изменяет размер LV; `fsadm` или `lvresize -r` координирует FS, но сокращение и увеличение имеют разные требования. `lvremove` уничтожает LV (PDF 139–149).

## 5. inode, каталоги, hard links (4.6)

```mermaid
flowchart TD
    D["Каталог: имя → inode"] --> I["inode: тип, права, блоки, link count"]
    D2["Другое имя, hard link"] --> I
    I --> B["Пул блоков данных"]
    RM["rm: удаление записи каталога"] --> LC["link count уменьшается"]
    LC --> DEC{"Остались ссылки?"}
    DEC -->|Да| KEEP["inode сохраняется"]
    DEC -->|Нет| REMOVE["inode и блоки могут освобождаться"]
```

PDF 150–155: `ls -i`/`stat` показывают inode; не все файловые системы поддерживают hard links. Таблицы inode/bitmap могут требовать исправления после несогласованного состояния.

## Примечания о рисунках

`rag/manifest.yaml` не кодирует иллюстрации отдельно. Схемы здесь объясняют **подтверждённые словами** связи, не визуальные детали рисунков 4.1–4.10. Любые данные о конкретном существующем сервере: **[Needs confirmation]**.
