# Commands, Prometheus конфигурация и Blackbox/Grok — глава 10

**Источник:** PDF 187–208 (`p0187:c01`–`p0208:c01`), `rag_only`. Исходные версии: Consul Exporter 0.8.0, MySQLd 0.9.0, Grok 0.2.8, Blackbox 0.22.0. **Никакие команды не выполнялись.** Классы `read-only`, `workload-generating`, `state-changing`. Для запуска/правки исходник не сообщает полного rollback: **[Needs confirmation]**.

## Consul Exporter (PDF 187–189)

**State-changing:** скачивание, извлечение и запуск exporter. Буквальный адрес **не рекомендуется копировать**: URL включает каталог `v0.3.0`, тогда как имя архива и запускаемый бинарник соответствуют `0.8.0` (PDF 188; [source-findings.md](source-findings.md)).

```text
wget https://github.com/prometheus/consul_exporter/releases/download/v0.3.0/consul_exporter-0.8.0.linux-amd64.tar.gz
tar -xzf consul_exporter-0.8.0.linux-amd64.tar.gz
cd consul_exporter-0.8.0.linux-amd64/
./consul_exporter
```

Это **транскрипция учебного примера, не проверенный install script**. Риск: неизвестная доступность URL/архива и изменение работы хоста. Verification: `http://localhost:9107/metrics`, `consul_up`, `consul_catalog_service_node_healthy`, `consul_serf_lan_members`. Rollback [Needs confirmation].

**State-changing — `prometheus.yml`, пример 10.2, PDF 189:**

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: consul
   static_configs:
    - targets:
      - localhost:9107
```

При проблемах Consul одновременно **read-only** проверять `up` и `consul_up`; `consul_exporter_build_info`, `process_*`, `go_*` характеризуют сам exporter (PDF 188).

## MySQLd Exporter (PDF 189–190)

**State-changing, чувствительные доступы:** пример 10.3 демонстрирует использование Docker mysql client с `--net=host`, создание пользователя и выдачу разрешений. **Демонстрационные исходные пароли не воспроизводятся.** Для DBA/оператора ниже приведены только структурные операции с заменителями; это **санитизированная запись**, не буквальный runnable скрипт. Действия могут изменять полномочия и поверхность доступа БД; предварительная проверка прав обязательна. Rollback [Needs confirmation].

```text
docker run -it --net=host --rm mysql mysql -h 127.0.0.1 -P 3306 -uroot -p<ADMIN_PASSWORD_PLACEHOLDER>
CREATE USER 'prometheus'@'127.0.0.1' IDENTIFIED BY '<MONITORING_PASSWORD_PLACEHOLDER>' WITH MAX_USER_CONNECTIONS 3;
GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'prometheus'@'127.0.0.1';
```

**State-changing — `~/.my.cnf`, пример 10.4 (секрет замещён placeholder):**

```ini
[client]
user = prometheus
password = <MONITORING_PASSWORD_PLACEHOLDER>
host = 127.0.0.1
```

Нужна отдельная локальная проверка владельца/прав файла с секретом и согласование более узкой политики прав: [Needs confirmation]. Проверка: при успешной работе exporter `http://localhost:9104/metrics` содержит `mysql_up`, `mysql_global_variables_*`, `mysql_global_status_*` (PDF 190).

**State-changing — исторический установочный блок, пример 10.5 (PDF 189), не подтверждён для текущей версии:**

```text
wget https://github.com/prometheus/mysqld_exporter/releases/download/v0.9.0/mysqld_exporter-0.9.0.linux-amd64.tar.gz
tar -xzf mysqld_exporter-0.9.0.linux-amd64.tar.gz
cd mysqld_exporter-0.9.0.linux-amd64/
./mysqld_exporter
```

**State-changing — scrape job, пример 10.6, PDF 190:**

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: mysqld
   static_configs:
    - targets:
      - localhost:9104
```

## Grok Exporter: журналы → метрики (PDF 191–193)

**State-changing:** создать `example.log` и `grok.yml`, затем запустить `./grok_exporter -config grok.yml`. **Workload-generating:** чтение и разбор всего журнала при `readall: true`; сам источник указывает, что в production использовать `false`. Verification: локальный exporter `http://localhost:9144`. Rollback [Needs confirmation].

