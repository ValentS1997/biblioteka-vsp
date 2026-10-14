# Глава 16. Функции

**Книга:** «Запускаем Prometheus. Мониторинг инфраструктуры и приложений» (Жюльен Пивотто, Брайан Бразил, Books.kz, 2023). **Inventory:** 0040.  
**Book ID:** `prometheus-up-and-running-pivotto-brazil-ru-2023`. **Контракт:** `BIBLIOTEKA-VSP-CHAPTER-ARTIFACT-COLLECTION v1.7`. **Состояние:** `RAG_GROUNDED` до отдельной целевой валидации. **Режим:** `rag_only`, без прямого чтения PDF, внешних источников и модельных дополнений.

## Provenance

- Глава 16 начинается на **PDF 273**, `p0273:c01`, заканчивается на **PDF 293**, `p0293:c01`. Глава 17 «Правила записи» начинается на PDF 294, `p0294:c01`.
- **21 адресуемый чанк** `p0273:c01`–`p0293:c01` из `rag/chunks/p0201-p0300/`; `source_locator: pdf_page=273..293`.
- SHA256 источника: `ab45c7bc9a393b15bc60628dfceaa45db71388fd28e75c5c55ab6eaf5930f787`; `rag/acceptance.yaml: ACCEPTED`.
- Исторический контекст издания — PromQL 2.37.0, «69 функций» по PDF 273; состояние текущей версии [Needs confirmation].

## Тематический обзор

| Раздел | PDF | Функции и смысл |
| --- | --- | --- |
| Типы | 273–275 | `vector`, `scalar`, static typing; переход scalar ↔ instant vector |
| Математика | 275–279 | `abs`, `ln`, `log2`, `log10`, `exp`, `sqrt`, `ceil`, `floor`, `round`, `clamp*`, `sgn`, тригонометрия |
| UTC и timestamps | 279–282 | `time`, `minute/hour/day_*`, `days_in_month`, `month`, `year`, `timestamp` |
| Метки | 282–283 | `label_replace`, `label_join` |
| Отсутствующие серии | 283–284 | `absent`, `absent_over_time` |
| Сортировка и Histogram | 284–285 | `sort`, `sort_desc`, `histogram_quantile` |
| Counter | 285–289 | `rate`, `increase`, `irate`, `resets` |
| Gauge | 289–292 | `changes`, `deriv`, `predict_linear`, `delta`, `idelta`, `holt_winters` |
| По времени | 292–293 | `sum/count/avg/stddev/stdvar/min/max/quantile_over_time`, `present_over_time`, `last_over_time` |

## Суть главы

**Типы аргументов фиксированы.** Большинство функций возвращают instant vector; `time`, `pi`, `scalar` возвращают scalar в описанной версии. Функции для range vector, например `rate` и `avg_over_time`, анализируют одну серию и возвращают instant vector, а не range vector (PDF 273).

1. `vector(1)` создаёт одиночный sample без меток; `scalar(v)` превращает вектор с ровно одним sample в scalar, при нуле или множестве samples возвращает NaN (PDF 274).
2. `time()-process_start_time_seconds` измеряет uptime; `timestamp(up)` возвращает отметку времени исходной точки, а `hour()` и другие календарные функции работают в UTC (PDF 279–282).
3. `absent(up{job="missing"})` обнаруживает исчезнувшую цель, которое не выявить по `up==0`; `absent_over_time(up{job="myjob"}[1h])` проверяет отсутствие в течение часа (PDF 283–284).
4. `rate` учитывает сбросы Counter, экстраполирует край диапазона, рекомендуется окно ≥4× scrape interval; `increase` = rate × seconds; `irate` зависит только от последних двух samples и нежелателен для алертов; `resets` помогает обнаружить уменьшения (PDF 285–289).
5. `changes` — число изменений Gauge; `deriv` — наклон линейной регрессии; `predict_linear` — прогноз, `holt_winters` — сглаживание; `delta`/`idelta` не обрабатывают Counter resets (PDF 289–292).
6. `*_over_time` агрегируют точки каждой серии без временных весов; при изменении частоты scrape меняется вклад разных периодов. Для Counter авторы предлагают `rate(x_total[1h])` вместо некорректного без подзапроса `avg_over_time(rate(x_total[5m])[1h])` (PDF 292–293).
7. Для Histogram с обычными Counter bucket нужно сначала `rate`, затем `histogram_quantile`; buckets кумулятивны, обязательно `+Inf` (PDF 285).

## Findings и ограничения

- PDF 275: в примере `scalar(count(...` нарушены закрывающие скобки и фигурная скобка; не копировать.
- PDF 278: `clip_max`/`clip_min` в тексте против `clamp*` в заголовке и коде.
- PDF 284: `sort(node_filesystem_size_bytes)`, а вывод маркирован `node_filesystem_free_bytes`.
- PDF 293: без подзапроса `avg_over_time(rate(x_total[5m])[1h])` назван ошибочным; глава 13 описывает подзапросы, поэтому не обобщать на все возможные формы работы с `rate`.
- Подробности: [source-findings.md](source-findings.md). Рисунок 16.1 доступен как подпись, не как исходное изображение.
- Отдельных вопросов, упражнений и самостоятельного итога главы в данном RAG нет: условные `summary.md`, `review-questions.md`, `review-answers.md` не создаются.

## Артефакты

[cheatsheet.md](cheatsheet.md) · [commands.md](commands.md) · [diagram.md](diagram.md) · [visual-cheatsheet.svg](visual-cheatsheet.svg) · [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg) · [source-findings.md](source-findings.md).

**Без изменений:** PDF, RAG, метаданные, CI workflows, статус чтения.
