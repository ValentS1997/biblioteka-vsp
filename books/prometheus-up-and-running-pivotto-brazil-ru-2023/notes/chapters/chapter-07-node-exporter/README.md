# Глава 7. Node Exporter

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023, русское издание).  
**Inventory:** `0040`. **Book ID:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED` до целевой валидации и review.  
**Источник:** строго `rag_only`: только канонический RAG, без прямого PDF, интернета или данных из памяти модели.

## Граница и происхождение

- Начало: PDF **131**, `p0131:c01`, заголовок «Глава 7. Node Exporter».
- Конец: PDF **143**, `p0143:c01`; на PDF **144** (`p0144:c01`) начинается глава 8 «Обнаружение служб».
- **PDF-страницы:** 131–143; **печатные:** 131–143 согласно заголовкам RAG. **source locator:** `pdf_page=131..143`.
- **Объём:** 13 страниц, 13 чанков `p0131:c01`–`p0143:c01` в `rag/chunks/p0101-p0200/pNNNN-c01.md`.
- **SHA256 исходника:** `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. `rag/acceptance.yaml: ACCEPTED`; manifest корпуса: `READY_WITH_KNOWN_LIMITATIONS`.
- Границы сверены по самим чанкам, не только по оглавлению.

## Карта главы

| Раздел | PDF | Метрики и назначение |
| --- | --- | --- |
| Обзор Node Exporter | 131–132 | Уровень Unix-узла, не приложений; непривилегированный пользователь, коллекторы, /metrics, пример 1.4.0 и Linux 5.18.0 |
| CPU | 132–133 | `node_cpu_seconds_total{cpu,mode}`, `node_cpu_guest_seconds_total`, доли через `rate` |
| Файловая система | 133–134 | `node_filesystem_*{device,fstype,mountpoint}`, размер, доступность, inode; `df` / `df -i` |
| Диски | 134–135 | `node_disk_*{device}`: операции, время, байты, интенсивность, среднее время чтения |
| Сеть | 135 | `node_network_receive_bytes_total`, `node_network_transmit_bytes_total`, пакеты |
| Память | 136 | `node_memory_*` из `/proc/meminfo`, свободно / кэш / available |
| Аппаратные датчики | 136–137 | `node_hwmon_*`, температура и сенсорная метка через `group_left` |
| Stat, uname, OS | 137–138 | uptime, прерывания, forks, context switches, `node_uname_info`, `node_os_info` |
| Средняя нагрузка и PSI | 139–140 | `node_load{1,5,15}`, `node_pressure_*` waiting/stalled |
| Textfile collector | 140–143 | Каталог `.prom`, cron, атомарное переименование, `node_textfile_mtime_seconds`, timestamps |

## Основные принципы

1. **Node Exporter — не агент наблюдения за каждым процессом.** Он экспортирует метрики машины. Для служб Prometheus должен отдельно собирать их собственные метрики (PDF 131, 141).
2. **Привилегии и размещение:** по книге Node Exporter работает без root как сервис на узле. Контейнерная установка возможна, но требует корректного доступа к файловым системам хоста через `--path.procfs`, `--path.sysfs`, `--path.rootfs`; готовой Docker-команды глава не даёт (PDF 132).
3. **Семантика важнее названия.** `node_filesystem_avail_bytes` описывает пространство, доступное пользователям, в отличие от `free_bytes` с резервом для root; `MemFree` отличается от фактически доступной памяти; `node_load*` не равны просто загрузке CPU (PDF 133–139).
4. **Источниковые запросы сначала требуют нормализации Counter через `rate`.** Примеры охватывают CPU idle, диск, сетевые байты, память под давлением и дополнительные метки hardware sensors (PDF 133–140).
5. **PSI измеряет ожидание ресурсов:** waiting и stalled для памяти/I/O; CPU — waiting, см. `rate(node_pressure_memory_waiting_seconds_total[1m])` (PDF 139–140).
6. **Textfile collector дополняет именно машинные метрики.** Отдельный job может атомарно записывать файл `.prom` и экспортировать его через Node Exporter, не заставляя Node Exporter выполнять привилегированные команды. Batch уровня службы относится к Pushgateway (PDF 140–143).

## Важные ограничения

- Примеры отражают **Node Exporter 1.4.0**, **Linux 5.18.0** (PDF 132). Наличие отдельных метрик и флагов зависит от платформы и версии; действующая установка не проверялась.
- Исходный текст на PDF 134 говорит об используемом дисковом пространстве рядом с `node_filesystem_avail_bytes / node_filesystem_size_bytes`, то есть с отношением **доступного** пространства. Точная исходная формулировка сохранена без исправления в [source-findings.md](source-findings.md).
- На PDF 136 в описании `node_memory_MemAvailable` опущен суффикс `_bytes` относительно соглашения соседних метрик, при этом точное имя не подтверждено другим примером в этой главе; запись помечена [Needs confirmation] и не выдаётся за рабочий селектор.
- В примере cron PDF 142 читается `/etc/shadow` с привилегиями root; задача показана только для анализа, **не выполнялась** и не предлагается как безопасная без локальной оценки доступа и утечек. Конкретная процедура rollback в книге отсутствует.
- Из 7-й главы не получены самостоятельные мультимодальные объекты. SVG ниже — построенные по RAG карты, не реконструкции графиков издательства.
- Явного отдельного итогового summary, контрольных вопросов и упражнений в PDF 131–143 нет. Условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — чек-лист наблюдения, интерпретация и безопасные действия.
- [commands.md](commands.md) — подтверждённые команды, флаги, выражения PromQL с классификацией.
- [diagram.md](diagram.md) — схема сбора и выбора источников для machine/batch-метрик.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная карта.
- [source-findings.md](source-findings.md) — проблемы источника и ограничения.

**Reading progress и канонический источник не меняются.**
