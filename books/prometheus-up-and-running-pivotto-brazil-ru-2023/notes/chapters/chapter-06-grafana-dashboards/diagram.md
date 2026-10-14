# Mermaid-схемы главы 6

**Источник:** RAG `p0112:c01`–`p0129:c01` (PDF 112–129). Схемы выведены из текста; оригинальные рисунки 6.1–6.19 не воспроизводятся.

## Поток данных и конфигурирование дашборда

```mermaid
flowchart LR
    NODE["Node Exporter<br/>network, uname"]
    PROM["Prometheus :9090<br/>метрики и PromQL"]
    GRA["Grafana :3000<br/>data source: Prometheus"]
    DB["Dashboard"]
    TS["Time series<br/>memory"]
    STAT["Stat<br/>series / kernel"]
    TABLE["Table<br/>network receive"]
    STATE["State timeline<br/>up"]
    NODE -->|"HTTP /metrics (pull)"| PROM
    GRA -->|"queries"| PROM
    GRA --> DB
    DB --> TS
    DB --> STAT
    DB --> TABLE
    DB --> STATE
```

Основание: PDF 112–125. Prometheus выполняет pull Node Exporter (глава 2); Grafana выполняет запросы к Prometheus через настроенный источник данных (PDF 115–116).

## Практический выбор панели

```mermaid
flowchart TD
    A["Что нужно увидеть?"]
    B{"Изменение во времени?"}
    C["Time series<br/>process_resident_memory_bytes"]
    D{"Одно число или метка?"}
    E["Stat<br/>head_series / kernel release"]
    F{"Несколько серий в колонках?"}
    G["Table<br/>Instant network rate"]
    H{"Смены дискретного состояния?"}
    I["State timeline<br/>up (mapping требует проверки)"]
    J["[Needs confirmation]<br/>выбрать другую визуализацию"]
    A --> B
    B -->|"да"| C
    B -->|"нет"| D
    D -->|"да"| E
    D -->|"нет"| F
    F -->|"да"| G
    F -->|"нет"| H
    H -->|"да"| I
    H -->|"нет"| J
```

Основание: PDF 117–125. Выбор типов панелей следует примерам главы; `DOWN=2` из PDF 125 конфликтует с текстом главы 2.

## Общий дашборд с переменной устройства

```mermaid
flowchart TD
    V["Dashboard Variable Device<br/>label_values(node_network_receive_bytes_total, device)"]
    DROP["Пользователь выбирает интерфейс"]
    RATE["Time series<br/>rate(receive_bytes_total{device=...}[$__rate_interval])"]
    DUP["Duplicate panel<br/>Bytes Transmit"]
    CHECK["Исходящий PromQL PDF 128<br/>[Source code mismatch]"]
    SHARE["Share dashboard<br/>URL с выбранным Device/time range"]
    V --> DROP
    DROP --> RATE
    RATE --> DUP
    DUP --> CHECK
    DROP --> SHARE
```

Основание: PDF 126–129. Функция `label_values` выполняется в контексте переменных Grafana, а не в PromQL.
