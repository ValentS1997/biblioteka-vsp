# Cheatsheet — глава 15: Двухместные операторы

**Источник:** PDF 258–272, `p0258:c01`–`p0272:c01`, строго `rag_only`. Примеры не исполнялись, исторические метрики могут отсутствовать в текущей TSDB.

## Symptom / problem framing

- **Нужны проценты/отношения двух метрик:** делить два мгновенных вектора с одинаковыми метками, например `process_open_fds / process_max_fds` (PDF 263).
- **Результат пуст:** при несовпадении хотя бы одной target/instrumentation label соответствующие образцы двух instant vectors не объединятся (PDF 263).
- **Ошибка `multiple matches for labels`:** `ignoring`/ `on` оставили неоднозначное отношение «многие к одному», нужно анализировать ключ и явную кратность `group_left`/`group_right` (PDF 265–266).
- **Алерт/дашборд показывает только истинные группы:** `count(... > 10)` не содержит 0 для остальных, нужен `sum(... > bool 10)` для численности либо `avg(... > bool threshold)` для доли (PDF 261–262).
- **После добавления info label исчезает ряд:** по умолчанию arithmetic vector matching оставляет только присутствующие на обеих сторонах; в книге приведено дополнение метриками через `or` (PDF 267–269).
- **Метрика `node_custom_metric` отсутствует:** `or up * 0` создаст 0 даже при провальном scrape и посторонних job; предпочтительнее `or (up{job="node"} == 1) * 0` из книги (PDF 269–270).

## Baseline / context

- `0` (scalar) не равен `{} 0` (одиночный vector sample). В арифметике instant vector + scalar имя метрики удаляется даже при `+ 0`; сравнение-фильтр с scalar сохраняет имя и значения; `bool` превращает их в 0/1 (PDF 258–262).
- Шесть основных арифметических операторов `+ - * / % ^`, дополнительно `atan2` (PDF 259–260). Сравнения `== != > < >= <=` (PDF 260).
- Для двух instant vectors matching по умолчанию сравнивает labels, кроме `__name__`; `on` указывает разрешённые метки, `ignoring` исключает из ключа (PDF 263–264).
- `group_left` разрешает *многие слева / один справа* и сохраняет левые labels, `group_left(version)` копирует выбранную информационную метку справа (PDF 265–267). `group_right` меняет стороны, в книге рекомендован `group_left` (PDF 268).
- `or`/ `unless`/ `and` работают как операции над множествами присутствующих рядов; many-to-many для них допустим (PDF 268–271).
- Для `hour()` UTC-час и синтаксис `and on()` применяются к скаляровидному instant vector без labels (PDF 271).

## Read-only checks

1. Сравнить `process_open_fds / process_max_fds` и наличие пар с одинаковыми `instance`, `job`; при отсутствии пары выражение не вернёт левый образец (PDF 263).
2. `process_open_fds > 10` и `process_open_fds > bool 10` дают разный смысл: 14 vs 1/0 у каждого job (PDF 260–262).
3. Проверить `sum without(instance)(process_open_fds > bool 10)` — в source `{job="prometheus"} 1`, `{job="node"} 0`; `avg without(instance)(count without(device)(node_disk_io_now) > bool 4)` даёт долю машин с минимум пятью устройствами (PDF 262).
4. Для idle CPU: `sum without(cpu)(rate(node_cpu_seconds_total{mode="idle"}[5m])) / ignoring(mode) sum without(mode,cpu)(rate(node_cpu_seconds_total[5m]))`; отслеживать удаление `mode` в ключе (PDF 263–264).
5. Если много CPU-режимов, использовать `/ ignoring(mode) group_left`, а не считать, что `ignoring` сам позволяет many-to-one (PDF 265–266).
6. Для переноса `version`: `up * on(instance) group_left(version) prometheus_build_info`; предварительно проверить уникальность RHS для каждой выбранной группы, при необходимости расширить ключ `job` (PDF 266–267).
7. Для разреженных labels сравнить узкий `* ignoring(label) group_left(label)` и дополнение `or ignoring(label)(node_hwmon_temp_celsius*0+1)`, чтобы сохранить sensor=temp1 (PDF 267–269).
8. Для доступного node без `node_custom_metric`: `up{job="node"} == 1 unless node_custom_metric` и вариант `unless on(job, instance)`, когда `node_custom_metric` содержит дополнительные instrumented labels (PDF 270).
9. Объединённое условие через `and`: latency слишком высока и rate запросов больше единицы; выборка по времени с `and on() hour() >= 9 < 17` — UTC (PDF 271).

## Interpretation

- Сравнение двух instant vectors как фильтр возвращает **значения левого** операнда, поэтому `process_open_fds > process_max_fds*.5` предпочтительнее обратной перестановки для алерта (PDF 264–265).
- `on(instance)` безопасен лишь при фактической уникальности target. Даже здесь нужно учитывать возможный `job` (PDF 267).
- Отсутствие label и label с пустой строкой равнозначны в примере дополнения hardware sensor (PDF 269); ряд `temp1` появляется без `label`.
- `x*0+1` может оставить `NaN` как `NaN`: сноска PDF 269. Для `up` правило `up==1` фильтрует неуспешные scrape (PDF 269–270).
- `unless` **по примерам** возвращает левую группу, если справа нет пары; описание на PDF 270 ошибочно говорит о возврате правой группы в другом случае. Не распространять конфликтное словесное правило, см. [source-findings.md](source-findings.md).
- Приоритет: `^` → `* / % atan2` → `+ -` → сравнения → `unless and` → `or`; `^` правоассоциативен, прочие слева направо в своей группе (PDF 272).

## Next action

- Перед сравнением или делением составить список меток с обеих сторон, выяснить intended key, проверить cardinality one-to-one/one-to-many; затем выбирать `ignoring` или `on` и при необходимости `group_left` (PDF 263–268).
- Для метрики здоровья сохранять фактическое значение слева при сравнении и различать отсутствие ряда и 0 — особенно в алертах (PDF 261, 265, 269–270).
- Для логического `and` проверить, что сравниваемые instant vectors совпадают по labels либо явным `on()`, иначе результат может стать пустым (PDF 270–271).

## Modifying action / verification / rollback

- **Modifying action:** [Not applicable]. Все показанные выражения PromQL являются read-only по отношению к TSDB. Выполнение тяжёлого запроса всё же создаёт вычислительную нагрузку; безопасные квоты не описаны в RAG.
- **Verification:** результаты matching имеют ожидаемые `job`, `instance`, `mode`, `version`; отсутствующие пары не создают артефактных series; `bool` даёт 0 и 1; `or`/`unless`/`and` сохраняют левое значение в соответствии с примерами (PDF 261–271).
- **Rollback:** [Not applicable] для простого чтения. Изменение правил алертов/дашбордов и его откат в PDF 258–272 не описаны — [Needs confirmation].
