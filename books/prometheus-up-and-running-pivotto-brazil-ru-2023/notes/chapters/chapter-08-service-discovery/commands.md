# Commands, config и relabel — глава 8

**Источник:** RAG PDF 144–169 (`p0144:c01`–`p0169:c01`). **Ничего не выполнялось.** Исходная книга иллюстрирует Prometheus **2.37.0**; текущая совместимость неизвестна. Примеры не являются готовыми production-config. Классы: `read-only`, `state-changing`, `workload-generating`.

## Read-only: контроль обнаруженных целей

| Проверка | Класс | Смысл, источник |
| --- | --- | --- |
| `http://localhost:9090/service-discovery` | read-only | Страница обнаруженных целей и внутренних метаданных, `show more` (PDF 148–153) |
| `http://localhost:9090/targets` (Targets в UI) | read-only | В тексте описана страница Targets (PDF 148, сноска); фактическая доступность [Needs confirmation] |
| `prometheus_sd_http_failures_total` | read-only (PromQL metric selector) | Счётчик ошибок обновления HTTP SD (PDF 150) |
| `/metrics` | read-only | Проверка реального exporter; обнаруженная служба Consul по книге сама не экспонирует метрики (PDF 151) |

## Изменения статического и файлового SD

**Все блоки YAML/JSON ниже — `state-changing`, если записаны в конфигурацию Prometheus; эффект — изменение списка целей и меток.** Проверка после согласованного применения: `/service-discovery` и scrape действительного exporter. **Rollback/reload: [Needs confirmation].**

**Static SD**, пример 8.1, PDF 146:

```yaml
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
        - localhost:9090
```

**File SD**, пример 8.4, PDF 148 (синтетические хосты учебного текста):

```json
[
  {
    "targets": ["host1:9100", "host2:9100"],
    "labels": {"team": "infra", "job": "node"}
  },
  {
    "targets": ["host1:9090"],
    "labels": {"team": "monitoring", "job": "prometheus"}
  }
]
```

**File SD config**, пример 8.5, PDF 148:

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
```

Книга разрешает `.json` для JSON, `.yml`/`.yaml` для YAML. Подстановочные символы возможны в **имени файла**, но не компоненте каталога; путь относительно рабочего каталога Prometheus. Для обновления — атомарное переименование (PDF 147–150). **State-changing:** генерация/замена файлов; не считать формат YAML/JSON взаимозаменяемым.

**HTTP SD**, пример 8.6, PDF 150:

```yaml
scrape_configs:
 - job_name: cmdb
   http_sd_configs:
    - url: http://cmdb.local/prometheus-service-discovery
```

Endpoint должен отдавать JSON из file SD, `Content-Type: application/json`, HTTP 200; по книге default refresh каждые 60 секунд, параметр `refresh_interval`. **Риск:** недоступный источник после перезапуска оставляет пустой набор целей, потому что cache недолговечен (PDF 150). **Проверка:** счётчик `prometheus_sd_http_failures_total`; rollback [Needs confirmation]. Источник `cmdb.local` — учебный адрес, не проверенный в окружении.

**Consul SD**, пример 8.9, PDF 151:

```yaml
scrape_configs:
 - job_name: consul
   consul_sd_configs:
    - server: 'localhost:8500'
```

Consul в книге запускается разработческим режимом `./consul agent -dev`, после исторических `wget` и `unzip` версии 1.0.2 (PDF 151). **Класс:** `state-changing` (запуск сервиса и сетевые операции), `workload-generating`; **не исполнять** на production как руководство по установке. Verification: `http://localhost:8500/` и `/service-discovery` (PDF 151). Rollback [Needs confirmation].

**EC2 SD**, пример 8.10, PDF 153; **данные доступа заменены placeholders**:

```yaml
scrape_configs:
 - job_name: ec2
   ec2_sd_configs:
    - region: <region>
      access_key: <access-key-placeholder>
      secret_key: <secret-key-placeholder>
```

