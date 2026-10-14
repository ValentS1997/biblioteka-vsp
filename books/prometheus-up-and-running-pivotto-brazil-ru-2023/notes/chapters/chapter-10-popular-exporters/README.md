# Глава 10. Популярные экспортеры

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023, русское издание).  
**Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Состояние:** `RAG_GROUNDED` до целевой валидации и ревью.  
**Source policy:** `rag_only`; без прямого чтения исходного PDF, внешних источников и заполнения пробелов памятью модели.

## Границы и provenance

- Глава 10 «Популярные экспортеры» начинается на PDF **187**, чанк `p0187:c01`, и заканчивается на PDF **208**, чанк `p0208:c01`; PDF **209**, `p0209:c01`, начинает главу 11 «Работа с другими системами мониторинга».
- **PDF и печатные страницы:** 187–208, `source_locator: pdf_page=187..208`.
- **22 последовательных адресуемых чанка**: `p0187:c01`–`p0200:c01` в `rag/chunks/p0101-p0200/` и `p0201:c01`–`p0208:c01` в `rag/chunks/p0201-p0300/`.
- **Source SHA256:** `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; книжный `rag/acceptance.yaml` имеет статус `ACCEPTED`, `rag/manifest.yaml` — `READY_WITH_KNOWN_LIMITATIONS`.
- Границы подтверждены заголовками самих чанков, не одним оглавлением.

## Карта главы

| Раздел | PDF | Содержание |
| --- | --- | --- |
| Архитектура экспортеров | 187 | Один экспортер на экземпляр приложения, близость к цели, метки |
| Consul Exporter | 187–189 | Consul на 8500; exporter `:9107`; `consul_up`, здоровье служб и агентов; `up` |
| MySQLd Exporter | 189–190 | Учётная запись для мониторинга, `~/.my.cnf`, `:9104`, `mysql_up`, переменные/status |
| Grok Exporter | 190–193 | Журнал → регулярные выражения → Counter/Histogram; `grok.yml`, `:9144`, `readall` |
| Blackbox: обзор | 193–194 | Отдельное зондирование целей ICMP/TCP/HTTP/DNS через `/probe`, `:9115` |
| ICMP | 194–199 | `probe_success`, IP, DNS, привилегии, debug; пример `icmp_ipv4` |
| TCP | 199–200 | `tcp_connect`, `ssh_banner`, TLS, срок действия сертификата |
| HTTP | 201–203 | `http_2xx`, статус и длительность фаз, проверка HTTPS/содержимого |
| DNS | 203–205 | `dns_tcp`, `query_name`, MX; мониторинг DNS-серверов |
| Multitarget / relabel | 205–207 | `__param_target`, `instance`, `__address__`, мониторинг нескольких сайтов и SSH через Consul |
| Тайм-ауты | 208 | `X-Prometheus-Scrape-Timeout-Seconds`, `scrape_timeout`, `--timeout-offset` |

## Главный принцип и выводы

**Экспортер — адаптер чужих данных к модели pull Prometheus.** Прямое инструментирование приложения предпочтительно, а при невозможности оно заменяется exporter, обычно привязанным к тому же экземпляру приложения. **Blackbox и SNMP — исключение:** exporter располагается отдельно, а проверяемую цель получает как параметр запроса (PDF 187, 193–194).

1. **Не смешивать доступность exporter и доступность приложения.** `up` сообщает об успешном scrape exporter. `consul_up`, `mysql_up` и `probe_success` показывают результат сбора/проверки настоящей цели и нужны для контроля её работоспособности (PDF 188, 190, 196, 206).
2. **Consul Exporter** показывает взгляд отдельного агента на кластер; `consul_serf_lan_members` может отличаться между участниками, поэтому авторы предлагают опрашивать разных агентов и агрегировать PromQL (PDF 188).
3. **MySQLd Exporter** работает от отдельной учётной записи. В примере есть `GRANT PROCESS, REPLICATION CLIENT, SELECT`, файл `~/.my.cnf` и `mysql_global_variables_*` / `mysql_global_status_*`. Демонстрационные пароли из печатного листинга намеренно **не воспроизводятся** (PDF 189–190).
4. **Grok Exporter** извлекает метрики из текста журнала, но требует описать каждый тип метрики и шаблон. `readall: true` — только учебный режим; для промышленного окружения в книге рекомендовано `false` (PDF 191–193).
5. **Blackbox** имеет разные модули проверки: ICMP — доступность сети, TCP — сокет/баннер, HTTP — ответ/фазы/TLS, DNS — собственно сервер DNS. Метрики диагностики включают `probe_duration_seconds`, `probe_http_status_code`, `probe_http_duration_seconds`, `probe_ip_protocol` и `probe_success` (PDF 195–205).
6. **Маршрутизация multitarget:** исходный URL цели проходит через `__param_target` и `instance`, а `__address__` переписывается на `127.0.0.1:9115`, чтобы Prometheus обратился к Blackbox Exporter, а не непосредственно к проверяемому сайту (PDF 205–207).
7. **Не превращать Blackbox в открытый прокси.** Авторский текст указывает, что конфигурация модулей не может произвольно переопределяться URL-параметрами; передавать допустимые цели только через согласованный механизм обнаружения (PDF 203).

## Исходные ограничения и source findings

- **PDF 188:** URL Consul Exporter содержит каталог `v0.3.0`, а имя архива и сообщение о сборке — `0.8.0` ([source-findings.md](source-findings.md)).
- **PDF 191–193:** три значения задержки входного журнала (`1.23`, `3.2`, `4.6`) не согласованы с приведёнными bucket и `_sum 0.57`. В выводе `log_http_request_latency_seconds_total` имеет `TYPE histogram`, несмотря на Counter-подобный суффикс `_total`; не корректировать источник молча.
- **PDF 196–197:** текст связывает `probe_ip_protocol=6` с разными IP-версиями (IPv4 на 196, IPv6 на 197).
- **PDF 198–199:** текст говорит о `selected_ip_protocol: ipv4`, но фрагмент YAML содержит `preferred_ip_protocol: ip4`.
- **PDF 202–203:** описание проверки содержит «Prometheus» в теле, пример regex ищет `oreillymedia`.
- **PDF 205–206:** два варианта списка сайтов в примере 10.10 (код и разбор) различаются.
- Отдельные рисунки Blackbox 10.1–10.2 из RAG представлены только подписями, не изображениями. Современная совместимость экспортёров и действительность учебных адресов не проверялись.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — эксплуатационный чек-лист.
- [commands.md](commands.md) — команды и конфигурации, подтверждённые текстом, с классификацией риска.
- [diagram.md](diagram.md) — Mermaid: архитектура и relabel.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная схема.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная схема.
- [source-findings.md](source-findings.md) — регистр расхождений.

**Условные артефакты:** явного отдельного заключительного summary, review questions или упражнений на PDF 187–208 нет; `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

**Не изменять:** исходный PDF, канонический RAG, metadata/reading progress, CI workflows.
