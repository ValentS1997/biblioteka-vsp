# Source findings — глава 13

**Provenance:** PDF 227–245, `p0227:c01`–`p0245:c01`; SHA256 `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`. `rag_only`, никакой silent correction, внешних сведений или подмены источника. Возможные ошибки извлечения и оригинального издания не разграничиваются без прямой проверки.

## F-01 — [Source wording/code mismatch]: `size_bytes` vs `free_bytes` и правильная сумма другого ряда

- **RAG `p0228:c01`**, PromQL: `sum without(device, fstype, mountpoint)(node_filesystem_size_bytes)`.
- **Там же**, исходные строки перечислены как `node_filesystem_free_bytes` со значениями `70300672`, `30791843840`, `817094656`, `5238784`, `826912768`.
- **Там же**, ожидаемая сумма `32511390720`. Арифметическая сумма **перечисленных free_bytes равна этому числу**: `70300672 + 30791843840 + 817094656 + 5238784 + 826912768 = 32511390720`.
- **Проблема:** объявлен selector **`size_bytes`**, а данные и ожидаемое число относятся к **`free_bytes`**. Это несовпадение *имени семейства*, не доказанная арифметическая ошибка. Не менять selector из оригинала silently; проверка actual `size_bytes` в среде [Needs confirmation].

## F-02 — [Source code mismatch]: потерян суффикс `_seconds` в Histogram

- **RAG `p0231:c01`–`p0232:c01`:** определена `prometheus_tsdb_compaction_duration_seconds_bucket` и первый `histogram_quantile(0.90, rate(prometheus_tsdb_compaction_duration_seconds_bucket[1d]))`.
- **RAG `p0232:c01`**, агрегированный вариант: `sum without(instance)(rate(prometheus_tsdb_compaction_duration_bucket[1d]))`.
- **RAG `p0233:c01`:** аналогичные `_sum`/`_count` тоже использованы под `prometheus_tsdb_compaction_duration_` без `_seconds`.
- **Следствие:** два базовых имени семейства в примерах не совпадают; семантика подхода (aggregate buckets before quantile) сохраняется, но фактические series [Needs confirmation]. Не исправлять source silently.

## F-03 — [Source wording/code mismatch]: `__name__` vs `name`

- **RAG `p0235:c01`:** объясняется, что имя метрики хранится в `__name__`.
- **Там же** «эквивалент» `process_resident_memory_bytes{job="node"}` дан как `{name="process_resident_memory_bytes",job="node"}`.
- **Там же** ниже приведён `{__name__=~".+"}`, подтверждающий упоминание `__name__`.
- **Следствие:** эквивалент с `name` не согласован с правилом этого же абзаца. В `commands.md` он не объявлен рабочим. Исправление [Needs confirmation].

## F-04 — [Source wording/code mismatch]: начало vs окончание окна `@`

- **RAG `p0236:c01`:** range `[1m]` возвращает образцы **за минуту до** момента оценки.
- **RAG `p0240:c01`:** `rate(http_requests_total[5m] @ 1667491200)` описан как частота «за 5-минутный интервал, **начинающийся** в тот же момент времени».
- **Следствие:** словесная направленность диапазона расходится с определением range для selector. Не менять вычисление по памяти; до использования исторического периода проверить семантику выбранной версии [Needs confirmation].

## F-05 — [Source wording/code mismatch]: сингулярное имя счётчика HTTP

- **RAG `p0240:c01`**, описание примера говорит «изменения `http_request_total`».
- **Там же**, PromQL применяет `rate(http_requests_total[1m])` и `topk(5, rate(http_requests_total[1h] @ end()))`.
- **Следствие:** `http_request_total` / `http_requests_total` — разные имена; source example использует второе. Допустимые series конкретной TSDB [Needs confirmation].

## F-06 — [Source contradiction]: API range-query и сериализованный `__name__`

- **RAG `p0242:c01`:** HTTP URL `/api/v1/query?query=prometheus_tsdb_head_samples_appended_total[1m]`.
- **Там же**, массив `matrix` содержит `"__name__": "process_resident_memory_bytes"` для обоих series.
- **Проблема:** запрос и response показывают разные метрики; не считать JSON достоверным fixture именно этого URL. Вероятно ошибка подстановки/извлечения [Needs confirmation].

## F-07 — [Source code mismatch] / [Source extraction issue]: некорректная JSON-запятая

- **RAG `p0243:c01`–`p0244:c01`:** JSON `/api/v1/query_range`, массив `values`, последний элемент `[1514765700, "146.8"],` перед закрывающей скобкой.
- **Проблема:** завершающая запятая делает приведённый ответ невалидным по строгому синтаксису JSON. В `commands.md` приведён URL, не копия JSON-fixture. Корректировка источника не выполняется.

## F-08 — [Needs confirmation]: исторические ограничения и экранные изображения

- **RAG `p0244:c01`–`p0245:c01`:** лимит 11 000 шагов, рекомендации по `step` и выравниванию отчётности; перенос на сегодняшнюю конфигурацию/версию сервера не проверен.
- **RAG `p0237:c01`:** рис. 13.1 представлен текстовой подписью без самостоятельного снимка Console.
- **RAG `p0238:c01`:** `1.5h` назван допустимым интервалом. Внеисточниковая проверка современной синтаксической поддержки не делалась — [Needs confirmation].
- **Решение:** визуальные схемы строятся по доступному тексту. Лимиты, экраны и флаги конкретного сервера не утверждаются как текущие.

Регистр описывает наблюдаемые свойства канонического извлечённого текста, не претендуя на исправление печатного издания.
