# Cheatsheet — глава 18 «Оповещение»

**Источник:** PDF 307–320, RAG `p0307:c01`–`p0320:c01`. Строго `rag_only`, без проверки актуальности версий/конфигураций. Код не исполнялся.

## Symptom / problem framing

- **Не приходит уведомление:** различить: alert rule вернул пустой vector? он pending из-за `for`? firing, но нет Alertmanager? severity отфильтрована в `alert_relabel_configs`? Конкретные receiver/маршруты этой главой не покрыты (PDF 307–309, 310, 318–319).
- **Слишком много ложных срабатываний:** устойчивое `for: 5m` и фильтр `*_over_time`; требовать стабильности identity labelset. Одного evaluation обычно недостаточно (PDF 310–312).
- **Оповещение бесконечно pending:** входной series исчезает при неудачном scrape или меняются labels, сбрасывая `for`. Для `process_open_fds` показано окно `max_over_time(...[5m])` (PDF 311–313).
- **Тихо пропали все цели:** `up{job="node"} == 0` обнаруживает failed scrape существующего target, но отсутствие самого `up` — другой сценарий; chapter 16 `absent` (в главе 18 подробно не повторён) (PDF 308, 312).
- **Alertmanager получил много alerts:** отдельный ряд `InstanceDown` на каждый instance; группировка уведомлений делается в Alertmanager, а не преобразованием имён в Prometheus (PDF 307–309).
- **Пейджинг не туда:** `severity`/`team`/`service`, настройки `alert_relabel_configs`, `external_labels`, а затем маршруты Alertmanager — последний шаг раскрывается в следующей главе (PDF 312–313, 318–320).

## Baseline

| Концепт | Семантика источника | PDF |
| --- | --- | --- |
| `alert` + `expr` | Каждая серия instant-vector становится отдельным alert | 308–309 |
| Идентичность | Labels, включая `alertname`, кроме `__name__` | 309 |
| `for` | Pending до непрерывного сохранения одной серии; затем firing | 310–311 |
| `ALERTS` | `alertstate="pending"/"firing"`; resolved не создаёт активный sample | 309 |
| `ALERTS_FOR_STATE` | Хранение начала alert для восстановления после перезапуска | 309 |
| `severity` | Например, `ticket` или `page` | 312–314 |
| `annotations` | Информация/ссылки/динамический `$value` без изменения identity | 315–317 |
| `alert_relabel_configs` | После external_labels, до отправки Alertmanager | 319–320 |
| `external_labels` | Идентифицируют сервер, не видны в rule annotations и HTTP API | 319–320 |

## Read-only проверка

1. Просмотреть результат PromQL выражения: `avg without(instance)(up{job="node"}) < 0.5`; пустой vector значит нет активного alert; одна серия даёт одно оповещение (PDF 308).
2. Открыть `http://localhost:9090/alerts` и проверить pending/firing и labelset; следить за `ALERTS` и `ALERTS_FOR_STATE` (PDF 309–311).
3. Проверить, сохраняется ли состояние `for` при пропуске одной не-`up` метрики; по книге `max_over_time(process_open_fds[5m])` переживает одиночный scrape loss за счёт окна (PDF 311–312).
4. Сравнить `up{job="blackbox"} == 0` и `probe_success{job="blackbox"} == 0`: failure scrape и failure probe — разные причины (PDF 312).
5. Посмотреть labels, включая `job`/`instance`/другие target labels, `severity`, `team`; убедиться, что меняющиеся значения `$value` вынесены в `annotations`, а не в labels (PDF 308–309, 313–316).
6. Просмотреть `alerting.alertmanagers`, `alert_relabel_configs` (например, drop severity=info) и `global.external_labels`. Параметры маршрутизации receiver в Alertmanager в этой главе не приведены (PDF 318–320).
7. Динамические `query` и `range` в аннотациях могут быть дорогими: число экземпляров alerts влияет на число выполняемых запросов (PDF 315–316).
8. `hour()` работает в UTC: `and on() hour() >= 9 < 17` означает UTC, не часовой пояс оператора (PDF 309).

## Interpretation

- Наличие alert в состоянии pending **не означает**, что Alertmanager уже уведомлён; отправка начнётся после firing (PDF 310).
- `severity: page` и `severity: ticket` у двух одноимённых правил могут породить два alerts. Источник предостерегает от наивного взаимоисключения уровней у порога 95 % (PDF 313).
- `external_labels` применяются после rule evaluation: не используются в Prometheus `annotations`, но Alertmanager получает их. Одноимённая label исходного ряда имеет приоритет (PDF 319–320).
- Практика авторов: `for` чаще 5m/10m/30m/1h; пейджинг при реальном пользовательском симптоме, владельце и необходимом действии. Это качественная рекомендация, а не строгая гарантия/универсальный порог (PDF 311, 314, 317–318).

## Next action

- Сначала определить действие оператора и владельца; затем выбрать метрику, устойчивый порог, `for`, стабильные labels, краткие annotations и способ доставки (PDF 310–318).
- Для `ManyInstancesDown` проверять сохранение `job` и других target labels; авторы предпочитают `without(instance)`, а не `by(job)`, чтобы не потерять дополнительные группы (PDF 308).
- Для внешних labels выбирать стабильный общий контекст Prometheus; изменяющиеся между целями метки лучше target labels (PDF 319–320).

## Modifying actions / verification / rollback

- **State-changing:** создание/правка `rules.yml`, изменение `prometheus.yml`, restart/reload сервера, включение/отключение отправки alerts, изменение политики routing/drop. В этой главе нет процедуры безопасной активации/отката: **[Needs confirmation]**.
- **Workload-generating:** частые правила и annotation templates с `query` особенно для сотен alerts (PDF 316).
- **Verification:** оповещения переходят pending → firing; после восстановления series исчезают из firing; получаются ожидаемые stable labels, severity и annotations; Alertmanager получает alerts с внешними labels, если они применимы (PDF 307–320).
- **Rollback:** нет source-backed команд отмены, отмены отправленных уведомлений или восстановления исторических состояний. **[Needs confirmation]**. Никакие правила и конфигурации не применялись.
