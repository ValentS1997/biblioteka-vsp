# Шпаргалка: storage workflow по главе 4

Цель: локализовать нужный storage layer, собрать read-only evidence и только затем выполнять минимальное изменение.

## Storage stack

```text
physical/virtual block device
        ↓
partition table (MBR/GPT)
        ↓
partition / Physical Volume
        ↓
LVM Volume Group / Logical Volume   [optional]
        ↓
filesystem or swap
        ↓
mount point
        ↓
files/directories in user space
```

## 1. Read-only baseline

### Partition table

```bash
parted -l
fdisk -l
journalctl -k
```

Что проверить:
- какой block device выбран;
- MBR или GPT;
- размер и границы partitions;
- есть ли LVM flag;
- совпадает ли ожидаемая topology с kernel messages.

Для SSD alignment источник показывает чтение стартового сектора через sysfs:

```bash
cat /sys/block/sdf/sdf2/start
```

### Mounted filesystems

```bash
mount
blkid
df
df DIR
du -s
```

Интерпретация:
- `mount` — device, mount point, type, options;
- `blkid` — filesystem UUID/type;
- `df` — capacity/usage;
- `du` — usage по directory tree.

### LVM inventory

```bash
pvs
pvdisplay
vgs
vgdisplay
lvs
lvdisplay
dmsetup info
dmsetup table
```

Mental model:
- PV = physical block device/partition prepared for LVM;
- VG = pool из одного или нескольких PV;
- LV = virtual block device allocated from VG;
- device mapper = kernel mapping layer.

## 2. Partitioning safety

Источник различает:
- `fdisk`: изменения готовятся в памяти и записываются при подтверждённом выходе;
- `parted`: изменения применяются сразу.

До изменения partition table:
1. подтвердить target device;
2. подтвердить backup важных данных;
3. убедиться, что target partitions не используются;
4. сохранить read-only baseline.

Forced reread partition table показан через `blockdev --rereadpt`, но это уже state-changing kernel action.

## 3. Filesystem creation boundary

`mkfs` создаёт новую filesystem поверх block device.

Risk: источник прямо предупреждает, что создание новой filesystem поверх существующей уничтожает старые данные.

Verification после создания:
- diagnostic output;
- UUID;
- backup superblock numbers для ext-family;
- `blkid`.

## 4. Mount / unmount

Manual mount имеет модель:

```text
device/UUID + filesystem type + mount point + options
```

Read-only safety option:
- `ro` / `-r`.

Security-related options:
- `exec/noexec`;
- `suid/nosuid`;
- `ro/rw`.

`umount` автоматически синхронизирует buffered changes перед отключением filesystem.

Если filesystem нельзя размонтировать перед shutdown, источник рекомендует выполнить `sync`.

## 5. /etc/fstab

Шесть полей:

1. device или UUID;
2. mount point;
3. filesystem type;
4. options;
5. dump field — в главе рекомендуется 0;
6. fsck order: 1 для root, 2 для других local disk filesystems, 0 для исключённых.

После изменения fstab проверять смысл каждой строки до boot-time использования. Команда `mount -a` применяет подходящие записи, кроме `noauto`.

## 6. fsck workflow

Нельзя запускать fsck на mounted filesystem.

Исключение в источнике: root filesystem, mounted read-only в single-user mode.

При подозрении на серьёзную ошибку:

```text
hardware/config sanity
        ↓
read-only / no-change check
        ↓
оценить масштаб проблемы
        ↓
repair только после подтверждения причины/риска
```

Источник упоминает:
- `fsck -n` для проверки без изменений;
- backup superblocks;
- `mkfs -n` для просмотра backup superblock locations без создания filesystem;
- `debugfs` как recovery tool, который по умолчанию открывает filesystem read-only.

## 7. Swap

Read-only check:

```bash
free
```

Swap может быть:
- dedicated partition;
- ordinary file.

State model:
```text
empty partition/file
   ↓
swap signature
   ↓
swapon
   ↓
kernel swap pool
```

Для `swapoff` должно оставаться достаточно memory/swap capacity для активных pages.

## 8. LVM

```text
PV1 ─┐
     ├─ VG ── LV1 ── filesystem
PV2 ─┘      └─ LV2 ── swap/filesystem
```

Read-only:
- `pvs/pvdisplay`;
- `vgs/vgdisplay`;
- `lvs/lvdisplay`.

State-changing:
- create/extend VG;
- create/remove/resize LV;
- resize filesystem inside LV.

Ключевой риск: LV resize и filesystem resize — разные операции. Увеличение ext2/3/4 возможно online, а уменьшение mounted filesystem — нет; источник рекомендует координировать размеры через LVM tooling.

## 9. Inode model

```text
directory entry: "file" → inode N
inode N → metadata + data blocks
hard link → ещё одна directory entry → тот же inode N
```

`ls -i` показывает inode number.

Link count = количество directory entries, указывающих на inode.

Block bitmap хранит состояние free/used blocks. fsck сравнивает directory/inode structure с allocation metadata и исправляет несогласованность.

## Verification / acceptance

Перед завершением storage change подтвердить:
- ожидаемую partition/LVM topology;
- expected UUID/type;
- mount point/options;
- capacity;
- отсутствие неожиданных kernel/filesystem errors;
- возможность повторно прочитать конфигурацию после reboot, если изменение persistent.

## Rollback

- `fdisk`: до записи можно выйти без сохранения, если изменения ещё не committed.
- mount option change: remount к предыдущим options, если состояние позволяет.
- STOP/rollback для destructive `mkfs`, partition overwrite, LV removal: `[Needs confirmation]`; рассчитывать на backup/recovery, а не на обратимость.
- LVM resize rollback зависит от filesystem и направления resize: `[Needs confirmation]`.
