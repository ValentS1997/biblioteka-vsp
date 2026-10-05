# Команды и интерфейсы главы 4

Ниже только команды, явно подтверждённые RAG главы 4. State-changing storage operations помечены отдельно.

| Команда / интерфейс | Назначение | Тип | Risk / verification |
|---|---|---|---|
| `parted -l` | Просмотреть partition tables | read-only | Базовый inventory MBR/GPT |
| `fdisk -l` | Просмотреть partition data | read-only | Обратить внимание на sector size |
| `journalctl -k` | Kernel messages о block devices/partitions | read-only | Сопоставить kernel view |
| `blockdev --rereadpt DEVICE` | Заставить kernel перечитать partition table | state-changing | Только после подтверждённого изменения table |
| `fdisk DEVICE` | Интерактивное редактирование partition table | state-changing | Backup + target unused; запись происходит только после явного save |
| `cat /sys/block/.../start` | Проверить стартовый sector partition | read-only | Используется для SSD alignment |
| `ls -l /sbin/mkfs.*` | Просмотреть filesystem-specific mkfs tools | read-only | Показывает wrappers/symlinks |
| `mkfs -t ext4 DEVICE` | Создать ext4 filesystem | state-changing | Destructive: уничтожает прежнюю filesystem/data |
| `mount` | Показать mounted filesystems | read-only | Device, mountpoint, type, options |
| `mount -t TYPE DEVICE MOUNTPOINT` | Смонтировать filesystem | state-changing | Проверить target mountpoint и filesystem |
| `umount MOUNTPOINT` | Размонтировать filesystem | state-changing | Kernel синхронизирует buffered changes |
| `blkid` | Показать UUID и filesystem type | read-only | Stable identity вместо device name |
| `mount UUID=... MOUNTPOINT` | Mount по filesystem UUID | state-changing | Проверить UUID через blkid |
| `sync` | Сбросить buffered writes на disks | state-changing | Используется перед shutdown, если umount невозможен |
| `mount -o ...` | Задать mount options | state-changing | В главе: ro/rw, exec/noexec, suid/nosuid и др. |
| `mount -n -o remount /` | Remount root в recovery context | state-changing | Специальный operational сценарий |
| `mount -a` | Mount entries из fstab, кроме noauto | state-changing | Проверять fstab до запуска |
| `df`, `df DIR` | Capacity/usage filesystem | read-only | Проверка свободного места |
| `du`, `du -s` | Usage directory tree | read-only | Ищет, где занято место |
| `fsck DEVICE` | Проверить/восстановить filesystem | state-changing | Никогда не на mounted FS, кроме оговорённого read-only root case |
| `fsck -n DEVICE` | Проверка без изменений | read-only | Предпочтительный первый check при подозрении на серьёзную ошибку |
| `fsck -b NUM DEVICE` | Использовать backup superblock | state-changing | Recovery operation |
| `mkfs -n DEVICE` | Показать backup superblock locations без создания FS | read-only | Критично не потерять `-n` |
| `e2fsck -fy DEVICE` | Проверка ext3/ext4 с journal handling | state-changing | Repair path; требует verified target/offline state |
| `free` | Показать memory/swap usage | read-only | Swap baseline |
| `mkswap DEV_OR_FILE` | Добавить swap signature | state-changing | Target должен быть предназначен под swap |
| `swapon DEV_OR_FILE` | Добавить swap в kernel pool | state-changing | Проверить free/usage |
| `swapoff DEV_OR_FILE` | Удалить swap из pool | state-changing | Нужна достаточная оставшаяся память |
| `pvs` / `pvdisplay` | Просмотр LVM Physical Volumes | read-only | PV/VG/PE/UUID |
| `vgs` / `vgdisplay` | Просмотр Volume Groups | read-only | VSize/VFree/PV/LV |
| `lvs` / `lvdisplay` | Просмотр Logical Volumes | read-only | LV path/size/status |
| `pvscan` | Пересканировать LVM PV | read-only/discovery | Источник предлагает при непоявившихся изменениях |
| `vgcreate` | Создать VG и при необходимости PV | state-changing | Меняет LVM metadata |
| `vgextend` | Добавить PV в VG | state-changing | Проверить target PV |
| `lvcreate` | Создать LV | state-changing | Проверить VG free extents |
| `lvremove` | Удалить LV | state-changing | High risk; source отдельно предупреждает о синтаксисе |
| `lvresize` | Изменить размер LV | state-changing | Координировать с filesystem size |
| `fsadm resize` | Изменить размер filesystem | state-changing | Использует filesystem-specific tools |
| `dmsetup info` | Показать device mapper devices | read-only | Kernel mapping state |
| `dmsetup table` | Показать mapping table | read-only | Связь LV с physical extents |
| `ls -i` | Показать inode numbers | read-only | Используется в разделе 4.6 |
| `stat` | Подробная inode/file metadata | read-only | Упомянут как более подробный check |

## Source safety boundaries

### Partitioning
Источник требует backup важных данных и отсутствие использования target partitions перед изменением table.

### mkfs
Создание filesystem поверх существующей структуры уничтожает старые данные.

### fsck
Источник прямо запрещает fsck на mounted filesystem, кроме read-only root в специальном recovery mode.

### LVM
`lvremove` может удалить не тот scope при ошибочном синтаксисе. Удаляемый LV должен быть неиспользуемым, а важные данные — заранее перемещены или сохранены.

### Resize
Размер LV и размер filesystem — два разных состояния. Нельзя считать, что изменение одного автоматически безопасно меняет другое.

### Swap
Перед `swapoff` система должна иметь достаточно оставшейся памяти для активных pages.

## Концептуальные интерфейсы

- VFS — общий kernel interface разных filesystem implementations.
- Device Mapper — kernel mapping layer под LVM.
- inode table + directory entries + block allocation metadata — внутренняя структура традиционной Unix filesystem.
