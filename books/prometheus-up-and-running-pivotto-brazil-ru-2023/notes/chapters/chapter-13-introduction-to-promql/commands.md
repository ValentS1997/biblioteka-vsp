# PromQL и HTTP API — примеры главы 13

**Источник:** строго PDF 227–245 (`p0227:c01`–`p0245:c01`). Все запросы **read-only** относительно TSDB, но могут создавать вычислительную нагрузку (**workload-generating**); **не исполнялись**. Исторические series/числа не гарантированы для текущего сервера. Нет state-changing команд; rollback **[Not applicable]**. Административные API на PDF 240 названы, но их вызовы в главе не приведены и не реконструируются.

## 1. Gauge, Counter и агрегация (PDF 227–230)

```promql
sum without(device, fstype, mountpoint)(node_filesystem_size_bytes)
max without(device, fstype, mountpoint)(node_filesystem_size_bytes)
sum without(device, fstype, mountpoint, instance)(node_filesystem_size_bytes)
avg without(instance, job)(process_open_fds)
rate(node_network_receive_bytes_total[5m])
sum without(device)(rate(node_network_receive_bytes_total[5m]))
sum without(instance)(rate(node_network_receive_bytes_total{device="eth0"}[5m]))
```

**Чтение:** `rate` производит байты/сек из Counter. В выводе `sum without` сохраняет все метки, которые не перечислены. **[Source wording/code mismatch]** PDF 228: в первом выражении `size_bytes`, но приведённые исходные ряды `free_bytes` и число **32511390720** являются их суммой. Это **несовпадение имени**, а не арифметики; см. [source-findings.md](source-findings.md). Проверка в среде: сравнить семейства и реальный результат, не использовать напечатанное значение как ответ запроса `size_bytes`.

## 2. Summary: суммировать числитель и знаменатель до деления (PDF 230–231)

```promql
sum without(handler)(rate(http_response_size_bytes_sum[5m]))
/
sum without(handler)(rate(http_response_size_bytes_count[5m]))
```

По книге *неверно* усреднять отдельные средние:

```promql
avg without(instance)(
    sum without(handler)(rate(http_response_size_bytes_sum[5m]))
  /
    sum without(handler)(rate(http_response_size_bytes_count[5m]))
)
```

Для нескольких экземпляров корректное выражение из PDF 231:

```promql
sum without(instance)(
  sum without(handler)(rate(http_response_size_bytes_sum[5m]))
)
/
sum without(instance)(
  sum without(handler)(rate(http_response_size_bytes_count[5m]))
)
```

Сноска PDF 230 предупреждает о переименовании одного имени метрики в Prometheus 2.3.0. Фактическое имя на пользовательском сервере: **[Needs confirmation]**.

## 3. Histogram и квантиль (PDF 231–233)

```promql
histogram_quantile(
    0.90,
    rate(prometheus_tsdb_compaction_duration_seconds_bucket[1d]))
```

Здесь длинное окно `1d` авторы выбрали из-за редких compaction events. Высокие квантили при малом числе событий и диапазонах часов/дней могут быть ненадёжны и дороги. **Другой источниковый листинг PDF 232:**

```promql
histogram_quantile(
  0.90,
  sum without(instance)(rate(prometheus_tsdb_compaction_duration_bucket[1d])))
```

**[Source code mismatch]:** во втором имени отсутствует `_seconds`. Также PDF 233 приводит `prometheus_tsdb_compaction_duration_sum` и `_count`. Сохраняем оба варианта, **не объявляем второй рабочим** без проверки реального семейства.

## 4. Селекторы и staleness (PDF 233–237)

```promql
process_resident_memory_bytes{job="node"}
node_filesystem_size_bytes{job="node",mountpoint=~"/run/.*",mountpoint!~"/run/user/.*"}
process_cpu_seconds_total[1m]
rate(process_cpu_seconds_total[1m])
{__name__=~".+"}
```

`=`, `!=`, `=~`, `!~` — четыре matchers; RE2 неявно anchored, условия AND. Важное ограничение из PDF 235: пустое `{}`, `{foo=""}`, `{foo=~".*"}` вызывают ошибку, допустимы `{foo="",bar="x"}`, `{foo!=""}`, `{foo=~".+"}`. По книге селектор `{__name__=~".+"}` может выбрать очень много series и **дорого обойтись**; не выполнять на production без лимитов.

