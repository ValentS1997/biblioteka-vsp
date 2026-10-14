# Cheatsheet — глава 11: другие системы мониторинга

**Provenance:** canonical RAG `p0209:c01`–`p0214:c01`, PDF 209–214. Версии из учебного источника, без внешних подтверждений.

## Symptom / problem framing

- У приложений уже есть InfluxDB/StatsD/collectd/Graphite/JMX и невозможно сразу перейти на прямое инструментирование Prometheus: выбирать соответствующий exporter для постепенного перехода (PDF 209–211).
- Приложение отправило timestamp InfluxDB, но `/metrics` выводит значение без времени: exporter отражает текущую метрику и Prometheus присваивает время scrape (PDF 212).
- StatsD событие пришло на порт 9125, но Prometheus ничего не собирает: порт событий (TCP/UDP) отличен от HTTP `:9102/metrics` (PDF 213).
- После перевода dot-separated StatsD имён нет labels `region`/`path`: нужно явное `mapping.yml` и флаг `-statsd.mapping-config` (PDF 213–214).
- Один общий exporter стал узким местом или продолжает жить после приложения: авторы предлагают один exporter на экземпляр с синхронизированным lifecycle (PDF 214).
- SNMP медленно отвечает: проверить близость экспортера к устройствам, объём выбранных OID/метрик и `scrape_interval` (PDF 210).

## Baseline / context

- **InfluxDB Exporter 0.10.0** по книге: HTTP `http://localhost:9122/write` для line protocol и `http://localhost:9122/metrics` для pull (PDF 211–212).
- **StatsD Exporter 0.22.8:** TCP/UDP `:9125` для событий и Prometheus `:9102` для метрик (PDF 213).
- StatsD `|g` — Gauge, `|c` — Counter, `|ms` — timing observation. Точные типы экспортируемых timer-series/единицы в конкретной версии [Needs confirmation] (PDF 213).
- `app.http.requests.eu-west-1./foo:1|c` → `app_http_requests_total{region="eu-west-1",path="/foo"} 1`, благодаря шаблону `match: app.http.requests.*.*` (PDF 213–214).
- `collectd` не имеет labels в описании книги; `Graphite` имеет точечные имена, но Graphite 1.1.0 добавил tags (PDF 209–210).
- JVM JMX Exporter — Java agent с regex mapping mBean; SNMP Exporter — устройство/MIB/generator; SaaS API — квоты и возможная стоимость (PDF 210).

## Read-only checks

1. Открыть `http://localhost:9122/metrics`; после учебного `/write` проверить `example_metric{foo="bar"} 43`. **Присутствие ряда без исходного timestamp ожидаемо** (PDF 212).
2. Открыть `http://localhost:9102/metrics`; проверить `example_gauge 123`, а после `mapping.yml` — `app_http_requests_total` с labels (PDF 213–214).
3. Проверить конфигурацию Prometheus `scrape_configs`: для InfluxDB source example `job_name: application_name`, `localhost:9122` (PDF 212). Для StatsD source не приводит отдельного `prometheus.yml` scrape job в PDF 212–214; не придумывать.
4. Сопоставить реальные единицы `|ms` с желаемыми базовыми единицами Prometheus: в книге предупреждение, что стандартизация StatsD и единицы часто неоднозначны (PDF 213).
5. Для dot-separated mapping сверить `labels.region` и `labels.path`; в текстовом объяснении region отличается от вывода по наличию дефиса (PDF 213–214).
6. Проверить, что импортирующий exporter живёт в том же цикле запуска/остановки приложения (PDF 214); конкретный инструмент контроля жизненного цикла в главе не задан.

## Interpretation

- Отправленный timestamp InfluxDB в JSON/line protocol не означает, что будет сохранено старое время образца в Prometheus: он привязывается к времени scrape по объяснению авторов (PDF 212).
- `StatsD` принимает события и агрегирует их внутри exporter, а не передаёт на каждый event отдельный time series sample (PDF 212–213).
- Для SNMP могут потребоваться MIB от поставщиков и собственный generator, устройство может не отвечать за разумное время (PDF 210).
- NRPE годится как временный способ сохранить нестандартные проверки Nagios; JMX/Dropwizard могут потребовать дополнительных расходов и конфигурации (PDF 211).
- SaaS API расходы и rate limits упомянуты без чисел; эксплуатационные лимиты [Needs confirmation] (PDF 210).

## Next action

- Разделить переходные системы по модели данных: line protocol (InfluxDB), события (StatsD), dot hierarchy (Graphite), JMX mBean, SNMP/MIB, облачный API (PDF 209–211).
- Для InfluxDB подтвердить требования к timestamp/history: если важен исходный timestamp, глава **не даёт решения через описанный exporter** (PDF 212).
- Для StatsD сделать целевые labels явно через mapping и согласовать метрики с API/запросами; использовать `readall` здесь не относится к StatsD (PDF 213–214).
- Запускать push-to-pull exporter на каждый экземпляр с единым lifecycle, чтобы избежать stale series, изменения labels и масштабного узкого места (PDF 214).

## Modifying action

- Запуск `./influxdb_exporter`, `./statsd_exporter` — процесс/порт, state-changing, workload-generating; зависит от текущего бинарника, прав и OS (PDF 211, 213).
- `curl -XPOST .../write --data-binary ...` отправляет и изменяет состояние экспортера; **не read-only**, несмотря на возможность последующего GET /metrics (PDF 212).
- `echo 'example_gauge:123|g' | nc localhost 9125` и counters/timers — передают StatsD события и изменяют агрегаты экспортера; **workload-generating / state-changing для измеряемого состояния** (PDF 213–214).
- Запись `mapping.yml` и запуск `./statsd_exporter -statsd.mapping-config mapping.yml` меняют интерпретацию labels; поведение промышленных версий: [Needs confirmation] (PDF 213–214).
- Для SNMP изменение конфигурации/опроса устройств может создать нагрузку; в книге нет готовых команд/файлов (PDF 210).

## Verification / acceptance checks

- InfluxDB пример показывает `example_metric{foo="bar"} 43` при `/metrics` и отсутствие исходного timestamp; Prometheus может опрашивать endpoint `:9122` (PDF 212).
- StatsD `example_gauge 123` выводится у `:9102/metrics`; маппинг создаёт два Counter-children с регионами/путями `/foo`, `/bar` (PDF 213–214).
- У каждого приложения отдельный exporter, запускается/останавливается вместе с ним: проверка в реальном runtime [Needs confirmation] (PDF 214).
- Численные ограничения API, латентность SNMP и соответствие типов в текущих релизах должны измеряться отдельно: [Needs confirmation].

## Rollback

- PDF 209–214 **не содержит процедуры безопасного rollback** бинарников, mapping или scrape config: [Needs confirmation].
- Отменить старые push-события как обратимую операцию источник не позволяет; восстановление прежних агрегатов/labels возможно лишь по внешней процедуре: [Needs confirmation].
- Никакие команды не выполнялись и реальные данные не изменены.
