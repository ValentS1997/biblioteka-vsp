# Диаграммы — глава 8. Расширенные концепции запросов

**Source:** PDF 244–272, RAG `p0244:c01`–`p0272:c01`.

## 1. CASE

```mermaid
flowchart TD
  A["CASE"] --> B{"Тип"}
  B --> C["Simple CASE: compare one expression"]
  B --> D["Searched CASE: arbitrary predicates"]
  C --> E["WHEN → THEN"]
  D --> E
  E --> F["first matching branch wins"]
  F --> G["ELSE or NULL if absent"]
```

## 2. GROUP BY versus window function

```mermaid
flowchart LR
  R["Input rows"] --> G["GROUP BY + aggregate"]
  G --> G1["One output row per group"]
  R --> W["Window function OVER(...)"]
  W --> W1["Preserve each input row"]
```

## 3. Window anatomy

```mermaid
flowchart TD
  F["Window function"] --> O["OVER"]
  O --> P["PARTITION BY: split windows"]
  O --> S["ORDER BY: order rows"]
  O --> FR["ROWS / RANGE frame"]
  P --> X["ROW_NUMBER / RANK / FIRST_VALUE / LAG / AVG / SUM"]
  S --> X
  FR --> X
```

## 4. Ranking choice

```mermaid
flowchart TD
  T["Ties possible?"] --> A["ROW_NUMBER: force unique sequence"]
  T --> B["RANK: ties share rank, gaps remain"]
  T --> C["DENSE_RANK: ties share rank, no gaps"]
```

## 5. Reshaping

```mermaid
flowchart LR
  A["Rows: name + fruit"] --> P["PIVOT / CASE"]
  P --> B["Columns per fruit"]
  C["Columns fruit_one/two/thr"] --> U["UNPIVOT / UNION ALL"]
  U --> D["Rows: fruit + rank"]
```

## Boundary

Все схемы read-only и описывают source semantics. PIVOT/window/grouping support, default frames and performance require target-version verification.