**[Source code mismatch] PDF 235:** текст объясняет `__name__`, но следующий «эквивалент» пишет `{name="process_resident_memory_bytes",job="node"}`; расхождение в имени метки зарегистрировано, не выдавать `{name=...}` за подтверждённый эквивалент.

## 5. Subquery и работа со временем (PDF 238–240)

```promql
max_over_time(rate(http_requests_total[5m])[30m:1m])
process_resident_memory_bytes{job="node"} offset 1h
process_resident_memory_bytes{job="node"} - process_resident_memory_bytes{job="node"} offset 1h
rate(process_cpu_seconds_total{job="node"}[5m]) - rate(process_cpu_seconds_total{job="node"}[5m] offset 1h)
http_requests_total @ 1667491200
rate(http_requests_total[1m]) and topk(5, rate(http_requests_total[1h] @ end()))
```

`[30m:1m]` — выполнить внутреннее выражение через 1 минуту на протяжении 30 минут. `offset` сдвигает selector, `@` фиксирует время selector; `start()` и `end()` описаны для range-query. По PDF 238 интервалы `ms,s,m,h,d,w,y` и `90m`, `1h30m`, `1.5h` приведены как разрешённые, `30m1h` как запрещённый. **Современная синтаксическая поддержка `1.5h`: [Needs confirmation]**. На PDF 240 слова о «начале» окна для `[5m] @ timestamp` отличаются от пояснения range как предшествующего времени на PDF 236; зарегистрировано, не менять source.

## 6. HTTP API `query` — GET/read-only, потенциально workload-generating (PDF 240–243)

Буквальные URL из RAG:

```text
http://localhost:9090/api/v1/query?query=process_resident_memory_bytes
http://localhost:9090/api/v1/query?query=process_resident_memory_bytes&time=1514764800
http://localhost:9090/api/v1/query?query=42
http://localhost:9090/api/v1/query?query=prometheus_tsdb_head_samples_appended_total[1m]
```

Форма результатов:

```text
status: success | error
data.resultType: vector | matrix | scalar
vector: result[].metric + result[].value = [timestamp, "sample"]
matrix: result[].metric + result[].values = [[timestamp,"sample"], ...]
scalar: result = [timestamp, "42"]
```

Timestamp API в секундах; значение — строка, что допускает сериализацию `NaN`/`+Inf` по тексту (PDF 241). **[Source contradiction] PDF 242:** URL запрашивает `prometheus_tsdb_head_samples_appended_total[1m]`, но JSON содержит `process_resident_memory_bytes`, поэтому этот пример нельзя принимать как согласованный ответ.

## 7. HTTP API `query_range` — GET/read-only, потенциально тяжёлый (PDF 243–245)

```text
http://localhost:9090/api/v1/query_range?query=rate(prometheus_tsdb_head_samples_appended_total[5m])&start=1514764800&end=1514765700&step=60
```

`start`/`end`/ `step`: серия instant-вычислений; результат `matrix`, значение `end` включительно, если совпало с шагом. **Range окна функции `rate` должно быть длиннее `step` хотя бы на 1–2 scrape intervals**, иначе часть выборок пропускается (PDF 244). Источник сообщает лимит **11 000 шагов** и возможность деления отчёта на несколько запросов (PDF 244–245). Для почасового выравнивания приведено выражение Python `(time.time() // 3600) * 3600` (PDF 245); его исполняемость/значение в окружении: [Needs confirmation]. **JSON PDF 244 содержит завершающую запятую** после финальной записи `values`; его нельзя использовать как валидный JSON-fixture без отдельной исправленной копии с отметкой об исправлении.

## Приёмка и rollback

Проверка: правильно возвращаются `resultType`, labels, количество samples, timestamps, время окна и стабильность подзапросов; значение совпадает с текущими TSDB series, а не историческими цифрами книги. Модификация состояния в главе не описана, rollback для приведённых GET и PromQL **[Not applicable]**. Безопасный контроль ресурсоёмких запросов и актуальные runtime-ограничения: **[Needs confirmation]**.
