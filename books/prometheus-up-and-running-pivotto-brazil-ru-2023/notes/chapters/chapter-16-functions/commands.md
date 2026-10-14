# Commands / PromQL — глава 16

**Источник:** PDF 273–293, `p0273:c01`–`p0293:c01` (`rag_only`). Все выражения **read-only** относительно TSDB, но могут быть **workload-generating**. Ничего не исполнялось; реальные метрики и версия сервера [Needs confirmation]. Modifying commands: **[Not applicable]**; rollback чтения **[Not applicable]**.

## Конверсии и вычисления (PDF 273–279)

```promql
vector(1)
sum(some_gauge) or vector(0)
scalar(ln(vector(2)))
year(process_start_time_seconds) == scalar(year())
abs(process_open_fds - 15)
log10(
  sum without(instance)(rate(requests_failed_total[1h]))
  /
  sum without(instance)(rate(requests_total[1h]))
) * -1
ln(x) / ln(3)
exp(vector(1))
sqrt(vector(9))
vector(9) ^ 0.5
ceil(vector(0.1))
round(vector(5.5))
round(vector(2446), 1000)
clamp_min(process_open_fds, 10)
clamp(process_open_fds, 10, 20)
sgn(vector(100))
sin(vector(pi()/2))
```

`vector(1)` даёт `{} 1`; `scalar` при числе рядов, отличном от одного, даёт NaN. Функции над instant vectors обычно удаляют имя метрики. `ln` аргумента 0 или отрицательного значения и деление rates могут давать пограничные случаи; источник советует использовать логарифмическую шкалу графиков (PDF 276). **Source inconsistency PDF 278:** prose `clip_max/clip_min`, фактические `clamp*`; исполняемый синтаксис текущего сервера [Needs confirmation].

**Не готов к копированию (PDF 275, source-broken):**
```text
sum(rate(node_cpu_seconds_total{mode!="idle",instance="localhost:9090"}[5m]))
/
scalar(count(node_cpu_seconds_total{mode="idle",instance="localhost:9090"))
```
Второй selector/вызов имеют некорректные закрытия; **не выдавать этот блок за runnable PromQL**. Другой вариант из того же PDF:
```promql
sum without(cpu, mode)(rate(node_cpu_seconds_total{mode!="idle"}[5m]))
/
count without(cpu, mode)(node_cpu_seconds_total{mode="idle"})
```

## Время, sample timestamps и календарь (PDF 279–282)

```promql
time()
time() - process_start_time_seconds
time() - my_job_last_success_seconds > 3600
minute()
hour()
day_of_week()
day_of_month()
day_of_year()
days_in_month()
month()
year()
year(process_start_time_seconds)
timestamp(up)
node_time_seconds - timestamp(node_time_seconds)
```

В книге 05.11.2022 13:37 **UTC**: `minute=37`, `hour=13`, `day_of_week=6`, `day_of_month=5`, `day_of_year=309`, `month=11`. Значения не являются актуальными. `timestamp(up)` у instant selector относится к реальному sample; `time()` — к моменту оценки, а `node_time_seconds` — к текущим часам узла. Оценка часов через разницу только приблизительная из-за сетевой/системной задержки.

**Количество процессов, начавших работу в текущем месяце (PDF 281):**
```promql
sum(
  (year(process_start_time_seconds) == bool scalar(year()))
  *
  (month(process_start_time_seconds) == bool scalar(month()))
)
```

## Метки, absent и сортировка (PDF 282–285)

```promql
label_replace(node_disk_read_bytes_total, "dev", "${1}", "device", "(.*)")
label_join(node_disk_read_bytes_total, "combined", "-", "instance", "job")
absent(up{job="missing"})
absent(non_existent{job="foo",env="dev"})
absent_over_time(up{job="myjob"}[1h])
sort(node_filesystem_size_bytes)
```

**Risk:** `label_replace` на Counter лучше применять после `rate` (сноска PDF 282); предпочтительнее устранять неконсистентность в source или `metric_relabel_configs`. `absent(up{job="missing"})` возвращает `{job="missing"} 1` только если таких рядов нет. `absent` с regex matcher не переносит такую метку. **Source finding PDF 284:** `sort(node_filesystem_size_bytes)`, но перечисленный вывод `node_filesystem_free_bytes`; не использовать как согласованный fixture.

## Histogram / Counter (PDF 285–289)

```promql
histogram_quantile(
  0.90,
  rate(prometheus_tsdb_compaction_duration_seconds_bucket[1d])
)
rate(process_cpu_seconds_total[1m])
rate(x_total[5m])
increase(x_total[5m])
irate(process_cpu_seconds_total[5m])
resets(process_cpu_seconds_total[1h])
```

- `histogram_quantile` нуждается в кумулятивных buckets и `+Inf`; Counter buckets требуют `rate` перед вычислением квантиля (PDF 285).
- `rate` интерпретирует уменьшение как reset и экстраполирует края; рекомендуемое окно ≥4× `scrape_interval` (PDF 285–288).
- `increase(x_total[5m])` в описании эквивалентно `rate(x_total[5m]) * 300`; результат может быть дробным. В source-примере `21@2s,22@7s,24@12s` экстраполяция на 15 секунд даёт `4.5` (PDF 287).
- `irate` смотрит лишь последние два samples, на алертах нежелателен. `resets` возвращает количество уменьшений счётчика (PDF 288–289). Изображение графика 16.1 доступно лишь по подписи в RAG.

## Gauge, прогноз и over_time (PDF 289–293)

```promql
changes(process_start_time_seconds[1h])
deriv(process_resident_memory_bytes[1h])
predict_linear(node_filesystem_free_bytes{job="node"}[1h], 4 * 3600)
holt_winters(process_resident_memory_bytes[1h], 0.1, 0.5)
max_over_time(process_resident_memory_bytes[1h])
max without(instance)(max_over_time(process_resident_memory_bytes[1h]))
rate(x_total[1h])
```

`changes` фиксирует изменения Gauge; `deriv` и `predict_linear` используют регрессию; `holt_winters` в источнике использует коэффициенты между 0 и 1. `delta`/`idelta` не обрабатывают сбросы Counter, не подменяют `increase`/`irate`.

**Историческая ошибка типов (PDF 293) — не запускать:**
```text
avg_over_time(rate(x_total[5m])[1h])
```
`rate` возвращает instant vector, а `avg_over_time` ожидает range vector; **это конкретная запись без явного subquery step**, тогда как в главе 13 разобраны subqueries. Подменять учебный пример и делать категорические утверждения о современных версиях без проверки не следует.

## Проверки и принятие

Проверять наличие и типы series, labels, timestamps, значение `rate` и влияние сбросов, качество прогноза и число samples в диапазоне. Для `avg_over_time` учитывать смещение от нерегулярного scrape (PDF 292). Вся активность в анализе ограничена чтением RAG и подготовкой документации.
