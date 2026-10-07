# Mermaid — глава 3 «Устройства»

Источник: `p0079:c01`–`p0101:c01` (PDF/печатные страницы 79–101). Диаграммы синтезированы из словесного описания; **не** копии рисунков 3.1–3.3.

## 1. Device interface и информационная модель

```mermaid
flowchart TB
  USER["User-space process"] --> IO["Файловые операции"]
  IO --> DEV["/dev: device node"]
  DEV --> BC{"Тип интерфейса"}
  BC --> B["b: блочный, выбор блока"]
  BC --> C["c: символьный, поток"]
  BC --> IPC["p/s: pipe и Unix socket (IPC)"]
  B --> K["Kernel driver"]
  C --> K
  K --> HW["Hardware / kernel-backed device"]
  SYS["/sys/devices: топология и атрибуты"] -.-> K
  SB["/sys/block: symlink на block device"] -.-> SYS
  NOTE["Не каждому устройству нужен /dev node"] -.-> DEV
```

PDF 79–82: назначение `/dev` — интерфейс ввода-вывода; `/sys` — отражение конфигурации и свойств. Major/minor связывают node с представлением устройства ядром.

## 2. Обнаружение /devtmpfs / udev (3.5, с. 89–95)

```mermaid
flowchart TD
  HW["Ядро обнаруживает устройство"] --> SYS["sysfs: /sys/devices"]
  HW --> NODE["devtmpfs: ядро предоставляет /dev node"]
  HW --> EVENT["uevent с атрибутами"]
  EVENT --> DAEMON["udevd получает uevent"]
  DAEMON --> RULES["Читает применимые rules в порядке"]
  RULES --> PERMS["Настройка прав и дополнительных атрибутов"]
  RULES --> LINKS["Создание ссылок /dev/disk/by-id"]
  NODE --> INFO["udevadm info: P/N/S/E"]
  SYS --> INFO
  LINKS --> INFO
  EVENT --> MON["udevadm monitor: KERNEL"]
  DAEMON --> MON2["udevadm monitor: UDEV"]
```

Правила из `/lib/udev/rules.d` и `/etc/udev/rules.d` используют условные выражения `==`/`!=` и директивы `=`/`+=`/`:=` (PDF 91–93). В RAG имеются различающиеся переменные внутри примера import — `source-findings.md`.

## 3. Read-only локализация устройства

```mermaid
flowchart TD
  START["Устройство неизвестно или сменилось имя"] --> DEV["ls /dev; ls -l (тип/major/minor)"]
  DEV --> SYS["ls -l /sys/block"]
  SYS --> INFO["udevadm info --query=all --name=/dev/sda"]
  INFO --> STABLE["ls -l /dev/disk/by-id"]
  STABLE --> Q{"Есть подтверждённое соответствие?"}
  Q -->|Нет| STOP["[Needs confirmation]; не изменять"]
  Q -->|Да| CLASS["Проверить класс: lsscsi / nvme list"]
  CLASS --> EVENTS["При необходимости udevadm monitor"]
  EVENTS --> DONE["Зафиксировать node, sysfs path, атрибуты"]
```

**Никакой из адресов `/dev/sda` не гарантирован** на машине пользователя. Глава не даёт универсального repair workflow; переход к изменению требует отдельного анализа.

## 4. SCSI stack: USB-storage и SATA/ATA (3.6)

```mermaid
flowchart TB
  APP["Приложение (user space)"] --> BD["Обычный block device /dev/sd* или /dev/sr*"]
  APP --> SG["Generic SCSI /dev/sg*"]
  BD --> U["SCSI upper layer: sd/sr"]
  SG --> G["SCSI generic interface"]
  U --> MID["SCSI middle layer: маршрутизация"]
  G --> MID
  MID --> LOW["SCSI lower layer: hardware adapter / bridge"]
  LOW --> SCSI["Традиционный SCSI / SAS"]
  LOW --> USB["USB-storage bridge → USB subsystem"]
  LOW --> ATA["libata → ATA/SATA"]
```

По PDF 95–100: `lsscsi` отображает **host:bus:target:LUN**; `lsscsi -g` дополнительно выводит generic node. Упрощение на диаграмме — *SCSI как слои с мостами*, а не точный граф рисунка 3.2.

## 5. Изменяющие операции — отдельная граница

```mermaid
flowchart TD
  OBS["Read-only: info / sysfs / lsscsi"] --> CHECK{"Известен объект и подтверждён риск?"}
  CHECK -->|Нет| HALT["[Needs confirmation] — стоп"]
  CHECK -->|Да| PLAN["Согласовать change plan + rollback"]
  PLAN --> ACTION["dd / mknod / udev rules / chvt (при необходимости)"]
  ACTION --> VERIFY["Readback результата"]
  VERIFY --> DECIDE{"Acceptance?"}
  DECIDE -->|Нет| ROLLBACK["Rollback: [Needs confirmation] — глава не даёт алгоритм"]
  DECIDE -->|Да| KEEP["Зафиксировать состояние"]
```

**Опасность:** запись на disk raw device может уничтожить данные; `mknod` с major/minor из печатного примера нельзя применять без подтверждения; `udev` rules требуют отдельной проверки. Эта диаграмма отражает контрольные ограничения, а не предлагает менять конфигурацию.