**Исходный пример журнала:**

```text
GET /foo 1.23
GET /bar 3.2
POST /foo 4.6
```

**Исходная конфигурация Grok, пример 10.7:**

```yaml
global:
  config_version: 2
input:
  type: file
  path: example.log
  readall: true  # В промышленном окружении используйте значение false
grok:
  additional_patterns:
   - 'METHOD [A-Z]+'
   - 'PATH [^ ]+'
   - 'NUMBER [0-9.]+'
metrics:
 - type: counter
   name: log_http_requests_total
   help: HTTP requests
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   labels:
     path: '{{.path}}'
 - type: histogram
   name: log_http_request_latency_seconds_total
   help: HTTP request latency
   match: '%{METHOD} %{PATH:path} %{NUMBER:latency}'
   value: '{{.latency}}'
server:
   port: 9144
```

**State-changing / workload-generating:** `./grok_exporter -config grok.yml` (PDF 192). По PDF 193 ожидаемый Counter `log_http_requests_total{path="/bar"} 1` и `{path="/foo"} 2`. **Важно:** показанные значения histogram `_sum 0.57`, `_count 3` и buckets **не согласованы** со значениями 1.23, 3.2, 4.6 в исходном журнале. Не использовать этот числовой вывод как golden test. Отдельно имя histogram имеет суффикс `_total` по источнику; см. [source-findings.md](source-findings.md).

**State-changing — scrape job Grok, пример 10.8, PDF 193:**

```yaml
global:
  scrape_interval: 10s
scrape_configs:
 - job_name: grok
   static_configs:
    - targets:
       - localhost:9144
```

## Blackbox Exporter (PDF 193–208)

**State-changing и привилегированное исполнение — пример 10.9:** в книге описаны `wget` выпуска `v0.22.0`, `tar -xzf`, `cd`, `sudo ./blackbox_exporter`; требует низкоуровневых ICMP-sockets и позволяет альтернативу `CAP_NET_RAW` (PDF 194–195). **Не запускать с sudo без согласования прав и ограничений**. Версия устаревшая для современного стенда: [Needs confirmation]. Rollback [Needs confirmation].

**Read-only** просмотр локальной страницы статуса `http://localhost:9115/`; путь `/metrics` — здоровье процесса самого Blackbox. **Workload-generating** `/probe` генерирует сетевые запросы даже когда вызывается через GET; считать каждую проверку внешним воздействием (PDF 194–196).

| Пример HTTP GET из книги | Класс / роль |
| --- | --- |
| `http://localhost:9115/probe?module=icmp&target=localhost` | workload-generating, локальный ICMP |
| `http://localhost:9115/probe?module=icmp&target=www.google.com&debug=true` | workload-generating, внешняя цель; debug содержит подробный вывод |
| `http://localhost:9115/probe?module=icmp_ipv4&target=www.google.com` | workload-generating; требует предварительной настройки blackbox.yml |
| `http://localhost:9115/probe?module=tcp_connect&target=localhost:22` | workload-generating, подключение TCP |
| `http://localhost:9115/probe?module=http_2xx&target=https://www.oreilly.com/` | workload-generating, HTTP(S) |
| `http://localhost:9115/probe?module=dns_tcp&target=8.8.8.8` | workload-generating, TCP DNS query |
| `http://localhost:9115/probe?module=dns_mx_present_rp_io&target=8.8.8.8` | workload-generating, DNS MX |

Адреса внешних систем — **учебные цели**, их доступность и разрешение probing не установлены, поэтому не запускались. В книге показан URL с нарушенным пробелом `& target=...` на PDF 196 — не копировать как валидную строку: [source-findings.md](source-findings.md).

### Blackbox modules (state-changing: редактирование `blackbox.yml`)

**ICMP**, PDF 196 и 198–199:
```yaml
icmp:
  prober: icmp
icmp_ipv4:
  prober: icmp
  icmp:
    preferred_ip_protocol: ip4
```

