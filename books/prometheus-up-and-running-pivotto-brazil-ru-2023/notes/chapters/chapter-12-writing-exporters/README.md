# Глава 12. Разработка экспортеров

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023, перевод второго издания).  
**Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус артефактов:** `RAG_GROUNDED` (не `VERIFIED`/`ACCEPTED`).  
**Источник:** строго `rag_only`: только канонические текстовые чанки; без чтения PDF напрямую, веб-поиска и модельного восполнения пробелов.

## Границы и provenance

- PDF **215**, `p0215:c01`: заголовок «Глава 12. Разработка экспортеров».
- PDF **225**, `p0225:c01`: конец рекомендаций и переход к PromQL. PDF **226**, `p0226:c01`: начало части IV «PromQL»; PDF **227**, `p0227:c01`: глава 13.
- **PDF и печатные страницы:** 215–225; `source_locator: pdf_page=215..225`. **11 чанков:** `p0215:c01`–`p0225:c01` из `rag/chunks/p0201-p0300/pNNNN-c01.md`.
- Source PDF SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; книжное `rag/acceptance.yaml: ACCEPTED`, `rag/manifest.yaml: READY_WITH_KNOWN_LIMITATIONS`. Границы подтверждены по RAG, не только по оглавлению.

## Карта главы

| Раздел | PDF | Содержание |
| --- | --- | --- |
| Постановка задачи и Consul Telemetry | 215–216 | JSON `/v1/agent/metrics`: `Gauges`, `Counters`, `Samples`, единицы и семантика |
| Пример 12.2: Go exporter | 217–218 | `ConsulCollector`, `Describe`, `Collect`, `NewDesc`, `MustNewConstMetric`, `promhttp.Handler` |
| Пользовательские сборщики | 219–222 | `prometheus.Collector`, статические и динамические `Desc`, ошибки Consul, `consul_up`, `UntypedValue`, регистр |
| Пример 12.3: Python exporter | 222–223 | `GaugeMetricFamily`, `CounterMetricFamily`, `SummaryMetricFamily`, `REGISTRY`, `start_http_server` |
| Метки | 223–224 | Go `NewDesc` с именами и значениями labels; Python создание семейства с `add_metric`; согласованность HELP |
| Методические рекомендации | 224–225 | Правила имён, типов, единиц, кардинальности, агрегация в PromQL, scrape без кеша, синхронность и инструментирование exporter |

## Главный принцип

**Экспортер — адаптер семантики исходной системы к метрикам Prometheus, выполняющий сбор синхронно с каждым scrape.** При наличии прямой инструментации или готового экспортера авторы предпочитают их созданию нового. Главная сложность — определить реальное значение метрик и единицы измерения (PDF 215, 219, 224).

1. **Источниковые Gauges/Counters/Samples нужно осмыслить.** В примере Consul API возвращает Gauges `Value`, Counters `Count/Sum` и Samples `Count/Sum`; Samples объявлены таймерами в **миллисекундах**, поэтому для секунд применяется `s.Sum/1000`. Названия сторонних типов могут не совпадать с семантикой Counter Prometheus (PDF 215–218).
2. **Go Collector обязан реализовать `Describe` и `Collect`.** `Describe` перечисляет известные заранее семейства, используется при регистрации. В примере `consul_up` известна заранее; остальные `Desc` создаются внутри `Collect`. В тексте говорится, что клиент Go требует хотя бы одно описание (PDF 217, 219–221).
3. **Отражать здоровье интеграции:** `consul_up=0` при ошибке создания API-клиента или получения данных и `1` при успехе; это не метрика доступности HTTP самого экспортера (PDF 217, 220).
4. **Имена и типы:** regex `[^a-zA-Z0-9:_]` заменяет недопустимые символы на `_`; Counters получают `_total`, Samples — пару `_seconds_count`/`_seconds_sum` у Go, Python использует `SummaryMetricFamily` (PDF 217–223).
5. **Метки — часть схемы:** Go задаёт имена labels в `NewDesc`, их значения в `MustNewConstMetric`; Python создаёт одно семейство и добавляет child посредством `add_metric`. HELP-строки одноимённых метрик должны совпадать, иначе scrape проваливается (PDF 223–224).
6. **Метрики приложения и экспортера различны.** Default registry добавляет `go_`/`process_` и позволяет отслеживать `process_open_fds`; возможны собственные `myexporter_scrape_duration_seconds`, `cloudwatch_requests_total` (PDF 222, 225).
7. **Не переносить избыточную логику в exporter.** Не экспортировать готовые `rate` и проценты там, где доступны Counter/числитель/знаменатель; избегать сырых min/max/stddev, сумм дублирующих labels, общих `env="prod"`. Объект мониторинга и exporter должны иметь общий жизненный цикл (PDF 224–225).

## Дефекты источника и ограничения

- **[Source contradiction]** PDF 216 и 218: исходный `Samples[0].Sum=0.13156799972057343`, Go-код делит сумму на `1000`, но пример `/metrics` на PDF 218 выводит `..._seconds_sum=1.3156799972057343e-01` без фактического уменьшения в 1000 раз. Подробно в [source-findings.md](source-findings.md).
- **[Source code mismatch]** PDF 223: `SummaryMetricFamily(..., count_value=c["Count"], sum_value=s["Sum"]/1000)` внутри `for s in metrics["Samples"]`: `c` осталась из предыдущего цикла по Counters и может обозначать не то наблюдение (или быть не определена).
- **[Source code mismatch]** PDF 221: вторичный фрагмент в разделе Counters использует `float64(s.Count)`, а полный Go-листинг PDF 218 — `float64(c.Count)`.
- **[Needs confirmation]** Сторонние Counters из Consul содержат `Count` и `Sum`; в примере выбирается `c.Count`, но без полной семантики источника нельзя установить, что именно отражает каждое поле (PDF 216–218).
- Go-клиент в книге используется с `go get -d -u`; текущая совместимость опций и API не проверена. Изображений главы, доступных как самостоятельные мультимодальные объекты, в RAG не обнаружено.
- В главе **нет явного отдельного end-of-chapter summary и контрольных вопросов/упражнений**: `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Комплект

- [cheatsheet.md](cheatsheet.md) — обзор и эксплуатационные проверки.
- [commands.md](commands.md) — Go/Python/API и команды, подтверждённые RAG, с рисками.
- [diagram.md](diagram.md) — Mermaid-карты Collector/scrape и выбора типов.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная карта.
- [source-findings.md](source-findings.md) — регистр противоречий.

**Без изменений:** канонический PDF, RAG, metadata, CI-workflows, `reading/progress.yaml`.
