# Глава 4. Экспортирование метрик

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023; перевод 2-го англоязычного издания).  
**Inventory:** `0040`. **Book ID:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED`; отдельная проверка и review обязательны.  
**Источник:** строго `rag_only`; без прямого доступа к PDF, внешнего поиска и модельного дополнения.

## Граница главы и provenance

- Заголовок главы 4 «Экспортирование метрик» находится в PDF-чанке `p0076:c01`; последний текст главы — `p0096:c01`. В `p0097:c01` начинается глава 5 «Метки».
- **PDF и печатные страницы:** 76–96; `source_locator: pdf_page=76..96`.
- **Объём:** 21 последовательный адресуемый чанк `p0076:c01`–`p0096:c01`, расположены в `rag/chunks/p0001-p0100/pNNNN-c01.md` относительно корня книги.
- Исходный SHA256: `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; полно-книжный `rag/acceptance.yaml`: `ACCEPTED`; `rag/manifest.yaml`: `READY_WITH_KNOWN_LIMITATIONS`.
- Граница подтверждена заголовками RAG, а не только оглавлением (`p0006:c01`, `p0006:c02`).

## Карта главы

| Раздел | PDF | Содержание |
| --- | --- | --- |
| Основы экспортирования | 76–77 | HTTP `/metrics`, реестр, форматы Prometheus и OpenMetrics, разделение инструментирования и экспорта |
| Python | 77–82 | `start_http_server`, WSGI `make_wsgi_app`, Twisted и многопроцессный Gunicorn |
| Go | 82–83 | `promhttp.Handler()`, `promauto.NewCounter`, регистрация `MustRegister` |
| Java | 83–86 | `HTTPServer`, `MetricsServlet`, `DefaultExports.initialize()`, Maven-примеры |
| Pushgateway | 86–89 | Временные batch jobs, кэш последнего состояния, `honor_labels`, PUT/POST/DELETE, группировка и очистка |
| Мосты и парсеры | 90–91 | `GraphiteBridge`, `CollectorRegistry.collect`, `text_string_to_metric_families` |
| Текстовый формат Prometheus | 91–94 | `HELP`, `TYPE`, метки, `le`, escaping, timestamps, `promtool check metrics` |
| OpenMetrics 1.0.0 | 94–96 | `# EOF`, `UNIT`, `Info`, `StateSet`, `GaugeHistogram`, различия меток и отметок времени |

## Главный принцип

**Инструментирование и экспорт — разные задачи.** Приложение может регистрировать метрики и показывать их через HTTP. Prometheus выполняет pull endpoint, а форматы текста определяют, как интерпретировать семейства метрик (PDF 76–78, 91–96). Для краткоживущих **batch jobs уровня службы** Pushgateway временно сохраняет последнюю отправленную группу, но не превращает Prometheus в push-систему (PDF 86–89).

## Эксплуатационные границы

- В Gunicorn агрегировать метрики рабочих процессов через `MultiProcessCollector`; обрабатывать `child_exit`; `prometheus_multiproc_dir` должен быть пустым **до** запуска нового приложения. Пример содержит разрушительную команду `rm -rf`: **не выполнять её без проверки пути, окна обслуживания и rollback** (PDF 79–82).
- Pushgateway предназначен не для любой метрики и не для произвольной смены pull на push. Группы сохраняются до удаления; не использовать изменяющиеся ключи группировки и очищать группы у снятых с эксплуатации заданий (PDF 86–89).
- Для проверок экспортируемого текста приведено `curl http://localhost:8000/metrics | promtool check metrics` (PDF 94). Наличие HTTP-ответа **не доказывает корректность** формата.
- Примеры Java `simpleclient 0.16.0`, `jetty-servlet 11.0.11` и Gunicorn из книги исторические; современная совместимость не установлена без внешних источников.
- В RAG обнаружены проблемы в Python-примере и формулировке времени OpenMetrics: [source-findings.md](source-findings.md). Изображения рис. 4.1–4.2 не представлены отдельными объектами.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — диагностический конспект и управление рисками.
- [commands.md](commands.md) — только исходные команды, API, файлы конфигурации и форматы с классами операций.
- [diagram.md](diagram.md) — архитектура pull/Pushgateway и диагностический путь.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — расширенная визуальная карта.
- [source-findings.md](source-findings.md) — регистр расхождений и ограничений.

**Условные артефакты:** отдельного итогового «Резюме», контрольных вопросов или упражнений в `p0076:c01`–`p0096:c01` не обнаружено. `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

**Без изменений:** исходный PDF, RAG/идентификаторы генераций, registry/reading state. 
