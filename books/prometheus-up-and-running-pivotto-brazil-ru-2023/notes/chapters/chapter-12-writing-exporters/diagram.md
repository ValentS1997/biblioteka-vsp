# Mermaid — глава 12 «Разработка экспортеров»

**Источник:** PDF 215–225, `p0215:c01`–`p0225:c01`, только RAG. Схемы — производные от текста, не реконструкция издательских рисунков.

## От чужой семантики до /metrics

```mermaid
flowchart LR
  SRC["Consul API<br/>Gauges / Counters / Samples"]
  COLL["ConsulCollector.Collect<br/>каждый scrape"]
  GAUGE["GaugeValue<br/>g.Value"]
  COUNTER["CounterValue<br/>c.Count, имя _total"]
  SAMPLE["Samples: Count, Sum<br/>ms → sec / 1000"]
  REG["Default registry<br/>consul_up + go_ + process_"]
  HTTP["/metrics :8000"]
  PROM["Prometheus pull"]
  SRC --> COLL
  COLL --> GAUGE
  COLL --> COUNTER
  COLL --> SAMPLE
  GAUGE --> REG
  COUNTER --> REG
  SAMPLE --> REG
  REG --> HTTP
  PROM -->|"scrape"| HTTP
```

PDF 215–222. Go в примере представляет Samples двумя Counter-семействами, Python использует SummaryMetricFamily. Пример published `_seconds_sum` противоречит операции `/1000`, см. [source-findings.md](source-findings.md).

## Методы пользовательского Collector

```mermaid
flowchart TD
  D["Describe: известные Desc<br/>consul_up"]
  R["prometheus.MustRegister(c)"]
  S["Prometheus scrape"]
  C["Collect: запрос API Consul"]
  Q{"API доступен?"}
  U0["consul_up = 0<br/>закончить сбор"]
  U1["consul_up = 1"]
  O["Создать динамические Desc<br/>и ConstMetric"]
  V["/metrics: семейства и labels"]
  D --> R
  R --> S --> C --> Q
  Q -->|"нет"| U0 --> V
  Q -->|"да"| U1 --> O --> V
```

PDF 217–221. В тексте Go клиент требует минимум один `Desc` в `Describe`; для полностью динамических метрик предложен фиктивный.

## Рекомендации по проектированию

```mermaid
flowchart TD
  A["Внешние метрики"]
  T{"Тип и единицы понятны?"}
  U["Использовать UntypedValue<br/>или не утверждать тип"]
  N["Gauge / Counter / Samples"]
  L["Нормализовать имена,<br/>секунды / байты, labels"]
  F["Передать raw counter,<br/>sum и count"]
  P["В PromQL: rate, деление,<br/>агрегация"]
  K["Контроль кардинальности,<br/>один exporter/экземпляр"]
  A --> T
  T -->|"нет"| U
  T -->|"да"| N --> L --> F --> P --> K
```

PDF 216, 224–225. Избегать label totals, machine-level метрик в прикладном exporter и ненужного кеширования. Реальный migration/rollback не приведён: [Needs confirmation].
