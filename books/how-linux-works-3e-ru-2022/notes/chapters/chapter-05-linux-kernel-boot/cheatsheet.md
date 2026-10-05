# Шпаргалка: boot troubleshooting по главе 5

Цель: определить последний успешно достигнутый boot layer и только после этого менять configuration.

## Symptom / problem framing

Нужно определить последний успешно достигнутый boot layer и не менять boot configuration до локализации сбоя.

Типовые границы:
- firmware / BIOS / UEFI;
- bootloader / GRUB;
- kernel image и command line;
- device/subsystem initialization;
- root filesystem;
- переход к PID 1.

## Baseline / context

Source-derived boot chain:

~~~text
firmware
  ↓
bootloader
  ↓
kernel image + command line
  ↓
kernel initialization
  ↓
root filesystem
  ↓
init / PID 1
~~~

GRUB root, Linux `root=` и root уже работающей системы — разные понятия.

## Read-only checks

~~~bash
journalctl -k
dmesg
cat /proc/cmdline
efibootmgr
grub-mkconfig
~~~

Также источник использует `/sys/firmware/efi` и read-only GRUB commands `ls`, `ls -l`, `echo $root`, `set`.

## Interpretation

- нет kernel evidence → искать проблему на firmware/bootloader layer;
- kernel есть, но root не достигнут → проверять command line/root/device path;
- root достигнут, PID 1 не стартует → граница переходит к следующей главе;
- UEFI/ESP и BIOS/MBR используют разные boot mechanisms;
- generated `grub.cfg` не следует редактировать вручную.

## Next action

1. Определить boot mode.
2. Подтвердить фактическую kernel command line.
3. Проверить GRUB root/prefix и наличие kernel/initrd.
4. Использовать временное GRUB menu edit для ограниченного эксперимента, если это достаточно.
5. Persistent changes делать только после backup и с recovery path.

## Modifying action

Source-confirmed state-changing operations:
- GRUB menu/runtime directives;
- `grub-mkconfig -o ...`;
- `grub-install ...`;
- Secure Boot configuration как отдельная security boundary.

Bootloader installation может сделать систему незагружаемой; без конкретного layout rollback остаётся `[Needs confirmation]`.


## Boot chain

```text
firmware (BIOS/UEFI)
      ↓
bootloader
      ↓
kernel image + kernel command line
      ↓
kernel init: CPU → memory → buses → devices → subsystems
      ↓
root filesystem
      ↓
init / PID 1
      ↓
user space
```

Глава 5 подробно покрывает путь до запуска PID 1.

## 1. Read-only boot evidence

### Kernel journal

```bash
journalctl -k
dmesg
```

Источник также указывает параметр `-b` для просмотра других boot sessions и файл `/var/log/kern.log` в системах без systemd.

Что искать:
- device discovery;
- driver/subsystem initialization;
- root filesystem mount;
- переход к запуску init/systemd;
- ранние errors.

### Kernel command line

```bash
cat /proc/cmdline
```

Ключевые поля главы:
- `root=...` — root filesystem;
- `ro` — initial read-only root mount;
- `quiet`, `splash` — влияют на visible boot output;
- другие flags и `key=value`.

Если kernel уже запущен, `/proc/cmdline` — фактическое evidence того, какие параметры он получил.

## 2. Определить firmware model

Источник предлагает:
- запустить `efibootmgr`;
- проверить наличие `/sys/firmware/efi`.

Interpretation:
- список EFI boot targets → UEFI;
- сообщение об отсутствии EFI variables → BIOS;
- наличие `/sys/firmware/efi` → UEFI.

Не смешивать:
- BIOS boot partition;
- EFI System Partition (ESP).

Это разные boot mechanisms.

## 3. GRUB: три разных root concept

### Linux root
Kernel parameter:
```text
root=...
```

### GRUB root
Filesystem, из которой GRUB читает kernel/initrd/config.

### Host filesystem root
Обычный `/` уже работающей Linux system.

