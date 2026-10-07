# Глава 8. Расширенные концепции запросов

**Книга:** Элис Жао, «SQL. Карманный справочник», 4-е изд.  
**Book ID:** `sql-pocket-guide-alice-zhao-4e-ru`  
**Контракт:** `CHAPTER-ANALYSIS-REQUEST v1.3` → `CHAPTER-ARTIFACT-COLLECTION v1.7`  
**Статус:** `RAG_GROUNDED`. SQL не выполнялся.

## Источник и границы

- Canonical source: `source/book.pdf`.
- SHA-256: `d2f6ccf4bae2ca1376e7818749f5482c1e358ce8aecccb2bb86b9f54173a1591`.
- Глава 8: **PDF 244–272**, **29 chunks**, `p0244:c01`–`p0272:c01`.
- Boundary evidence: начало `p0244:c01`, конец UNPIVOT/UNION ALL `p0272:c01`, глава 9 начинается `p0273:c01`.
- Оглавление главы: `p0011:c01`.
- Режим `rag_only`: без внешнего web/direct-PDF/model-memory corrections.
- Source/RAG согласованы; ранее BOOK-READINESS = READY. Reading остаётся `planned`.

## Карта главы

| Раздел | PDF | RAG |
|---|---:|---|
| CASE: simple и searched | 244–248 | `p0244:c01`–`p0248:c01` |
| GROUP BY и агрегирование списков | 248–253 | `p0248:c01`–`p0253:c01` |
| ROLLUP / CUBE / GROUPING SETS | 254–256 | `p0254:c01`–`p0256:c01` |
| Window functions: basics/ranking | 256–260 | `p0256:c01`–`p0260:c01` |
| FIRST/NTH/ROW_NUMBER/LAG | 261–265 | `p0261:c01`–`p0265:c01` |
| Moving average / running total / ROWS vs RANGE | 266–268 | `p0266:c01`–`p0268:c01` |
| PIVOT / UNPIVOT + manual alternatives | 268–272 | `p0268:c01`–`p0272:c01` |

## Основные выводы

1. **CASE** позволяет временно отображать значения по IF/THEN/ELSE-логике. Simple CASE сравнивает одно выражение, searched CASE принимает произвольные predicates; первое сработавшее WHEN имеет приоритет (`p0245:c01`–`p0248:c01`).
2. **GROUP BY + aggregates** возвращает одну строку на группу. Для списков source показывает GROUP_CONCAT/LISTAGG/ARRAY_AGG/STRING_AGG и разные dialect forms (`p0249:c01`–`p0253:c01`).
3. **ROLLUP/CUBE/GROUPING SETS** добавляют subtotal/total/custom grouping combinations; product support различается (`p0254:c01`–`p0256:c01`).
4. **Window functions** возвращают значение для каждой строки, не схлопывая группы. Базовая форма: `function() OVER (PARTITION BY ... ORDER BY ...)` (`p0256:c01`–`p0258:c01`).
5. **Ranking:** ROW_NUMBER разрывает ties, RANK сохраняет ties с пропусками, DENSE_RANK сохраняет ties без пропусков (`p0259:c01`–`p0260:c01`).
6. **FIRST_VALUE/NTH_VALUE/LAG** применяются к позиции внутри окна; фильтрация результата оконной функции в source делается через derived table/subquery (`p0261:c01`–`p0265:c01`).
7. **Frames:** `ROWS BETWEEN ...` используется для moving average и running total; `RANGE` группирует peers с одинаковым ORDER BY value в показанном примере (`p0266:c01`–`p0268:c01`).
8. **PIVOT/UNPIVOT** source относит к Oracle/SQL Server; MySQL/PostgreSQL/SQLite получают manual alternatives через CASE и UNION ALL (`p0268:c01`–`p0272:c01`).

## Operational boundary

Все основные примеры главы — read-only `SELECT`. Потенциально workload-generating: GROUP BY/CUBE, window functions, regex-like manual transforms, PIVOT/UNPIVOT и derived tables. Source не даёт performance benchmark или execution plan.

CASE может быть использован внутри UPDATE, но глава лишь упоминает это как способ сохранить отображаемые значения; никакой authorization на state-changing DML из этого не следует.

## Source findings

Зафиксированы без silent correction:
- `spendings` input на PDF 254 не соответствует агрегированному output;
- MySQL `WITH ROLLUP` в тексте одновременно связывается с SQL Server;
- GROUPING SETS output повторяет `2019`, хотя source totals показывают отдельный 2020 total;
- optimization claim про сокращённый GROUP BY не измерен;
- SQL Server UNPIVOT source не создаёт numeric `rank`, показанный в expected output;
- manual UNPIVOT использует `fruit_three`, хотя source table называется `fruit_thr`;
- утверждение, что MySQL не поддерживает constants like `1 AS rank`, остаётся source assertion [Needs confirmation];
- window defaults/support и LISTAGG/ARRAY_AGG variants остаются version-sensitive [Needs confirmation].

Полный register: [source-findings.md](source-findings.md).

## Артефакты

- [cheatsheet.md](cheatsheet.md)
- [commands.md](commands.md)
- [diagram.md](diagram.md)
- [visual-cheatsheet.svg](visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](visual-cheatsheet-detailed.svg)
- [source-findings.md](source-findings.md)

Явного chapter-end summary/review section перед главой 9 нет.