**Источник в прозе пишет `selected_ip_protocol: ipv4`, а YAML использует `preferred_ip_protocol: ip4`**. YAML здесь приведён как буквальный пример, не как подтверждённый релизный API. Verification: debug / `probe_ip_protocol`; rollback [Needs confirmation].

**TCP, SSH баннер и TLS**, PDF 199–200:

```yaml
tcp_connect:
  prober: tcp
ssh_banner:
  prober: tcp
  tcp:
    query_response:
    - expect: "^SSH-2.0-"
tcp_connect_tls:
  prober: tcp
  tcp:
    tls: true
```

Метрика `probe_failed_due_to_regex` диагностирует несоответствие баннера; `probe_ssl_last_chain_expiry_timestamp_seconds` — срок действия сертификата TLS (PDF 200).

**HTTP**, PDF 202–203:

```yaml
http_200_ssl_prometheus:
  prober: http
  http:
    valid_status_codes: [200]
    fail_if_not_ssl: true
    fail_if_not_matches_regexp:
      - oreillymedia
```

**Несогласованность:** окружающий текст обещает проверку слова «Prometheus», а regex проверяет `oreillymedia` (PDF 202–203). Точная семантика не заменяется молча; проверить целевой URL и ожидаемый текст: [Needs confirmation].

**DNS**, PDF 204:

```yaml
dns_tcp:
  prober: dns
  dns:
    transport_protocol: "tcp"
    query_name: "www.prometheus.io"
dns_mx_present_rp_io:
  prober: dns
  dns:
    query_name: "prometheus.io"
    query_type: "MX"
    validate_answer_rrs:
      fail_if_not_matches_regexp:
        - ".+"
```

DNS-цель `target` — сервер DNS, `query_name` — запрашиваемая запись. В книге также сравнивается с `dig -tcp @8.8.8.8 www.prometheus.io`; это **workload-generating**, не команда, выполнявшаяся в данном анализе (PDF 204).

### Prometheus → Blackbox multitarget (пример 10.10, PDF 205–206)

**State-changing:** relabel-конфигурация меняет фактический адрес scrape и параметр пробы; `__param_target` хранит проверяемый сайт, `instance` сохраняет его идентичность, `__address__` указывает на Blackbox. Verification: Targets, `up`, `probe_success`. Rollback [Needs confirmation].

```yaml
scrape_configs:
 - job_name: blackbox
   metrics_path: /probe
   params:
     module: [http_2xx]
   static_configs:
    - targets:
       - http://www.prometheus.io
       - http://www.robustperception.io
       - http://demo.robustperception.io
   relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: 127.0.0.1:9115
```

Последние два relabel правила и адрес exporter продолжаются на PDF 206. **Этот список targets — буквальный из первоначального листинга PDF 205**, а в повторном разборе PDF 206 приведён **другой** набор целей (`https://www.prometheus.io`, `https://www.oreilly.com`, `https://demo.do.prometheus.io`); source finding, не тихое исправление.

**Пример 10.11, PDF 207:** альтернативно `consul_sd_configs` с `server: 'localhost:8500'`; `__meta_consul_address` преобразуется в `__param_target` через `replacement: '${1}:22'`, затем `instance`, а `__address__=127.0.0.1:9115`. Это проверка SSH с `module: [ssh_banner]`. **State-changing** для prometheus.yml, **workload-generating** для каждой цели; проверить scope discovered hosts, rollback [Needs confirmation].

### Timeout и диагностика (PDF 208)

- `scrape_timeout` **state-changing** — задаёт окно опроса Prometheus.
- Заголовок `X-Prometheus-Scrape-Timeout-Seconds` **автоматический**, не инструкция по ручной отправке.
- Параметр `timeout` в blackbox.yml и флаг `--timeout-offset` **state-changing** — ограничивают время probe; точные значения не указаны, rollback [Needs confirmation].
- `SIGHUP` назван способом reload Blackbox (PDF 199), но источником **не приведена конкретная shell-команда посылки сигнала**; не изобретать.
