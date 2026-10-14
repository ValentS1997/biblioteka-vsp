# Mermaid — глава 14: операторы агрегирования

**Источник:** `p0246:c01`–`p0257:c01`, PDF 246–257, `rag_only`. Схемы созданы по тексту главы.

## Группировка: без потери контекста алерта

```mermaid
flowchart LR
  SRC["node_filesystem_size_bytes<br/>device, fstype, mountpoint,<br/>job, instance, возможно env"]
  W["sum without(fstype,mountpoint)<br/>удалить перечисленные метки"]
  BY["sum by(job,instance,device)<br/>оставить перечисленные метки"]
  WP["device, job, instance, env<br/>дополнительные target labels"]
  BP["device, job, instance<br/>env потерян"]
  SRC --> W --> WP
  SRC --> BY --> BP
```

PDF 246–249. Когда присутствуют только пять labels из примера, результаты одинаковы. Нельзя указать оба модификатора в одной операции.

## Как выбрать агрегатор

```mermaid
flowchart TD
  A["Что требуется от instant-vector?"]
  SUM["sum: сумма значений"]
  CNT["count: число серий<br/>group: только наличие"]
  AVG["avg: среднее"]
  DEV["stddev/stdvar: разброс"]
  MIN["min/max: крайние значения групп"]
  TOP["topk/bottomk: k исходных рядов"]
  Q["quantile: перцентиль группы"]
  VAL["count_values: частоты значений"]
  A --> SUM
  A --> CNT
  A --> AVG
  A --> DEV
  A --> MIN
  A --> TOP
  A --> Q
  A --> VAL
```

PDF 249–257. `topk`/`bottomk` сохраняют полный набор labels исходных рядов; `quantile` не равен `quantile_over_time` или `histogram_quantile`.

## Counter: скорость, затем агрегация

```mermaid
flowchart LR
  COUNTER["node_disk_read_bytes_total<br/>разные моменты перезапуска"]
  RATE["rate(...[5m])<br/>байты/сек"]
  GROUP["sum without(device)<br/>общая скорость на машину"]
  COUNTER --> RATE --> GROUP
```

PDF 250. Сумма необработанных счётчиков не интерпретируется как текущая скорость.

## Пустые данные и исторический topk

```mermaid
flowchart TD
  EMPTY["non_existent_metric<br/>нет рядов"]
  AGG["sum или count"]
  OUT["empty instant-vector<br/>не числовой 0"]
  TOP["topk(5, some_gauge)<br/>query_range с многими шагами"]
  CHANGE["На каждом шаге<br/>разные 5 рядов"]
  MANY["Множество уникальных рядов<br/>может быть намного больше 5"]
  EMPTY --> AGG --> OUT
  TOP --> CHANGE --> MANY
```

PDF 249, 254. Для topk фиксированного набора книга предлагает модификатор `@` из главы 13. Реальный план запросов зависит от окружения: [Needs confirmation].
