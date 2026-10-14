# Глава 21. Собираем все вместе

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023). **Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`; **статус:** `RAG_GROUNDED` (не `VERIFIED` / `ACCEPTED`).  
**Source policy:** строгий `rag_only`: только канонические RAG-чанки; прямого чтения PDF, web и модельного восполнения исходника не было.

## Границы и происхождение

- PDF **350**, `p0350:c01`: «Глава 21. Собираем все вместе». PDF **374**, `p0374:c01`: конец раздела «Получение помощи» и заключение книги; PDF **375**, `p0375:c01`: начало «Предметного указателя».
- **PDF/печатные страницы: 350–374**; `source_locator: pdf_page=350..374`. **25 чанков** `p0350:c01`–`p0374:c01`, каталог `rag/chunks/p0301-p0400/`.
- Исходный PDF SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; книжное `rag/acceptance.yaml: ACCEPTED`, `rag/manifest.yaml: READY_WITH_KNOWN_LIMITATIONS`. Исторический контекст Prometheus 2.x, Alertmanager 0.24.0, экспериментальный agent mode, не текущая документация.

## Карта главы

| Раздел | PDF | О чём говорится |
| --- | --- | --- |
| Планирование развертывания | 350–351 | Начать с Node Exporter/Prometheus → экспортеры SNMP/JMX/Blackbox → инструментирование приложений, RED и интеграции StatsD/Graphite |
| Расширение Prometheus | 351–353 | Рядом с целями и областью отказа; один Prometheus на ЦОД как отправная точка; вертикальное сегментирование по командам/системам |
| Глобальная федерация | 353–356 | Агрегаты через `/federate`, `match[]`, `honor_labels`, `external_labels`; ограничить global cardinality |
| Долгосрочное хранение | 356–358 | Snapshot/delete admin API, `--web.enable-admin-api`, remote_write/read, `write_relabel_configs`, Thanos/Cortex/Mimir, experimental agent |
| Эксплуатация: ресурсы | 358–360 | Samples/sec, TSDB, retention, SSD, RAM, CPU, сеть, fd и запас мощности |
| Конфигурация и сеть | 360–363 | Unix-файлы, SIGTERM/SIGHUP, Ansible/Pulumi/K8s Operator, template external labels, pull, proxy/NAT |
| Планирование сбоев | 363–366 | Разные области отказа, две реплики Prometheus, `alert_relabel_configs` для dedup и уникальные `external_labels` для записи/федерации |
| Кластер Alertmanager | 366–367 | Fanout каждого Prometheus на все Alertmanager, gossip/peer, возможные дубликаты при partition |
| Мета- и перекрёстный мониторинг | 367–368 | Опрос самого мониторинга и взаимный контроль, dead-man switch / external heartbeat |
| Диагностика производительности | 368–371 | Missed rule eval, notification queue, SD, TSDB metrics, `topk` cardinality, `scrape_samples_scraped`, `hashmod`, dropping |
| Горизонтальное сегментирование | 371–373 | `hashmod` раздаёт цели нескольким scrapers, уникальная метка `scraper`, осторожное `remote_read.read_recent: true` |
| Управление изменениями и помощь | 373–374 | Эволюция labels, стабильный метрик-API, сообщества Prometheus и коммерческая поддержка |

## Архитектурные принципы из источника

1. **Внедрение поэтапно:** Node Exporter (Windows Exporter для Windows) + Prometheus, затем готовые экспортеры и метрики своего кода. В HTTP-библиотеках общего пользования начать с RED (Rate, Errors, Duration). Развёртывание консолидации систем мониторинга зависит от среды, а не универсальный приказ (PDF 350–351).
2. **Локальность и изоляция отказов:** Prometheus обычно опрашивает цели в той же сети/ЦОД. Отделение по командам/сервисам («вертикальное сегментирование») предпочтительнее распределённой конструкции из огромного числа зависимых серверов; причина может быть социальной, не только CPU (PDF 351–353).
3. **Федерация — глобальные агрегаты, не глобальный мониторинг каждого instance.** `/federate` с `match[]` и `honor_labels: true`, уникальные `external_labels` для источника. Локальные dashboards и alerts должны оставаться работоспособны при повреждении WAN (PDF 353–356). Не копировать весь TSDB по федерации и не превращать один сервер в proxy другого.
4. **Retention и remote storage:** локальные snapshots `/api/v1/admin/tsdb/snapshot`, административное удаление `/api/v1/admin/tsdb/delete`, удалённая запись/чтение, selective `write_relabel_configs`. Для административных endpoint требуется `--web.enable-admin-api` (PDF 356–358). Это **изменяющие состояние и рискованные** процедуры, не инструкция выполнять их без резервной копии, авторизации и rollback.
5. **Ресурсы надо считать, а не угадывать:** `rate(prometheus_tsdb_head_samples_appended_total[5m])`; source оценка ~2 байта/sampled для диска и ~20 байт сетевого трафика/sampled; для 100 000 samples/sec и 15 дней названо около 240 Гбайт хранилища и 8 Гбайт RAM в качестве отправных точек (PDF 358–360). Цифры не гарантированы для других версий/TSDB/нагрузок.
6. **Файловая система и хранение:** SSD предпочтителен, NFS/EFS не поддерживается в контексте источника; каждый Prometheus должен иметь свой собственный TSDB directory. `--storage.tsdb.retention.time`, `--storage.tsdb.path`, `--storage.tsdb.retention.size` управляют retention и размещением (PDF 359).
7. **Pull-model:** размещать Prometheus внутри зоны, где достижимы цели; использовать прокси/SSH/PushProx при сетевых ограничениях. Pushgateway не предназначен для переноса регулярного мониторинга экземпляров в push и не сохраняет `up`/staleness semantics (PDF 362).
8. **Сбой мониторинга не должен быть единым отказом оповещения.** Две идентично опрашивающие Prometheus-реплики плюс дедупликация Alertmanager. Внешние метки уникальны для источников remote-write/federation; `alert_relabel_configs` может убрать номер реплики из alert labelset **только перед доставкой** (PDF 364–366).
9. **Cluster Alertmanager/AP:** Prometheus отправляет alerts каждому Alertmanager, который использует peer/gossip, silences и задержку между уведомлениями. Network partition может вызвать дубликаты вместо потери уведомлений (PDF 366–367). Мета- и cross-monitoring плюс end-to-end heartbeat обнаруживают отказ самой цепочки мониторинга (PDF 367–368).
10. **Производительность:** сначала использовать низкостоимостные `scrape_samples_scraped`, `scrape_samples_post_metric_relabeling`, `scrape_duration_seconds` и внутренние rule/notification/SD метрики; тяжёлый `topk(count by(__name__))` запускать осторожно. Уменьшать кардинальность в исходной инструментации; `metric_relabel_configs` только снижает TSDB storage, не расход сети на передачу метрики (PDF 368–371).
11. **`hashmod` и шардирование:** для экстренной диагностики `modulus:10` с `keep regex:0` оставляет ~10 % целей; для production sharding `modulus:4`, `scraper:2`, `regex:2`. Этот способ авторы считают более сложным, чем вертикальное разделение, и предупреждают против прозрачного центрального proxy всех shard TSDB (PDF 370–373).
12. **Управление изменениями:** не считать прежние метки неизменяемыми навсегда; для долгого анализа отслеживать изменения имен и, где нужен стабильный интерфейс, обдумать контракт на основе recording rules (PDF 373).

## Source findings и риски

- **PDF 363:** утверждение об отсутствии «встроенной поддержки шифрования» в Prometheus соседствует с главой **20** (PDF 345–349), где встроенный TLS явно описан. Это внутренняя несогласованность scope/version, [Needs confirmation], не дополнять без проверки.
- **PDF 356:** «10 000 samples/sec, 2 байта/sample, чуть меньше 600 Гбайт в год» зависит от единиц GB/GiB; грубая цифра нуждается в единицах и расчёте.
- **PDF 365:** `regex: (.+)\d+` удаляет цифру из `region: dublin1` перед отправкой в Alertmanager, но уникальные labels должны **сохраниться** в federation и remote-write — это намеренно **разные** namespace/pipelines.
- **PDF 369:** аварийный совет остановить Prometheus и удалить/переименовать TSDB-каталог — **разрушительная мера**, без source-backed полного восстановления. Не исполнять.
- **PDF 372:** `read_recent: true` отключает оптимизацию remote read для local recent — риск нагрузки и единой точки отказа.
- **PDF 355/358/359/360:** оценки ~10k series для крупного federation target, ~5x ресурса cluster storage, память/диск/сеть — опыт/правила оценки авторов, не универсальная норма.
- Регистр с локаторами и ограничениями — [source-findings.md](source-findings.md). Рис. 21.1–21.2 доступны текстово, схемы синтезированы из RAG.
- PDF 373 содержит одно предложение-резюме главы, но **самостоятельный отдельный раздел summary отсутствует**. Списка review questions/exercises нет: условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

[cheatsheet.md](cheatsheet.md) — архитектурные/операционные решения; [commands.md](commands.md) — source YAML, PromQL, CLI и безопасная классификация; [diagram.md](diagram.md) — Mermaid; [visual-cheatsheet.svg](visual-cheatsheet.svg) — краткая карта; [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная карта; [source-findings.md](source-findings.md) — source limitations.

**Без изменений:** PDF, RAG, метаданные, workflow, `reading/progress.yaml`. Никаких команд запуска/удаления TSDB, обработки внешних метрик или рестартов не выполнялось.
