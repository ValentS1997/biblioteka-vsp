# Cheatsheet — глава 10: популярные экспортеры

**Основание:** PDF 187–208, RAG `p0187:c01`–`p0208:c01`. Примеры источника исторические: Consul Exporter 0.8.0, MySQLd Exporter 0.9.0, Grok Exporter 0.2.8, Blackbox Exporter 0.22.0; текущая совместимость [Needs confirmation].

## Symptom / problem framing

- `up=1`, но сервис не отвечает: Prometheus сумел опросить exporter, а не обязательно исходный Consul/MySQL/HTTP endpoint (PDF 188, 190, 196, 206).
- Экспортер не может преобразовать выходные данные приложения: в книге предложен Grok Exporter как вариант для журналов, требующий явных regex и семантики метрик (PDF 190–193).
- Нужно проверить внешний сайт / DNS / SSH: Blackbox запускает пробу по `/probe?module=...&target=...` и отдаёт `probe_success` (PDF 193–205).
- У Blackbox `probe_success=0`, а ping прошёл: по примеру может различаться разрешение имён/DNS и выбор IPv4/IPv6; получить debug и посмотреть `probe_ip_protocol` (PDF 196–199).
- Много целей, но одна конфигурация Blackbox: маршрутизировать `__address__` → `__param_target` → `instance`, а затем адрес самого exporter через relabel (PDF 205–207).
- Высокая кардинальность от произвольных лог-меток или экспортеров: оценить стабильность меток и поведение `metric_relabel_configs` (PDF 187, 191–193).

## Baseline / context

- Для процесса предпочтителен exporter рядом с экземпляром, а не один exporter на много произвольных задач; Blackbox/SNMP — удалённые зонды (PDF 187, 193–194).
- Consul Exporter по примеру слушает `:9107`, Consul `:8500`; основные метрики `consul_up`, `consul_catalog_service_node_healthy`, `consul_serf_lan_members` (PDF 187–189).
- MySQLd Exporter `:9104`; нужен мониторинговый DB-user и `~/.my.cnf`, без передачи пользовательских секретов в Git (PDF 189–190).
- Grok Exporter `:9144` читает `example.log`, извлекает `log_http_requests_total{path=...}` и histogram, использует `readall: true` лишь для демонстрации (PDF 191–193).
- Blackbox Exporter `:9115`: `/metrics` — метрики процесса exporter, `/probe` — метрики пробы; целевой ресурс задаёт параметр `target`, модуль — `module` (PDF 194–196).
- ICMP может требовать `sudo` / `CAP_NET_RAW`, исходный запуск `sudo ./blackbox_exporter`; production-права [Needs confirmation] (PDF 194–195).
- Тайм-аут Blackbox учитывает заголовок `X-Prometheus-Scrape-Timeout-Seconds`; опция `timeout` модуля может ограничить дополнительно (PDF 208).

## Read-only checks

1. Смотреть Consul exporter `http://localhost:9107/metrics`, проверять **обе** `up` и `consul_up` (PDF 188).
2. Смотреть MySQLd exporter `http://localhost:9104/metrics`, `mysql_up`, `mysql_global_variables_*` и `mysql_global_status_*` (PDF 190).
3. Смотреть Grok `http://localhost:9144`, проверять `log_http_requests_total` по `path`, histogram `_bucket/_count/_sum`, сверять с реальным журналом (PDF 191–193). В учебном примере есть внутреннее расхождение чисел.
4. Просмотреть `http://localhost:9115/` — страница состояния Blackbox; `http://localhost:9115/probe?module=icmp&target=localhost` — ICMP-проба (PDF 194–195).
5. При сбое открыть учебный debug `.../probe?module=icmp&target=www.google.com&debug=true`; это **создаёт сетевую нагрузку**, хотя не меняет локальные данные (PDF 197–198).
6. Для TCP `?module=tcp_connect&target=localhost:22` или модуль `ssh_banner`; для HTTP `?module=http_2xx&target=https://www.oreilly.com/`; для DNS `?module=dns_tcp&target=8.8.8.8` (PDF 199–204).
7. На Prometheus Targets проверить, что `instance` содержит URL исходной цели, а `__address__` перед scrape указывает на локальный Blackbox `:9115` (PDF 205–207).

