# Mermaid — глава 13 «Введение в PromQL»

**Источник:** PDF 227–245, `p0227:c01`–`p0245:c01`, `rag_only`. Схемы обобщают текст; оригинальный скриншот 13.1 в RAG недоступен как изображение.

## Тип метрики определяет порядок вычислений

```mermaid
flowchart TD
  A["Временные ряды"]
  GA["Gauge: текущие значения"]
  CO["Counter: монотонное накопление"]
  SU["Summary: _sum, _count, quantile"]
  HI["Histogram: _bucket{le}, _sum, _count"]
  G["sum/max/avg without(labels)"]
  C["rate(metric_total[5m]) → sum"]
  S["sum(rate(_sum)) / sum(rate(_count))"]
  H["sum(rate(_bucket)) → histogram_quantile"]
  A --> GA --> G
  A --> CO --> C
  A --> SU --> S
  A --> HI --> H
```

Основание PDF 227–233. Не усреднять предварительно вычисленные средние или Summary quantiles. В источнике есть несовпадение имени histogram bucket во втором примере, см. [source-findings.md](source-findings.md).

## Instant vs range и временные модификаторы

```mermaid
flowchart TD
  S["Селектор с метками"]
  M["Matchers = != =~ !~"]
  IN["Instant: максимум 1 sample на series"]
  RA["Range [1m]: несколько сырых samples"]
  OFF["offset 1h / @ UNIX / @ end()"]
  SUB["Subquery [30m:1m]"]
  ST["Staleness marker исключает instant series"]
  FUN["rate / avg_over_time и другие функции"]
  S --> M
  M --> IN
  M --> RA
  IN --> ST
  IN --> OFF
  RA --> FUN
  FUN --> SUB
```

Основание PDF 233–240. Range selector сохраняет фактические timestamps, но не выдаёт staleness markers. Для custom sample timestamps есть особенность lookback из PDF 236.

## HTTP API и step

```mermaid
flowchart LR
  USER["PromQL выражение"]
  Q["/api/v1/query<br/>одна оценка, time"]
  QR["/api/v1/query_range<br/>start, end, step"]
  I["vector / matrix / scalar"]
  STEPS["Последовательность instant-оценок"]
  RESULT["matrix: series и values"]
  USER --> Q --> I
  USER --> QR --> STEPS --> RESULT
```

Основание PDF 240–245. У `query_range` конец включается при попадании на шаг; range для `rate` больше шага; лимит 11 000 шагов указан в книге. При пустой выборке нет автоматической дорисовки.
