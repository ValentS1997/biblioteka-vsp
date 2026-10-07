# Диаграммы — глава 3 «Язык SQL»

**Источник:** RAG PDF 55–69 (`p0055:c01`–`p0069:c01`). Mermaid-схемы воспроизводят **текстовые концепции главы**, не утверждают конкретный физический план SQL-движка и не являются результатом выполнения запросов.

## 1. Императивный алгоритм и декларативный SQL

```mermaid
flowchart LR
  A["Требуется сумма значений"] --> B{"Способ описания"}
  B --> P["Python: указать шаги"]
  P --> P1["calories → total = 0"]
  P1 --> P2["for: накопить сумму"]
  P2 --> P3["print(total)"]
  B --> S["SQL: указать результат"]
  S --> S1["SELECT SUM(calories)"]
  S1 --> S2["FROM workouts"]
  S2 --> S3["Способ вычисления выбирает система"]
```

**Provenance:** `p0055:c01`, `p0056:c01`. SQL в книге описан как декларативный язык специального назначения. Детали оптимизации конкретной СУБД не представлены.

## 2. Анатомия SELECT из главы

```mermaid
flowchart TD
  Q["SELECT … FROM … WHERE … GROUP BY …"]
  Q --> SEL["SELECT: e.name и COUNT(s.sale_id) AS num_sales"]
  Q --> FROM["FROM: employee e LEFT JOIN sales s ON ..."]
  Q --> WHERE["WHERE: YEAR(s.sale_date) = 2021 AND closed IS NOT NULL"]
  Q --> GROUP["GROUP BY e.name"]
  SEL --> ALIAS["num_sales — псевдоним; COUNT — функция"]
  FROM --> TABLES["employee/sales — таблицы; e/s — псевдонимы"]
  WHERE --> PRED["предикаты → TRUE / FALSE / UNKNOWN"]
  GROUP --> TERM["группировка"]
```

**Provenance:** `p0059:c01`–`p0065:c01`. Это **разбор составных частей**, а не граф физического выполнения.

## 3. Пять подъязыков и зона влияния

```mermaid
flowchart TB
  SQL["SQL"] --> DQL["DQL: SELECT — запрос данных"]
  SQL --> DDL["DDL: CREATE, ALTER, DROP — объекты/схема"]
  SQL --> DML["DML: INSERT, UPDATE, DELETE — данные"]
  SQL --> DCL["DCL: GRANT, REVOKE — доступ"]
  SQL --> TCL["TCL: COMMIT, ROLLBACK — транзакции"]
  DQL --> READ["Чтение: подтверждённые права нужны"]
  DDL --> CHANGE["Изменение: approval и rollback"]
  DML --> CHANGE
  DCL --> CHANGE
  TCL --> CHANGE
```

**Provenance:** `p0068:c01`, `p0069:c01`. Слова из таблицы автора **не являются готовой процедурой на запись**; цель, схема, владелец, привилегии и верификация — [Needs confirmation].

## 4. Выбор переносимого синтаксиса в рамках объяснения автора

```mermaid
flowchart TD
  A["Есть SQL-запрос"] --> B{"Использует особенность РСУБД?"}
  B -- "например, Oracle DECODE" --> C["Потенциальная привязка к диалекту"]
  B -- "только стандартные конструкции" --> D["Проверить поддержку в целевой РСУБД"]
  C --> E["Проверить семантику и варианты переписывания"]
  D --> F["Подтвердить результат на разрешённой тестовой БД"]
  E --> F
  F --> G["Отдельная верификация: [Needs confirmation]"]
```

**Provenance:** `p0057:c01`–`p0059:c01`. Ветка проверки/подтверждения — критерий неопределённости, а не дополнительная команда SQL. Случай `DECODE`/`CASE` зарегистрирован в `source-findings.md`.

## Acceptance / boundaries

- Использованы только элементы главы 3, SQL примеры и терминология источника.
- Декларативность не отождествлена с конкретным физическим планом.
- `SELECT` отделён от DDL/DML/DCL/TCL.
- Схематические блоки не дополняются неописанными особенностями БД.
- Source-level разночтения сохранены, см. `source-findings.md`.
