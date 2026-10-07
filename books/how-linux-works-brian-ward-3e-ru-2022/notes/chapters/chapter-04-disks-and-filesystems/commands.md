# Команды — глава 4 «Диски и файловые системы»

**Provenance:** `how-linux-works-brian-ward-3e-ru-2022:p0102:c01`–`p0155:c01` (PDF/печатные с. 102–155). `/dev/sdd`, `/dev/sdf2`, `myvg` — примеры автора, **не** реальные устройства читателя.

Обозначения: **RO** — чтение/наблюдение; **WG** — длительное наблюдение или нагрузка; **SC** — изменение диска, FS, swap, LVM, конфигурации. Все потенциально опасные команды — учебный синтаксис, не инструкция к запуску.

## Read-only commands

| Команда из текста | Действие | Source PDF |
|---|---|---:|
| `lsblk`, `parted -l`, `fdisk -l` | Список устройств и таблицы разделов | 105–110 |
| `parted /dev/sdb print` | Таблица разделов выбранного демонстрационного диска | 140 |
| `cat /proc/partitions`, `journalctl -k` | Представление разделов ядром, сообщения | 107–111 |
| `cat /sys/block/sdf/sdf2/start` | Номер начального сектора для оценки alignment | 113–114 |
| `mount` (без аргументов), `blkid` | Текущие FS, mountpoints, UUID, типы | 118–120 |
| `ls -l /sbin/mkfs.*` | Исполняемые имена и ссылки mkfs | 116 |
| `df`, `df dir`, `df -h` | Занятость файловой системы; целевой каталог | 124–125 |
| `du`, `du -s *` | Объём дерева каталогов; `*` не охватывает dotfiles | 125–126 |
| `free` | RAM и swap | 130 |
| `pvs`, `pvdisplay`, `pvscan` | Физические тома/метаданные LVM | 138–141 |
| `vgs`, `vgdisplay` | Группы томов, VSize, VFree, PE | 134–136 |
| `lvs`, `lvdisplay` | Логические тома, LV Path/size/state | 136–137 |
| `ls -l /dev/ubuntu-vg/root` | Symlink на `/dev/dm-0` в примере | 137 |
| `dmsetup info`, `dmsetup table` | Kernel mapper topology / linear extents | 147–149 |
| `ls -i`, `stat`, `ls -l` | inode, метаданные, link count | 152–153 |
| `dd if=/dev/sdb1 count=1000 \| strings \| less` | Чтение LVM metadata через pipe; не копирует на диск | 147 |

`udevadm monitor --kernel` — **WG/RO**: длительное наблюдение событий изменения разделов (§4.1.2, PDF 109). `df` и `du` описаны также с опциями `-k`, `-m` и `-h` (PDF 125).

`fsck -n` по книге предлагает **проверку без записи**, но запуск fsck по **смонтированной** FS автор запрещает; это **условно read-only** с обязательным preflight (§4.2.11, PDF 127–128). `mkfs -n` в разделе 4.2.11 применяется **только** для поиска номеров резервных суперблоков; иная реализация: **[Needs confirmation]**.

## State-changing: разметка, FS и конфигурация

| Инструмент/пример | Изменение и риск | Проверка | Rollback |
|---|---|---|---|
| `fdisk /dev/sdd` (интерактивно: `p/d/n/w/q`) | `w` пишет partition table; `q` до записи выходит без commit | `parted -l`, `/proc/partitions` | `q` только **до** записи; затем [Needs confirmation] |
| `parted` (режим изменения) | Применяет правки разделов немедленно | `parted -l` | [Needs confirmation] |
| `blockdev --rereadpt /dev/sdf` | Принуждает ядро перечитать partition table | `cat /proc/partitions` | [Needs confirmation] |
| `mkfs -t ext4 /dev/sdf2` | Новая FS на разделе **уничтожает прежнюю** | `blkid` после операции | Только проверенная копия; иначе [Needs confirmation] |
| `mount -t ext4 /dev/sdf2 /home/extra` | Смонтировать FS на каталог | `mount`, `df` | `umount`, если безопасно; иначе [Needs confirmation] |
| `umount mountpoint` | Отсоединить FS и сбросить записи | `mount` | [Needs confirmation] |
| `mount -n -o remount /` | Смена mount state корня в rescue контексте | `mount` | [Needs confirmation] |
| `mount -a`, редактирование `/etc/fstab` | Множество mountpoints или постоянная конфигурация | `mount` | [Needs confirmation] |
| `sync` | Сброс буфера записи на диск | Прямой тест завершения не дан | [Not applicable] |

Автор предупреждает: `fdisk` применяет запись без дополнительного вопроса при `w` (PDF 111); `mkfs` уничтожает данные существующей FS (117); `mount -a` может затронуть многие точки (123).

## State-changing: repair, swap, LVM

| Команда или семейство | Эффект / риск | Проверка | Rollback |
|---|---|---|---|
| `fsck`/`e2fsck` с исправлением, `fsck -p/-y` | Меняет inode/superblock и directory structures; риск разрушить данные | Только демонтированная FS, `fsck -n` | [Needs confirmation] |
| `fsck -b num` | Использует backup superblock | Требуется достоверный адрес резервного блока | [Needs confirmation] |
| `mkswap` / `swapon` / `swapoff` | Перезапись swap signature, изменение active swap | `free` | [Needs confirmation] |
| `dd` + `mkswap` + `swapon` (swap-файл) | Создаёт файл и активирует подкачку | `free`; параметры и права файла [Needs confirmation] | [Needs confirmation] |
| `vgcreate`, `vgextend`, `lvcreate` | Создание PV/VG/LV, изменение LVM метаданных | `pvs/vgs/lvs`, `vgdisplay` | [Needs confirmation] |
| `lvremove` | Удаляет LV и его содержимое; опасный неверный синтаксис | `lvs`, `vgs` | [Needs confirmation] |
| `lvresize`, `fsadm resize`, `lvresize -r` | Resize тома и FS, разная последовательность при grow/shrink | `lvs`, `df` | [Needs confirmation] |
| `mkdir`, `echo > file`, `ln`, `rm` (inodes) | Меняют имена и link count в опыте | `ls -i`, `stat` | [Needs confirmation] |

**Высокий риск:** `lvremove myvg/mylv2` (PDF 144) и ввод с пробелом вместо `/` могут затронуть **несколько LV**; не использовать как готовое действие. При сокращении FS сначала требуется подходящее уменьшение файловой системы, а не обратный порядок увеличения (PDF 145). `fsck` на mounted RW FS автор прямо запрещает (PDF 127).

## Именованные сущности и предел применения

`/proc/partitions`, `/sys/block`, `/etc/fstab`, `/dev/dm-*`, `/dev/mapper`, `/proc`, `/sys`, `lost+found` — интерфейсы и пути, не отдельные shell-команды. `tune2fs(8)`, `mke2fs(8)` упомянуты как справочная документация, но дополнительные флаги здесь не придумываются.

**Source anomalies:** разное имя устройства у текста и `mkfs` команды (117), повторение UUID в выводе `blkid` (119), расхождение имён VG (141). См. `source-findings.md`; ни один вариант не исправлен по памяти.