Секретные поля в исходной конфигурации присутствуют; реальные значения запрещено помещать в артефакт. По книге минимальный API permission `EC2:DescribeInstances`, политика `AmazonEC2ReadOnlyAccess` приведена как простой вариант (PDF 152). **Класс:** `state-changing`; риск доступа к облачному API/секретов; проверка — discovery с EC2 metadata и IP. Раскрытие реальных ключей и изменение IAM не санкционированы: [Needs confirmation].

## Relabel target: действие применяется ДО scrape

Все следующие правила `state-changing` при добавлении в `relabel_configs`, поскольку изменяют состав/имена целей. После применения проверить `/service-discovery`; rollback [Needs confirmation].

| Пример, PDF | Исходный фрагмент relabel rule | Эффект и риск |
| --- | --- | --- |
| 8.11, 155 | `source_labels: [team]`; `regex: infra`; `action: keep` | Оставляет только team=infra; другие targets исключаются |
| 8.12, 155 | Два `keep` подряд для `infra`, `monitoring` | **Все цели исключены** — обязательное пересечение несовместимых условий |
| 8.13, 155 | `regex: infra\|monitoring`; `action: keep` | Условие «одно или другое», сохраняет обе группы |
| 8.14, 156 | `source_labels: [job, team]`; `regex: prometheus;monitoring`; `action: drop` | Исключает конкретную комбинацию job/team |
| 8.15, 159 | `source_labels: [team]`; `regex: monitoring`; `replacement: monitor`; `target_label: team`; `action: replace` | Переименовывает значение; **история рядов меняет идентичность** |
| 8.16, 159 | `regex: '(.*)ing'`; `replacement: '${1}'`; `target_label: team` | Убирает завершающий ing из совпадающих значений; риск неожиданных замен |
| 8.17–8.18, 160–161 | `source_labels: []`; `target_label: team` | Удаление team через пустое значение/поведение по умолчанию |
| 8.19, 161 | `source_labels: [__meta_consul_address]`; `replacement: '${1}:9100'`; `target_label: __address__` | Переключает scrape на Node Exporter порт 9100 |
| 8.20, 162 | `source_labels: [__meta_consul_node]`; `replacement: '${1}:9100'`; `target_label: instance` | Удобочитаемое instance; `__address__` отдельно остаётся IP:9100 |
| 8.21, 163 | `source_labels: [__meta_ec2_tag_service]`; `target_label: job`, затем `action: labelmap` | Соглашение service/monitor_ для EC2 metadata; **regex `__meta_ec2_public_tag_monitor_(.*)` в источнике конфликтует с другими именами meta-меток** |
| 8.22, 163–164 | `source_labels: [__meta_ionos_server_type]`; `target_label: server_type`; `action: lowercase` | Нормализует регистр значения |
| 8.23, 164 | `source_labels: [__meta_consul_tags]`; `regex: '.*,prod,.*'`; `action: keep` | Оставляет цели с тегом prod |
| 8.24, 164–165 | `regex: '.*,(prod\|staging\|dev),.*'`; `target_label: env` | Преобразует известное значение из списка в env |

**Полный пример `keep` (8.11, PDF 155):**

```yaml
scrape_configs:
 - job_name: file
   file_sd_configs:
    - files:
       - '*.json'
   relabel_configs:
    - source_labels: [team]
      regex: infra
      action: keep
```

**Полный пример построения адреса Node Exporter из Consul** (8.19, PDF 161):

```yaml
scrape_configs:
 - job_name: node
   consul_sd_configs:
    - server: 'localhost:8500'
   relabel_configs:
    - source_labels: [__meta_consul_address]
      regex: '(.*)'
      replacement: '${1}:9100'
      target_label: __address__
```

Регулярные выражения relabel по источнику — RE2 и anchored; `source_labels` объединяются `;`, если нет иного `separator` (PDF 154–157). Имена `__meta_*` являются промежуточными, `__tmp` зарезервирован для временной метки (PDF 161, 165). Не изменять целевую идентичность во время штатной диагностики без плана: [Needs confirmation].

