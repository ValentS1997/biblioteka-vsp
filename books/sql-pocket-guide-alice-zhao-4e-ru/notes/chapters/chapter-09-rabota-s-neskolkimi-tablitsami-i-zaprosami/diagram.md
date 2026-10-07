# Диаграммы — глава 9. Работа с несколькими таблицами и запросами

**Source:** PDF 273–303, RAG `p0273:c01`–`p0303:c01`.

## 1. JOIN versus set operations

```mermaid
flowchart LR
  A["Multiple tables / queries"] --> J["JOIN"]
  A --> S["UNION / EXCEPT / INTERSECT"]
  J --> J1["Combine columns by row relationship"]
  S --> S1["Combine/compare result rows"]
```

## 2. JOIN family

```mermaid
flowchart TD
  J["JOIN"] --> I["INNER: matched rows"]
  J --> L["LEFT: all left + matches"]
  J --> R["RIGHT: all right + matches"]
  J --> F["FULL: both sides"]
  J --> C["CROSS: Cartesian product"]
  J --> S["SELF: same table twice"]
```

## 3. CTE anatomy

```mermaid
flowchart TD
  W["WITH name AS (...)"] --> N["Non-recursive CTE"]
  W --> R["Recursive CTE"]
  N --> N1["Reference named result in later SELECT"]
  R --> A["Anchor SELECT"]
  A --> U["UNION ALL"]
  U --> M["Recursive member references CTE"]
  M --> T["Termination predicate"]
```

## 4. Recursive date fill

```mermaid
flowchart LR
  D["Generate date sequence"] --> L["LEFT JOIN source prices"]
  L --> N["Missing rows become NULL"]
  N --> F["Optional COALESCE + LAG for shown one-row gaps"]
```

## 5. Safety boundary

```mermaid
flowchart TD
  A["Before execution"] --> B["Verify join keys / set columns"]
  B --> C["Estimate cardinality / recursion depth"]
  C --> D{"Expected bounded result?"}
  D -- "yes" --> E["Run read-only query"]
  D -- "no / unknown" --> F["Stop: [Needs confirmation]"]
```

## Boundary

Все примеры read-only. CROSS JOIN/recursive CTE могут быть workload-generating; source не задаёт production timeout/cancellation procedure.
