# Cheatsheet — глава 16: Функции PromQL

**Источник:** PDF 273–293, `p0273:c01`–`p0293:c01` (21 RAG chunks). Историческое описание PromQL 2.37.0; текущая совместимость: [Needs confirmation]. **Никакие запросы не выполнялись**.

## Symptom / problem framing

- `scalar` даёт NaN: instant vector пуст или содержит больше одного sample (PDF 274).
- `up==0` не сообщает об исчезнувшем job: в таком случае отсутствует и `up`; использовать `absent`/ `absent_over_time` (PDF 283–284).
- Шумные скорости Counter: `irate` использует лишь последние два samples и не рекомендован для алертов; `rate` сглаживает и обрабатывает resets (PDF 286–289).
- Диск может заполниться позже: `predict_linear(node_filesystem_free_bytes{job="node"}[1h],4*3600)` прогнозирует будущий Gauge по тренду (PDF 290–291).
- Среднее по времени изменилось при изменении scrape interval: `avg_over_time` усредняет samples, не время между ними (PDF 292).
- Разные метки мешают сопоставлению: сначала исправить источник/ `metric_relabel_configs`, при невозможности — `label_replace`/`label_join` (PDF 282–283).

## Baseline и функции

| Класс | Имена | PDF |
| --- | --- | --- |
| Конверсия | `vector`, `scalar` | 273–275 |
| Math | `abs`, `ln/log2/log10`, `exp`, `sqrt`, `ceil/floor/round`, `clamp`, `clamp_min/max`, `sgn`, trig | 275–279 |
| Календарь | `time`, `minute/hour/day_*`, `days_in_month`, `month`, `year`, `timestamp` | 279–282 |
| Метки | `label_replace`, `label_join` | 282–283 |
| Отсутствие | `absent`, `absent_over_time` | 283–284 |
| Сортировка/квантили | `sort`, `sort_desc`, `histogram_quantile` | 284–285 |
| Counter | `rate`, `increase`, `irate`, `resets` | 285–289 |
| Gauge | `changes`, `deriv`, `predict_linear`, `delta`, `idelta`, `holt_winters` | 289–292 |
| Range series | `sum/count/avg/stddev/stdvar/min/max/quantile_over_time`, `present_over_time`, `last_over_time` | 292–293 |

## Read-only checks

1. `vector(1)`, `scalar(ln(vector(2)))`; fallback `sum(some_gauge) or vector(0)` — различать отсутствие данных и фактический ноль (PDF 274).
2. `time()-process_start_time_seconds`, `timestamp(up)` и `node_time_seconds-timestamp(node_time_seconds)`: время события, sample и задержка/clock skew — разные величины (PDF 280–282).
3. `absent(up{job="missing"})`, `absent_over_time(up{job="myjob"}[1h])`: обнаружение отсутствующего job и отсутствия за интервал (PDF 283–284).
4. `rate(process_cpu_seconds_total[1m])` и `resets(process_cpu_seconds_total[1h])`: средняя скорость и факты уменьшения Counter. Нужны как минимум два samples; рекомендуемый range для `rate` ≥4 scrape intervals (PDF 285–289).
5. `changes(process_start_time_seconds[1h])`: сколько раз наблюдалось изменение времени запуска (PDF 289).
6. `deriv(process_resident_memory_bytes[1h])`, `predict_linear(node_filesystem_free_bytes{job="node"}[1h],4*3600)`: скорость изменения и прогноз. `holt_winters(...,0.1,0.5)` — сглаживание (PDF 290–292).
7. `max_over_time(process_resident_memory_bytes[1h])` — максимум по времени одного процесса; `max without(instance)(max_over_time(...))` — максимум среди экземпляров (PDF 292).
8. `histogram_quantile(0.90,rate(prometheus_tsdb_compaction_duration_seconds_bucket[1d]))` — квантиль Counter-buckets с `+Inf` (PDF 285).

## Interpretation / выбор

- **Counter → `rate`** для алертов и оперативной диагностики; `increase` для отчётов, `irate` только когда важны быстрые колебания (PDF 286–289).
- **Gauge → `changes/deriv/predict_linear`**, учитывая пилообразные графики и поведение вне модели линейного тренда (PDF 289–291).
- **Время → UTC:** `hour()`, `day_of_week()`; воскресенье имеет индекс 0 (PDF 279–281).
- **Absent → пустота vs ноль:** `absent` может унаследовать labels из equality-selector, но не из regex и не из произвольного выражения (PDF 283).
- **Range analysis** не взвешивает samples по времени; нерегулярные scrape и пропуски смещают средние (PDF 292).

## Next action / verification

- Проверить input/output types, actual labelset, data cadence, real reset events, окно анализа, нормализацию единиц seconds/bytes и корректность прогнозируемого тренда.
- При сбоях не использовать некорректные source примеры PDF 275, 278, 284 как эталон; сравнить с [source-findings.md](source-findings.md).
- Не рассчитывать на обнаружение всех редких Counter changes между scrape; для точных событий источник рекомендует рассмотрение журналов (PDF 286–287).

## Modifying action и rollback

**[Not applicable]**: только read-only PromQL. Вычисления могут быть workload-generating для крупной TSDB, лимиты среды [Needs confirmation]. Изменения dashboards/alerts или внешних конфигураций глава не описывает; rollback таких действий [Needs confirmation].
