# Глава 11. Работа с другими системами мониторинга

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023).  
**Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Шаблон:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED` — до адресной валидации и review.  
**Source policy:** `rag_only`, без прямого чтения PDF, внешнего веб-поиска и замены источника памятью модели.

## Граница главы и provenance

- PDF **209**, `p0209:c01`: «Глава 11. Работа с другими системами мониторинга».
- PDF **214**, `p0214:c01`: окончание главы с рекомендацией и анонсом следующей. PDF **215**, `p0215:c01`: заголовок главы 12 «Разработка экспортеров».
- **PDF/печатные страницы:** 209–214. `source_locator: pdf_page=209..214`.
- **6 последовательных адресуемых чанков:** `p0209:c01`–`p0214:c01` в `rag/chunks/p0201-p0300/pNNNN-c01.md`.
- **Source SHA256:** `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. Канонический `rag/acceptance.yaml` — `ACCEPTED`; `rag/manifest.yaml` — `READY_WITH_KNOWN_LIMITATIONS`.
- Источник главы проверен по заголовкам чанков, не только по оглавлению.

## Тематическая карта

| Раздел | PDF | Результат |
| --- | --- | --- |
| Вступление и другие системы | 209–211 | Плавная миграция; InfluxDB, collectd, Graphite, StatsD, JMX, SNMP, SaaS, NRPE, Dropwizard |
| InfluxDB Exporter | 211–212 | Line protocol через HTTP `:9122/write`, pull `:9122/metrics`, преобразование labels, время scrape |
| StatsD Exporter | 212–214 | События на TCP/UDP `:9125`, exporter HTTP `:9102`, Gauge/Counter/timer, mappings `*.*` в метки |
| Рекомендации по эксплуатации | 214 | Один push-to-pull exporter на экземпляр приложения с общим жизненным циклом |

## Главные выводы

1. **Поэтапная миграция реалистичнее одномоментного перехода.** Экспортеры превращают данные старых систем в метрики Prometheus, но автоматичность преобразования зависит от семантики исходной модели (PDF 209–211).
2. **InfluxDB Exporter:** приложение отправляет line protocol `example_metric,foo=bar value=43 1517339868000000000` в `/write`, exporter показывает `example_metric{foo="bar"} 43` в `/metrics`. Переданная метка времени не выводится: при отсутствии timestamp Prometheus использует **время scrape**, и историю push-событий такое представление не восстанавливает (PDF 211–212).
3. **StatsD Exporter:** события `example_gauge:123|g`, `example_counter_total:1|c`, `example_latency_total:20|ms` преобразуются во внутренние метрики экспортера; для получения меток из имён с точками используется `mapping.yml`, `match: app.http.requests.*.*` и `labels` с `${1}`/`${2}` (PDF 212–214).
4. **Не все прежние модели равноценны Prometheus.** collectd без собственных меток, Graphite/StatsD с точечными именами, JMX с разнородными mBean, SNMP с MIB требуют различной степени сопоставления имён/типов/меток (PDF 209–211). В сноске к Graphite отмечена поддержка тегов в версии 1.1.0 — не считать фразу о «нет key-value labels» универсальной для всех версий (PDF 210).
5. **SNMP Exporter — удалённый тип экспортера**, близкий к Blackbox: размещать сетево близко к устройствам из-за многословности SNMP и увеличивать интервал scrape/уменьшать набор метрик при медленных устройствах (PDF 210).
6. **Внешние SaaS экспортеры** (CloudWatch, New Relic, Pingdom, Stackdriver) могут иметь ограничения API и финансовую стоимость (PDF 210); конкретные тарифы, квоты и текущие названия продуктов не известны в `rag_only`.
7. **Управлять жизненным циклом:** для InfluxDB/Graphite/StatsD/Collectd push-to-pull авторы рекомендуют один exporter на экземпляр приложения, запускать, останавливать и перезапускать одновременно с ним, предотвращая stale state, смену labels и централизованное узкое место (PDF 214).
8. **NRPE и Dropwizard** — переходные случаи: старые Nagios-проверки могут временно жить через NRPE, а при контроле Java-кода авторы предпочитают прямую интеграцию Dropwizard через Java client вместо JMX (PDF 211).

## Исходные особенности и ограничения

- **PDF 213–214:** промежуточный текст описывает `region="euwest-1"`, тогда как исходное имя события и фактический exposition — `eu-west-1`. Это текстовое несоответствие зарегистрировано в [source-findings.md](source-findings.md), исправлять канонический текст нельзя.
- **PDF 213:** `example_latency_total:20|ms` подан как StatsD timing observation с именем, похожим на Counter (`_total`). Автор не утверждает, что итоговое имя после преобразования служит Counter; не выдавать пример за стабильное готовое соглашение именования для Histogram/Summary.
- В главе есть исторические версии InfluxDB Exporter 0.10.0 и StatsD Exporter 0.22.8. Текущие бинарники, параметры флагов, поддержка SaaS-API и политики безопасности не верифицированы.
- Для InfluxDB push необходимо оценить семантику timestamp, для StatsD — протокол TCP/UDP и преобразование единиц. **Нельзя обещать восстановление исторических временных меток** (PDF 212–213).
- Выделенного конца с проверочными вопросами/упражнениями или отдельного итогового summary в диапазоне не обнаружено. Условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — диагноз, baseline, read-only и modifying checks, verification и rollback.
- [commands.md](commands.md) — только source-backed команды, события и конфигурации, классификация риска.
- [diagram.md](diagram.md) — Mermaid, переход push-to-pull и жизненный цикл.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная карта.
- [source-findings.md](source-findings.md) — регистр source wording/семантики и допущений.

**Не изменяются:** канонический PDF, RAG, metadata, файлы статуса чтения и CI templates.
