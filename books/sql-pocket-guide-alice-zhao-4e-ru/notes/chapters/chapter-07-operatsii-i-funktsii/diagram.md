# Диаграммы — глава 7. Операции и функции

**Source:** PDF 190–243, RAG `p0190:c01`–`p0243:c01`.

## 1. Operations vs functions

```mermaid
flowchart TD
  SQL["SQL expression"] --> O["Operations"]
  SQL --> F["Functions"]
  O --> L["Logical: AND / OR / NOT"]
  O --> C["Comparison: = / BETWEEN / EXISTS / IN / LIKE"]
  O --> M["Math: + - * / %"]
  F --> A["Aggregate"]
  F --> N["Numeric"]
  F --> S["String"]
  F --> D["Date/time"]
  F --> U["NULL"]
```

## 2. NULL-sensitive predicate flow

```mermaid
flowchart TD
  A["Predicate / subquery"] --> B{"NULL possible?"}
  B -- "no" --> C["Evaluate normally"]
  B -- "yes" --> D["Use explicit NULL-aware logic"]
  D --> E["IS NULL / IS NOT NULL"]
  D --> F["Prefer NOT EXISTS over risky NOT IN case from source"]
```

## 3. Function portability

```mermaid
flowchart TD
  A["Need operation/function"] --> B["Identify target RDBMS/version"]
  B --> C["Choose source-confirmed dialect variant"]
  C --> D["Test boundary/NULL/case/timezone"]
  D --> E{"Expected output?"}
  E -- "yes" --> F["Use in read-only query"]
  E -- "no" --> G["Stop / [Needs confirmation]"]
```

## 4. Date/time conversions

```mermaid
flowchart LR
  S["String/date/time input"] --> C["CAST / product-specific parser"]
  C --> E["EXTRACT / DATEDIFF / AGE / DATEPART / strftime"]
  E --> V["Verify unit + timezone + locale"]
```

## 5. Change boundary

```mermaid
flowchart TD
  A["Function/operator in SELECT"] --> R["Read-only expression"]
  A --> D["Same expression reused in UPDATE/DELETE"]
  D --> X["State-changing DML: separate change control"]
```

**Boundary:** diagrams express source concepts only; physical execution plans and current product behavior are not asserted.
