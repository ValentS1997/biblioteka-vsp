# Команды главы 20

Только команды и формы команд, подтвержденные RAG главы 20.

## Discovery / read-only

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| mount | Показать текущие mount points | новый/существующий disk не смонтирован с неожиданными options | read-only |
| lsblk | Показать block devices Linux | size/device topology, новый диск | read-only |
| lsblk -o +MODEL,SERIAL | Добавить model/serial к lsblk | точная идентичность диска перед изменениями | read-only |
| geom disk list | Показать disks FreeBSD | device name/size и отсутствие ошибочной идентификации | read-only |
| hdparm -I <device> | Получить подробную информацию physical disk | model/firmware/capabilities; только physical/non-virtualized context | read-only |
| camcontrol devlist | Показать FreeBSD CAM devices | physical devices и адресация | read-only |
| smartctl | Interactive/scripted SMART query tool | exact options в главе не указаны: [Needs confirmation] | read-only |
| vgdisplay <VG> | Показать LVM volume group | free extents/size/status | read-only |
| lvdisplay | Проверить logical volumes/snapshots | snapshot state и active/inactive status | read-only |
| cat /proc/mdstat | Показать Linux md arrays и rebuild state | degraded state, recovery/rebuild progress | read-only |
| mdadm --detail --scan | Вывести current RAID ARRAY definitions | UUID/name/metadata для documentation | read-only |
| df -h <mountpoint> | Проверить filesystem size/use | ожидаемый размер после resize/mount | read-only |
| blkid | Определить filesystem UUID | stable identity для fstab | read-only |
| swapon -s | Показать active Linux swap | active swap devices | read-only |
| swapctl -l | Показать active FreeBSD swap | active swap devices | read-only |
| zpool list | Показать ZFS pools | size/free/health | read-only |
| zpool status <pool> | Показать ZFS vdev topology и errors | ONLINE/degraded state, READ/WRITE/CKSUM | read-only |
| zfs list -r <dataset> | Показать dataset hierarchy | used/available/refer/mountpoint | read-only |
| zfs get all <dataset> | Показать properties и inheritance source | local/inherited/default properties | read-only |
| btrfs filesystem usage <mountpoint> | Показать Btrfs device/block-group usage | allocated/unallocated/profile usage | read-only |

## Partition / filesystem creation

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo fdisk <disk> | Создать/изменить Linux partition table interactively | exact target disk verified before write; GPT/partition layout | state-changing |
| sudo mkfs -t ext4 -L <label> <partition> | Создать ext4 filesystem | correct partition, label and resulting filesystem | state-changing |
| sudo mkdir <mountpoint> | Создать mount point | path is intended | state-changing |
| sudo mount LABEL=<label> <mountpoint> | Смонтировать filesystem по stable label | correct filesystem mounted at intended path | state-changing |
| sudo gpart create -s GPT <disk> | Создать GPT table FreeBSD | exact disk identity; new GPT exists | state-changing |
| sudo gpart add -l <label> -t freebsd-ufs -a 1M <disk> | Создать FreeBSD UFS partition | partition label/type/alignment | state-changing |
| sudo newfs -L <label> <partition> | Создать UFS filesystem | correct partition and filesystem label | state-changing |

Перед любой командой partition/mkfs: повторно сверить model, serial, size и отсутствие нужных данных. Universal rollback после записи partition table или mkfs: [Needs confirmation].

## Secure erase — необратимо

~~~bash
sudo hdparm --user-master u --security-set-pass <password> <device>
[Needs confirmation: в RAG OCR второй hdparm token отображён как --security-set-erase; exact destructive syntax не нормализуется без дополнительного source evidence]
sudo camcontrol security <disk> -U user -s <password> -e <password>
~~~

Тип: state-changing, destructive.

Effect: уничтожение данных на накопителе.

Precondition:
- device identity проверена;
- данные больше не нужны либо существует проверенная резервная копия;
- точное hardware behavior подтверждено.

