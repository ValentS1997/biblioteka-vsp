# Глава 8 — source findings

**Book:** `cybersecurity-risk-hubbard-seiersen-ru`. **Boundary:** EPUB spine 34–35. **Mode:** `rag_only`.

## F-01 — [Source extraction issue] Рисунки 8.1–8.2 отсутствуют как самостоятельные RAG-изображения

- **Рис. 8.1:** дерево цепных правил, spine 35, `OPS/ch1-33.xhtml`, `e0035:c03`.
- **Рис. 8.2:** пример decomposition крупной утечки с conditional probabilities, `e0035:c04`.
- В RAG есть подписи и подробная textual derivation, но нет исходной геометрии дерева/таблицы и визуального layout.
- Решение: chapter SVG/Mermaid показывают только концептуальную схему; не выдаются за копию original figures.

## F-02 — [Source extraction issue] Повреждённая скобочная запись шага 3

- Locator: spine 35, `OPS/ch1-33.xhtml`, chunk `e0035:c04`.
- Символьная формула непосредственно перед числом:
  ```text
  P(УЭУ | КУД) = P(КУД | УЭУ)P(УЭУ)/P(КУД)
  ```
- Числовая строка в extracted text:
  ```text
  = (0,25 (0,01)/(0,0124) = 20,16 %.
  ```
- Наблюдение: после `0,25` отсутствует закрывающая/операционная скобочная структура; строка синтаксически повреждена.
- Значение `20,16%` и символьная формула доступны в источнике, но chapter artifacts **не заменяют** повреждённую строку «правильной» записью без отдельной сверки оригинального layout.
- Adjudication: `[Needs confirmation]` визуальной сверкой издания.

## F-03 — [Source extraction issue] Табличный layout входных/derived values рис. 8.2 не извлечён

Текст `e0035:c04` говорит о левом столбце входных данных калиброванных экспертов и правом столбце производных величин. Полная исходная таблица/рисунок не представлена структурированным объектом. Артефакты не додумывают недостающие строки и layout.

## F-04 — [External artifact not retrieved] «Наивный» байесовский калькулятор / spreadsheet

Spine 34–35 упоминает downloadable spreadsheet с сайта книги. Текущий контракт `rag_only`; внешний файл не загружался, не исполнялся и не использовался для исправления F-02.

## F-05 — [Source-context caution] Penetration test в главе — гипотетическое evidence, не operational instruction

В `e0034:c02–c03` и `e0035:c04–c05` penetration test используется как observable variable для обновления вероятности. Глава не предоставляет authorization, tooling, target scope или safe-execution procedure. Артефакты не превращают пример в pentest runbook.

**Итог:** canonical EPUB, checksum и RAG не изменялись.
