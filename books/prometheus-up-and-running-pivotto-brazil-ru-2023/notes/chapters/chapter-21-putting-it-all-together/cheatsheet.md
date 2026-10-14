# Cheatsheet — глава 21: внедрение и эксплуатация Prometheus

**Источник:** PDF 350–374, `p0350:c01`–`p0374:c01`, strict `rag_only`. Все рекомендации — в границах версии/опыта книги, конкретная инфраструктура [Needs confirmation]. **Не запускались команды, не менялись настройки и не удалялись данные.**

## Выбор архитектуры

| Проблема/симптом | Предпосылки | Read-only проверка | Интерпретация / следующий шаг |
| --- | --- | --- | --- |
| Внедрение с нуля | Нет охвата инфраструктуры | Инвентаризация Node/Windows, JVM, SNMP, внешних endpoint (PDF 350–351) | Запустить небольшой локальный Prometheus, добавить экспортёры, затем RED в общих библиотеках |
| Рост кардинальности | Команды/приложения добавили labels | `scrape_samples_scraped`, `scrape_samples_post_metric_relabeling`, cardinality query (PDF 352, 369–370) | Предпочесть исправить код, затем targeted drop или выделенный сервер |
| Нужно видеть все ЦОД | Локальные автономные Prometheus | Проверить наличие агрегатов `job:.*` и уникальные external labels (PDF 353–356) | `/federate` для агрегированных рядов; не копировать все instance |
| Не хватает истории | Планирование capacity на годы | Ingest samples/sec, retention, требуемые метрики, стоимость (PDF 356–360) | Snapshot/remote storage, selective remote write; протестировать на нагрузке |
| Нет алертов при падении Prometheus | Одна машина/зона отказа | Проверить число реплик, сеть и дедуп labels Alertmanager (PDF 364–366) | Две реплики для оповещений, согласованное `alert_relabel_configs` |
| Alertmanager недоступен | Все уведомления зависят от одного процесса | Проверить peer list, полный fanout со всех Prometheus (PDF 366–367) | Кластер Alertmanager с допускаемыми дубликатами при partition |
| Сломался мониторинг мониторинга | Self-scrape не выявляет падение Prometheus | Перекрестный опрос, meta-Prometheus, heartbeat (PDF 367–368) | Метамониторинг и end-to-end dead-man switch на всю цепочку |
| Графики тайм-аутят | Медленные rules/дорогие запросы | `prometheus_rule_group_iterations_missed_total`, `...last_duration_seconds`, `...interval_seconds` (PDF 368–369) | Сначала диагностика, затем оптимизация метрики и recording rules |
| Опрос цели превышает лимит | Высокая кардинальность | `scrape_duration_seconds`, `scrape_samples_scraped` (PDF 369) | Снизить series, временно sampling с `hashmod`; не создавать единую proxy TSDB |
| В системе NAT/firewall | Prometheus не может опрашивать targets | Проверить network path и доступность (PDF 362) | Prometheus внутри зоны целей; при необходимости PushProx, SSH или proxy_url, НЕ Pushgateway |
| Требуются сложные авторизации | Native web security недостаточно | Сопоставить `--web.external-url`/`--web.route-prefix`, reverse proxy (PDF 362–363) | Инфраструктурная аутентификация на proxy; учесть конфликт про TLS с гл.20 |
| Изменились label names | Эволюция систем | Проверить потребителей исторических рядов (PDF 373) | Записать историю изменений; stable recording rules как API для длительной аналитики |

## Read-only preflight и диагностика

