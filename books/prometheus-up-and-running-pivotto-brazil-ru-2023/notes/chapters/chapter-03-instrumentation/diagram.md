# Диаграммы главы 3 по RAG

**Привязка:** PDF 54–75, `p0054:c01`–`p0075:c01`. Не реконструкция издательских рисунков.

## Прямое инструментирование и запросы

```mermaid
flowchart LR
    CODE["Приложение Python: do_GET()"]
    API["prometheus_client: Counter, Gauge, Summary, Histogram"]
    REG["Реестр метрик Python"]
    HTTP["start_http_server(8000): /metrics"]
    PROM["Prometheus: scrape localhost:8000/metrics, 10s"]
    PQL["Expression Browser: python_info, rate(), histogram_quantile()"]
    CODE -->|"inc, set, observe, time"| API
    API -->|"регистрация"| REG
    REG --> HTTP
    PROM -->|"HTTP pull"| HTTP
    PROM --> PQL
```

Источник: PDF 54–57, 61–66. Направление HTTP pull — от Prometheus к endpoint; пользовательский обработчик приложения в примере слушает отдельно на порту 8001.

## Выбор метрики для задачи

```mermaid
flowchart TD
    A["Какой тип наблюдения нужен?"]
    B{"Накопленное событие / размер?"}
    C["Counter: inc() и rate()"]
    D{"Текущее состояние может уменьшаться?"}
    E["Gauge: set(), inc(), dec()"]
    F{"Длительность / размер наблюдения?"}
    G["Summary: _sum/_count, среднее"]
    H["Histogram: _bucket, p95, SLA"]
    I["Уточнить измерение: [Needs confirmation]"]
    A --> B
    B -->|"да"| C
    B -->|"нет"| D
    D -->|"да"| E
    D -->|"нет"| F
    F -->|"да, среднее"| G
    F -->|"да, распределение"| H
    F -->|"нет"| I
```

Источник: PDF 56–68. Histogram использует кумулятивные buckets; квантили вычисляются приближённо. Выбор между Summary/Histogram основан на вопросах главы, не заменяет performance-тест.

## Где инструментировать

```mermaid
flowchart TD
    S["Тип компонента"]
    ONLINE["Онлайн-сервис / RPC: RED"]
    OFFLINE["Очередь / конвейер / workers: USE"]
    BATCH["Периодическое batch-задание"]
    OUT1["Частота; ошибки; задержка, включая неуспешные запросы"]
    OUT2["Нагрузка; насыщение/очередь; ошибки"]
    OUT3["Длительность; этапы; последний успешный запуск"]
    S --> ONLINE --> OUT1
    S --> OFFLINE --> OUT2
    S --> BATCH --> OUT3
```

Источник: PDF 70–72. У batch упомянуты Pushgateway и textfile collector, но реализация рассматривается в следующих главах.
