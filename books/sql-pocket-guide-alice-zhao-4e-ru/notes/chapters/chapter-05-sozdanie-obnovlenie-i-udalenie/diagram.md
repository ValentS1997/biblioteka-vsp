# Диаграммы — глава 5. Создание, обновление и удаление

**Источник:** PDF 105–154, RAG `p0105:c01`–`p0154:c01`.  
Схемы отражают логику главы и change-control boundary; ничего не исполнялось.

## 1. Объекты и типы изменений

```mermaid
flowchart TB
  DB["Database"] --> T["Tables"]
  T --> C["Columns / constraints"]
  T --> R["Rows"]
  DB --> I["Indexes"]
  DB --> V["Views"]

  DB --> DBC["CREATE / DROP DATABASE"]
  T --> TC["CREATE / ALTER / DROP TABLE"]
  C --> CC["NOT NULL / DEFAULT / CHECK / UNIQUE / PK / FK"]
  R --> RC["INSERT / UPDATE / DELETE"]
  I --> IC["CREATE / DROP INDEX"]
  V --> VC["CREATE / REPLACE / DROP VIEW"]
```

**Provenance:** `p0105:c01`–`p0149:c01`. Все правые ветки — state-changing.

## 2. Rollback-first workflow для DML, показанный главой

```mermaid
flowchart TD
  A["Подтвердить target DB и таблицу"] --> B["SELECT baseline"]
  B --> C["START / BEGIN TRANSACTION"]
  C --> D["SELECT preview с тем же WHERE"]
  D --> E["UPDATE / DELETE"]
  E --> F["SELECT verification"]
  F --> G{"Результат ожидаемый?"}
  G -- "да" --> H["COMMIT"]
  G -- "нет" --> I["ROLLBACK"]
  H --> J["Изменение становится постоянным по примеру главы"]
  I --> K["Отмена незакоммиченного изменения"]
```

**Provenance:** `p0137:c01`–`p0139:c01`, `p0149:c01`–`p0154:c01`.  
Точный transactional behavior DDL/конкретной РСУБД — [Needs confirmation].

## 3. WHERE как blast-radius control

```mermaid
flowchart LR
  U["UPDATE / DELETE"] --> W{"Есть WHERE?"}
  W -- "да" --> P["Воздействие на отфильтрованные строки"]
  W -- "нет" --> A["Воздействие на всю таблицу"]
  P --> V["SELECT verification"]
  A --> V
  V --> C{"В transaction до COMMIT?"}
  C -- "да" --> R["ROLLBACK возможен по примеру"]
  C -- "нет / неизвестно" --> X["Rollback: [Needs confirmation]"]
```

**Provenance:** `p0133:c01`, `p0137:c01`–`p0139:c01`, `p0151:c01`–`p0154:c01`.

## 4. Изменение структуры таблицы

```mermaid
flowchart TD
  A["Inspect: table / columns / constraints"] --> B{"Нужно изменить schema?"}
  B -- "rename/add/constraint" --> C["ALTER TABLE"]
  B -- "SQLite workaround из книги" --> D["CREATE replacement table"]
  D --> E["INSERT SELECT copy"]
  E --> F["SELECT verify"]
  F --> G["DROP old table"]
  G --> H["RENAME replacement"]
  C --> I["Describe / constraint check"]
  H --> I
```

**Provenance:** `p0128:c01`–`p0136:c01`. SQLite workaround — многошаговый state-changing pattern, не гарантированно atomic.

## 5. Index и view

```mermaid
flowchart LR
  Q["Повторяемый запрос"] --> I["CREATE INDEX"]
  I --> P["Ожидаемое ускорение чтения"]
  I --> O["Цена: storage / update overhead"]
  L["Сложный SELECT"] --> V["CREATE VIEW"]
  V --> R["Повторно query view"]
```

**Provenance:** `p0141:c01`–`p0149:c01`. Реальный performance effect [Needs confirmation].

## Acceptance boundary

- Read-only baseline должен предшествовать change.
- DROP/CASCADE и all-row UPDATE/DELETE считаются destructive.
- `COMMIT` отделён от verification.
- Source findings не скрыты: privilege wording, `' US'`, identifier `страна`, Oracle quotes, transaction wording.
- Не добавлены команды вне `p0105:c01`–`p0154:c01`.
