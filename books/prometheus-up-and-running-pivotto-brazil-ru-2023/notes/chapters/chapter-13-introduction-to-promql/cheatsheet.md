# Cheatsheet — глава 13: Введение в PromQL

**Provenance:** canonical RAG `p0227:c01`–`p0245:c01`, PDF 227–245. Примеры соответствуют контексту Prometheus 2.x и Prometheus 2.37.1 в книге; работа нынешних версий [Needs confirmation].

## Symptom / problem framing

- Gauge с множеством labels трудно суммировать: `sum without(...)` удаляет названные labels и сохраняет остальные (PDF 227–229).
- Counter показывает накопление, но нужна скорость: `rate(metric_total[5m])`, затем агрегировать по интересующим labels (PDF 229).
- Среднее по экземплярам выглядит искажённым: сначала агрегировать `_sum` и `_count`, затем делить; не брать среднее от средних (PDF 230–231).
- Квантиль по нескольким экземплярам кажется неверной: сначала агрегировать histogram buckets, затем `histogram_quantile`; Summary quantiles не агрегировать (PDF 231–233).
- Неожиданно исчезает цель из instant-query: учитывать staleness marker и 5-минутное окно просмотра (PDF 235–236).
- API возвращает `matrix` вместо `vector` или пустые данные: проверять тип selector, время выполнения, исторический диапазон и series (PDF 240–244).

## Baseline / context

- `sum without(device,fstype,mountpoint)(node_filesystem_size_bytes)` — пример агрегирования данных файловых систем (PDF 228). **В тексте ниже перечислены `node_filesystem_free_bytes`, а не `size_bytes`**: численный результат источника не следует считать golden-test.
- Счетчик `node_network_receive_bytes_total`: скорость `rate(...[5m])`, суммарная скорость `sum without(device)(rate(...[5m]))` (PDF 229).
- Summary: `http_response_size_bytes_sum` и `http_response_size_bytes_count`; Histogram: `prometheus_tsdb_compaction_duration_seconds_bucket{le}` (PDF 230–233).
- Matchers `=`, `!=`, `=~`, `!~`; все условия в одном selector образуют AND. RE2 regex matches anchored (PDF 233–235).
- Instant selector — до одного образца на series; range selector `[1m]` — множество исходных точек. Допустимые по тексту обозначения интервалов `ms,s,m,h,d,w,y`; комбинации упорядочены от более крупных к меньшим (PDF 235–238).
- Subquery `[30m:1m]`, `offset 1h`, `@ 1667491200`, `@ end()`; API `query`/`query_range` (PDF 238–245).

## Read-only checks

1. В expression browser проверить `rate(node_network_receive_bytes_total[5m])` и `sum without(device)(rate(node_network_receive_bytes_total[5m]))` (PDF 229).
2. Проверить совпадение оставшихся labels `job`, `instance` при `sum without(...)`; операций с полями вне source RAG не добавлять (PDF 228).
3. Выполнить `process_resident_memory_bytes{job="node"}` и range selector `process_cpu_seconds_total[1m]`; сравнить один sample на ряд против нескольких (PDF 233, 236–237).
4. Проверить select `job!="node"`, `job=~"n.*"`, `mountpoint!~"/run/user/.*"` с конкретной метрикой; пустые selectors `{}`, `{foo=""}`, `{foo=~".*"}` запрещены источником (PDF 234–235).
5. Проверить `offset` на одном selector без изменения момента запроса целиком, затем при необходимости `@` с временем Unix (PDF 239–240).
6. Для `query` сравнить `/api/v1/query?query=42` (scalar), `...query=process_resident_memory_bytes` (vector), `...query=process_cpu_seconds_total[1m]` (matrix по правилу главы; буквальный API-пример PDF 242 использует другую метрику и конфликтует с JSON) (PDF 241–243).
7. Для `query_range` проверить `start`, `end`, `step` и window в `rate`. Источник рекомендует range дольше step на один-два scrape intervals (PDF 243–245).

## Interpretation

- Преобразованные instant vectors получают время оценки, raw range samples сохраняют исходные timestamps; API в JSON instant sample показывает `value: [timestamp, "string"]` (PDF 235–237, 241).
- Staleness: временной ряд с маркером устаревания не попадает в instant vector; range vector пропускает маркеры, но возвращает остальные исходные samples. Для экспортированных custom timestamps логика особая (PDF 235–237).
- `rate` экстраполирует и выдаёт дробный результат, если scrape не согласован с границами окна; это не арифметическая ошибка (PDF 229).
- `histogram_quantile(0.90,...)` на ~12 compaction events за сутки — иллюстративно, высокие квантили на малом числе событий ненадёжны; широкий range может быть дорогим (PDF 231–232).
- `query_range` — шаговые мгновенные вычисления, `end` включается, если совпадает с шагом; пропущенный результат шага не дополняется автоматически (PDF 243–245).

## Next action

- Выяснить тип метрики: Gauge → агрегирование текущего значения; Counter → `rate`; Summary → агрегировать count/sum и делить; Histogram → агрегировать buckets и затем вычислять квантиль (PDF 227–233).
- Ограничивать series конкретными labels до сложной агрегации; избегать потенциально дорогого `{__name__=~".+"}` (PDF 234–235).
- Для статистики и отчётов задавать согласованное время; для исторических срезов использовать `offset` или `@`, учитывая фактические timestamps (PDF 238–245).
- При построении графиков выбирать шаг относительно range в `rate`, а слишком длинные запросы разделять (PDF 243–245).

## Modifying action

**[Not applicable]**: все буквальные PromQL-примеры и `/api/v1/query`, `/api/v1/query_range` главы — read-only относительно TSDB. Глава 13 упоминает существование отдельных **административных API** со снимками и удалением рядов (PDF 240), но не приводит URL/команд для вызова; их не реконструировать и не выполнять. Runtime-изменений нет.

## Verification / acceptance checks

- `sum without` удаляет только перечисленные метки и возвращает ожидаемое количество групп по фактическим рядам (PDF 228).
- Для Counter `rate(...)` возвращает значения в единицах за секунду; `sum without(device)(rate(...))` оставляет остальные labels (PDF 229).
- Ratio Summary вычисляется из суммы `rate(_sum)` / суммы `rate(_count)`; квантиль histogram — после bucket aggregation (PDF 230–233).
- `query` возвращает `status: success` и подходящий `resultType`, `query_range` — matrix с timestamps по start/step/end при наличии данных; JSON страницы 244 нельзя копировать как валидный без отдельной корректировки (PDF 240–245).
- Реальные численные значения и наличие старых метрик источником не гарантируются: [Needs confirmation].

## Rollback

**[Not applicable]**: в этом RAG-фрагменте приведены read-only запросы и API. Для административных методов snapshot/delete подробные действия и rollback отсутствуют — [Needs confirmation]; эти API **не вызываются**.
