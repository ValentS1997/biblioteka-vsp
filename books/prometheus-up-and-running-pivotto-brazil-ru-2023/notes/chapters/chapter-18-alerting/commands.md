# Commands и правила YAML — глава 18 «Оповещение»

**Источник:** канонический RAG PDF 307–320 (`p0307:c01`–`p0320:c01`). **Ничего не исполнялось.** PromQL проверка выражения — `read-only`, но может быть `workload-generating`. Включение/изменение файлов правил, конфигурации и отправка alerts — `state-changing`. В главе нет пошаговых команд безопасного reload/rollback: [Needs confirmation].

## 1. Правило записи и оповещения в одной группе (PDF 308)

**State-changing при активации файла правил:**

```yaml
groups:
 - name: node_rules
   rules:
    - record: job:up:avg
      expr: avg without(instance)(up{job="node"})
    - alert: ManyInstancesDown
      expr: job:up:avg{job="node"} < 0.5
```

Каждый непустой instant-vector sample alert `expr` становится отдельным alert. Операторы фильтрации, например `< 0.5`, допустимы и полезны в alert rules, в отличие от типичных recording rules. `without` сохраняет дополнительные target labels для Alertmanager.

**Read-only PromQL для отдельного экземпляра (PDF 308):**
```promql
up{job="node"} == 0
```
В правиле `- alert: InstanceDown` оно создаёт один alert на каждый обнаруженный down-target; отсутствующая серия не равна серии с `up=0`.

## 2. Условие времени и batch job (PDF 309–310)

**State-changing при активации:**

```yaml
- alert: ManyInstancesDown
  expr: >
    (
        avg without(instance)(up{job="node"}) < 0.5
      and on()
        hour() >= 9 < 17
    )
- alert: BatchJobNoRecentSuccess
  expr: >
    time() - my_batch_job_last_success_time_seconds{job="batch"} > 86400*2
```

Период в первом условии — **09:00–17:00 UTC**, не местное время. `time()` у batch job — время оценки в секундах, 86400*2 — два дня. Конкретный интервал между успешными заданиями и актуальные имена series зависят от среды: [Needs confirmation].

## 3. Pending / firing и устойчивость (PDF 310–312)

```yaml
groups:
- name: node_rules
  rules:
  - record: job:up:avg
    expr: avg without(instance)(up{job="node"})
  - alert: ManyInstancesDown
    expr: avg without(instance)(up{job="node"}) < 0.5
    for: 5m
```

`for: 5m` требует непрерывного присутствия того же alert labelset на протяжении окна. Pending не отправляется Alertmanager. **Read-only наблюдение** `http://localhost:9090/alerts`; `ALERTS{alertstate="pending"}` и `ALERTS{alertstate="firing"}` отражают состояние (PDF 309–311).

**Source original: одиночный scrape miss может сбить `for`:**
```yaml
- alert: FDsNearLimit
  expr: >
    process_open_fds > process_max_fds * .8
  for: 5m
```

**Source alternative с окном на обеих метриках:**
```yaml
- alert: FDsNearLimit
  expr:
    (
        max_over_time(process_open_fds[5m])
      >
        max_over_time(process_max_fds[5m]) * 0.9
    )
  for: 5m
```

Оба правила иллюстративные: `0.8` и `0.9` — **разные пороги в двух примерах**, а не доказательство эквивалентной политики. `max_over_time` помогает с пропущенным scrape, но не гарантирует сигнал при полном отсутствии истории.

**Различить Blackbox exporter scrape и probe (PDF 312):**
```yaml
- alert: ProbeFailing
  expr: up{job="blackbox"} == 0 or probe_success{job="blackbox"} == 0
  for: 5m
```

## 4. Severity и два порога (PDF 312–313)

```yaml
- alert: InstanceDown
  expr: up{job="node"} == 0
  for: 1h
  labels:
    severity: ticket
- alert: ManyInstancesDown
  expr: job:up:avg{job="node"} < 0.5
  for: 5m
  labels:
    severity: page
```