## Настройки scrape: значения и риски (PDF 165–166)

| Ключ | Класс | Source-derived назначение |
| --- | --- | --- |
| `scrape_timeout: 5s` | state-changing | Тайм-аут scrape |
| `scrape_interval` | state-changing | Интервал опроса, по книге лучше единый |
| `metrics_path: /admin/metrics` | state-changing | Путь без query string; для параметров использовать `params` |
| `params: {foo: [bar]}` | state-changing | Параметры URL |
| `scheme: https` | state-changing | HTTPS transport |
| `tls_config`, `authorization`, `basic_auth` | state-changing | TLS/credentials; точная защищённая схема зависит от окружения |
| `insecure_skip_verify: true` | state-changing, unsafe | **Отключает проверку сертификата; по книге не рекомендуется** |
| `proxy_url` | state-changing | Прокси для получения метрик |

В примере 8.25 в PDF 165 пароль дан явно в учебном блоке; **он намеренно не воспроизводится**. Никаких реальных секретов, токенов и ключей сюда не включено. `http_sd_configs` в примере 8.7 (PDF 150) содержит HTTP URL вместе с `tls_config`; действенность такой пары [Needs confirmation], см. [source-findings.md](source-findings.md). Verification: доступность exporter при соответствующем методе авторизации; rollback [Needs confirmation].

## Metric relabel: действие ПОСЛЕ scrape, ДО записи

**State-changing:** эти правила исключают метрики/метки из хранилища. Важный риск: `up` не попадает под `metric_relabel_configs`, а переданные по сети метрики уже потратили полосу и ресурсы на парсинг (PDF 167–168). Проверка: ожидаемое отсутствие сохранённых рядов при сохранении метрики `up` самого scrape; rollback [Needs confirmation].

**Пример 8.26, PDF 167–168:**
```yaml
scrape_configs:
 - job_name: prometheus
   static_configs:
    - targets:
       - localhost:9090
   metric_relabel_configs:
    - source_labels: [__name__]
      regex: http_request_size_bytes
      action: drop
```

**Пример 8.27, PDF 168:** `source_labels: [__name__, le]`, `regex: 'prometheus_tsdb_compaction_duration_seconds_bucket;(4|32|256)'`, `action: drop`. Книга запрещает удалять bucket `+Inf` в таком сценарии.

**Пример 8.28, PDF 168–169:** `regex: 'node_.*'`, `action: labeldrop` в `metric_relabel_configs`; риск удалить label, от которого зависит уникальность временных рядов. `labelkeep` требует явно оставить важные `__name__`, `le`, `quantile` (PDF 169).

## `honor_labels` и конфликт имени (PDF 169)

**State-changing:** `honor_labels: true` меняет приоритет между target labels и метками, экспортированными приложением. По умолчанию при конфликте `job` исходная инструментированная метка переименовывается в `exported_job`; при `honor_labels` приоритет у экспортированной метки. Для Pushgateway `instance=""` при `honor_labels: true` имеет особую семантику отсутствия instance. Проверить полный состав меток до сохранения. Rollback [Needs confirmation].

## Source defects

- PDF 163: `__meta_ec2_public_tag_monitor_(.*)` в 8.21 не согласован с именами `__meta_ec2_tag_*` (PDF 153, 163).
- PDF 166–167: учебный блок двух заданий содержит `relabel`, а не `relabel_configs`, поэтому **не распространяется как запускаемый YAML**.
- PDF 167: слово `metrics_relabel_configs` (мн. число) конфликтует с ключом `metric_relabel_configs` из примеров 8.26–8.28.
- PDF 157: строка regex `a(b/c*)` рядом с описанием чередования не соответствует форме `infra|monitoring` (PDF 155); сохранить как исходную проблему, не использовать в продуктивных правилах.
