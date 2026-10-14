# Cheatsheet — глава 4: экспортирование метрик

**Основание:** RAG `p0076:c01`–`p0096:c01`, PDF 76–96. Сведения о версиях и API — исторические утверждения книги.

## Symptom / problem framing

- Метрики зарегистрированы в приложении, но Prometheus их не видит: регистрация и экспорт — разные этапы; проверить endpoint и scrape (PDF 76–78).
- В Gunicorn часть метрик «пропадает» или счётчики будто уменьшаются: scrape может попадать к разным worker с неполными локальными значениями. Нужен multiprocess-режим (PDF 79–82).
- Короткое batch-задание завершается до scrape: рассмотреть Pushgateway **для batch уровня службы**, а не произвольной цели (PDF 86–89).
- Эндпоинт доступен, но данные не принимаются: вручную сформированный exposition может содержать ошибку форматирования; использовать `promtool check metrics` (PDF 91–94).

## Baseline / context

- Обычный экспорт — HTTP endpoint, по соглашению `/metrics`; путь можно изменить. Экспорт настраивают на верхнем уровне приложения, чаще всего один раз (PDF 76–78).
- Python: `start_http_server(8000)` или WSGI `make_wsgi_app()`; Twisted тоже может использовать WSGIResource (PDF 77–79).
- Go: `promhttp.Handler()` и регистрация `promauto.NewCounter` / `MustRegister` (PDF 82–83).
- Java: `HTTPServer(8000)` или `MetricsServlet`; `DefaultExports.initialize()` экспортирует process/JVM (PDF 83–86).
- Pushgateway `:9091`: последние batch-метрики; Prometheus продолжает периодически опрашивать этот кеш (PDF 86–89).
- Форматы: Prometheus `text/plain; version=0.0.4`; OpenMetrics `application/openmetrics-text; version=1.0.0` (PDF 91, 94).

## Read-only checks

1. Посмотреть ответ `/metrics` и заголовок Content-Type; проверить, что Prometheus способен выполнить scrape (PDF 76, 91, 94).
2. `curl http://localhost:8000/metrics | promtool check metrics` — анализ формата, без редактирования системы (PDF 94).
3. Проверить `# HELP`/`# TYPE` и группировку временных рядов одной метрики, `_sum`, `_count`, `_bucket{le="..."}`, `+Inf` у Histogram (PDF 91–92).
4. В OpenMetrics проверить завершающий `# EOF`, возможный `# UNIT`, `Info`/`StateSet`/`GaugeHistogram`; trailing comma у labels там не допускается (PDF 94–96).
5. Для Pushgateway посмотреть `push_time_seconds`, `push_failure_time_seconds` и неизменность групп (PDF 89).
6. Для Gunicorn убедиться, что scraper видит объединённые значения в `MultiProcessCollector`, а не случайный worker; отсутствие `python_info` и `process_` в примере ожидается (PDF 79–81).

## Interpretation

- HTTP доступность недостаточна для корректного exposition. Ошибки включают финальный newline, CRLF и недопустимые имена (PDF 94).
- Сегменты Histogram кумулятивны, последний `le="+Inf"` обязателен, а `_count` должен совпадать с `+Inf` (PDF 92).
- В Prometheus-text timestamps указаны в **миллисекундах**; в поясняющей сноске OpenMetrics — **секунды**. В тексте на PDF 96 есть противоречие, см. [source-findings.md](source-findings.md).
- `push_to_gateway`: HTTP PUT заменяет метрики группы; `pushadd_to_gateway`: POST заменяет совпадающие имена, сохраняя остальные; `delete_from_gateway`: DELETE удаляет метрики группы (PDF 88).
- Pushgateway хранит последнюю отправку, поэтому это не полная история каждого запуска batch (PDF 87–89).

## Next action

- Для обычного сервера выбрать экспорт прямо из процесса; если есть HTTP-фреймворк, подключить WSGI/Servlet/Handler вместо отдельного сервера (PDF 77–86).
- Для multiprocess Python использовать сборщик, предназначенный для агрегирования всех worker, и обработчик `child_exit` (PDF 79–82).
- Для краткоживущего batch уровня службы использовать Pushgateway по подтверждённой архитектуре; для привязанного к жизненному циклу машины backup в главе рекомендован textfile collector Node Exporter (PDF 86–87).
- При ручном форматировании проверить payload с помощью `promtool` до эксплуатации (PDF 91–94).

## Modifying action

- Подключение WSGI/Twisted/Go/Java endpoint меняет код и может открыть HTTP-порт; применить ограничения сетевого доступа в своей среде: [Needs confirmation] (PDF 77–86).
- Multiprocess Gunicorn требует переменной `prometheus_multiproc_dir`, каталога и запуска `gunicorn -w 2 -c config.py app:app`; **опасный `rm -rf $prometheus_multiproc_dir` в источнике не является безопасной командой для прямого копирования** (PDF 79–82).
- Pushgateway `push_to_gateway`, `pushadd_to_gateway`, `delete_from_gateway` меняют сохранённую группу; необходимо учитывать, что метрики сохраняются после окончания процесса (PDF 88–89).
- `GraphiteBridge(...).start(10)` передаёт данные в отдельную систему и изменяет внешний поток телеметрии (PDF 90).

## Verification / acceptance checks

- Для Python WSGI запрос `/metrics` достигает `metrics_app`, остальные пути возвращаются основной службой (PDF 78).
- В Go и Java endpoint доступен и метрики появляются в реестре; тестирование конкретного окружения: [Needs confirmation].
- Gunicorn выдаёт агрегированные `http_requests_total` и `http_requests_inprogress` (PDF 80–81).
- Pushgateway доступен на `:9091`, `honor_labels: true`, данные последней отправки и времена отправки видны в группе (PDF 87–89).
- `promtool check metrics` не сообщает ошибок формата на проверяемом потоке (PDF 94).

## Rollback

- Для code/exporter/framework: вернуть предыдущую версию кода/конфигурации, проверить endpoint и scrape. **Конкретный порядок rollback в главе не приведён: [Needs confirmation].**
- Для Pushgateway: `delete_from_gateway` удаляет группу; удаление — **не восстановление старого значения**. Восстановление предыдущего состояния: [Needs confirmation] (PDF 88–89).
- Для Gunicorn **до любой очистки каталога** проверить, что указан верный path и что процесс остановлен; резервная копия и процедура восстановления: [Needs confirmation]. Нельзя выполнять опасное удаление на работающем экземпляре (PDF 81–82).
