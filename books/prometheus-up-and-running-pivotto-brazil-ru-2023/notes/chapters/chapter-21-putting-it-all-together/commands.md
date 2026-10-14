# Commands, PromQL и конфигурация — глава 21

**Источник:** PDF 350–374, RAG `p0350:c01`–`p0374:c01`, strict `rag_only`. **Ничего не выполнялось.** Конфигурационные листинги source-derived и исторические; `state-changing` после применения, PromQL `read-only` (иногда `workload-generating`), admin endpoints `destructive`. Целевые hostnames — демонстрационные, реальные endpoints/secrets [Needs confirmation].

## 1. Федерация — агрегаты между дата-центрами (PDF 353–356)

**State-changing при добавлении в `prometheus.yml` глобального сервера; workload-generating при регулярном scrape:**

```yaml
scrape_configs:
  - job_name: 'federate'
    honor_labels: true
    metrics_path: '/federate'
    params:
      'match[]':
        - '{__name__=~"job:.*"}'
    static_configs:
      - targets:
          - 'prometheus-dublin:9090'
          - 'prometheus-berlin:9090'
          - 'prometheus-new-york:9090'
```

Это **нормализация отступов** source PDF 353–354 без изменения существенных полей, не подтверждённый runtime YAML. `match[]` выбирает instant vector samples; несколько параметров дают объединение. `honor_labels: true` избегает конфликта target labels при federation, особенно `instance`, который `/federate` может добавлять пустым (PDF 354, сноска). `global.external_labels` идентифицирует источник. **Не** использовать федерацию для всех metric series, proxy всей TSDB или извлечения каждой `instance`: авторы называют это антипаттерном (PDF 354–355).

## 2. Снимки, удаление и remote storage (PDF 356–358)

**State-changing / potentially destructive endpoints (названы в источнике, но не оформлены в готовые curl-команды):**

```text
POST /api/v1/admin/tsdb/snapshot
/api/v1/admin/tsdb/delete?match[]=...&start=...&end=...
--web.enable-admin-api
```

- Snapshot создаёт snapshot directory с hard links и возвращает имя каталога, после **экспорта резервной копии** источник советует удалить временный снимок (PDF 356).
- Delete принимает `match[]`, `start`, `end` и удаляет данные при следующем compaction; **destructive, без source-backed rollback**, полный адрес/метод для delete отдельной исполнимой командой не приводится (PDF 357).
- Эти endpoint **требуют `--web.enable-admin-api`** и защиты доступа, флаг повышает риск. Реальных вызовов не было.

**State-changing при активации в prometheus.yml:**

```yaml
remote_write:
  - url: http://localhost:1234/write
remote_read:
  - url: http://localhost:1234/read
```

Это source destinations для иллюстрации, не реальные интеграции. `write_relabel_configs` фильтрует данные для цены/объёма; уникальные `external_labels` нужны, чтобы не смешать потоки от разных серверов. У remote read длинные запросы могут перегружать сеть/хранилище.

**Historical experimental agent flag, state-changing:**
```text
--enable-feature=agent
```
В книге agent mode специально назван экспериментальным, он отправляет данные посредством remote write и не поддерживает локальные queries/recording rules (PDF 358). Актуальная совместимость [Needs confirmation]. Встроенные способы настройки Thanos/Cortex/Mimir в главе **не приводятся**, не изобретать.

## 3. Resource sizing, monitoring, retention (PDF 358–360)

**Read-only PromQL (potentially expensive only under broad high-cardinality load):**
```promql
rate(prometheus_tsdb_head_samples_appended_total[5m])
process_max_fds
```

Первое показывает sample ingest rate (Prometheus 2.x по source), второе — fd limit в `/metrics`. Вычислительная оценка из PDF 359–360: хранение `2 bytes/sample` — консервативный ориентир, `20 bytes/sample` — приблизительная сетевая величина, `100000 samples/sec` — учебная база 15-дневной дисковой и RAM оценки. **Не принимать расчет как измеренный профиль TSDB пользователя.**

**State-changing при запуске Prometheus:**
```text
--storage.tsdb.retention.time
--storage.tsdb.retention.size
--storage.tsdb.path
```
Это **только имена флагов без значений** из PDF 359. Размер retention не гарантирует конкретную длительность и не должен исчерпывать диск при compaction. NFS/EFS и совместно используемый несколькими Prometheus storage directory запрещены в контексте главы.

## 4. Прокси, pull-модель и управления конфигурацией (PDF 360–363)

**Source flags, state-changing when applied:**
```text
--web.enable-lifecycle
--web.external-url
--web.route-prefix
proxy_url
```

`--web.external-url` настраивает внешний адрес после reverse proxy; `--web.route-prefix` требуется при изменении path prefix. `proxy_url` используется при scrape через прокси (PDF 362–363). `--web.enable-lifecycle` — для HTTP lifecycle согласно PDF 361, не открывать незащищённый endpoint. Пример команды запуска прокси/SSH/PushProx и политика авторизации не даны. Для тестового Prometheus авторы советуют удалить из конфига Alertmanager и remote-write endpoints, чтобы избежать действий на реальных системах (PDF 361–362).

## 5. HA Prometheus и дублирующие оповещения (PDF 364–366)

**Source YAML, state-changing when activated:**

```yaml
global:
  external_labels:
    region: dublin1
alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']
  alert_relabel_configs:
    - source_labels: [region]
      regex: (.+)\d+
      target_label: region
```

