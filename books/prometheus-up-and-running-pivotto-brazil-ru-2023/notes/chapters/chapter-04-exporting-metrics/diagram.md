# Глава 4 — диаграммы по RAG

**Источник:** PDF 76–96 (`p0076:c01`–`p0096:c01`). Эти Mermaid-схемы — текстовые конструкции по источнику, не воспроизведение рисунков 4.1–4.2.

## Экспорт из долгоживущего процесса

```mermaid
flowchart LR
    A["Код приложения<br/>Counter/Gauge/Histogram"]
    R["Реестр клиентской библиотеки"]
    E["HTTP endpoint /metrics<br/>WSGI / Handler / Servlet"]
    P["Prometheus<br/>периодический scrape"]
    Q["PromQL / storage / alerting"]
    A -->|"регистрация"| R
    R -->|"текст Prometheus или OpenMetrics"| E
    P -->|"HTTP GET /metrics (pull)"| E
    P --> Q
```

RAG PDF 76–85. Для многопроцессного Gunicorn используется `MultiProcessCollector` с чтением файлов worker при scrape (PDF 79–82).

## Pushgateway: только cache для service-level batch

```mermaid
flowchart LR
    B["Краткое batch-задание<br/>может завершиться до scrape"]
    G["Pushgateway :9091<br/>хранит последнюю группу"]
    P["Prometheus<br/>обычный pull, honor_labels"]
    B -->|"PUT / POST: передача по окончании"| G
    P -->|"HTTP scrape"| G
    D["При выводе из эксплуатации<br/>DELETE группы"]
    D --> G
```

RAG PDF 86–89. Pushgateway не превращает Prometheus в push-систему: у клиента временная отправка, у Prometheus постоянный pull. Для привязанных к машине заданий в книге рекомендован textfile collector, разбираемый в главе 7.

## Проверка формата и источник ошибок

```mermaid
flowchart TD
    A["Есть endpoint /metrics?"]
    B{"HTTP ответ доступен?"}
    C["Проверить endpoint, маршрут и экспорт<br/>[Needs confirmation]"]
    D["curl .../metrics | promtool check metrics"]
    E{"Формат валиден?"}
    F["Проверить HELP/TYPE, newline, имена,<br/>escaping, timestamps, EOF для OpenMetrics"]
    G["Проверить scrape Prometheus и метки"]
    A --> B
    B -->|"нет"| C
    B -->|"да"| D
    D --> E
    E -->|"нет"| F
    E -->|"да"| G
```

RAG PDF 91–96. Последовательность проверок — диагностическая интерпретация утверждений главы; конкретный deployment и rollback не даны: [Needs confirmation].
