# Глава 10. Как мне?..

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `CHAPTER-ANALYSIS-REQUEST v1.3` → `CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус:** `RAG_GROUNDED`. SQL не выполнялся.

## Источник и границы

- Canonical source: `source/book.pdf`.
- SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 10: **PDF 304–315**, **12 page-chunks**, `p0304:c01`–`p0315:c01`.
- Boundary evidence: начало главы `p0304:c01`; блок «Заключительные слова» на `p0315:c01`; `p0316:c01` — «Об авторе».
- Оглавление главы: `p0012:c01`.
- Режим `rag_only`: без external web/direct-PDF/model-memory corrections.
- Source SHA/RAG manifest согласованы; ранее BOOK-READINESS = READY. Reading остаётся `planned`.

## Карта главы

| Задача | PDF | RAG |
|---|---:|---|
| Найти уникальные и повторяющиеся строки | 304–306 | `p0304:c01`–`p0306:c01` |
| Найти строку с максимальным значением внутри группы | 307–309 | `p0307:c01`–`p0309:c01` |
| Конкатенировать поля одной/нескольких строк | 309–311 | `p0309:c01`–`p0311:c01` |
| Найти таблицы по имени столбца | 311–313 | `p0311:c01`–`p0313:c01` |
| UPDATE по совпадающему id в другой таблице | 313–315 | `p0313:c01`–`p0315:c01` |
| Заключительные слова | 315 | `p0315:c01` |

## Основные выводы

1. **DISTINCT** возвращает уникальные комбинации выбранных столбцов; для поиска только дублирующихся комбинаций source использует `GROUP BY ... HAVING COUNT(*) > 1` и затем JOIN обратно к исходной таблице, чтобы вернуть id (`p0305:c01`–`p0306:c01`).
2. **Max-per-group** решается в два этапа: сначала `MAX(date)` на каждого employee, затем JOIN обратно к `sales`, чтобы вернуть остальные столбцы (`p0307:c01`–`p0309:c01`).
3. **Конкатенация внутри строки**: `CONCAT` или `||`; **между строками**: GROUP_CONCAT/LISTAGG/ARRAY_AGG/STRING_AGG в зависимости от РСУБД (`p0309:c01`–`p0311:c01`).
4. **Поиск колонок в metadata** выполняется через information_schema/all_tab_columns, а SQLite source предлагает `.tables` + `pragma table_info(...)` (`p0311:c01`–`p0312:c01`).
5. **Cross-table UPDATE** — единственная state-changing процедура главы. Source показывает разные dialect forms для MySQL, Oracle, PostgreSQL/SQLite и SQL Server и отдельно предупреждает, что отмена после UPDATE возможна только если заранее начата transaction (`p0313:c01`–`p0315:c01`).
6. Финальный блок книги подчёркивает, что SQL намного шире рассмотренных примеров и что синтаксис заметно различается между РСУБД (`p0315:c01`).

## Operational boundary

- Все SELECT/metadata-примеры — read-only.
- `UPDATE` на PDF 314 — **state-changing** и не является готовой production-инструкцией.
- Перед UPDATE нужны target DB/schema, owner/approval, transaction semantics, preview SELECT, expected affected rows и rollback path: **[Needs confirmation]**.
- Source сам говорит: после UPDATE откат невозможен, кроме случая, когда transaction была начата заранее.

## Source findings

Зафиксированы без silent correction:
- duplicate-query не рассматривает дубли по NULL-key combinations;
- max-per-group query может вернуть несколько строк при tie по максимальной date;
- PostgreSQL ARRAY_AGG выдаётся рядом со string aggregators, хотя output-shape не установлен source;
- metadata statement «без последнего filter будут все таблицы» не учитывает visibility/privilege scope — [Needs confirmation];
- SQLite metadata limitation — version/source assertion [Needs confirmation];
- Oracle UPDATE без WHERE ограничивает не только matched rows и для unmatched scalar subquery outcome не разобран;
- PostgreSQL/SQLite UPDATE example повторно включает `deals d` в FROM и одновременно target `deals`, что создаёт source-level semantic ambiguity;
- transaction rollback warning source-supported, но concrete target semantics всё равно [Needs confirmation].

Полный register: [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [summary.md](summary.md) — explicit «Заключительные слова».
- [source-findings.md](source-findings.md)

Review questions/exercises в `p0304:c01`–`p0315:c01` не обнаружены.
