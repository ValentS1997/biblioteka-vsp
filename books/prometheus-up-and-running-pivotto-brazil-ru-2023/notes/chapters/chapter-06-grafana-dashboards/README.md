# Глава 6. Создание дашбордов с Grafana

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023; перевод второго англоязычного издания).  
**Inventory:** `0040`. **Book ID:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус артефактов:** `RAG_GROUNDED`, не `VERIFIED`/`ACCEPTED`.  
**Источник:** только `rag_only`: адресуемый RAG, без прямого доступа к PDF, внешних источников или модельного восполнения пробелов.

## Граница, provenance и готовность

- Заголовок «Глава 6. Создание дашбордов с Grafana» начинается на PDF **112**: `p0112:c01`.
- PDF **129**, `p0129:c01`, завершает главу словами о следующей главе, посвящённой Node Exporter. PDF **130**, `p0130:c01`, — заголовок части III; PDF **131**, `p0131:c01`, — «Глава 7. Node Exporter».
- **PDF и печатные страницы:** 112–129; `source_locator: pdf_page=112..129`.
- **Объём:** 18 страниц и 18 адресуемых чанков `p0112:c01`–`p0129:c01`, путь `rag/chunks/p0101-p0200/pNNNN-c01.md`.
- Исходный PDF SHA256: `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. Канонический книжный `rag/acceptance.yaml` — `ACCEPTED`; `rag/manifest.yaml` — `READY_WITH_KNOWN_LIMITATIONS`.
- Границы проверены по RAG-тексту, а не только по оглавлению.

## Карта главы

| Раздел | PDF | Результат |
| --- | --- | --- |
| Вводная часть и Promdash/консольные шаблоны | 112–113 | Назначение дашборда, выбор Grafana; историческая справка |
| Установка | 113–114 | `docker run`, Grafana **9.1.6**, адрес `:3000`, смена пароля |
| Источники данных | 115–116 | Добавление Prometheus URL `http://localhost:9090`, `Save & Test` |
| Дашборды, панели и «стена графиков» | 116–117 | Новый дашборд, панели, сохранение, когнитивная нагрузка |
| Time series и время | 117–121 | `process_resident_memory_bytes`, легенда `{{job}}`, IEC bytes, time range, aliasing |
| Stat | 121–123 | `prometheus_tsdb_head_series`, `node_uname_info` и метка `release` |
| Table | 123–124 | `rate(node_network_receive_bytes_total[1m])`, Instant/Table, скрытие полей, bytes/sec |
| State timeline | 125 | `up`, `{{job}} / {{instance}}`, отображение состояний |
| Переменные шаблона | 126–129 | `Device`, `label_values`, `$Device`, `$__rate_interval`, дублирование панелей, Share |

## Основной принцип

**Дашборд служит диагностической цели и аудитории, а не максимальному числу графиков.** Grafana визуализирует данные, собираемые Prometheus, через настроенный источник данных; панели используют PromQL, легенды, единицы измерения и управление временем. По тексту главы обзорный дашборд должен быть понятен с первого взгляда, а углублённый может иметь больше деталей (PDF 112–117).

## Краткий учебный сценарий

1. В локальном учебном примере запустить Grafana 9.1.6, открыть `http://localhost:3000/`, войти в интерфейс и заменить пароль по умолчанию (PDF 113–114). Это исторический **локальный** пример, не production-процедура.
2. Создать data source типа Prometheus с URL `http://localhost:9090`, выполнить `Save & Test` и проверить, что Prometheus доступен из Grafana (PDF 115–116).
3. Создать дашборд, Time series для памяти процесса; задать `{{job}}`, `data/bytes (IEC)`, `Memory Usage`; применить изменения и сохранить дашборд (PDF 116–119).
4. Добавить Stat для `prometheus_tsdb_head_series` и Stat с `node_uname_info` / `release`; затем Table с сетевым приёмом и State timeline с `up` (PDF 121–125).
5. Создать `Device` через Grafana `label_values(node_network_receive_bytes_total, device)`; связать Time series с переменной `$Device`, затем воспользоваться обновлением, дублированием и Share (PDF 126–129).

## Обнаруженные проблемы и ограничения

- **[Source wording/code mismatch]** PDF 125: интерфейсный mapping `up` описан как 1→UP и **2→DOWN**, тогда как семантика `up == 0` для DOWN дана в RAG главы 2 (`p0047:c01`–`p0048:c01`). В артефактах обе исходные версии сохранены, без скрытого исправления.
- **[Source code mismatch]** PDF 128: выражение исходящего трафика записано как `rate(node_network_transmit_bytes_total {device=~"$Device"})[$__rate_interval]`; размещение скобок нельзя воспроизводить как проверенную рабочую формулу. Подробности в [source-findings.md](source-findings.md).
- Схемы и скриншоты рис. 6.1–6.19 присутствуют в RAG как подписи, но не как отдельные графические объекты; две SVG-схемы здесь построены по тексту, **не реконструируют** издательские изображения.
- Пример `docker run` использует `--net=host` и **без тома** сохраняет состояние внутри контейнера; логин/пароль `admin/admin` — исторические демонстрационные значения, не рекомендуемая production-конфигурация (PDF 113).
- Условных отдельного заключительного summary, review-questions и review-answers в RAG главы нет. Соответствующие файлы не создаются.

## Артефакты

- [cheatsheet.md](cheatsheet.md) — эксплуатационная памятка по панелям, переменным и проверкам.
- [commands.md](commands.md) — только команды, PromQL и операции GUI, подтверждённые RAG.
- [diagram.md](diagram.md) — поток метрик и схема выбора панели.
- [visual-cheatsheet.svg](visual-cheatsheet.svg) — компактная визуальная карта.
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) — подробная визуальная карта.
- [source-findings.md](source-findings.md) — подтверждённые расхождения и ограничения RAG.

**Не изменялись:** `source/book.pdf`, `rag/`, `metadata.yaml`, `reading/progress.yaml`.