Второй server по source использует `region: dublin2`. После `alert_relabel_configs` оба отправляют в Alertmanager label `region=dublin`, чтобы **alert identities совпадали**. При этом исходные `external_labels` для federation и remote_write обязаны оставаться уникальными. **Не переносить нормализацию replica-label в remote write**, иначе могут конфликтовать отличающиеся samples. Риск неявного отбрасывания других цифр/имен в regex [Needs confirmation].

## 6. Кластер Alertmanager — две peer-команды (PDF 366–367)

**Source literal, state-changing (запуск процесса, сеть/уведомления):**

```sh
# На машине foo
alertmanager --cluster.peer bar:9094

# На машине bar
alertmanager --cluster.peer foo:9094
```

Все Alertmanager должны иметь одинаковый `alertmanager.yml`; каждый Prometheus должен отправлять alerts всем AM instances. Gossip/AP допускает возможные дубликаты при network partition (PDF 366–367). Проверка peer list в Alertmanager Status и создания Silence для проверки propagation в source; создание Silence **state-changing**. Реальные hostname, credentials/ports, TLS и безопасные startup/rollback [Needs confirmation].

## 7. Метамониторинг и оценка проблем (PDF 367–369)

**Read-only PromQL / metric names из source:**
```promql
prometheus_rule_group_iterations_missed_total
prometheus_rule_group_last_duration_seconds
prometheus_rule_group_interval_seconds
prometheus_notifications_dropped_total
prometheus_notifications_queue_length
prometheus_notifications_queue_capacity
prometheus_sd_file_read_errors_total
prometheus_sd_ec2_refresh_failures_total
prometheus_rule_evaluation_failures_total
prometheus_tsdb_compactions_failed_total
prometheus_tsdb_wal_corruptions_total
scrape_samples_scraped
scrape_samples_post_metric_relabeling
scrape_duration_seconds
```

Указываются имена metrics, не гарантированно существующие в текущей версии. `scrape_samples_scraped` считает samples в `/metrics` до metric relabeling, `scrape_samples_post_metric_relabeling` — после, `scrape_duration_seconds` сигнализирует о времени scrape (PDF 369).

**Workload-generating, potentially expensive PromQL:**
```promql
topk(10, count by(__name__)({__name__=~".+"}))
```

Источник прямо предупреждает о полном переборе активных series (PDF 369). Не запускать без учета query budget крупного production Prometheus.

**Особо опасный source текст:** «остановить Prometheus, удалить каталог хранилища и снова запустить» — **разрушительное решение самого крайнего случая**, в этой коллекции **не даётся shell-команда удаления**, backup/rollback [Needs confirmation].

## 8. hashmod: диагностическая выборка, не рекомендуемый default (PDF 370)

**State-changing при изменении `scrape_configs`; ~90% целей перестанут опрашиваться:**
```yaml
scrape_configs:
  - job_name: my_job
    # Настройки service discovery в source опущены
    relabel_configs:
      - source_labels: [__address__]
        modulus: 10
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: 0
        action: keep
```

`modulus:10`, `keep regex:0` оставляет только одну hash-группу. Изменение `regex:1`–`9` выбирает другую часть целей. Это **экспериментальная диагностика**, не подход для незаметного постоянного выключения 90 % monitoring coverage. `modulus=10` не доказывает точную долю в произвольной небольшой выборке.

## 9. Отбрасывание дорогостоящей метрики после scrape и sample_limit (PDF 370–371)

**State-changing; может прекратить сбор метрики:**
```yaml
scrape_configs:
  - job_name: some_application
    static_configs:
      - targets:
          - localhost:1234
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: expensive_metric_name
        action: drop
```

Это **экономит storage**, но метрика уже отправлена по сети и распознана Prometheus. `sample_limit` — имя configuration field, исходник не приводит конкретного значения; превышение после `metric_relabel_configs` приводит к **ошибке всего scrape и отсутствию samples**. Настройка не является нормальным механизмом quotas.

## 10. Horizontal scraping, source shard=2/4 и remote_read (PDF 371–373)

**State-changing; комментированные строки намеренно обозначают недостающую SD-конфигурацию:**
```yaml
global:
  external_labels:
    env: prod
    scraper: 2
scrape_configs:
  - job_name: my_job
    # Здесь находятся настройки обнаружения служб и т. д.
    relabel_configs:
      - source_labels: [__address__]
        modulus: 4
        target_label: __tmp_hash
        action: hashmod
      - source_labels: [__tmp_hash]
        regex: 2
        action: keep
```

**Пример remote-read ведущего сервера:**
```yaml
global:
  external_labels:
    env: prod
remote_read:
  - url: http://scraper0:9090/api/v1/read
    read_recent: true
  - url: http://scraper1:9090/api/v1/read
    read_recent: true
  - url: http://scraper2:9090/api/v1/read
    read_recent: true
  - url: http://scraper3:9090/api/v1/read
    read_recent: true
```

`read_recent: true` заставляет remote read обращаться за свежими данными даже в случае, когда оптимизация обычно избегала бы этого (PDF 372). **Не использовать как общий прозрачный proxy** для всех Prometheus: один дорогой запрос может перегрузить все shards. Лучше предварительно агрегировать на scrapers.

## Verification / rollback

Перед применением: проверить метки, источники, валидность YAML, SD, key uniqueness, нагрузку, доступность локальных оповещений, owner и изолированный тестовый Prometheus без реальных receivers/remote-write. При проверке после изменений — низкостоимостные scrape metrics, rule eval, queue alerts, timeouts и TSDB ingest. **Rollback [Needs confirmation]**: глава не содержит полного алгоритма восстановления после удаления TSDB, неправильного relabel/shard assignment, потери данных remote write или утраты уведомлений. Реальные команды не выполнялись.
