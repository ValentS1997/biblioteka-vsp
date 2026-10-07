# Диаграммы — глава 6. Типы данных

**Source:** PDF 155–189, RAG `p0155:c01`–`p0189:c01`.  
Схемы отражают только текст главы; SQL не выполнялся.

## 1. Выбор типа данных

```mermaid
flowchart TD
  A["Новый столбец"] --> B{"Категория значения"}
  B --> N["Numeric"]
  B --> S["String / Unicode"]
  B --> D["Date / time"]
  B --> O["Boolean / binary / other"]

  N --> N1{"Точность нужна?"}
  N1 -- "целое" --> I["Integer family"]
  N1 -- "точное decimal" --> F["DECIMAL / NUMERIC"]
  N1 -- "approximate" --> FP["Floating-point"]

  S --> S1{"Длина / charset"}
  S1 --> C["CHAR / VARCHAR / TEXT"]
  S1 --> U["Unicode-capable type"]

  D --> D1["DATE / TIME / TIMESTAMP-family"]
  O --> O1["BOOLEAN / BIT / BLOB / BYTEA / VARBINARY"]

  I --> X["Проверить range + storage + RDBMS"]
  F --> X
  FP --> X
  C --> X
  U --> X
  D1 --> X
  O1 --> X
```

**Provenance:** `p0157:c01`–`p0189:c01`.

## 2. Exact versus approximate numeric

```mermaid
flowchart LR
  V["Числовое значение"] --> Q{"Нужна точная decimal семантика?"}
  Q -- "да" --> D["DECIMAL / NUMERIC"]
  Q -- "нет / допускается approximation" --> F["FLOAT / REAL / product-specific"]
  D --> P["precision + scale"]
  F --> R["округление / сравнение могут отличаться"]
```

**Source:** `p0162:c01`–`p0165:c01`. Конкретные type names зависят от РСУБД.

## 3. Date/time: typed literal or conversion

```mermaid
flowchart TD
  A["Текст, похожий на дату/время"] --> B{"Что нужно?"}
  B --> D["DATE"]
  B --> T["TIME"]
  B --> TS["TIMESTAMP / DATETIME"]
  D --> C["DATE literal или CAST"]
  T --> C
  TS --> C
  C --> R["Проверить dialect / format / timezone"]
```

**Source:** `p0173:c01`–`p0183:c01`. SQLite model в книге отдельно использует TEXT/REAL/INTEGER.

## 4. Schema-test boundary

```mermaid
flowchart TD
  A["Выбрать candidate type"] --> B["Подтвердить RDBMS/version"]
  B --> C["CREATE test table — state-changing"]
  C --> D["INSERT representative values — state-changing"]
  D --> E["SELECT round-trip — read-only"]
  E --> F{"Значения/precision/encoding ожидаемы?"}
  F -- "да" --> G["Candidate accepted for design review"]
  F -- "нет" --> H["Не переносить в real schema"]
  H --> I["Rollback/cleanup: [Needs confirmation]"]
```

Глава 6 показывает CREATE/INSERT/SELECT как учебный pattern, но не даёт универсального rollback.

## 5. External file strategy

```mermaid
flowchart LR
  F["Файл"] --> A{"Подход по книге"}
  A --> P["Хранить path/reference"]
  A --> B["Хранить binary value в DB"]
  P --> P1["VARCHAR-like column"]
  B --> B1["BLOB / BYTEA / VARBINARY family"]
  P1 --> V["Выбор зависит от system requirements"]
  B1 --> V
```

**Source:** `p0185:c01`–`p0189:c01`. Threshold 1 MB — source heuristic, not benchmark.

## Boundaries

- Не подставлены современные product limits.
- Не исправлены damaged ASCII/Unicode exponents.
- MySQL datetime mismatch и SQLite datetime mismatch вынесены в `source-findings.md`.
- CREATE/INSERT/ALTER SESSION — state-changing.
