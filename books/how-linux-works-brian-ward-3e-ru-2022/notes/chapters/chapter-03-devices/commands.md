# Команды и интерфейсы — глава 3 «Устройства»

**Source:** `p0079:c01`–`p0101:c01`, PDF/печатные страницы 79–101. Команды взяты из главы; подставленные имена носителей являются примерами автора, а не значениями реального сервера.

## Read-only: исследование устройств

| Команда | Назначение | Глава/страница |
|---|---|---:|
| `ls /dev`, `ls -l` | Узлы, права, тип `b/c/p/s`, major/minor | 3.1 / 80–81 |
| `ls -l /sys/block`, `cat dev` | Ссылки на блоки в sysfs и major:minor внутри каталога устройства | 3.2 / 82 |
| `udevadm info --query=all --name=/dev/sda` | Узел, sysfs-путь, символьные ссылки, окружение udev | 3.2, 3.5 / 82,93 |
| `journalctl -k` | Сообщения ядра | 3.4 / 83 |
| `mount` (без аргументов) | Список уже доступных монтирований | 3.4 / 83 |
| `cat /proc/devices` | Major-номера устройств с доступными драйверами | 3.4 / 83–84 |
| `lsscsi` | SCSI-устройства с адресами и именами | 3.4, 3.6 / 84,96 |
| `nvme list` | NVMe-устройства | 3.4.3 / 85 |
| `ls -l /dev/disk/by-id` | Symlinks на текущие узлы дисков | 3.5.1 / 90 |
| `udevadm monitor` | Длительный мониторинг KERNEL и UDEV событий | 3.5.4 / 94 |
| `udevadm monitor --kernel --subsystem-match=scsi` | События ядра подсистемы SCSI | 3.5.4 / 95 |
| `lsscsi -g` | Плюс generic SCSI nodes `/dev/sg*` | 3.6.3 / 100 |
| `lsusb` | Упомянутая утилита USB (полного примера не дано) | 3.6.1 / 99 |

`udevadm monitor --property`, флаги `--kernel` и `--udev` отдельно упомянуты в §3.5.4 для фильтрации или отображения атрибутов. Команды monitor отнесены к **workload-generating observation**, остальные — **read-only**. `cat dev` зависит от `cwd` в sysfs: не применять без подтверждения каталога.

## State-changing: опасные примеры из книги

| Операция | Класс | Эффект и риск | Проверка / rollback |
|---|---|---|---|
| `echo blah blah > /dev/null` | state-changing device I/O | Ядро отбрасывает вывод, `/dev/null` не является диском | Проверка: [Not applicable]; откат: [Not applicable] |
| `dd` (§3.3, `if/of/bs/count/skip`) | state-changing file/device I/O | Копирует блоки в выходной файл; неверный `of` может повредить данные | [Needs confirmation] |
| `mknod` (§3.4.11) | state-changing, privileged | Создаёт device node. Учебный пример с `/dev/sda1` не предназначен для хоста пользователя | [Needs confirmation] |
| `chvt 1` | state-changing console | Переключает tty из привилегированной сессии | Исходная консоль и откат [Needs confirmation] |
| `screen` + serial device | workload-generating / potentially modifying | Интерактивный обмен данными с внешним устройством | Настройка и rollback [Needs confirmation] |
| Редактирование udev rules | state-changing config | Меняет права, ссылки, обработку uevents | Применение/проверка/rollback [Needs confirmation] |
| udevadm trigger/reload | state-changing (возможности инструмента) | Перезагружает правила или инициирует события | Точный синтаксис не дан: [Needs confirmation] |

Глава предупреждает: параметры `dd` в стиле `name=value`; пример из §3.3 пишет **1024 байта** нулей из `/dev/zero` в новый выходной файл. Опасно подменять выходной путь на устройство. Пример `mknod` задаёт блочное устройство major 8, minor 1, но **не** подтверждает эти номера на конкретном сервере.

## Device families — идентификаторы, а не исполняемые команды

| Имя | Объяснение главы |
|---|---|
| `/dev/sd*` | SCSI-подобные диски; имена зависят от обнаружения |
| `/dev/nvme*` | NVMe |
| `/dev/vd*`, `/dev/xvd*` | Виртуальные диски |
| `/dev/dm-*`, `/dev/mapper/*` | Device mapper / LVM |
| `/dev/sr*`, `/dev/sg*` | Optical block и generic SCSI |
| `/dev/tty*`, `/dev/pts/*` | Терминалы и PTY |
| `/dev/ttyS*`, `/dev/ttyUSB*`, `/dev/ttyACM*` | Последовательные порты |
| `/dev/snd/*` | Звук (ALSA) |

## udev / kernel

В §3.5.2 условия имеют `==`, `!=`; действия — `=`, `+=` и `:=`. Механизмы `IMPORT{program}` и `SYMLINK+=` показаны в отрывках с переносами и расхождением `$devnode`/`$tempnode`. **Не использовать эти отрывки как готовую конфигурацию** — см. `source-findings.md`.

**Safety:** сначала установить фактический путь, атрибуты и класс устройства read-only проверками. Изменение сырых устройств без подтверждения цели, проверки и backup/rollback не поддержано главой.