Rollback: отсутствует / [Needs confirmation].

## LVM2

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo pvcreate <partition> | Инициализировать LVM physical volume | correct partition; PV created | state-changing |
| sudo vgcreate <VG> <PV> | Создать volume group | VG size/free extents | state-changing |
| sudo vgdisplay <VG> | Проверить volume group | free extents before allocation | read-only |
| sudo lvcreate -L <size> -n <LV> <VG> | Создать logical volume | intended size/name | state-changing |
| sudo lvcreate -L <size> -s -n <snap> <VG>/<LV> | Создать LVM snapshot | snapshot size and active state | state-changing |
| sudo umount <mountpoint> | Размонтировать filesystem | no required active use | state-changing |
| sudo lvchange -an <VG>/<LV> | Деактивировать LV | LV inactive before operation requiring it | state-changing |
| sudo lvresize -L +<size> <VG>/<LV> | Увеличить LV | intended new LV size | state-changing |
| sudo lvchange -ay <VG>/<LV> | Активировать LV | LV active | state-changing |
| sudo resize2fs <LV-device> | Расширить ext filesystem до размера device | filesystem resized successfully | workload-generating |
| xfs_growfs <filesystem> | Расширить XFS | filesystem must be mounted; resulting size | workload-generating |
| growfs <filesystem> | Расширить UFS | resulting filesystem size | workload-generating |

Source ordering:
- grow: volume first, filesystem second;
- shrink: filesystem first, volume second.

Snapshot risk: если allocated snapshot space закончится, snapshot перестает быть usable.

## Linux md RAID

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo mdadm --create /dev/md/<name> --level=5 --raid-devices=3 <p1> <p2> <p3> | Создать RAID5 array | correct components; /proc/mdstat; rebuild progress | workload-generating |
| cat /proc/mdstat | Monitor md state | [UU_]-style state, recovery/rebuild progress | read-only |
| sudo mdadm --detail --scan | Получить ARRAY line для mdadm.conf | logical name/UUID/metadata | read-only |
| sudo mdadm -S /dev/md/<name> | Остановить array | array stopped safely | state-changing |
| sudo mdadm -As /dev/md/<name> | Активировать documented array | array assembled/active | state-changing |
| sudo mdadm /dev/md/<name> -f <component> | Пометить component failed | array enters expected degraded state | state-changing |
| sudo mdadm /dev/md/<name> -r <component> | Удалить failed component | device removed from array | state-changing |
| sudo mdadm /dev/md/<name> -a <component> | Добавить/re-add component | rebuild starts; monitor /proc/mdstat | workload-generating |
| sudo systemctl enable mdmonitor | Включить md monitoring на показанных distributions | monitor service enabled | state-changing |

Rebuild может занимать часы/дни. RAID продолжает обслуживать I/O в degraded state, поэтому monitoring обязателен.

## Traditional filesystems / fstab / swap

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| fsck <filesystem> | Проверка/исправление filesystem | exact filesystem and repair impact | state-changing |
| sudo mount <device> <mountpoint> | Смонтировать filesystem | correct source/target/options | state-changing |
| sudo mount -a -t ext4 | Смонтировать ext4 entries из fstab | fstab entries valid; expected mounts | state-changing |
| umount <mountpoint> | Размонтировать filesystem | no active users/processes | state-changing |
| gpart show -l <disk> | Показать GPT partition labels FreeBSD | stable partition identity | read-only |
| gpart modify -i <index> -l <label> <disk> | Изменить GPT partition label | correct partition index/label | state-changing |
| tunefs -p <device> | Показать UFS label/properties | current label | read-only |
| tunefs -L <label> <device> | Установить UFS label | filesystem unmounted first | state-changing |
| e2label | Читать/задавать ext filesystem label | exact invocation в главе не приведена: [Needs confirmation] | state-changing |
| xfs_admin | Читать/задавать XFS administrative label | exact invocation в главе не приведена: [Needs confirmation] | state-changing |
| mkswap <device> | Инициализировать Linux swap area | correct device; UUID created | state-changing |
| swapon <device> | Включить swap | device active afterwards | state-changing |
| swapon -s | Показать active swap | expected swap devices | read-only |