**Отдельный source example с одинаковым именем, но разной severity и threshold:**
```yaml
- alert: FDsNearLimit
  expr: >
    process_open_fds > process_max_fds * .95
  for: 5m
  labels:
    severity: page
- alert: FDsNearLimit
  expr: >
    process_open_fds > process_max_fds * .8
  for: 5m
  labels:
    severity: ticket
```

При >95 % могут активироваться оба. Автор прямо предупреждает об опасности грубого взаимного исключения, если сигнал дрожит вокруг порога. Метки `severity` и `team/service` предназначены для маршрутизации, но конкретная конфигурация маршрутов в главе 18 не приводится.

## 5. Аннотации и Go templates (PDF 315–317)

**Source example — динамическое значение только в annotations:**
```yaml
groups:
  - name: node_rules
    rules:
      - alert: ManyInstancesDown
        for: 5m
        expr: avg without(instance)(up{job="node"}) * 100 < 50
        labels:
          severity: page
        annotations:
          summary: 'Only {{printf "%.2f" $value}}% of instances are up.'
```

`$value` — число результата expr после `*100`; `$labels.job` — метка идентичности. Самое важное: **не копировать `$value` в labels**.

**Query/range внутри annotations (PDF 316):**
```yaml
- alert: ManyInstancesDown
  for: 5m
  expr: avg without(instance)(up{job="node"}) < 0.5
  labels:
    severity: page
  annotations:
    summary: 'More than half of instances are down.'
    description: >
      Down instances: {{ range query "up{job=\"node\"} == 0" }}
        {{ .Labels.instance }}
      {{ end }}
```

Шаблон может создавать отдельные запросы к TSDB **для каждого alert**, особенно при высокой кардинальности. Дорогой запрос в annotations повышает нагрузку при evaluation.

**Source static dashboard URL (PDF 316):** `http://some.grafana:3000/dashboard/db/prometheus` — учебный адрес, не проверенный реальный dashboard, не использовать как production URL.

## 6. Prometheus → Alertmanager (PDF 318–320)

**State-changing при активации `prometheus.yml`:**
```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s
alerting:
  alertmanagers:
    - static_configs:
      - targets: ['localhost:9093']
rule_files:
  - rules.yml
scrape_configs:
  - job_name: node
    static_configs:
      - targets:
        - localhost:9100
  - job_name: prometheus
    static_configs:
      - targets:
        - localhost:9090
```

В PDF 318 встроен ссылочный маркер `❶` после `static_configs:`; он **исключён из YAML как издательская сноска**, исходный текст не исправлялся. Адрес `localhost:9093` — пример; секреты, сеть и HA Alertmanager [Needs confirmation].

**Отбрасывать информационные alerts до Alertmanager (PDF 319):**
```yaml
alerting:
  alertmanagers:
    - static_configs:
      - targets: ['localhost:9093']
  alert_relabel_configs:
    - source_labels: [severity]
      regex: info
      action: drop
```
Это меняет политику доставки и может **потерять уведомления**; не применять без проверки владельцем.

**Внешние метки (PDF 319–320):**
```yaml
global:
  scrape_interval: 10s
  evaluation_interval: 10s
  external_labels:
    region: eu-west-1
    env: prod
    team: frontend
alerting:
  alertmanagers:
    - static_configs:
      - targets: ['localhost:9093']
```

`external_labels` добавляются после вычисления alert rule, но перед `alert_relabel_configs`. Они **не** видны в шаблонах annotations Prometheus; Alertmanager использует их для маршрутизации/notification templates. Если в ряду уже есть label того же имени, она имеет приоритет.

## Verification / rollback

- Preflight: согласовать owner, severity, threshold, `for`, доступность Alertmanager, стабильность labels и отсутствие marker `❶` в YAML. Конкретный `promtool` и reload описаны в главе 17, **здесь их команды не повторены как будто из главы 18**.
- Наблюдать `/alerts`, `ALERTS`, `ALERTS_FOR_STATE`, работу pending→firing→resolved, внешний labelset и фактическое получение в Alertmanager.
- **Rollback: [Needs confirmation]**: источник не описывает удаление отправленных уведомлений или безопасный откат изменённой политики. Ни YAML, ни endpoint не менялись.
