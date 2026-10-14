# Commands, API, Go/Python — глава 12

**Строгий источник:** PDF 215–225 (`p0215:c01`–`p0225:c01`), `rag_only`. Код переписан только из source RAG. **Ничего не выполнялось**. Классификация: `read-only`, `workload-generating`, `state-changing`. Для действия, меняющего среду, указаны эффект, риск, проверка; rollback в книге отсутствует — `[Needs confirmation]`.

## Получить исходные метрики Consul

**Read-only / workload-generating (сетевой запрос):** посетить `http://localhost:8500/v1/agent/metrics` (PDF 215). Источниковый JSON имеет `Gauges`, `Counters`, `Samples` и `Points`. Форма фрагмента из PDF 215–216:

```json
{
  "Timestamp": "2018-01-31 14:42:10 +0000 UTC",
  "Gauges": [
    {"Name": "consul.autopilot.failure_tolerance", "Value": 0, "Labels": {}}
  ],
  "Points": [],
  "Counters": [
    {"Name": "consul.raft.apply", "Count": 1, "Sum": 2, "Min": 1, "Max": 1, "Mean": 1, "Stddev": 0, "Labels": {}}
  ],
  "Samples": [
    {"Name": "consul.fsm.coordinate.batch-update",
     "Count": 1, "Sum": 0.13156799972057343,
     "Min": 0.13156799972057343, "Max": 0.13156799972057343,
     "Mean": 0.13156799972057343, "Stddev": 0, "Labels": {}}
  ]
}
```

Значения учебные и исторические, не измерения пользовательского Consul. В тексте книги Samples определены как timers **в миллисекундах** (PDF 216).

## Go Collector — исходный полный пример 12.2 (PDF 217–218)

**State-changing (код/запуск):** экспортирует метрики, регистрирует Collector и открывает HTTP `:8000/metrics`; `ConsulCollector.Collect` обращается к Consul при каждом scrape, создаёт `consul_up` и новые значения. **Риск:** нет production-конфигурации для Consul, а опубликованное значение `_seconds_sum` не соответствует делению на 1000. Не объявлять sample executable golden test без отдельной проверки. Rollback: [Needs confirmation].

```go
package main

import (
    "log"
    "net/http"
    "regexp"

    "github.com/hashicorp/consul/api"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
)

var (
    up = prometheus.NewDesc(
        "consul_up",
        "Was talking to Consul successful.",
        nil, nil,
    )
    invalidChars = regexp.MustCompile("[^a-zA-Z0-9:_]")
)

type ConsulCollector struct{}

func (c ConsulCollector) Describe(ch chan<- *prometheus.Desc) {
    ch <- up
}

func (c ConsulCollector) Collect(ch chan<- prometheus.Metric) {
    consul, err := api.NewClient(api.DefaultConfig())
    if err != nil {
        ch <- prometheus.MustNewConstMetric(up, prometheus.GaugeValue, 0)
        return
    }

    metrics, err := consul.Agent().Metrics()
    if err != nil {
        ch <- prometheus.MustNewConstMetric(up, prometheus.GaugeValue, 0)
        return
    }
    ch <- prometheus.MustNewConstMetric(up, prometheus.GaugeValue, 1)

    for _, g := range metrics.Gauges {
        name := invalidChars.ReplaceAllLiteralString(g.Name, "_")
        desc := prometheus.NewDesc(name, "Consul metric "+g.Name, nil,
            g.Labels)
        ch <- prometheus.MustNewConstMetric(
                desc, prometheus.GaugeValue, float64(g.Value))
    }

    for _, c := range metrics.Counters {
        name := invalidChars.ReplaceAllLiteralString(c.Name, "_")
        desc := prometheus.NewDesc(name+"_total", "Consul metric "+c.Name,
                nil, c.Labels)
        ch <- prometheus.MustNewConstMetric(
                desc, prometheus.CounterValue, float64(c.Count))
    }

    for _, s := range metrics.Samples {
        // Таймеры в миллисекундах; преобразуем в секунды.
        name := invalidChars.ReplaceAllLiteralString(s.Name, "_") +
            "_seconds"
        countDesc := prometheus.NewDesc(
                name+"_count", "Consul metric "+s.Name, nil, s.Labels)
        ch <- prometheus.MustNewConstMetric(
                countDesc, prometheus.CounterValue, float64(s.Count))
        sumDesc := prometheus.NewDesc(
                name+"_sum", "Consul metric "+s.Name, nil, s.Labels)
        ch <- prometheus.MustNewConstMetric(
                sumDesc, prometheus.CounterValue, s.Sum/1000)
    }
}

func main() {
    c := ConsulCollector{}
    prometheus.MustRegister(c)
    http.Handle("/metrics", promhttp.Handler())
    log.Fatal(http.ListenAndServe(":8000", nil))
}
```

Исходные русскоязычные комментарии в листинге PDF 217–218 перефразированы кратко; логика и операторы сохранены. **[Source code mismatch]** отдельный фрагмент PDF 221 использует `float64(s.Count)` вместо `float64(c.Count)` у `for _, c := range metrics.Counters`; полный листинг выше сохраняет `c.Count` с PDF 218. См. [source-findings.md](source-findings.md).

