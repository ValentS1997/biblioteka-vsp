# Диаграммы — глава 10. Как мне?..

**Source:** PDF 304–315, RAG `p0304:c01`–`p0315:c01`.

## 1. Duplicate workflow

```mermaid
flowchart TD
  A["teas"] --> D["DISTINCT tea, temperature"]
  A --> G["GROUP BY tea, temperature"]
  G --> H["HAVING COUNT(*) > 1"]
  H --> J["JOIN back to teas"]
  J --> R["Return original row ids"]
```

## 2. Max row per group

```mermaid
flowchart LR
  S["sales"] --> A["GROUP BY employee + MAX(date)"]
  A --> J["JOIN back on employee + recent_date"]
  J --> R["Return id / date / sales"]
```

## 3. Concatenation patterns

```mermaid
flowchart TD
  C["Concatenate"] --> O["Within one row"]
  C --> M["Across multiple rows"]
  O --> F["CONCAT or ||"]
  M --> G["GROUP_CONCAT / LISTAGG / ARRAY_AGG / STRING_AGG"]
```

## 4. Cross-table UPDATE safety flow

```mermaid
flowchart TD
  A["Confirm target DB / dialect"] --> B["Preview matching ids and values"]
  B --> C["Confirm expected affected count"]
  C --> D["Start transaction if supported"]
  D --> E["Dialect-specific UPDATE"]
  E --> F["SELECT verification"]
  F --> G{"Expected result?"}
  G -- "yes" --> H["COMMIT"]
  G -- "no" --> I["ROLLBACK if still available"]
```

## Boundary

Read-only patterns are analytical. UPDATE is state-changing and requires separate transaction/rollback verification.