## Interpretation

- `probe_success=1` — успешная проверка, `0` — ошибка; метрика `up` проверяет сам exporter (PDF 196, 206).
- `probe_http_duration_seconds{phase=...}` раскладывает длительность на `resolve`, `connect`, `tls`, `processing`, `transfer`; `probe_http_status_code` и `probe_http_redirects` помогают разбирать HTTP (PDF 201–202).
- `probe_ssl_last_chain_expiry_timestamp_seconds` и `probe_ssl_earliest_cert_expiry` в книге связаны со сроком жизни цепочки сертификатов (PDF 200–202).
- `probe_failed_due_to_regex` при проверке `ssh_banner` становится 1, если баннер не совпадает (PDF 200).
- В исходнике встречается конфликт `probe_ip_protocol=6` и словесного IPv4 на PDF 196 vs. IPv6 на PDF 197. Не определять версию протокола по несовместимому объяснению без отдельного подтверждения (см. [source-findings.md](source-findings.md)).
- GROK histogram пример на PDF 193 нельзя использовать как эталон численной агрегации входного лога: есть несоответствие суммы и bucket значениям исходных задержек (PDF 191–193).

## Next action

- Сначала определить класс задачи: нужен внутренний Counter/Gauge приложения, его exporter, лог-конвертация или удалённая blackbox-проверка (PDF 187–194).
- При сбоях Consul/MySQL сверить `up` и `*_up`, затем метрики exporter, а не предполагать, что scrape подтверждает здоровье приложения (PDF 188–190).
- Если `probe_success=0`, читать debug, DNS/IP-предпочтение и отдельные фазы/ответы; решение о создании нового Blackbox-модуля принимать после диагностики (PDF 195–204).
- Для множества сайтов применить relabel-архитектуру `__param_target`, `instance`, `__address__` без открытого прокси (PDF 205–207).

## Modifying action

- Загрузка и запуск исторических двоичных экспортёров, создание `my.cnf`, DB-user и GRANT — **state-changing**; возможны утечки паролей и изменение прав БД (PDF 188–190).
- `./grok_exporter -config grok.yml` с `readall: true` анализирует весь файл и создаёт метрики; производственное `false` в источнике (PDF 191–192).
- `sudo ./blackbox_exporter` и сетевые пробы — привилегии/сетевая нагрузка; **не выполнять без локального одобрения**, минимальные права [Needs confirmation] (PDF 194–195).
- Изменения `blackbox.yml` для ICMP/TCP/HTTP/DNS и `prometheus.yml` для relabel меняют целевые запросы/метрики; источник описывает перезапуск или `SIGHUP` для Blackbox, но не даёт полного плана rollback (PDF 198–208).
- Перед любым автоматическим Blackbox probing оценить допустимость тестируемых целей и запретить использование exporter как открытого сетевого прокси (PDF 203).

## Verification / acceptance checks

- Экспортер отвечает `/metrics`, приложение отдельно сообщает здоровье через `consul_up`/`mysql_up`; проверить изменяющиеся состояния на тестовом стенде (PDF 188–190).
- Grok Counters/Histograms соответствуют **фактическому** логу, а не несогласованным числам примера; histograms проверяются по bucket/count/sum (PDF 191–193).
- Blackbox `/probe` показывает результат `probe_success` и фазовые метрики; Prometheus Targets отражает `instance` проверяемого ресурса, а exporter отвечает на `:9115` (PDF 195–207).
- Scrape timeout не меньше фактической длительности в тестовой среде; точные значения и безопасные пороги не указаны: [Needs confirmation] (PDF 208).
- Секреты БД, Kubernetes/OS privileges и доступность публичных доменов в пользовательской среде [Needs confirmation].

## Rollback

- Для изменений DB-user, внешних бинарников, конфигурации и Blackbox-модулей в главе **не приведён безопасный пошаговый rollback**: [Needs confirmation].
- Возврат предыдущей конфигурации и ревизий требует внешнего контроля версии/владельцев/доступа; не создавать отсутствующие в RAG shell-команды.
- Действия с доступом к БД и root Blackbox запуском не производились.
