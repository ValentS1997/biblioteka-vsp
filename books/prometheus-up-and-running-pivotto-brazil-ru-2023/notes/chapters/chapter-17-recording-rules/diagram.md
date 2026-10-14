# Mermaid — глава 17 «Правила записи»

**Источник:** PDF 294–305, `p0294:c01`–`p0305:c01`, `rag_only`. Иллюстрации — новые логические схемы по RAG, не копия рис. 17.1.

## Конфигурация и цикл выполнения

```mermaid
flowchart TD
  CFG["prometheus.yml<br/>rule_files: rules.yml"]
  RULES["rules.yml<br/>groups → rules"]
  CHECK["promtool check config / check rules"]
  RELOAD["restart / SIGHUP / POST /-/reload"]
  EVAL["Периодическая evaluation<br/>evaluation_interval"]
  TSDB["Новые samples в Prometheus TSDB"]
  UI["/rules и метрики длительности"]
  CFG --> CHECK
  RULES --> CHECK
  CHECK --> RELOAD --> EVAL --> TSDB
  EVAL --> UI
```

PDF 294–296. Проверка файла read-only; reload и evaluation — state-changing. POST `/-/reload` требует `--web.enable-lifecycle`. Не подтверждённый rollback: [Needs confirmation].

## Порядок зависимых правил

```mermaid
flowchart LR
  RAW["node_disk_read_bytes_total"]
  RATE["rate(...[5m])"]
  AGG1["job_device:...:rate5m<br/>sum without(instance)"]
  AGG2["job:...:rate5m<br/>sum without(device)"]
  STORE["TSDB / метрики для дашбордов"]
  RAW --> RATE --> AGG1 --> AGG2 --> STORE
```

PDF 298. Обе записи находятся в **одной группе** и выполняются по очереди с одинаковым evaluation timestamp. Для Counter порядок `sum → rate` не использовать.

## Предварительный агрегат для функции over_time

```mermaid
flowchart TD
  C["x_total Counter по экземплярам"]
  R["rate(x_total{job=j}[5m])"]
  S["sum without(instance)"]
  REC["Записать job:x:rate5m"]
  HIST["Серия накоплена как история в TSDB"]
  MAX["max_over_time(job:x:rate5m{job=j}[1h])"]
  C --> R --> S --> REC --> HIST --> MAX
```

PDF 299. Не вычислять дорогостоящие исторические диапазоны каждую минуту, если нужен только периодический отчёт.

## Выбор назначения

```mermaid
flowchart TD
  Q["Зачем новое recording rule?"]
  DASH["Частый дорогой dashboard query"]
  FED["Федерация / длительное хранение"]
  API["Стабильный контракт для другой команды"]
  BAD["Только переименовать metric<br/>или агрегировать вообще всё"]
  DO["Целевой агрегат с нужными labels"]
  REFUSE["Не создавать правило;<br/>исправить источник или relabel"]
  Q --> DASH --> DO
  Q --> FED --> DO
  Q --> API --> DO
  Q --> BAD --> REFUSE
```

PDF 297–305. Названия исходных labels и их значения не следует переносить в имена метрик.
