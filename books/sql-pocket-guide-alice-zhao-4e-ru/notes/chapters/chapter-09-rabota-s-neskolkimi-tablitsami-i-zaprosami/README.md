# Глава 9. Работа с несколькими таблицами и запросами

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `CHAPTER-ANALYSIS-REQUEST v1.3` → `CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус:** `RAG_GROUNDED`. SQL не выполнялся.

## Источник и границы

- Canonical source: `source/book.pdf`.
- SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 9: **PDF 273–303**, **31 page-chunks**, `p0273:c01`–`p0303:c01`.
- RAG paths: `rag/chunks/p0201-p0300/p0273-c01.md` … `p0300-c01.md`, затем `rag/chunks/p0301-p0400/p0301-c01.md` … `p0303-c01.md`.
- Boundary evidence: начало главы `p0273:c01`; recursive CTE family-tree table заканчивается на `p0303:c01`; глава 10 начинается на `p0304:c01`.
- Оглавление: `p0012:c01`.
- Режим `rag_only`: без external web/direct PDF/model-memory corrections.
- Source SHA/RAG manifest согласованы; ранее BOOK-READINESS = READY. Reading остаётся `planned`.

## Карта главы

| Раздел | PDF | RAG |
|---|---:|---|
| JOIN overview и типы соединений | 273–277 | `p0273:c01`–`p0277:c01` |
| INNER JOIN и join conditions | 278–280 | `p0278:c01`–`p0280:c01` |
| LEFT/RIGHT/FULL OUTER JOIN | 281–282 | `p0281:c01`–`p0282:c01` |
| USING / NATURAL JOIN | 282–284 | `p0282:c01`–`p0284:c01` |
| CROSS JOIN / Self Join | 285–287 | `p0285:c01`–`p0287:c01` |
| UNION / UNION ALL | 287–292 | `p0287:c01`–`p0292:c01` |
| EXCEPT / INTERSECT | 292–294 | `p0292:c01`–`p0294:c01` |
| Non-recursive CTE vs subquery | 294–297 | `p0294:c01`–`p0297:c01` |
| Recursive CTE: sequences and hierarchy | 298–303 | `p0298:c01`–`p0303:c01` |

## Основные выводы

1. **JOIN combines columns; UNION-family combines result rows.** Это центральное различие главы (`p0287:c01`–`p0289:c01`).
2. **JOIN cardinality зависит от совпадений.** Дубликаты в одной стороне размножают строки результата; source показывает Deb дважды из-за двух pets (`p0274:c01`–`p0281:c01`).
3. **Outer joins сохраняют unmatched rows** и заполняют отсутствующую сторону NULL (`p0281:c01`–`p0282:c01`).
4. **USING/NATURAL JOIN сокращают синтаксис**, но NATURAL JOIN source прямо рекомендует не использовать в рабочем коде из-за зависимости от одинаковых имён столбцов/schema drift (`p0283:c01`–`p0284:c01`).
5. **CROSS JOIN создаёт Cartesian product**, а self join позволяет сравнивать строки одной таблицы (`p0285:c01`–`p0287:c01`).
6. **UNION removes duplicates; UNION ALL preserves them.** Количество столбцов должно совпадать; имена output берутся из первого SELECT согласно source (`p0289:c01`–`p0291:c01`).
7. **EXCEPT/INTERSECT** описывают difference/intersection result sets; Oracle использует MINUS вместо EXCEPT, MySQL workarounds source строит через NOT IN / INNER JOIN (`p0292:c01`–`p0293:c01`).
8. **CTE** — временный именованный result set. Recursive CTE состоит из anchor SELECT + recursive SELECT, соединённых UNION ALL (`p0294:c01`–`p0303:c01`).
9. **Recursive CTE** source применяет для генерации дат и обхода parent-child hierarchy (`p0298:c01`–`p0303:c01`).

## Operational boundary

Все законченные примеры главы — read-only SELECT/CTE. Однако потенциально workload-generating:
- CROSS JOIN;
- self join;
- UNION duplicate elimination;
- recursive CTE;
- hierarchy expansion;
- recursive date sequences.

Для production execution нужны target DB/version, expected cardinality, recursion limits и query-cost checks: **[Needs confirmation]**.

## Source findings

Зафиксированы без silent correction:
- self-join example с `INNER JOIN states s2 WHERE ...` не содержит ON;
- CTE example names `SUM(order_id)` as `num_orders`;
- UNION ALL performance explanation asserts hidden sort for UNION without execution-plan evidence;
- MySQL EXCEPT workaround uses NOT IN despite NULL caveat earlier in book;
- MySQL INTERSECT workaround joins only by `name`, while source INTERSECT compares both selected columns;
- set-operation precedence claim remains dialect/version-sensitive;
- Oracle “replace LIMIT 1 with ROWNUM = 1” is not shown as a full equivalent query around ORDER BY;
- recursive NULL-fill via one LAG handles shown one-row gaps but not demonstrated for consecutive gaps;
- RIGHT/FULL JOIN support claims and recursive-CTE syntax are edition/version assertions [Needs confirmation].

Полный register: [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

Явного chapter-end summary/review section перед главой 10 нет.
