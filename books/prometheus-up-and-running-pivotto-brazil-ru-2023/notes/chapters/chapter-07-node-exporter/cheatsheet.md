# Cheatsheet — Node Exporter (глава 7)

**Provenance:** PDF 131–143; RAG `p0131:c01`–`p0143:c01`. Примеры книги: Node Exporter 1.4.0 / Linux 5.18.0. Точные версии и значения рабочей машины: [Needs confirmation].

## Symptom / problem framing

- Метрик CPU/диска/сети нет или они непонятны: проверить `/metrics` и поддерживаемые коллекторы ОС (PDF 132–135).
- Неверно интерпретируется свободное место: `avail_bytes` предназначен обычным пользователям, `free_bytes` может включать резерв для root; в формуле доступной доли есть mismatch исходного пояснения (PDF 133–134).
- `MemFree` невелик, но реальная доступность памяти неизвестна: учесть кэш и буферы, а на подходящих ядрах эвристику `MemAvailable` (PDF 136).
- Неясно, какой ресурс перегружен: PSI-метрики дают ожидание CPU/memory/I/O, `node_load1/5/15` имеют другую семантику (PDF 139–140).
- Cron создаёт неполные `.prom` при scrape: использовать временный файл и атомарный `rename` в пределах одной файловой системы (PDF 142).
- Собственные метрики от пакетного задания не видны: различить machine-level batch (textfile) и service-level batch (Pushgateway) (PDF 141).

## Baseline / context

- Node Exporter экспортирует **узел**, не процессы/приложения; обычно его запускают без root напрямую как сервис Unix-хоста (PDF 131–132).
- На Docker-хосте контейнерная изоляция мешает чтению хостовых `/proc`/`/sys`; в главе лишь флаги `--path.procfs`, `--path.rootfs`, `--path.sysfs`, не полный compose/run (PDF 132).
- По книге можно включать/выключать категории `--collector.wifi` / `--no-collector.wifi`; `--collector.disable-defaults` снимает набор по умолчанию (PDF 132).
- CPU: `node_cpu_seconds_total{cpu,mode}`; диск: `node_disk_*`; сеть: `node_network_*`; FS: `node_filesystem_*`; память: `node_memory_*` (PDF 132–136).
- PSI требует поддержки ядра и может зависеть от `psi=1` при загрузке (PDF 139); эту настройку ядра нельзя менять без локальной процедуры.

## Read-only checks

1. Просмотреть доступные метрики `/metrics`, поскольку набор зависит от версии Node Exporter и ядра (PDF 132).
2. `avg without(cpu, mode)(rate(node_cpu_seconds_total{mode="idle"}[1m]))` — средняя доля CPU idle; `avg without(cpu)(rate(node_cpu_seconds_total[1m]))` — доли по режимам (PDF 133).
3. `df -i` — inode для FS; `node_filesystem_avail_bytes / node_filesystem_size_bytes` — **доля доступного** пространства по семантике метрик, несмотря на текстовое несоответствие RAG (PDF 133–134).
4. `rate(node_disk_io_time_seconds_total[1m])` и `rate(node_disk_read_time_seconds_total[1m]) / rate(node_disk_reads_completed_total[1m])` — интенсивность I/O и среднее время чтения (PDF 135).
5. `rate(node_network_receive_bytes_total[1m])` — входящие байты/с; аналогичные counters для отправки и пакетов перечислены на PDF 135.
6. `time() - node_boot_time_seconds` — время с запуска ядра; `count by(release)(node_uname_info)`, `count by(name, version)(node_os_info)` — состав узлов (PDF 137–138).
7. `rate(node_pressure_memory_waiting_seconds_total[1m])` — доля времени ожидания из счётчика PSI (PDF 139–140).
8. `node_textfile_mtime_seconds` — время изменения успешно прочитанного `.prom`; старый mtime может означать остановку задания cron (PDF 143).

## Interpretation

- Счётчики CPU/disk/network/PSI обычно исследуют через `rate`, а текущее `node_disk_io_now` — Gauge. Ряд `node_cpu_guest_seconds_total` уже пересекается с user/nice, суммирование может задвоить вклад (PDF 133–135).
- `node_memory_MemFree_bytes` не равно доступной для приложений памяти; CPU load включает и задачи в непрерываемом ожидании I/O (PDF 136, 139).
- `node_hwmon_temp_celsius` можно обогатить меткой `label` из `node_hwmon_sensor_label` через `group_left` (PDF 137).
- PSI `waiting` — некоторые задачи ждали, `stalled` — ни одна не продвигалась; для CPU в главе приведено только waiting (PDF 139–140).
- Textfile collector читает только файлы `.prom`, генерирует HELP при отсутствии, но несовпадающий HELP в нескольких файлах для одного имени метрики вызывает ошибку; **явные timestamps в textfile не допускаются** (PDF 141–143).
- `node_textfile_mtime_seconds` позволяет определить свежесть файла; не путать это с заданным пользователем timestamp образца (PDF 143).

## Next action

- Уточнить целевой контекст: метрика принадлежит машине, службе или заданию? Для службы не проксировать всё через один Node Exporter (PDF 131, 141).
- Проверить доступный `/metrics` и наличие нужного коллектора; не обещать одинаковый набор Linux/FreeBSD (PDF 132).
- При дисковых/памятных аномалиях интерпретировать корректные семантические счётчики вместо названий «free» или «load» (PDF 133–140).
- Для machine-level cron создать выделенный каталог текстовых метрик и обеспечить атомарную запись `.prom` (PDF 140–143).

## Modifying action

- Включение/отключение коллекторов флагами Node Exporter меняет доступный набор рядов и последующие запросы; конкретная процедура перезапуска не дана: [Needs confirmation] (PDF 132).
- Запуск `./node_exporter --collector.textfile.directory=$PWD/textfile` читает файлы из выбранного каталога и изменяет работающую конфигурацию экспорта (PDF 141–142).
- Создание каталога и `echo example_metric 1 > textfile/example.prom` меняют файлы; проверить путь и права (PDF 142).
- Исторический cron-пример из `/etc/crontab` считывает **только количество строк** в `/etc/shadow`, но требует root и пишет файл. **Не выполнять** без проверки полномочий/секретности и rollback (PDF 142).
- Включение PSI через параметр ядра `psi=1` — изменение загрузочной конфигурации; конкретный план вмешательства и восстановления: [Needs confirmation] (PDF 139).

## Verification / acceptance checks

- Эндпоинт Node Exporter выдаёт нужные семейства метрик; версии ОС/коллекторов отражаются в фактически полученном `/metrics` (PDF 132).
- Для textfile после примера 7.1 вывод включает `example_metric 1` со сгенерированным HELP/TYPE untyped (PDF 142).
- Файлы имеют расширение `.prom`, записываются атомарным переименованием, в одинаковых метриках из разных файлов совпадает HELP; timestamps отсутствуют (PDF 142–143).
- `node_textfile_mtime_seconds{file="..."}` соответствует последнему успешному обновлению; реальный допустимый возраст файла по SLA: [Needs confirmation] (PDF 143).
- Источниковую строку о «используемом пространстве» не считать доказанной формулой used/size: зарегистрирована в [source-findings.md](source-findings.md).

## Rollback

- Для коллекторов/запуска Node Exporter, PSI и cron точные команды rollback в этой главе не приведены: **[Needs confirmation]**.
- Для учебного `example.prom` обратная процедура требует контроля пути и результатов scrape, но команда удаления источником не показана: [Needs confirmation].
- Для производственной конфигурации и root cron нужна отдельная согласованная процедура резервирования/восстановления; не добавлять команды из памяти модели.
