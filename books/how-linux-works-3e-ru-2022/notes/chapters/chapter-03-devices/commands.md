# Команды и интерфейсы главы 3

Таблица включает только элементы, явно подтверждённые RAG главы 3.

| Команда / интерфейс | Назначение | Тип | Verification / risk / rollback |
|---|---|---|---|
| <code>ls /dev</code> | Показать device nodes | read-only | Использовать как обзор, не как persistent identity |
| <code>ls -l /dev/...</code> | Показать type, permissions, major/minor | read-only | Базовый check device node |
| <code>echo ... &gt; /dev/null</code> | Показать запись в character device | workload-generating | Данные отбрасываются <code>/dev/null</code> |
| <code>ls -l /sys/block</code> | Показать block devices через sysfs links | read-only | Помогает увидеть реальный sysfs path |
| <code>udevadm info --query=all --name=/dev/sda</code> | Связать device node с sysfs/udev attributes | read-only | Проверить P/N/S/E fields |
| <code>dd if=/dev/zero of=new_file bs=1024 count=1</code> | Учебный пример block copy в обычный файл | state-changing | Создаёт/перезаписывает <code>new_file</code>; source предупреждает о высокой опасности неверного output |
| <code>journalctl -k</code> | Kernel messages | read-only | Используется как fallback/discovery evidence |
| <code>cat /proc/devices</code> | Показать зарегистрированные block/character devices и major numbers | read-only | Сопоставлять с <code>ls -l</code> |
| <code>lsscsi</code> | Показать SCSI address, class, vendor и device node | read-only | Сопоставить адрес и <code>/dev</code> |
| <code>nvme list</code> | Показать NVMe devices | read-only | Для <code>/dev/nvme*</code> |
| <code>chvt 1</code> | Переключить virtual console | state-changing | Выполняется от root; можно переключиться обратно на нужную console |
| <code>screen DEVICE</code> | Подключиться к serial terminal/device | workload-generating | Нужны права read/write на device |
| <code>mknod /dev/sda1 b 8 1</code> | Ручное создание block device node | state-changing | Исторический/низкоуровневый механизм; современные системы используют devtmpfs/udev; rollback <code>[Needs confirmation]</code> |
| <code>ls -l /dev/disk/by-id</code> | Persistent symlinks для storage devices | read-only | Предпочтительнее короткого sd-name для идентификации |
| <code>/lib/udev/ata_id --export /dev/sda</code> | Получить ATA attributes для udev rule processing | read-only | Пример из разбора udev rules |
| <code>udevadm monitor</code> | Наблюдать kernel и udev events | read-only | Сравнить KERNEL и UDEV records |
| <code>udevadm monitor --kernel</code> | Только kernel uevents | read-only | Сужает event stream |
| <code>udevadm monitor --udev</code> | Только processed udev events | read-only | Сужает event stream |
| <code>udevadm monitor --udev --property</code> | Processed udev events с attributes | read-only | Полезно для анализа rules |
| <code>udevadm monitor --kernel --subsystem-match=scsi</code> | Только kernel events SCSI subsystem | read-only | Точечное наблюдение |
| <code>lsusb</code> | Показать USB devices/topology | read-only | Аналогичный discovery-инструмент для USB |
| <code>lsscsi -g</code> | Показать обычные и generic SCSI nodes | read-only | Выявляет <code>/dev/sg*</code> |

## Device types из <code>ls -l</code>

| Символ | Тип |
|---|---|
| <code>b</code> | block device |
| <code>c</code> | character device |
| <code>p</code> | named pipe |
| <code>s</code> | Unix-domain socket |

## Параметры dd, описанные в главе

| Parameter | Meaning |
|---|---|
| <code>if=file</code> | input file/stream |
| <code>of=file</code> | output file/stream |
| <code>bs=size</code> | единый block size |
| <code>ibs=size</code> | input block size |
| <code>obs=size</code> | output block size |
| <code>count=num</code> | количество blocks |
| <code>skip=num</code> | пропустить input blocks |

Safety: chapter explicitly warns that <code>dd</code> can easily damage files or device data. No command that writes directly to a real storage device is provided in this artifact.

## udev rule locations

- <code>/lib/udev/rules.d</code> — default rules;
- <code>/etc/udev/rules.d</code> — local overrides.

Условные expressions используют <code>==</code>/<code>!=</code>; directives — <code>=</code>, <code>+=</code>, <code>:=</code>.

## Common device naming

- <code>/dev/sd*</code> — SCSI/SATA/USB storage;
- <code>/dev/xvd*</code>, <code>/dev/vd*</code> — virtual disks;
- <code>/dev/nvme*</code> — NVMe;
- <code>/dev/dm-*</code>, <code>/dev/mapper/*</code> — device mapper;
- <code>/dev/sr*</code> — optical drives;
- <code>/dev/hd*</code> — legacy PATA;
- <code>/dev/tty*</code>, <code>/dev/pts/*</code> — terminals;
- <code>/dev/ttyS*</code>, <code>/dev/ttyUSB*</code>, <code>/dev/ttyACM*</code> — serial;
- <code>/dev/lp*</code> — parallel ports;
- <code>/dev/snd/*</code> — audio;
- <code>/dev/sg*</code> — generic SCSI.

## Safety notes

1. Не считать <code>/dev/sdX</code> постоянной идентичностью устройства.
2. Перед любым state-changing action подтвердить sysfs path и persistent identity.
3. <code>dd</code> — high-risk инструмент; output parameter проверять особенно тщательно.
4. Ручной <code>mknod</code> не является обычным современным workflow при наличии devtmpfs/udev.
5. Правила udev могут менять device setup; chapter analysis не расширяет их редактирование за пределы source.
