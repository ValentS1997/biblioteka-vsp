# Глава 18. Оповещение

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил; Books.kz, 2023). **Inventory:** `0040`; **book_id:** `prometheus-up-and-running-pivotto-brazil-ru-2023`.  
**Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Статус:** `RAG_GROUNDED`, не `VERIFIED`/ `ACCEPTED`.  
**Source policy:** `rag_only` — только канонические RAG-чанки; PDF напрямую, web и модельная память не использовались для восполнения пропусков.

## Границы / provenance

- PDF **307**, `p0307:c01`: «Глава 18. Оповещение». PDF **320**, `p0320:c01`: окончание главы, переход к Alertmanager. PDF **321**, `p0321:c01`: глава 19 «Alertmanager».
- **PDF/печатные страницы: 307–320**, `source_locator: pdf_page=307..320`. **14 page-addressable chunks** `p0307:c01`–`p0320:c01` в `rag/chunks/p0301-p0400/`.
- Source SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; `rag/acceptance.yaml: ACCEPTED`, `rag/manifest.yaml: READY_WITH_KNOWN_LIMITATIONS`.

## Карта главы

| Раздел | PDF | Факты источника |
| --- | --- | --- |
| Архитектура | 307–308 | Prometheus вычисляет условия и формирует alerts; Alertmanager группирует и рассылает notifications |
| Правила оповещения | 308–310 | `groups/rules/alert/expr`, instant-vector semantics, идентичность по labels, `ALERTS`, `ALERTS_FOR_STATE`, ограничение UTC |
| `for` и устойчивость | 310–312 | Pending → firing, устойчивое условие, срыв `for` при исчезновении ряда, `*_over_time`, `up` и `probe_success` |
| Метки оповещений | 312–314 | `severity: ticket/page`, `team/service`, стабильность идентичности, два порога одного имени |
| Аннотации и шаблоны | 315–317 | `annotations` vs labels; `$value`, `$labels`, `printf`, `query`, `range`; ссылки на dashboards/runbooks |
| Качество оповещений | 317–318 | Симптомы, затрагивающие пользователя; владелец и действие; шум и автоматизация |
| Передача Alertmanager | 318–319 | `alerting.alertmanagers`, service discovery, `alert_relabel_configs`, фильтр `severity=info` |
| Внешние метки | 319–320 | `global.external_labels` и область видимости, применение после вычисления правил, отсутствие в annotation templates |

## Ключевые принципы

1. **Не путать alerts и notifications.** Prometheus вычисляет правила, создаёт alert для каждого sample результата `expr` и направляет firing alerts в Alertmanager; Alertmanager маршрутизирует, группирует и отправляет уведомления (PDF 307–309). Пустой instant vector не вызывает alert. `InstanceDown: up{job="node"} == 0` создаёт отдельный alert на каждый отключённый экземпляр (PDF 308–309).
2. **Идентичность определяется labels**, включая `alertname`, но не `__name__`. `ALERTS{alertstate="pending"|"firing"}` показывает состояние; `ALERTS_FOR_STATE` хранит время начала для восстановления после рестарта. На PDF 309 встречается несогласованное написание `ALERT_FOR_STATE`: см. [source-findings.md](source-findings.md).
3. **`for` против ложных срабатываний:** condition обязано быть истинным и сохранять тот же labelset заданное время. Pending не передаётся Alertmanager; для source-примера `for: 5m`. Пропуск ряда может сбросить ожидание; `max_over_time` защищает от пропущенного scrape лишь для некоторых метрик. `up` отличается: при неудачном scrape оно обычно присутствует со значением 0 (PDF 310–312).
4. **Метки стабильны, аннотации изменяемы.** `severity`/`team` могут участвовать в маршрутизации Alertmanager; измеренное текущее значение нельзя помещать в меняющуюся label, поскольку это создаёт новые идентичности и сбрасывает `for`. Использовать `annotations` с `$value`, `$labels`, `query` и `range` (PDF 312–316).
5. **Стратегия оповещений ориентирована на действия.** Авторы предпочитают симптомы качества сервиса (задержка, ошибки), исчерпание ресурсов и проверку мониторинга; сообщения должны иметь ответственного, а лишние/не требующие человека — стать кандидатами для автоматизации (PDF 314, 317–318). Советы «не более двух инцидентов за день», «for от 5m» — практика/рекомендация авторов, не универсальный SLA.
6. **Трафик к Alertmanager:** `alerting.alertmanagers.static_configs.targets: ['localhost:9093']`; несколько Alertmanager получают каждый alert. `alert_relabel_configs` может отбрасывать `severity: info` (PDF 318–319).
7. **`external_labels` идентифицируют сервер** при взаимодействиях с Alertmanager, федерацией и remote read/write, но не отображаются в HTTP API. Они добавляются **после** расчёта правила (и до `alert_relabel_configs`), поэтому не доступны шаблонам аннотаций Prometheus; Alertmanager может использовать их в notification templates. Одноимённые метки самого ряда имеют приоритет (PDF 319–320).

## Source findings, ограничения и риски

- PDF 309: `ALERTS_FOR_STATE` в перечислении, но `ALERT_FOR_STATE` в следующем абзаце — лексическое расхождение, не «две разные» подтверждённые метрики.
- PDF 312–313: для одного имени `FDsNearLimit` приведены две severity/пороговые ветки (`0.95` page, `0.8` ticket). Авторы предупреждают, что оба alert могут активироваться; делать их взаимоисключающими без анализа `for` опасно.
- PDF 315–316: `query` внутри annotation template способен вызвать дорогие дополнительные PromQL-запросы, особенно при сотнях alerts.
- PDF 318–319: маркер сноски `❶` помещён прямо на строке `- static_configs:` в извлечении; копировать строку в YAML **без удаления издательского маркера нельзя**. Маркер не является параметром Prometheus.
- Скриншоты рисунков 18.1 и 18.2 в RAG представлены текстом/подписями, не самостоятельными изображениями; SVG здесь вновь синтезированные карты.
- Параметры Alertmanager, включая реальные маршруты, receivers, HA и подавление уведомлений, подробно рассматриваются **в главе 19**, а не в доступном источнике главы 18: [Needs confirmation].
- Явных отдельных review questions/exercises/end-of-chapter summary не обнаружено. Условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

[cheatsheet.md](cheatsheet.md) · [commands.md](commands.md) · [diagram.md](diagram.md) · [visual-cheatsheet.svg](visual-cheatsheet.svg) · [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) · [source-findings.md](source-findings.md).

**Не менялись:** канонический PDF, RAG, метаданные, CI templates/workflows, статус чтения.