**State-changing — зависимости и запуск Go из PDF 218:**

```sh
go get -d -u github.com/hashicorp/consul/api
go get -d -u github.com/prometheus/client_golang/prometheus
go run consul_metrics.go
```

Эффект: загрузка/изменение зависимостей и запуск сервиса на порту 8000; риск совместимости с версией Go и доступа к Consul, сетевой binding `:8000`. Verification: прочитать `http://localhost:8000/metrics`. Rollback для зависимостей, процесса и порта: [Needs confirmation].

**Read-only — соответствующие output имена по PDF 218:**

```text
consul_autopilot_failure_tolerance 0
consul_raft_apply_total 1
consul_fsm_coordinate_batch_update_seconds_count 1
consul_fsm_coordinate_batch_update_seconds_sum 1.3156799972057343e-01
```

**Этот численный output содержит [Source contradiction]:** исходная `Sum=0.13156799972057343`, а Go код `s.Sum/1000` даёт число, отличающееся от опубликованного. Вывод нельзя использовать как golden acceptance.

## Go: метки и динамические Desc (PDF 219–224)

**State-changing (код Collector):**
```go
func (c MyCollector) Collect(ch chan<- prometheus.Metric) {
  desc := prometheus.NewDesc(
    "example_gauge",
    "A help string.",
    []string{"foo", "baz"}, nil,
  )
  ch <- prometheus.MustNewConstMetric(
    desc, prometheus.GaugeValue, 1, "bar", "small")
  ch <- prometheus.MustNewConstMetric(
    desc, prometheus.GaugeValue, 2, "quu", "far")
}
```

Проверить ожидаемые `example_gauge{foo="bar",baz="small"} 1` и `example_gauge{foo="quu",baz="far"} 2`. Совпадение HELP у всех элементов одного имени обязательно. В Go `Describe` вызывается при регистрации; источниковый текст требует по меньшей мере один заранее описанный `Desc` (PDF 219–220).

## Python Collector — исходный пример 12.3 (PDF 222–223)

**State-changing (код/запуск):** регистрирует Collector в Python default REGISTRY и запускает `:8000`. **[Source code mismatch]:** внутри цикла `for s in metrics["Samples"]` передаётся `count_value=c["Count"]` (переменная `c` от предыдущего цикла Counter). **Пример не признаётся проверенно исполнимым**. Не исправлять silently. Возможная ошибка или неверное число samples при разных входных данных, см. [source-findings.md](source-findings.md). Rollback: [Needs confirmation].

```python
import json
import re
import time
from urllib.request import urlopen
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from prometheus_client.core import SummaryMetricFamily, REGISTRY
from prometheus_client import start_http_server

def sanitize_name(s):
    return re.sub(r"[^a-zA-Z0-9:_]", "_", s)

class ConsulCollector(object):
  def collect(self):
    out = urlopen("http://localhost:8500/v1/agent/metrics").read()
    metrics = json.loads(out.decode("utf-8"))

    for g in metrics["Gauges"]:
      yield GaugeMetricFamily(sanitize_name(g["Name"]),
          "Consul metric " + g["Name"], g["Value"])

    for c in metrics["Counters"]:
      yield CounterMetricFamily(sanitize_name(c["Name"]) + "_total",
          "Consul metric " + c["Name"], c["Count"])

    for s in metrics["Samples"]:
      yield SummaryMetricFamily(sanitize_name(s["Name"]) + "_seconds",
          "Consul metric " + s["Name"],
          count_value=c["Count"], sum_value=s["Sum"] / 1000)

if __name__ == '__main__':
  REGISTRY.register(ConsulCollector())
  start_http_server(8000)
  while True:
    time.sleep(1)
```

**Python метки, PDF 223–224 — state-changing (код):**
```python
class MyCollector(object):
  def collect(self):
    mf = GaugeMetricFamily("example_gauge", "A help string.",
        labels=["foo", "baz"])
    mf.add_metric(["bar", "small"], 1)
    mf.add_metric(["quu", "far"], 2)
    yield mf
```

## Эксплуатационные проверки и границы

- Действительный Consul Agent `:8500`, текущая версия библиотек, разрешённые имена и конкурирующие scrape: [Needs confirmation]. `ConsulCollector` не содержит отдельной процедуры настройки auth/адреса и создаёт клиент в каждом `Collect`, а книга рекомендует сделать параметры настраиваемыми и допускает reuse клиента (PDF 222).
- `MustNewConstMetric` принимает `GaugeValue`, `CounterValue`, `UntypedValue` (PDF 220), но **`UntypedValue` не используется в source run example**.
- Следует синхронно извлекать данные на каждом scrape, не кешировать, учитывать одновременные scrape (PDF 225).
- В целом математическую обработку, включая `rate` и отношения, оставить для PromQL; единицы seconds/bytes, не добавлять лишние environment target labels (PDF 224–225).
- `myexporter_scrape_duration_seconds` и `cloudwatch_requests_total` — предложенные именованные метрики диагностики/стоимости, **в главе не приведена команда их регистрации** (PDF 225).
