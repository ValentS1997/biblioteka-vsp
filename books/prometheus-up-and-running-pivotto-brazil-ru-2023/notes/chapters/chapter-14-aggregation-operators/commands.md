# PromQL — операторы агрегирования, глава 14

**Источник:** PDF 246–257, RAG `p0246:c01`–`p0257:c01`. Все выражения относятся к **read-only** вычислениям PromQL (при этом возможна **workload-generating** нагрузка); **не выполнялись**. Реальные результаты зависят от текущих рядов. **State-changing commands отсутствуют, rollback: [Not applicable].**

## Группировка: without и by (PDF 247–249)

```promql
sum without(fstype, mountpoint)(node_filesystem_size_bytes)
sum by(job, instance, device)(node_filesystem_size_bytes)
sum without()(node_filesystem_size_bytes)
sum by()(node_filesystem_size_bytes)
sum(node_filesystem_size_bytes)
count by(release)(node_uname_info)
```

- Первые две строки возвращают одинаковые 3 группы **только для приведённого набора меток** `device, fstype, mountpoint, job, instance`. После добавления новой target label они могут различаться: `without` её сохранит, `by` удалит (PDF 247–248).
- `sum without()` не суммирует между различными series, а убирает `__name__`; `sum by()`/`sum()` объединяет всё в один ряд без labels (PDF 248–249).
- В исходных цифрах PDF 247 для `device="tmpfs"` сумма **2486128640**; для всех FS автор приводит **92718116864** (PDF 249). Это числа **учебного** узла, не критерий для другого сервера.
- Пустая метрика остаётся пустой, в том числе для `count`:
```promql
sum(non_existent_metric)
count by(foo)(non_existent_metric)
count(non_existent_metric)
```
Expected: empty instant vector, **не** 0 (PDF 249).

## Сумма скорости Counter, count и число CPU (PDF 250–251)

```promql
sum without(fstype, mountpoint, device)(node_filesystem_size_bytes)
sum without(device)(rate(node_disk_read_bytes_total[5m]))
count without(device)(node_disk_read_bytes_total)
count without(cpu)(count without(mode)(node_cpu_seconds_total))
count(count by(cpu)(node_cpu_seconds_total))
```

- `sum(...rate(...))` — скорость данных по устройствам; `count(...)` — число рядов устройств, а не сумма байтов или rate.
- В nested `count` внутренний шаг устраняет `mode`, внешнему нужно посчитать процессоры (`cpu`); учебный результат `4` (PDF 250–251).
- Вложенный `count(count by(cpu)(...))` обобщает количество значений метки cpu в наборе, но не обязательно даёт число CPU **на каждом** узле при нескольких экземплярах (PDF 251).

## Среднее и group (PDF 251–252)

```promql
avg without(cpu)(rate(node_cpu_seconds_total[5m]))
sum without(cpu)(rate(node_cpu_seconds_total[5m]))
/
count without(cpu)(rate(node_cpu_seconds_total[5m]))
count by(instance)(
  group by(fstype, instance)(node_filesystem_files)
)
```

- Первая и следующая пара через `sum/count` дают одинаковое арифметическое среднее при соответствующем наборе рядов; `avg` компактнее (PDF 251).
- `group` отдаёт `1` на группу, делая акцент на labels, а не на значении. Во втором примере подсчитываются типы FS по каждому instance (PDF 252).
- `NaN` во входных данных может попасть в `avg`; избегать усреднения готовых средних. Сноска PDF 252 «1/0 = NaN» не принимается как проверенное правило: [source-findings.md](source-findings.md).

## Выбросы, разброс и крайние значения (PDF 252–254)

```promql
some_gauge
> ignoring(instance) group_left()
(
  avg without(instance)(some_gauge)
  +
  2 * stddev without(instance)(some_gauge)
)

max without(device, fstype, mountpoint)(node_filesystem_size_bytes)
topk without(device, fstype, mountpoint)(2, node_filesystem_size_bytes)
```

- Первый пример сравнивает значение экземпляра со средним группы + 2 стандартных отклонения. Использует vector matching, который раскрыт лишь в главе 15. Для узкого распределения порог может оказаться малоинформативным; в тексте предложено дополнительное правило «как минимум на 20% выше среднего», **но готовой формулы нет** (PDF 253).
- `max` возвращает значения **и метки группы**, `topk` — значения **и полный исходный набор меток**, в том числе `__name__` (PDF 253–254).
- `bottomk` работает в противоположную сторону и также возвращает до k исходных рядов; отдельный буквальный листинг `bottomk` в тексте отсутствует (PDF 254).
- При `query_range` набор topk изменяется между шагами; авторы предлагают использовать `@` для фиксирования момента. **Не реконструировать готовую query_range формулу** по одному абзацу (PDF 254).

## quantile: распределение между series (PDF 254–255)

```promql
quantile without(cpu)(0.9, rate(node_cpu_seconds_total{mode="system"}[5m]))
avg without(instance)(rate(process_cpu_seconds_total[5m]))
quantile without(instance)(0.25, rate(process_cpu_seconds_total[5m]))
quantile without(instance)(0.5, rate(process_cpu_seconds_total[5m]))
quantile without(instance)(0.75, rate(process_cpu_seconds_total[5m]))
```

- `quantile` — квантиль группы instant-vector. `quantile_over_time` работает с одной series в range-vector, `histogram_quantile` — с buckets histogram (PDF 255).
- Вывод для 0.9 из книги `0.024558620689654007`. **[Source interpretation mismatch]:** в прозе сказано «90 % процессоров не менее 0.02», что не следует безоговорочно принимать за корректную интерпретацию девяностого процентиля; дополнительная проверка необходима.

## count_values: частоты дискретных значений (PDF 255–257)

Исходный пример содержит шесть значений `software_version`: `7,4,8,4,7,4`.

```promql
count_values without(instance)("version", software_version)
count without(version)(
  count_values without(instance)("version", software_version)
)
count_values without(instance)(
  "devices",
  count without(device)(node_disk_io_now)
)
```

- Первый выводит частоты `version="7" → 2`, `"8" → 1`, `"4" → 3`; второй возвращает число уникальных версий `{job="j"} 3` (PDF 256).
- Последний строит частоты числа дисковых устройств на машинах; учебный пример `{devices="5",job="node"} 1` (PDF 257).
- **Предупреждение:** точные числа с плавающей точкой при высоком разнообразии создают множество series. Источник рекомендует применять `count_values` преимущественно к дискретным значениям (PDF 256).

## Высокая стоимость запросов / preflight

```promql
sort_desc(count by(__name__)({__name__=~".+"}))
```

**Potentially expensive, workload-generating.** Источник предупреждает, что выражение затрагивает **все активные series** (PDF 248). Не выполнять бесконтрольно против крупной production TSDB. В этой главе нет описанного безопасного порога/ограничения скорости: [Needs confirmation].

## Verification и ограничения

Сопоставить labels и число групп на тестовых данных, проверить отсутствие незаданных `env`/`cluster`, различить пустой vector и 0, проверить `rate` для Counter, не использовать цифры одной учебной машины как эталон другой. Операции здесь **не меняют** TSDB; rollback [Not applicable]. Поведение в конкретной установленной версии не проверялось.
