# Mermaid — глава 11: другие системы мониторинга

**Источник:** PDF 209–214 (`p0209:c01`–`p0214:c01`). Строго `rag_only`; диаграммы выведены из текстового описания.

## Push-to-pull без переноса временной истории

```mermaid
flowchart LR
  APP["Приложение<br/>InfluxDB line protocol"]
  WRITE["HTTP POST /write<br/>InfluxDB Exporter :9122"]
  METRICS["HTTP GET /metrics"]
  PROM["Prometheus scrape<br/>время опроса"]
  APP -->|"push с timestamp"| WRITE
  WRITE -->|"экспорт текущего значения<br/>без исходного timestamp"| METRICS
  PROM -->|"pull"| METRICS
```

Источник PDF 211–212. Наличие отметки времени в payload не делает exporter архивом событий.

## Преобразование StatsD события и dot-separated меток

```mermaid
flowchart TD
   EVENT["TCP/UDP :9125<br/>app.http.requests.eu-west-1./foo:1|c"]
   EXPORTER["StatsD Exporter<br/>обработка Counter"]
   MAP["mapping.yml<br/>match app.http.requests.*.*"]
   LABELS["labels: region=eu-west-1, path=/foo"]
   ENDPOINT["/metrics :9102"]
   PROM["Prometheus pull"]
   EVENT --> EXPORTER
   MAP --> EXPORTER
   EXPORTER --> LABELS --> ENDPOINT
   PROM --> ENDPOINT
```

Источник PDF 212–214. Классы операций различаются: входящие события изменяют агрегаты exporter, Prometheus читает экспозицию.

## Выбор стратегии перехода

```mermaid
flowchart TD
  A["Уже есть мониторинг приложения?"]
  B["Прямое инструментирование<br/>если возможно"]
  C["Внешний модельный exporter<br/>InfluxDB, StatsD, Graphite, collectd"]
  D["Специализированный exporter<br/>JMX, SNMP, SaaS, NRPE"]
  E["Согласовать mapping, единицы,<br/>labels и жизненный цикл"]
  F["Один exporter на приложение,<br/>запуск/остановка совместно"]
  A --> B
  A --> C --> E --> F
  A --> D --> E
```

PDF 209–214. Авторские рекомендации — переходные варианты, не универсальная автоматическая совместимость форматов.