Для fstab source рекомендует UUID/LABEL/PARTUUID/PARTLABEL вместо непостоянного /dev/sdX.

## ZFS

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo zpool create <pool> <device> | Создать pool | pool created/auto-mounted root dataset | state-changing |
| sudo zpool add <pool> <vdev...> | Добавить vdev | redundancy design and zpool status | state-changing |
| sudo zpool add -f <pool> <vdev...> | Force add despite replication-level warning | only intentional design; topology verified | state-changing |
| zpool list | Показать pools | capacity/health | read-only |
| zpool status <pool> | Показать vdevs/errors | ONLINE and zero unexpected errors | read-only |
| sudo zpool destroy <pool> | Уничтожить pool | destructive; exact pool confirmed | state-changing |
| sudo zfs create <pool>/<dataset> | Создать dataset | auto-mount/path/list output | state-changing |
| zfs list -r <pool> | Показать dataset hierarchy | used/available/mountpoint | read-only |
| sudo zfs set <property>=<value> <dataset> | Изменить property | effective/inherited value | state-changing |
| zfs get all <dataset> | Проверить properties | SOURCE and effective values | read-only |
| sudo zfs snapshot <dataset>@<snap> | Создать snapshot | snapshot exists/content accessible | state-changing |
| sudo zfs snapshot -r <dataset>@<snap> | Recursive snapshots | per-child snapshots exist | state-changing |
| sudo zfs rollback <dataset>@<snap> | Откатить dataset | target is allowed/latest snapshot context | state-changing |
| sudo zfs clone <dataset>@<snap> <clone> | Создать writable clone | clone dataset exists | state-changing |
| zfs destroy <snapshot-or-dataset> | Удалить ZFS object | dependencies/clones understood | state-changing |

Critical:
- zpool destroy/zfs destroy are destructive;
- zfs rollback may require removal of newer snapshots;
- exact rollback of destroy operations: [Needs confirmation].

## Btrfs

| Команда | Назначение | Что проверить | Тип |
|---|---|---|---|
| sudo mkfs.btrfs -L <label> -d raid1 <dev1> <dev2> | Создать Btrfs filesystem/pool | label/devices/profile | state-changing |
| sudo mount LABEL=<label> <mountpoint> | Mount Btrfs | expected filesystem mounted | state-changing |
| sudo btrfs filesystem usage <mountpoint> | Показать allocation/profile usage | device sizes, RAID profile, unallocated space | read-only |
| sudo btrfs device add <device> <mountpoint> | Добавить disk в mounted filesystem | new device appears in usage output | state-changing |
| sudo btrfs balance start --full-balance <mountpoint> | Перераспределить chunks | balance completes; usage redistributed | workload-generating |
| sudo btrfs balance start -dconvert=<profile> -mconvert=<profile> <mountpoint> | Изменить data/metadata RAID profile | conversion completes; new profiles visible | workload-generating |
| sudo btrfs subvolume create <path> | Создать subvolume | subvolume path exists | state-changing |
| sudo mount LABEL=<label> -o subvol=<path> <mountpoint> | Mount specific subvolume | intended subvolume visible | state-changing |
| sudo btrfs subvolume snapshot <src> <dst> | Создать writable snapshot | destination snapshot exists | state-changing |
| sudo btrfs subvolume snapshot -r <src> <dst> | Создать read-only snapshot | snapshot read-only | state-changing |

Btrfs balance and RAID conversion move existing extents and can generate substantial I/O. Universal rollback: [Needs confirmation].

## Backup

Chapter-specific command sequence for backup is not prescribed.

Acceptance is process-based:
- backup scope documented;
- storage location documented;
- encryption/key ownership documented;
- retention documented;
- access owners documented;
- restore procedure tested regularly.
