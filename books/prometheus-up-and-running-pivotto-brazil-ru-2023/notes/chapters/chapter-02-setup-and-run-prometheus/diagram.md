# Глава 2 — диаграммы по RAG

Граница: PDF 34–52; source `p0034:c01`–`p0052:c01`. Диаграммы **не** являются копиями издательских рисунков 2.1–2.19.

## Поток метрик и уведомлений

```mermaid
flowchart LR
    OP["Оператор: браузер выражений<br/>PromQL / Targets"]
    P["Prometheus :9090<br/>scrape 10s; rules 10s<br/>TSDB + /metrics"]
    N["Node Exporter :9100<br/>/metrics хоста"]
    R["rules.yml<br/>InstanceDown: up == 0<br/>for: 1m"]
    A["Alertmanager :9093<br/>group_by: alertname"]
    MAIL["SMTP localhost:25<br/>e-mail при доступной доставке"]
    P -->|"GET /metrics (pull)"| N
    P -->|"самосбор метрик"| P
    OP <-->|"чтение Targets, up, rate()"| P
    P -->|"оценка"| R
    R -->|"alert"| A
    A -->|"уведомление"| MAIL
```

Источники: PDF 35–38 (`p0035:c01`–`p0038:c01`), 43–46 (`p0043:c01`–`p0046:c01`), 48–52 (`p0048:c01`–`p0052:c01`). Стрелка к Node Exporter обозначает инициирование pull самим Prometheus, **не** push от экспортера.

## Учебная симуляция отказа

```mermaid
flowchart TD
    A["Обе цели UP<br/>up = 1"]
    B["Ctrl+C: остановлен Node Exporter<br/>(только учебный стенд)"]
    C["Следующий scrape: Node DOWN<br/>up = 0; Targets Error"]
    D["PromQL up == 0<br/>выбран только недоступный instance"]
    E["InstanceDown ожидает<br/>for: 1m"]
    F["Prometheus передаёт alert<br/>в Alertmanager"]
    G{"SMTP маршрут доступен?"}
    H["E-mail получателю"]
    I["Доставка не подтверждена<br/>[Needs confirmation]"]
    A --> B --> C --> D --> E --> F --> G
    G -->|"да"| H
    G -->|"не проверено"| I
```

Источник: PDF 47–52. Указанные условия описывают конкретный сценарий книги, не все возможные состояния системы. Процедуры восстановления реальной инфраструктуры вне главы: [Needs confirmation].