1. **Планирование:** выбрать область отказа, частоту scrape/evaluation и схему labels для каждого сервера. Не тянуть локальное оповещение через global federation (PDF 351–356).
2. **Нагрузка ingest:** `rate(prometheus_tsdb_head_samples_appended_total[5m])` (PDF 359). Источниковая оценка для диска 2 bytes/sample, сети 20 bytes/sample; SSD, выделенный TSDB directory, отказаться от NFS; память и CPU зависят от query/rules (PDF 359–360).
3. **Recording rules:** контролировать `prometheus_rule_group_iterations_missed_total`; сравнить `prometheus_rule_group_last_duration_seconds` с `prometheus_rule_group_interval_seconds`; при приближении/превышении время оценки становится критическим (PDF 369).
4. **Notifications:** `prometheus_notifications_dropped_total`; очередь `prometheus_notifications_queue_length` относительно `prometheus_notifications_queue_capacity` (PDF 369).
5. **Service discovery и storage:** `prometheus_sd_file_read_errors_total`, `prometheus_sd_ec2_refresh_failures_total`, `prometheus_rule_evaluation_failures_total`, `prometheus_tsdb_compactions_failed_total`, `prometheus_tsdb_wal_corruptions_total` (PDF 369). Названия/доступность зависят от версии.
6. **Стоимость series:** `topk(10, count by(__name__)({__name__=~".+"}))` — **potentially expensive**, перебирает все активные ряды (PDF 369). Сначала использовать дешёвые per-target scrape metrics (PDF 369).
7. **Надёжность:** убедиться, что Alertmanager сравнивает **совпадающие alert labelsets** для дублей, хотя external labels самих серверов уникальны для federation/remote write (PDF 364–366). Разделять критерии HA алертов и непрерывности графиков.
8. **Шардирование:** `hashmod` по `__address__` и `modulus` задаёт неизменяемый assignment без многократного выполнения одного target. `modulus:10`, `keep regex:0` отбирает один bucket, а `modulus:4`, `scraper:2`, `keep regex:2` — shard 2/4 (PDF 370–372).
9. **Проверка конфигурации:** тестовый Prometheus не должен отправлять реальные уведомления или remote-write данные; авторы советуют удалить эти настройки перед тестовым запуском (PDF 361–362).

## Семантика, которую нельзя терять

- **Федерация ≠ remote_read ≠ remote_write.** Федерация получает селективные агрегаты; remote_write отправляет samples по мере появления; remote_read даёт TSDB-запросам историю другого хранилища (PDF 353–358).
- **Два Prometheus**: разрешают HA уведомлений при общих labels; но автоматическое переключение Grafana между неидеально совпадающими рядами может создавать артефакты, в source для дашбордов автор предпочитает один источник с возможными пробелами (PDF 364–366).
- **Retention:** `--storage.tsdb.retention.size` не обязан точно соответствовать глубине истории; при уплотнении появляются дополнительные требования к объёму (PDF 359).
- **Drop vs сеть:** `metric_relabel_configs` снижает объём записываемых series, но метрика уже передана и распарсена (PDF 370–371). `sample_limit` превышен → весь scrape ошибочный и samples не загружены (PDF 371).
- **Пропуски и точность:** автор считает предсказуемую нагрузку важнее бесконечных retry; failed scrape даёт `up=0`, диапазон `rate` ≥4× scrape interval помогает пережить случайный miss (PDF 363–364). Это не универсальный SLO.
- **`read_recent:true`** на shard remote_read отключает оптимизацию, предотвращающую удалённые запросы для недавних локальных данных (PDF 372); повышенный риск нагрузки.

## Next action / modifying action / verification / rollback

- **Рекомендуемый ход:** измерить ingest, cardinality и latency; сначала исправить инструментированную метрику или отделить перегруженную команду, затем только при необходимости увеличивать количество scrapers/federation/storage (PDF 351–373).
- **State-changing:** редактировать/активировать `prometheus.yml`, `alertmanager.yml`, `relabel_configs`, `metric_relabel_configs`, `sample_limit`, `remote_write/read`, retention и `--web.enable-admin-api`; менять маршруты оповещений и storage (PDF 353–372). Реальные владельцы, approval/backup/rollback [Needs confirmation].
- **Высокий риск/разрушительно:** `/api/v1/admin/tsdb/delete`, удаление или переименование TSDB каталога, работа с snapshot, изменение federation/shard routing. Не выполнять без резервирования и конкретного согласованного плана (PDF 356–357, 369).
- **Verification:** сравнить expected series/labels, поработоспособность локальных alerts в WAN outage, метрики rule eval/notifications/TSDB, отсутствие неожиданных дублей или потерянных alerts, наличие автономной истории (PDF 354–369).
- **Rollback [Needs confirmation]:** книга перечисляет идеи snapshot/restart, но не задаёт воспроизводимой процедуры безопасного rollback ошибочного удаления/массового relabel или полного восстановления недостающих samples.

Подробные выражения, пути и исходные исключения — [commands.md](commands.md) и [source-findings.md](source-findings.md).
