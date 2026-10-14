# Диаграммы главы 7 — Node Exporter

**Основание:** PDF 131–143, `p0131:c01`–`p0143:c01`. Mermaid иллюстрирует исходный текст, не перенесённые из PDF изображения.

## Архитектура машинных метрик

```mermaid
flowchart LR
    HOST["Unix/Linux host"]
    KERNEL["Kernel: proc/stat, meminfo, diskstats, PSI"]
    NE["Node Exporter<br/>CPU, FS, disk, net, hwmon, OS"]
    TEXT["textfile collector<br/>выделенный каталог .prom"]
    PROM["Prometheus<br/>HTTP pull /metrics"]
    APP["Служба с собственными метриками"]
    HOST --> KERNEL --> NE
    TEXT --> NE
    PROM -->|"scrape"| NE
    PROM -->|"отдельный scrape"| APP
```

RAG PDF 131–132, 140–143. Node Exporter не выполняет shell-команды для сбора привилегированных данных; файлы готовит внешний процесс.

## Какую метрику изучать

```mermaid
flowchart TD
    A["Наблюдаемая проблема на узле"]
    CPU["CPU: node_cpu_seconds_total<br/>rate по режимам"]
    FS["FS: avail_bytes / size_bytes<br/>доля доступного"]
    IO["Disk: io_time, read_time, reads_completed<br/>rate и отношение"]
    NET["Network: receive_bytes_total<br/>rate за 1m"]
    MEM["Memory: MemFree, Cached, Buffers<br/>MemAvailable в тексте"]
    PRESS["PSI: pressure_memory_waiting<br/>rate за 1m"]
    TXT["Cron / machine-level batch<br/>node_textfile_mtime_seconds"]
    A --> CPU
    A --> FS
    A --> IO
    A --> NET
    A --> MEM
    A --> PRESS
    A --> TXT
```

Источник PDF 132–143. Формула FS на PDF 134 имеет несогласованное словесное пояснение, см. [source-findings.md](source-findings.md). Это карта выбора, не автоматическая диагностика.

## Безопасная цепочка textfile collector

```mermaid
flowchart TD
    A["Внешнее задание cron<br/>при необходимости привилегированное"]
    B["Подготовить метрики<br/>Prometheus text format"]
    C["Записать временный файл<br/>в том же каталоге/FS"]
    D["Атомарно переименовать<br/>в *.prom"]
    E["Node Exporter читает<br/>*.prom при scrape"]
    F["Prometheus получает<br/>метрики и mtime"]
    G["Проверить свежесть<br/>node_textfile_mtime_seconds"]
    A --> B --> C --> D --> E --> F --> G
```

Источник PDF 140–143. `/etc/shadow` из учебного примера не требуется для этой общей схемы и не является рекомендацией. Pushgateway применяется к batch уровня службы, а не к машинному textfile.
