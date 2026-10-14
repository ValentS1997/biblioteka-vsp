# Подтверждённые команды, настройки и PromQL — глава 7

**Источник:** PDF 131–143 (`p0131:c01`–`p0143:c01`); `rag_only`. **Ничего не запускалось.** Версии примеров: Node Exporter 1.4.0 / Linux 5.18.0 (PDF 132). `read-only` — запросы/просмотр, `state-changing` — запуск и модификация файлов/конфигурации, `workload-generating` — создание работой дополнительной нагрузки. Достоверность команд в текущей ОС [Needs confirmation].

## Read-only: диагностика

| Команда/метрика из RAG | Назначение | PDF |
| --- | --- | --- |
| `df`, `df -i` | Файловые системы / inode | 133–134 |
| `iostat -x` | Системное представление интенсивности I/O, сравниваемое в книге с метрикой диска | 135 |
| `sensor` | В книге это название команды получения температур, фактическая доступность программы [Needs confirmation] | 136 |
| `/metrics` | HTTP-путь для чтения доступных метрик Node Exporter | 132, 142 |
| `/proc/diskstats`, `/proc/meminfo`, `/proc/stat` | Источники метрик ядра; это пути, **не команды** | 134, 136–137 |

## PromQL (все read-only относительно хранилища метрик)

```promql
avg without(cpu, mode)(rate(node_cpu_seconds_total{mode="idle"}[1m]))
```
**PDF 133:** средняя доля времени простоя по процессорам.

```promql
avg without(cpu)(rate(node_cpu_seconds_total[1m]))
```
**PDF 133:** доли CPU-time по mode, агрегированные по cpu.

```promql
node_filesystem_avail_bytes / node_filesystem_size_bytes
```
**PDF 134:** по семантике `avail_bytes` это **доля доступного пространства**. Рядом в тексте упомянуто «используемое» пространство, что противоречит формуле; оригинальная формула не исправляется, см. [source-findings.md](source-findings.md).

```promql
rate(node_disk_io_time_seconds_total[1m])
```
**PDF 135:** время I/O за секунду (приближённая интенсивность).

```promql
rate(node_disk_read_time_seconds_total[1m])
/
rate(node_disk_reads_completed_total[1m])
```
**PDF 135:** среднее время чтения I/O.

```promql
rate(node_network_receive_bytes_total[1m])
```
**PDF 135:** скорость приёма байтов сетевого устройства по его метке `device`.

```promql
node_hwmon_temp_celsius
* ignoring(label) group_left(label)
node_hwmon_sensor_label
```
**PDF 137:** обогащение температурного ряда именем сенсора; исходная формулировка приведена без добавления иных operators.

```promql
time() - node_boot_time_seconds
```
**PDF 137:** длительность работы ядра (секунды).

```promql
count by(release)(node_uname_info)
```
**PDF 138:** количество машин по kernel release.

```promql
count by(name, version)(node_os_info)
```
**PDF 138:** количество машин по названию и версии дистрибутива.

```promql
rate(node_pressure_memory_waiting_seconds_total[1m])
```
**PDF 140:** скорость счётчика memory waiting PSI.

`node_textfile_mtime_seconds` — Gauge с временем успешного прочтения файла, **не команда** (PDF 143). Конкретного порога устаревания в главе нет.

## Изменяющие настройки флаги (PDF 132, 141)

| Флаг | Класс | Эффект, проверка, откат |
| --- | --- | --- |
| `--collector.wifi` | state-changing (конфигурация запуска) | Включает Wi-Fi collector; проверить метрики. Rollback [Needs confirmation]. |
| `--no-collector.wifi` | state-changing (конфигурация запуска) | Отключает Wi-Fi collector; может убрать ряды. Rollback [Needs confirmation]. |
| `--collector.disable-defaults` | state-changing (конфигурация запуска) | Выключает все default collectors кроме явно включённых. Rollback [Needs confirmation]. |
| `--path.procfs`, `--path.rootfs`, `--path.sysfs` | state-changing (Docker-конфигурация запуска) | Настройка доступа к хостовым FS; полную Docker-команду глава не содержит. Rollback [Needs confirmation]. |
| `--collector.textfile.directory` | state-changing (конфигурация запуска) | Задаёт выделенный каталог `.prom`; нужен для textfile collector. Rollback [Needs confirmation]. |
| `psi=1` | state-changing (параметр загрузки ядра) | Включение PSI, если поддерживается и выключен; процедура установки/отката [Needs confirmation]. |

## Textfile collector: исходный учебный пример 7.1 (PDF 142)

**State-changing (файлы и демон):** следующие команды создают локальный каталог/файл и запускают Node Exporter. Требуют проверки `$PWD`, порта и существующих данных; приводятся для анализа, **не исполнялись**.

```sh
mkdir textfile
echo example_metric 1 > textfile/example.prom
./node_exporter --collector.textfile.directory=$PWD/textfile
```

**Содержимое файла `textfile/example.prom`:**
```text
example_metric 1
```

**Ожидаемый exposition по книге, PDF 142:**
```text
# HELP example_metric Metric read from /some/path/textfile/example.prom
# TYPE example_metric untyped
example_metric 1
```

Реальный путь в `HELP` зависит от места хранения и не должен копироваться буквально как обещание среды. Команда запускает процесс (изменяет состояние системы), `mkdir` и redirection `>` изменяют ФС. Проверка: `/metrics` содержит `example_metric`. Rollback: [Needs confirmation].

## Cron и атомарная запись (PDF 142) — привилегированный учебный пример

**State-changing / workload-generating. Не копировать в `/etc/crontab` без отдельной процедуры безопасности.** Пример использует root для чтения `/etc/shadow` и считает непустые строки, **не отображая пароли или их хеши**. Но доступ к этому файлу чувствителен, а неправильный путь или разрешения могут создать утечку данных или ошибку работы.

**Оригинальная последовательность RAG:**
```text
TEXTFILE=/path/to/textfile/directory
# Весь следующий код должен быть набран в одну строку
*/5 * * * * root (echo -n 'shadow_entries '; grep -c . /etc/shadow)
    > $TEXTFILE/shadow.prom.$$
    && mv $TEXTFILE/shadow.prom.$$ $TEXTFILE/shadow.prom
```

RAG переносит строку cron; автор указывает, что действие должно быть одной строкой. Для сохранения provenance выше воспроизведена структура RAG, **а не копируемая рабочая crontab-запись**. `$$` в оболочке означает PID; `mv` внутри той же файловой системы использует атомарное переименование (PDF 142). Не выполнять до подтверждения `TEXTFILE`, доступа, владельца, файловой системы и rollback [Needs confirmation].

## Эксплуатационные предупреждения

- Нельзя помещать explicit timestamps в `.prom` для textfile collector (PDF 143).
- Он читает только `.prom`, и одинаковая метрика во многих файлах должна иметь одинаковую `HELP`; иначе ошибка (PDF 141–142).
- Не использовать textfile collector как замену pull-мониторинга приложений. Для service-level batch применять Pushgateway, описанный в главе 4 (PDF 141).
- Все флаги и пути соответствуют изложению Node Exporter 1.4.0. Совместимость с текущим узлом **не подтверждена**.