Для troubleshooting всегда уточнять, о каком root идёт речь.

## 4. GRUB read-only exploration

В GRUB command line источник показывает:

```text
grub> ls
grub> ls -l
grub> echo $root
grub> ls (hd0,msdos1)/
grub> ls ($root)/
grub> ls ($root)/boot
grub> set
```

Что это даёт:
- список devices/partitions;
- UUID и filesystem info;
- текущий GRUB root;
- наличие `/boot`, kernel image и GRUB files;
- значение `prefix`.

`prefix` указывает filesystem/directory, где GRUB ищет configuration и support files.

## 5. GRUB menu/editor

Источник указывает:
- Shift при BIOS boot;
- Esc при UEFI boot;
- `e` для редактирования выбранного menu entry;
- `c` для GRUB command line;
- Esc для возврата;
- `boot` после полной ручной конфигурации.

Редактирование menu entry удобно для временного boot correction. Persistent fix требует изменения generated configuration в работающей системе.

## 6. grub.cfg discipline

Источник прямо говорит: не редактировать generated `grub.cfg` напрямую.

Read-only generation:
```bash
grub-mkconfig
```

Эта форма пишет generated configuration в stdout.

Persistent generation:
```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

Перед записью:
1. backup existing configuration;
2. подтвердить правильный GRUB directory;
3. иметь recovery boot path.

Custom configuration source описан через `/etc/grub.d` и `custom.cfg`.

## 7. GRUB installation boundary

Пример MBR install из источника:

```bash
grub-install /dev/sda
```

Источник отдельно предупреждает: неправильная установка может сделать систему незагружаемой.

До install:
- определить BIOS/MBR или UEFI;
- подтвердить target disk;
- подтвердить GRUB directory;
- для UEFI — подтвердить ESP mount point;
- backup существующего boot state;
- иметь emergency boot plan.

Для внешнего storage source показывает форму:
```bash
grub-install --boot-directory=/mnt/boot /dev/sdc
```

Для UEFI source показывает форму с `--efi-directory` и `--bootloader-id`.

## 8. Secure Boot

Mental model:

```text
UEFI firmware
   ↓ verifies signature
signed loader / shim
   ↓
GRUB
   ↓
possibly signed kernel chain
```

Отключение Secure Boot source упоминает как возможный обход для experimentation, но это влияет на security boundary и не является универсальным решением.

## 9. MBR vs UEFI

### BIOS/MBR
```text
BIOS
 ↓
small boot code in MBR
 ↓
additional GRUB stages/core
 ↓
grub.cfg
 ↓
kernel
```

### UEFI
```text
UEFI firmware
 ↓
EFI System Partition (VFAT)
 ↓
EFI/<vendor>/*.efi
 ↓
GRUB/other loader
 ↓
kernel
```

## 10. Minimal troubleshooting flow

```text
boot failure
   ↓
есть kernel messages?
   ├─ нет → firmware / bootloader layer
   └─ да
       ↓
kernel reached root filesystem?
   ├─ нет → cmdline / root= / driver / early storage path
   └─ да
       ↓
PID 1 started?
   ├─ нет → boundary to chapter 6 topics
   └─ да → user-space startup, chapter 6+
```

## Verification / acceptance checks

После изменения boot configuration должно быть подтверждено:
- generated configuration содержит ожидаемый kernel/image/parameters;
- boot mode и target partition/device соответствуют системе;
- имеется известный recovery path;
- после reboot kernel получает ожидаемую `/proc/cmdline`;
- kernel journal доходит до expected stage.

## Rollback

- Temporary GRUB menu edit действует только на конкретную загрузку — это наиболее ограниченный способ экспериментировать.
- Persistent `grub.cfg` change: restore saved previous configuration, если boot environment доступен.
- Bootloader reinstall / MBR / ESP changes: `[Needs confirmation]` без конкретной machine layout; источник требует backup и emergency boot plan до изменения.
