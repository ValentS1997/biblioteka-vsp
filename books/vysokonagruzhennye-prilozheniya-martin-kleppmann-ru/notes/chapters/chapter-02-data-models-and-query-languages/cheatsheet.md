# Шпаргалка главы 2 — модели данных и языки запросов

## Symptom / problem framing

Одна и та же предметная область может быть представлена различными моделями данных, но каждая модель делает одни связи и запросы естественными, а другие — сложными.

Негативные сигналы:

- document model требует множества ручных joins в application code;
- relational schema плохо отражает сильно вложенный автономный документ;
- число и глубина связей заранее неизвестны, а запросы превращаются в громоздкие joins;
- «schemaless» данные фактически имеют структуру, но правила ее проверки не определены;
- query code фиксирует лишние детали выполнения и ограничивает optimizer.

## Baseline / context

### Relational

- tables/relations;
- IDs/foreign keys;
- joins естественны для связей;
- schema обычно явная и применяется при записи.

### Document

- автономные документы, например JSON;
- особенно естественны tree-like one-to-many;
- locality полезна при чтении больших частей документа целиком;
- отсутствие жесткой проверки при записи ближе к schema-on-read, а не к отсутствию схемы.

### Graph

- vertices + edges;
- incoming/outgoing traversal;
- labels позволяют хранить разные виды relationships;
- особенно естественны сложные many-to-many.

### Query style

- imperative: задает последовательность шагов;
- declarative: задает требуемый результат/паттерн, оставляя execution strategy optimizer'у.

## Read-only checks

1. Определить shape данных: documents, rows/relations или graph.
2. Классифицировать cardinality: one-to-one, one-to-many, many-to-one, many-to-many.
3. Проверить, где человекочитаемые значения дублируются вместо ссылок по ID.
4. Определить необходимость joins.
5. Проверить, должен ли application code эмулировать join несколькими запросами.
6. Проверить, читается ли документ целиком или только малый фрагмент.
7. Определить schema policy: write-time validation или read-time interpretation.
8. Определить query shape: fixed joins, aggregation, graph traversal, recursion.
9. Проверить, зависит ли query logic от порядка выполнения, который лучше оставить optimizer'у.
10. Оценить необходимость polyglot persistence.

## Interpretation

- Tree-like данные и whole-document reads → document model может быть естественной.
- Частые many-to-one/many-to-many → document model может переносить сложность в application code.
- Повторяющееся значение во множестве записей → normalization через ID может снизить redundancy и inconsistency risk.
- Разнородные records или внешне задаваемая структура → schema-on-read может быть естественнее.
- Одинаковая ожидаемая структура → explicit schema удобна для documentation/enforcement.
- Variable-length traversal → graph query model может быть естественнее фиксированной цепочки joins.
- Declarative query → optimizer получает свободу менять indexes/join order/parallel execution.
- MapReduce-style procedural logic → больше контроля, но выше query complexity и меньше свободы optimizer'а.

## Next action

1. Нарисовать entities и relationships.
2. Отметить cardinality.
3. Зафиксировать основные read/write/query patterns.
4. Сравнить relational/document/graph именно для этих patterns.
5. Выбрать модель, где частые операции выражаются естественно.
6. Проверить query language и свободу optimizer'а.
7. Протестировать representative queries до закрепления storage choice.

## Modifying action

Source-confirmed state-changing examples:

- Cypher `CREATE` создает vertices/edges;
- MongoDB MapReduce с `out: "monthlySharkReport"` записывает output collection;
- schema changes рассматриваются как отдельная operational concern.

Перед изменением нужно понимать data model и expected result.

## Verification / acceptance checks

Модель приемлема, если:

- типичные relationships выражаются без чрезмерного application-side glue;
- основные queries читаемы;
- duplication/normalization trade-off осознан;
- schema policy соответствует источнику данных;
- locality соответствует access pattern;
- query optimizer не ограничен ненужной procedural sequencing;
- graph traversal не превращается в неудобную заранее неизвестную цепочку joins.

## Rollback

- Read-only SELECT/MATCH/SPARQL SELECT: `[Not applicable]`.
- Cypher CREATE: `[Needs confirmation]`.
- MongoDB MapReduce output collection: `[Needs confirmation]`.
- Schema migration: `[Needs confirmation]`.

Глава не дает универсальных rollback-команд; они не добавлялись из model memory.
